from datetime import datetime
from common.constants import LEG_STATUS, STRATEGY_STATUS
from .instrument_settings import InstrumentSettings
from .legwise_settings import LegwiseSettings
from .entry_settings import EntrySettings
from .leg_builder.leg import Leg
from .overall_strategy_settings import OverallStrategySettings


class Strategy:
    def __init__(
            self,
            instrument_settings,
            legwise_settings,
            entry_settings,
            legs,
            overall_strategy_settings,
    ):
        index = instrument_settings.get("index")
        underlying_form = instrument_settings.get("underlying_form")
        self.instrument_settings = InstrumentSettings(index=index, underlying_form=underlying_form)

        square_off = legwise_settings.get("square_off")
        trail_sl_to_break_even = legwise_settings.get("trail_sl_to_break_even")
        self.legwise_settings = LegwiseSettings(square_off=square_off, trail_sl_to_break_even=trail_sl_to_break_even)

        strategy_type = entry_settings.get("strategy_type")
        entry_time = entry_settings.get("entry_time")
        exit_time = entry_settings.get("exit_time")
        no_re_entry_after = entry_settings.get("no_re_entry_after")
        no_re_entry_after_time = entry_settings.get("no_re_entry_after_time")
        self.entry_settings = EntrySettings(
            strategy_type=strategy_type,
            entry_time=entry_time,
            exit_time=exit_time,
            no_re_entry_after=no_re_entry_after,
            no_re_entry_after_time=no_re_entry_after_time
        )

        self.legs = list()
        for leg in legs:
            id = leg.get("id")
            lots = leg.get("lots")
            position = leg.get("position")
            option_type = leg.get("option_type")
            expiry = leg.get("expiry")
            strike_criteria = leg.get("strike_criteria")
            target_profit = leg.get("target_profit")
            stop_loss = leg.get("stop_loss")

            leg_object = Leg(
                id=id,
                lots=lots,
                position=position,
                option_type=option_type,
                expiry=expiry,
                strike_criteria=strike_criteria,
                target_profit=target_profit,
                stop_loss=stop_loss,
                index=index
            )
            self.legs.append(leg_object)

        self.entered = False
        self.active = False

        self.overall_strategy_settings = OverallStrategySettings(overall_strategy_settings)

        self.state = LEG_STATUS.PENDING


    def string_time_to_time(self, time_string):
        # Parse the time string into a datetime object
        time_obj = datetime.strptime(time_string, "%I:%M %p")
        time_component = time_obj.time()
        return time_component



    def take_entry(self, option_chain):
        entrys = []
        for leg in self.legs:
            option = leg.enter(
                option_chain
            )
            entrys.append(option)
        self.entered = True
        self.state = STRATEGY_STATUS.RUNNING
        return entrys

    def get_overall_strategy_mtm(self, option_chain):
        overall_mtm = 0
        for leg in self.legs:
            if leg.active:
                overall_mtm = overall_mtm + leg.get_mtm(option_chain)
        return overall_mtm

    def exit(self):
        actions = []
        for leg in self.legs:
            actions.append(leg.exit())
        self.state = STRATEGY_STATUS.EXITED
        return actions

    def overall_strategy_handler(self, option_chain):
        pass

    def pending_handler(self, option_chain):
        if self.entry_settings.can_enter(option_chain):
            return self.take_entry(option_chain)

    def running_handler(self, option_chain):
        action = self.overall_strategy_settings.overall_setting_reached(option_chain, self.state, self.legs)
        if action:
            if action == "exit":
                return self.exit()
        for leg in self.legs:
            action = leg.executor(option_chain)

    def exit_handler(self, option_chain):
        action = self.overall_strategy_settings.overall_setting_reached(option_chain, self.state, self.legs)
        if action:
            if action == "exit":
                return self.exit()

    def executor(self, option_chain):
        try:
            if self.state == STRATEGY_STATUS.RUNNING:
                return self.running_handler(option_chain)
            elif self.state == LEG_STATUS.PENDING:
                return self.pending_handler(option_chain)
            elif self.state == STRATEGY_STATUS.EXITED:
                return self.exit_handler(option_chain)
            elif self.state == STRATEGY_STATUS.RE_ENTERED:
                pass
            else:
                raise Exception("Strategy status not identified")
        except Exception as e:
            raise Exception(f"Unknown error while execution of strategy - ", e)
            # In case of exception also try to exit the strategy

