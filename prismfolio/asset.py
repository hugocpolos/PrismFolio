from prismfolio.targetparticipation import TargetParticipation

import json


class AssetPricingError(Exception):
    pass


class AssetWithNoPrice(Exception):
    pass


class Asset(TargetParticipation):
    def __init__(self, code: str, quantity: int, target_participation: float):
        self._check_code_argument(code)
        self._check_quantity_argument(quantity)
        super().__init__(target_participation)
        self._code = code
        self._quantity = quantity
        self._price = None
        self._price_earnings = 0.0
        self._current_participation = 0.0

    # Public
    def has_current_price(self):
        return self._price is not None

    def get_price(self):
        if not self.has_current_price():
            raise AssetWithNoPrice(
                f'{self._code} has no price yet. Call the method update_price() first.')

        return self._price

    def get_price_earnings(self):
        return self._price_earnings

    def get_code(self):
        return self._code

    def get_quantity(self):
        return self._quantity

    def buy(self, quantity: int):
        self._check_quantity_argument(quantity)
        self._quantity += quantity

    def update_price(self, pricing_function):
        try:
            self._price = pricing_function(self._code)
        except Exception as err:
            raise AssetPricingError(f"It is not possible to get the price of {self._code}. "
                                    f"{err}")
        return self._price

    def update_price_earnings(self, price_earnings_function):
        try:
            self._price_earnings = price_earnings_function(self._code)
        except Exception as err:
            raise AssetPricingError(f"It is not possible to get the price earning of {self._code}. "
                                    f"{err}")
        return self._price_earnings

    def get_total_amount(self):
        return self.get_price() * self.get_quantity()

    @classmethod
    def from_json(cls, json_data):
        return cls.from_dict(json.loads(json_data))

    @classmethod
    def from_dict(cls, dict_data):
        if not isinstance(dict_data, dict):
            raise TypeError(f"Expected a dict. Got a {type(dict_data)}")
        return cls(code=dict_data.get('code'), quantity=dict_data.get('quantity'),
                   target_participation=dict_data.get('target_participation'))

    def _check_code_argument(self, code: str):
        if not isinstance(code, str):
            raise TypeError(f"Code value must be a string. Got {type(code)} {code}")

        if len(code) == 0:
            raise ValueError("Code value must be a non empty string.")

    def _check_quantity_argument(self, quantity: int):
        if isinstance(quantity, bool) or not isinstance(quantity, int):
            raise TypeError(f"Quantity value must be an integer. Got {type(quantity)} {quantity}")

        if quantity < 0:
            raise ValueError(f"Quantity value can't be negative. Received {quantity}")
