import datetime

from .strike_criteria import StrikeCriteriaFactory
from .target_profit import TargetProfitFactory
from .stop_loss import StopLossFactory
from common.constants import LEG_STATUS, LOT_SIZE
from common.option_chain_parser import OptionChainParser


class Leg:
    def __init__(
            self,
            id,
            lots,
            position,
            option_type,
            expiry,
            strike_criteria,
            index,
            target_profit=None,
            stop_loss=None,
            trailing_stop_loss=None,
            re_entry_on_target=None,
            re_entry_on_stop_loss=None,
            simple_momentum=None,
            range_breakout=None
    ):
        self.lots = lots
        self.position = position
        self.option_type = option_type
        self.expiry = expiry
        self.target_profit = None
        self.stop_loss = None
        self.index = index
        self.strike_criteria = StrikeCriteriaFactory.create_strike_criteria_instance(
            strike_criteria["criteria"], strike_criteria["value"])

        if target_profit:
            self.target_profit = TargetProfitFactory.create_target_profit_instance(
                target_profit["criteria"], target_profit["value"])

        if stop_loss:
            self.stop_loss = StopLossFactory.create_stop_loss_instance(stop_loss["criteria"], stop_loss["value"])

        # entry data
        self.entry_strike_price = None
        self.underlying_price_at_entry = None
        self.entry_option_price = None
        self.is_entered = False
        self.entry_price = None
        self.status = LEG_STATUS.PENDING
        self.shares_per_lot = 0


    def set_position(self, strike_price):
        pass

    def enter(self, option_chain):
        underlying_asset_price = option_chain.underlying_asset_price
        self.entry_strike_price = self.strike_criteria.get_strike_price(underlying_asset_price, self.option_type)
        self.underlying_price_at_entry = underlying_asset_price

        option = option_chain.get_option(self.entry_strike_price, self.option_type)
        self.entry_price = option.ltp
        self.set_status_as_active()
        return self.output_formatter(self.entry_strike_price, self.position)

    def output_formatter(self, strike_price, position):
        return {
            "strike_price": strike_price,
            "position": position,
            "option_type": self.option_type,
            "expiry": self.expiry,
            "lots": self.lots,
            "time": datetime.datetime.now()
        }

    def is_target_profit_reached(self, ltp=None, underlying_ltp=None):
        if not self.is_entered:
            return False
        if self.target_profit:
            return self.target_profit.is_target_profit_reached(ltp=ltp, underlying_ltp=underlying_ltp)
        return False

    def _is_stop_loss_reached(self, ltp=None, underlying_ltp=None):
        if not self.is_entered:
            return False
        if self.stop_loss:
            return self.stop_loss.is_stop_loss_reached(ltp=ltp, underlying_ltp=underlying_ltp)
        return False

    def get_mtm_per_share(self, option_chain):
        option = OptionChainParser.get_option(option_chain, strike_price=self.entry_strike_price,
                                              option_type=self.option_type)
        if option.empty:
            return 0
        last_traded_price = option["ltp"].iloc[0]
        if self.position == "sell":
            mtm = -(last_traded_price - self.entry_price)
        elif self.position == "buy":
            mtm = last_traded_price - self.entry_price
        else:
            # This condition should never arrive
            mtm = None
        return mtm

    def exit(self):
        if self.position == "sell":
            position = "buy"
        else:
            position = "sell"
        if self.status == LEG_STATUS.ACTIVE:
            self.status = LEG_STATUS.EXITED
        if self.status == LEG_STATUS.RE_ENTERED:
            self.status = LEG_STATUS.RE_EXITED
        return self.output_formatter(self.entry_strike_price, position)

    def set_status_as_active(self):
        self.status = LEG_STATUS.ACTIVE

    @property
    def get_entry_strike_price(self):
        return self.entry_strike_price

    @property
    def get_lots(self):
        return self.lots

    @property
    def get_position(self):
        return self.position

    @property
    def get_option_type(self):
        return self.option_type

    @property
    def get_expiry(self):
        return self.expiry

    @property
    def active(self):
        return self.status == LEG_STATUS.ACTIVE

    def set_status_as_exited(self):
        self.status = LEG_STATUS.EXITED

    def get_mtm(self, option_chain):
        option = option_chain.get_option(strike_price=self.entry_strike_price, option_type=self.option_type)
        if not option:
            return None
        ltp = option.ltp
        if self.position == 'sell':
            return (self.entry_price - ltp) * LOT_SIZE[self.index]

    def pending_handler(self, option_chain):
        pass

    def active_handler(self, option_chain):
        underlying_ltp = option_chain.underlying_asset_price
        option = option_chain.get_option(strike_price=self.entry_strike_price, option_type=self.option_type)
        ltp = option.ltp

        # Target Profit
        if self.target_profit:
            if self.target_profit.is_target_profit_reached(
                self.position, leg_bid_price=self.entry_price, underlying_price_at_bid=self.underlying_price_at_entry,
                ltp=ltp, underlying_ltp=underlying_ltp
            ):
                return self.exit()

        # Stop Loss
        if self.stop_loss:
            if self.stop_loss.is_stop_loss_reached(
                    self.position, leg_bid_price=self.entry_price,
                    underlying_price_at_bid=self.underlying_price_at_entry,
                    ltp=ltp, underlying_ltp=underlying_ltp
            ):
                return self.exit()

        return None

    def squared_off_handler(self, option_chain):
        pass

    def exited_handler(self, option_chain):
        """here check if there is scope of re entry"""
        pass

    def failed_handler(self, option_chain):
        pass

    def re_entered_handler(self, option_chain):
        pass

    def re_exited_handler(self, option_chain):
        return

    def executor(self, option_chain):
        if self.status == LEG_STATUS.PENDING:
            return self.pending_handler(option_chain)
        if self.status == LEG_STATUS.ACTIVE:
            return self.active_handler(option_chain)
        if self.status == LEG_STATUS.SQUARED_OFF:
            return self.squared_off_handler(option_chain)
        if self.status == LEG_STATUS.EXITED:
            return self.exited_handler(option_chain)
        if self.status == LEG_STATUS.FAILED:
            return self.failed_handler(option_chain)
        if self.status == LEG_STATUS.RE_ENTERED:
            return self.re_entered_handler(option_chain)
        if self.status == LEG_STATUS.RE_EXITED:
            return self.re_exited_handler(option_chain)
        else:
            raise ValueError("Unknown leg status")
