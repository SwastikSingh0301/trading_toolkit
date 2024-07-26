from .common.constants import NUMBER_OF_SHARES_PER_LOT


class InstrumentSettings:
    def __init__(self, index, underlying_form):
        self.index = index
        self.underlying_form = underlying_form

    def number_of_shares_per_lot(self):
        if self.index == "nifty":
            return NUMBER_OF_SHARES_PER_LOT.NIFTY.value
        elif self.index == "finnifty":
            return NUMBER_OF_SHARES_PER_LOT.FINNIFTY.value
        elif self.index == "sensex":
            return NUMBER_OF_SHARES_PER_LOT.SENSEX.value
        elif self.index == "midcpnifty":
            return NUMBER_OF_SHARES_PER_LOT.MIDCPNIFTY.value
        elif self.index == "banknifty":
            return NUMBER_OF_SHARES_PER_LOT.BANKNIFTY.value
        elif self.index == "bankex":
            return NUMBER_OF_SHARES_PER_LOT.BANKEX.value
        else:
            raise ValueError("Invalid index name")
