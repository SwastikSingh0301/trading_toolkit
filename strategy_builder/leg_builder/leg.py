from .strike_criteria import StrikeCriteriaFactory
from .target_profit import TargetProfitFactory
from .stop_loss import StopLossFactory


class Leg:
    def __init__(
            self,
            lots,
            position,
            option_type,
            expiry,
            strike_criteria,
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
        self.strike_criteria = StrikeCriteriaFactory.create_strike_criteria_instance(
            strike_criteria, strike_criteria["value"])

        if target_profit:
            self.target_profit = TargetProfitFactory.create_target_profit_instance(
                target_profit, target_profit["value"])

        if stop_loss:
            self.stop_loss = StopLossFactory.create_stop_loss_instance(stop_loss, stop_loss["value"])

        self.entry_strike_price = None
        self.underlying_price_at_entry = None
        self.is_entered = False

    def enter(self, underlining_asset_price, option_chain):
        self.entry_strike_price = self.strike_criteria.get_strike_price(underlining_asset_price, self.option_type)
        self.underlying_price_at_entry = underlining_asset_price

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

    def set_is_entered(self, entered):
        self.is_entered = entered

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
