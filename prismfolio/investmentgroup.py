from prismfolio.asset import Asset
from prismfolio.targetparticipation import TargetParticipation

import json
import logging


class InvestmentGroup(TargetParticipation):
    def __init__(self, name: str, target_participation: float):
        self._check_name_argument(name)
        super().__init__(target_participation)
        self._name = name
        self._assets = list()

    # Public
    def get_name(self):
        return self._name

    def add_asset(self, asset: Asset):
        self._assets.append(asset)

    def has_asset(self):
        return len(self._assets) > 0

    def get_total_amount(self):
        return sum(x.get_total_amount() for x in self._assets)

    def update_asset_values(self, pricing_function):
        for asset in self._assets:
            asset.update_price(pricing_function)

    def update_asset_price_earnings(self, price_earnings_function):
        for asset in self._assets:
            asset.update_price_earnings(price_earnings_function)

    def get_assets(self):
        return self._assets

    @classmethod
    def from_json(cls, json_data):
        return cls.from_dict(json.loads(json_data))

    @classmethod
    def from_dict(cls, dict_data):
        if not isinstance(dict_data, dict):
            raise TypeError(f"Expected a dict. Got a {type(dict_data)}")

        _investment_group = cls(name=dict_data.get('name'),
                                target_participation=dict_data.get('target_participation'))
        for asset in dict_data.get('assets'):
            _investment_group.add_asset(Asset.from_dict(asset))

        _total_asset_participation = _investment_group._get_total_asset_target_participation()

        if _total_asset_participation > 100.0:
            logging.warning("The total asset participation on group '%s' is %.2f%%, which is "
                            "greater than 100%%." % (_investment_group.get_name(),
                                                     _total_asset_participation))

        if _total_asset_participation < 100.0:
            logging.warning("The total asset participation on group '%s' is %.2f%%, which is "
                            "lower than 100%%." % (_investment_group.get_name(),
                                                   _total_asset_participation))

        return _investment_group

    # Private
    def _check_name_argument(self, name: str):
        if not isinstance(name, str):
            raise TypeError(f"Name value must be a string. Got {type(name)} {name}")

        if len(name) == 0:
            raise ValueError("Name value must be a non empty string.")

    def _get_total_asset_target_participation(self):
        return sum(x.get_target_participation() for x in self._assets)
