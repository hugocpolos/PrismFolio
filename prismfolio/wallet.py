from prismfolio.investmentgroup import InvestmentGroup

import json
import logging


class Wallet:
    def __init__(self):
        self._investment_group = list()

    # Public
    def get_investment_groups(self):
        return self._investment_group

    def add_investment_group(self, investment_group: InvestmentGroup):
        self._investment_group.append(investment_group)

    def has_investment_group(self):
        return len(self._investment_group) > 0

    def get_total_amount(self):
        return sum(x.get_total_amount() for x in self._investment_group)

    def update_asset_values(self, pricing_function):
        for investment_group in self._investment_group:
            investment_group.update_asset_values(pricing_function)

    def update_asset_price_earnings(self, price_earnings_function):
        for investment_group in self._investment_group:
            investment_group.update_asset_price_earnings(price_earnings_function)

    @classmethod
    def from_json(cls, json_data):
        return cls.from_dict(json.loads(json_data))

    @classmethod
    def from_dict(cls, dict_data):
        if not isinstance(dict_data, dict):
            raise TypeError(f"Expected a dict. Got a {type(dict_data)}")

        _wallet = cls()

        for investment_group in dict_data.get('investment_groups'):
            _wallet.add_investment_group(InvestmentGroup.from_dict(investment_group))

        _total_groups_participation = _wallet._get_total_groups_target_participation()

        if _total_groups_participation > 100.0:
            logging.warning("The total investment groups on wallet is %.2f%%, which is "
                            "greater than 100%%." % _total_groups_participation)

        if _total_groups_participation < 100.0:
            logging.warning("The total investment groups participation on wallet is %.2f%%, which "
                            "is lower than 100%%." % _total_groups_participation)

        return _wallet

    # Private
    def _get_total_groups_target_participation(self):
        return sum(x.get_target_participation() for x in self._investment_group)
