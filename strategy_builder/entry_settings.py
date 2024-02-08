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
        self.validate(strategy_type, entry_time,exit_time, no_re_entry_after, no_re_entry_after_time)
        self.strategy_type = strategy_type
        self.entry_time = entry_time
        self.exit_time = exit_time
        self.no_re_entry_after = no_re_entry_after
        self.no_re_entry_after_time = no_re_entry_after_time

    def validate(self, strategy_type, entry_time, exit_time, no_re_entry_after, no_re_entry_after_time):
        # validation checks - entry and exit time in time format (or convert into time format),
        #                     no_re_entry_after is a bool and if no_re_entry_after present then no_re_entry_after_time
        #                     can not be null

        # Check if strategy_type is a valid value from the enum
        if not isinstance(strategy_type, STRATEGY_TYPE):
            raise ValueError("Invalid strategy_type value")
