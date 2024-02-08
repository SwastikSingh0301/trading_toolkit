from strategy_builder.common.constants import POSITION


class StopLoss:
    def is_stop_loss_reached(self, price_at_bid, last_traded_price, position):
        raise NotImplementedError("Subclasses must implement this method")

    def get_loss(self, price_at_bid, ltp, position):
        if position == POSITION.SELL.value:
            return ltp - price_at_bid
        else:
            return price_at_bid - ltp


class StopLossPoints(StopLoss):
    pass


class StopLossUnderlyingPoints:
    pass


class StopLossPercent(StopLoss):
    def __init__(self, value):
        self.stop_loss_percent = value

    def is_stop_loss_reached(self, position, leg_bid_price=None, underlying_price_at_bid=None, ltp=None, underlying_ltp=None):
        loss = self.get_loss(leg_bid_price, ltp, position)
        loss_percent = (loss * 100) / leg_bid_price
        return loss_percent > self.stop_loss_percent


class StopLossUnderlyingPercent(StopLoss):
    def __init__(self, value):
        self.stop_loss_underlying_percent = value

    def is_stop_loss_reached(self, position, leg_bid_price=None, underlying_price_at_bid=None, ltp=None, underlying_ltp=None):
        loss = self.get_loss(underlying_price_at_bid, underlying_ltp, position)
        loss_percent = (loss * 100) / underlying_ltp
        return loss_percent > self.stop_loss_underlying_percent


class StopLossFactory:
    @staticmethod
    def create_stop_loss_instance(stop_loss_type, value):
        if stop_loss_type == "percent":
            return StopLossPercent(value)
        elif stop_loss_type == "underlying_percent":
            return StopLossUnderlyingPercent(value)
        else:
            raise ValueError("Invalid stop loss type")
