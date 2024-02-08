class OverallStrategySettings:
    def __init__(
            self,
            overall_stop_loss,
            overall_re_entry_on_stoploss,
            overall_target,
            overall_re_entry_on_target
    ):
        self.overall_stop_loss = overall_stop_loss
        self.overall_re_entry_on_stoploss = overall_re_entry_on_stoploss
        self.overall_target = overall_target
        self.overall_re_entry_on_target = overall_re_entry_on_target

