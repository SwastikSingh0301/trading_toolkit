strategies = {
    "1": {
        "instrument_settings": {
            "index": "midcapnifty",
            "underlyingform": "cash"
        },
        "legwise_settings": {
            "square_off": "partial",
            "trail_sl_to_breakeven_price": None
        },
        "entry_settings": {
            "strategy_type": "intraday",
            "entry_time": "09:20 AM",
            "exit_time": "02:36 PM",
            "no_reentry_after": None,
        },
        "legs": [
            {   "id": 1,
                "lots": 1,
                "position": "sell",
                "option_type": "put",
                "expiry": "weekly",
                "strike_criteria": {
                    "criteria": "strike_type",
                    "value": "atm"
                },
                "target_profit": None,
                "stop_loss": {
                    "criteria": "percent",
                    "value": "5"
                },
                "trailing_stop_loss": None,
                "re_entry_on_target": None,
                "re_entry_on_stop_loss": {
                    "recost": 2,
                },
            }
        ],
        "overall_strategy_settings": {
            "overall_stop_loss": {
                "type": "max_loss",
                "value": -200
            },
            "overall_target_profit": {
                "type": "max_profit",
                "value": 200
            }
        },
        "overall_reentry_on_stop_loss": None,
        "overall_target": None,
        "trailing_options": {
            "lock_and_trail": {
                "if_profit_reaches": 700,
                "for_every_increase_in_profit_by": 20,
                "lock_profit": 350,
                "trail_profit_by": 20,
            }
        }
    }
}

class GetStrategy:
    def __init__(self, uuid):
        self.strategy = strategies.get(uuid)

    @property
    def instrument_settings(self):
        return self.strategy.get("instrument_settings")

    @property
    def legwise_settings(self):
        return self.strategy.get("legwise_settings")

    @property
    def entry_settings(self):
        return self.strategy.get("entry_settings")

    @property
    def overall_strategy_settings(self):
        return self.strategy.get("overall_strategy_settings")

    @property
    def legs(self):
        return self.strategy.get("legs")
