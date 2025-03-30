from prismfolio.investmentgroup import InvestmentGroup
from prismfolio.asset import Asset
from prismfolio.wallet import Wallet


class SuggestionNotReady(Exception):
    pass


class _BaseSuggestionDict:
    def __init__(self):
        self._suggestion = dict()

    def __getitem__(self, item):
        return self._suggestion[item]

    def __len__(self):
        return len(self._suggestion)

    def __iter__(self):
        for _, _v in self._suggestion.items():
            yield _v


class _BaseSuggestion:
    def __init__(self, item, total_amount, new_contribution):
        self._item = item
        self._new_contribution = new_contribution
        _total_after_new_contribution = total_amount + new_contribution
        self._ideal_investing = max(0, 0.01 * item.get_target_participation()
                                    * (_total_after_new_contribution)-item.get_total_amount())
        self._actual_investing = None

    def _get_ideal_investment(self):
        return self._ideal_investing

    def set_new_contribution(self, new_contribution):
        self._new_contribution = new_contribution

    def get_suggested_investment(self):
        if self._actual_investing is None:
            raise SuggestionNotReady("This asset suggestion is not ready, you cant instantiate "
                                     "this class directly.")
        return self._actual_investing

    def _calculate_actual_investing(self, total_ideal_investing):
        if total_ideal_investing == 0:
            self._actual_investing = 0
            return

        self._actual_investing = (self._ideal_investing /
                                  total_ideal_investing)*self._new_contribution


class _AssetSuggestion(_BaseSuggestion):
    def __init__(self, asset: Asset, total_amount, new_contribution):
        super().__init__(asset, total_amount, new_contribution)

    def get_suggested_shares_buying(self):
        return self.get_suggested_investment() // self._item.get_price()

    def get_asset(self):
        return self._item

    def __repr__(self):
        return f"""
            Asset: {self._item.get_code()}
            It is recommended to invest ${self._actual_investing:.2f},
            which corresponds to {self.get_suggested_shares_buying()} shares.
            """


class _InvestmentGroupSuggestion(_BaseSuggestion, _BaseSuggestionDict):
    def __init__(self, group: InvestmentGroup, total_amount, new_contribution):
        super().__init__(group, total_amount, new_contribution)
        self._suggestion = {x: _AssetSuggestion(
            x, group.get_total_amount(), new_contribution) for x in group.get_assets()}

        _total_ideal_investing = sum(
            self._suggestion[x]._get_ideal_investment() for x in self._suggestion)

        for item, suggestion in self._suggestion.items():
            suggestion._calculate_actual_investing(_total_ideal_investing)

    def update_contribution_value(self, contribution_value):
        _total_ideal_investing = sum(
            self._suggestion[x]._get_ideal_investment() for x in self._suggestion)
        for item, suggestion in self._suggestion.items():
            suggestion.set_new_contribution(contribution_value)
            suggestion._calculate_actual_investing(_total_ideal_investing)

    def get_investment_group(self):
        return self._item

    def __repr__(self):
        return f"""
            Group: {self._item.get_name()}
            It is recommended to invest ${self._actual_investing:.2f}.
            """


class WalletInvestmentSuggestion(_BaseSuggestionDict):
    def __init__(self, wallet: Wallet, new_contribution):
        super().__init__()
        self._suggestion = {x: _InvestmentGroupSuggestion(
            x, wallet.get_total_amount(), new_contribution) for x in wallet.get_investment_groups()}
        _total_ideal_investing = sum(
            self._suggestion[x]._get_ideal_investment() for x in self._suggestion)
        for item, suggestion in self._suggestion.items():
            suggestion._calculate_actual_investing(_total_ideal_investing)
        for item, suggestion in self._suggestion.items():
            suggestion.update_contribution_value(suggestion.get_suggested_investment())

    def __repr__(self):
        _s = ""
        for _group in self:
            _s += str(_group)
            for _asset in _group:
                _s += str(_asset)

        return _s
