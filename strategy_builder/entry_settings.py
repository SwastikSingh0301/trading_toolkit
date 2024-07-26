from datetime import datetime
from strategy_builder.common.constants import STRATEGY_TYPE


#this can be a django model
class EntrySettings:
    def __init__(
            self,
            strategy_type,
            entry_time,
            exit_time,
            no_re_entry_after=False,
            no_re_entry_after_time=None
    ):
        # convert entry time and exit time to time objects if they are string
        self.time_format = '%I:%M %p'
        self.validate(strategy_type, entry_time, exit_time, no_re_entry_after, no_re_entry_after_time)
        self.strategy_type = strategy_type
        self.entry_time = self.convert_time_str_to_time_object(entry_time)
        self.exit_time = self.convert_time_str_to_time_object(exit_time)
        self.no_re_entry_after = no_re_entry_after
        self.no_re_entry_after_time = self.convert_time_str_to_time_object(no_re_entry_after_time)

    def convert_time_str_to_time_object(self, time_str):
        if not time_str:
            return None
        if not isinstance(time_str, str):
            raise ValueError("expected time to be of string type")
        try:
            return datetime.strptime(time_str, self.time_format).time()
        except Exception as e:
            raise Exception(f"Error while converting time string to time object - {e}")


    def validate(self, strategy_type, entry_time, exit_time, no_re_entry_after, no_re_entry_after_time):
        # validation checks - entry and exit time in time format (or convert into time format),
        #                     no_re_entry_after is a bool and if no_re_entry_after present then no_re_entry_after_time
        #                     can not be null

        # Check if strategy_type is a valid value from the enum
        if strategy_type not in [st.value for st in STRATEGY_TYPE]:
            raise ValueError("Invalid strategy_type value")

    def can_enter(self, option_chain):
        if self.no_re_entry_after_time:
            return self.entry_time <= option_chain.time <= self.no_re_entry_after_time
        return option_chain.time >= self.entry_time
