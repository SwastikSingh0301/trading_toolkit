from .instrument_settings import InstrumentSettings
from .legwise_settings import LegwiseSettings
from .entry_settings import EntrySettings
from .leg_builder.leg import Leg


class Strategy:
    def __init__(
            self,
            instrument_settings,
            legwise_settings,
            entry_settings,
            legs,
            overall_strategy_settings
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

        leg_objects = list()
        for leg in legs:
            lots = leg.get("lots")
            position = leg.get("position")
            option_type = leg.get("option_type")
            expiry = leg.get("expiry")
            strike_criteria = leg.get("strike_criteria")
            target_profit = leg.get("target_profit")
            stop_loss = leg.get("stop_loss")

            leg_object = Leg(
                lots=lots,
                position=position,
                option_type=option_type,
                expiry=expiry,
                strike_criteria=strike_criteria,
                target_profit=target_profit,
                stop_loss=stop_loss
            )
            leg_objects.append(leg_object)



