import math


class MathOperations:
    @staticmethod
    def get_delta_between_two_numbers(x, y):
        return abs(x-y)

    @staticmethod
    def floor_function(x, base=50):
        return base * math.floor(x / base)

    @staticmethod
    def ceil_function(x, base=50):
        return base * math.ceil(x / base)

    @staticmethod
    def round_function(x, base=50):
        return base * round(x / base)