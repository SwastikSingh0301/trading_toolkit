from common.constants import STRATEGY_STATUS, OVERALL_STOP_LOSS_TYPES, OVERALL_TARGET_PROFIT_TYPES


class OverallStrategySettings:
    def __init__(
            self,
            overall_strategy_settings
    ):
        self.overall_stop_loss = None
        self.overall_target_profit = None
        self.overall_re_entry_on_stoploss = None
        self.overall_re_entry_on_target = None
        self.trailing_options = None
        self.overall_stop_loss_executed = None
        self.overall_target_profit_executed = None

        if not self.validate(overall_strategy_settings):
            return

        self.set_overall_stop_loss(overall_strategy_settings)
        self.set_overall_target_profit(overall_strategy_settings)
        self.set_overall_re_entry_on_stoploss(overall_strategy_settings)
        self.set_overall_re_entry_on_target(overall_strategy_settings)

    def set_overall_stop_loss(self, overall_strategy_settings):
        if "overall_stop_loss" in overall_strategy_settings:
            self.overall_stop_loss = overall_strategy_settings["overall_stop_loss"]

    def set_overall_target_profit(self, overall_strategy_settings):
        if "overall_target_profit" in overall_strategy_settings:
            self.overall_target_profit = overall_strategy_settings["overall_target_profit"]

    def set_overall_re_entry_on_stoploss(self, overall_strategy_settings):
        if "overall_re_entry_on_stoploss" in overall_strategy_settings:
            self.overall_re_entry_on_stoploss = overall_strategy_settings["overall_re_entry_on_stoploss"]

    def set_overall_re_entry_on_target(self, overall_strategy_settings):
        if "overall_re_entry_on_target" in overall_strategy_settings:
            self.overall_re_entry_on_target = overall_strategy_settings["overall_re_entry_on_target"]

    def validate(self, overall_strategy_settings):
        if not overall_strategy_settings:
            return False
        if not isinstance(overall_strategy_settings, dict):
            return False
        return True

    def _is_overall_stop_loss_reached(self, option_chain, legs):
        if self.overall_stop_loss.get("type") == OVERALL_STOP_LOSS_TYPES.MAX_LOSS:
            overall_mtm = 0
            for leg in legs:
                leg_mtm = leg.get_mtm(option_chain)
                if leg_mtm:
                    overall_mtm += leg.get_mtm(option_chain)
            print(overall_mtm)
            return overall_mtm < int(self.overall_stop_loss.get("value"))
        elif self.overall_stop_loss.get("type") == OVERALL_STOP_LOSS_TYPES.TOTAL_PREMIUM_PERCENT:
            """Implement Here overall stop loss percentage wise"""
            pass
        else:
            raise ValueError("non recognizable overall stop loss type")

        return False

    def _is_overall_target_profit_reached(self, option_chain, legs):
        if self.overall_target_profit.get("type") == OVERALL_TARGET_PROFIT_TYPES.MAX_PROFIT:
            overall_mtm = 0
            for leg in legs:
                leg_mtm = leg.get_mtm(option_chain)
                if leg_mtm:
                    overall_mtm += leg.get_mtm(option_chain)
                else:
                    return False
            return overall_mtm > int(self.overall_target_profit.get("value"))
        elif self.overall_target_profit.get("type") == OVERALL_TARGET_PROFIT_TYPES.TOTAL_PREMIUM_PERCENT:
            """Implement Here overall target profit percentage wise"""
            pass
        else:
            raise ValueError("non recognizable overall target profit type")

        return False

    def _can_overall_re_enter_on_stop_loss_reached(self, option_chain, legs):
        return False

    def _can_overall_re_enter_on_target_profit_reached(self, option_chain, legs):
        return False

    def overall_setting_reached(self, option_chain, strategy_state, legs):
        """
        :param option_chain:
        :param strategy_state:
        :param legs:
        :return: Return 'enter', 'exit' or None
        """
        if self.overall_stop_loss and strategy_state == STRATEGY_STATUS.RUNNING:
            if self._is_overall_stop_loss_reached(option_chain, legs):
                return 'exit'
        if self.overall_target_profit and strategy_state == STRATEGY_STATUS.RUNNING:
            if self._is_overall_target_profit_reached(option_chain, legs):
                return 'exit'
        if self.overall_target_profit and strategy_state == STRATEGY_STATUS.EXITED:
            if self._is_overall_stop_loss_reached(option_chain, legs):
                return 'enter'
        if self.overall_target_profit and strategy_state == STRATEGY_STATUS.EXITED:
            if self._is_overall_stop_loss_reached(option_chain, legs):
                return 'enter'
        pass





