from strategy_builder.common.constants import STRIKE_CRITERIA, OPTION_TYPE, STRIKE_PRICE_DELTA
from common.math_operations import MathOperations


class StrikeCriteria:
    def __init__(self):
        pass

    def get_strike_price(self, underlining_asset_price, option_type):
        raise NotImplementedError("Subclasses must implement this method")


class StrikeType(StrikeCriteria):
    def __init__(self, value):
        super().__init__()
        self.strike_type = value

    def get_strike_price(self, underlining_asset_price, option_type):
        if "otm" in self.strike_type:
            otm_distance = int(self.strike_type[3:])
            strike_price = self.get_strike_price_otm(underlining_asset_price, option_type, otm_distance)
        elif "itm" in self.strike_type:
            itm_distance = int(self.strike_type[3:])
            strike_price = self.get_strike_price_itm(underlining_asset_price, option_type, itm_distance)
        elif "atm" in self.strike_type:
            strike_price = self.get_atm_price(underlining_asset_price)
        else:
            raise ValueError("unexpected value as strike type")
        return strike_price

    def get_strike_price_otm(self, underlining_asset_price, option_type, otm_distance):
        if option_type == OPTION_TYPE.CALL.value:
            strike_price = self.get_atm_price(underlining_asset_price) + (otm_distance * STRIKE_PRICE_DELTA)
        elif option_type == OPTION_TYPE.PUT.value:
            strike_price = self.get_atm_price(underlining_asset_price) - (otm_distance * STRIKE_PRICE_DELTA)
        else:
            raise ValueError("option type is not readable")
        return strike_price

    def get_strike_price_itm(self, underlining_asset_price, option_type, itm_distance):
        if option_type == OPTION_TYPE.CALL.value:
            strike_price = self.get_atm_price(underlining_asset_price) - (itm_distance * STRIKE_PRICE_DELTA)
        elif option_type == OPTION_TYPE.PUT.value:
            strike_price = self.get_atm_price(underlining_asset_price) + (itm_distance * STRIKE_PRICE_DELTA)
        else:
            raise ValueError("option type is not readable")
        return strike_price


    def get_atm_price(self, underlining_asset_price):
        return MathOperations.round_function(underlining_asset_price)


class PremiumRange(StrikeCriteria):
    def __init__(self, value):
        super().__init__()
        self.lower = value.get("lower")
        self.upper = value.get("upper")

    pass


class ClosestPremium:
    def __init__(self, value):
        super().__init__()
        self.strike_type = value


class PremiumGreaterThanEqual:
    pass


class PremiumLessThanEqual:

    pass


class StrikeCriteriaFactory:
    @staticmethod
    def create_strike_criteria_instance(strike_criteria, value):
        if strike_criteria == STRIKE_CRITERIA.STRIKE_TYPE.value:
            return StrikeType(value)
        elif strike_criteria == STRIKE_CRITERIA.PREMIUM_RANGE.value:
            return PremiumRange(value)
        elif strike_criteria == STRIKE_CRITERIA.CLOSEST_PREMIUM.value:
            return ClosestPremium(value)
        else:
            raise ValueError("Invalid stop loss type")
