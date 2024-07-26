class OptionChainParser:

    @staticmethod
    def get_underlying_asset_price(option_chain):
        pass

    @staticmethod
    def get_option(option_chain, strike_price, option_type, index=None, expiry=None):
        option = option_chain[
            (option_chain["strike_price"] == strike_price) &
            (option_chain["instrument_type"] == option_type)
        ]
        return option


    @staticmethod
    def get_ltp(option_chain, strike_price, option_type):
        option = OptionChainParser.get_option(option_chain, strike_price, option_type)
        if option.empty:
            return None
        return option.iloc[0].ltp

    @staticmethod
    def get_underlying_ltp(option_chain):
        underlying_asset = option_chain[option_chain["ticker"] == "underlying_asset"]
        return underlying_asset.iloc[0].ltp
