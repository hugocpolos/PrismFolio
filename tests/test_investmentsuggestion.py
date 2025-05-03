from prismfolio.asset import Asset
from prismfolio.investmentgroup import InvestmentGroup
from prismfolio.investmentsuggestion import WalletInvestmentSuggestion
from prismfolio.wallet import Wallet


def test_suggestion_with_assets():
    g1 = InvestmentGroup('A stocks', 50.0)
    g1.add_asset(Asset('A1', 100, 50.0))
    g1.add_asset(Asset('A2', 40, 50.0))
    g1.update_asset_values(lambda x: 1.0)

    g2 = InvestmentGroup('B stocks', 50.0)
    g2.add_asset(Asset('B1', 0, 100.0))
    g2.update_asset_values(lambda x: 10.0)

    w = Wallet()
    w.add_investment_group(g1)
    w.add_investment_group(g2)

    wallet_suggestion = WalletInvestmentSuggestion(w, 0)
    assert wallet_suggestion is not None

    for group_suggestion in wallet_suggestion:
        assert group_suggestion.get_suggested_investment() == 0
        for asset_suggestion in group_suggestion:
            assert asset_suggestion.get_suggested_investment() == 0
            assert asset_suggestion.get_suggested_shares_buying() == 0


def test_suggestion_with_an_empty_wallet():
    w = Wallet()
    w.update_asset_values(lambda x: 1.0)
    wallet_suggestion = WalletInvestmentSuggestion(w, 100)
    assert wallet_suggestion is not None
    assert len(wallet_suggestion) == 0


def test_suggestion_with_single_group_and_single_asset():
    w = Wallet()
    g1 = InvestmentGroup('G1', 100.0)
    a1 = Asset('A1', 0, 100.0)

    g1.add_asset(a1)
    w.add_investment_group(g1)

    w.update_asset_values(lambda x: 1.0)

    wallet_suggestion = WalletInvestmentSuggestion(w, 100)
    assert wallet_suggestion is not None
    assert wallet_suggestion[g1] is not None
    assert wallet_suggestion[g1][a1] is not None

    assert wallet_suggestion[g1].get_suggested_investment() == 100
    assert wallet_suggestion[g1][a1].get_suggested_investment() == 100


def test_suggestion_with_single_group_and_multiple_asset():
    w = Wallet()
    g1 = InvestmentGroup('G1', 100.0)
    a1 = Asset('A1', 0, 20.0)
    a2 = Asset('A2', 0, 20.0)
    a3 = Asset('A3', 0, 20.0)
    a4 = Asset('A4', 0, 20.0)
    a5 = Asset('A5', 0, 20.0)

    def pricing_function(x):
        return {
            "A1": 1.0,
            "A2": 2.0,
            "A3": 3.0,
            "A4": 4.0,
            "A5": 7.0,
        }.get(x)

    g1.add_asset(a1)
    g1.add_asset(a2)
    g1.add_asset(a3)
    g1.add_asset(a4)
    g1.add_asset(a5)
    w.add_investment_group(g1)
    w.update_asset_values(pricing_function)

    wallet_suggestion = WalletInvestmentSuggestion(w, 100)
    a1_investment = wallet_suggestion[g1][a1].get_suggested_investment()
    a1_shares = wallet_suggestion[g1][a1].get_suggested_shares_buying()
    a2_investment = wallet_suggestion[g1][a2].get_suggested_investment()
    a2_shares = wallet_suggestion[g1][a2].get_suggested_shares_buying()
    a3_investment = wallet_suggestion[g1][a3].get_suggested_investment()
    a3_shares = wallet_suggestion[g1][a3].get_suggested_shares_buying()
    a4_investment = wallet_suggestion[g1][a4].get_suggested_investment()
    a4_shares = wallet_suggestion[g1][a4].get_suggested_shares_buying()
    a5_investment = wallet_suggestion[g1][a5].get_suggested_investment()
    a5_shares = wallet_suggestion[g1][a5].get_suggested_shares_buying()

    assert a1_investment == 20.0
    assert a2_investment == 20.0
    assert a3_investment == 20.0
    assert a4_investment == 20.0
    assert a5_investment == 20.0

    assert a1_shares == 20.0
    assert a2_shares == 10.0
    assert a3_shares == 6.0
    assert a4_shares == 5.0
    assert a5_shares == 2.0


def test_suggestion_with_multiple_group():
    w = Wallet()
    g1 = InvestmentGroup('G1', 50.0)
    g2 = InvestmentGroup('G2', 50.0)
    w.add_investment_group(g1)
    w.add_investment_group(g2)
    w.update_asset_values(lambda x: 10)

    wallet_suggestion = WalletInvestmentSuggestion(w, 100)
    assert wallet_suggestion is not None
    assert wallet_suggestion[g1] is not None
    assert wallet_suggestion[g2] is not None
    assert wallet_suggestion[g1].get_suggested_investment() == 50
    assert wallet_suggestion[g2].get_suggested_investment() == 50


def test_suggestion_with_multiple_group_and_assets():
    w = Wallet()
    g1 = InvestmentGroup('G1', 50.0)
    a1 = Asset('A1', 100, 100.0)
    g1.add_asset(a1)

    g2 = InvestmentGroup('G2', 50.0)
    a2 = Asset('A2', 0, 100.0)
    g2.add_asset(a2)

    w.add_investment_group(g1)
    w.add_investment_group(g2)
    w.update_asset_values(lambda x: 10)

    wallet_suggestion = WalletInvestmentSuggestion(w, 100)
    assert wallet_suggestion is not None
    assert wallet_suggestion[g1] is not None
    assert wallet_suggestion[g2] is not None
    assert wallet_suggestion[g1].get_suggested_investment() == 0
    assert wallet_suggestion[g2].get_suggested_investment() == 100
    assert wallet_suggestion[g1][a1].get_suggested_investment() == 0
    assert wallet_suggestion[g1][a1].get_suggested_shares_buying() == 0
    assert wallet_suggestion[g2][a2].get_suggested_investment() == 100
    assert wallet_suggestion[g2][a2].get_suggested_shares_buying() == 10


def test_suggestion_no_remainder_single_group_single_asset():
    w = Wallet()
    g1 = InvestmentGroup('G1', 100.0)
    a1 = Asset('A1', 0, 100.0)
    g1.add_asset(a1)
    w.add_investment_group(g1)
    w.update_asset_values(lambda x: 1.0)

    wallet_suggestion = WalletInvestmentSuggestion(w, 100)
    assert wallet_suggestion.get_remainder() == 0
    assert wallet_suggestion[g1].get_remainder() == 0
    assert wallet_suggestion[g1][a1].get_remainder() == 0


def test_suggestion_no_remainder_single_group_multiple_asset():
    w = Wallet()
    g1 = InvestmentGroup('G1', 100.0)
    a1 = Asset('A1', 0, 30.0)
    a2 = Asset('A2', 0, 70.0)
    g1.add_asset(a1)
    g1.add_asset(a2)
    w.add_investment_group(g1)
    w.update_asset_values(lambda x: 1.0)

    wallet_suggestion = WalletInvestmentSuggestion(w, 100)
    assert wallet_suggestion.get_remainder() == 0
    assert wallet_suggestion[g1].get_remainder() == 0
    assert wallet_suggestion[g1][a1].get_remainder() == 0
    assert wallet_suggestion[g1][a2].get_remainder() == 0


def test_suggestion_no_remainder_multiple_group():
    w = Wallet()
    g1 = InvestmentGroup('G1', 50.0)
    a1 = Asset('A1', 0, 50.0)
    a2 = Asset('A2', 0, 50.0)
    g1.add_asset(a1)
    g1.add_asset(a2)

    g2 = InvestmentGroup('G2', 50.0)
    a3 = Asset('A3', 0, 25.0)
    a4 = Asset('A4', 0, 25.0)
    a5 = Asset('A5', 0, 25.0)
    a6 = Asset('A6', 0, 25.0)
    g2.add_asset(a3)
    g2.add_asset(a4)
    g2.add_asset(a5)
    g2.add_asset(a6)

    w.add_investment_group(g1)
    w.add_investment_group(g2)

    w.update_asset_values(lambda x: 1.0)

    wallet_suggestion = WalletInvestmentSuggestion(w, 200)
    assert wallet_suggestion.get_remainder() == 0
    assert wallet_suggestion[g1].get_remainder() == 0
    assert wallet_suggestion[g2].get_remainder() == 0
    assert wallet_suggestion[g1][a1].get_remainder() == 0
    assert wallet_suggestion[g1][a2].get_remainder() == 0
    assert wallet_suggestion[g2][a3].get_remainder() == 0
    assert wallet_suggestion[g2][a4].get_remainder() == 0
    assert wallet_suggestion[g2][a5].get_remainder() == 0
    assert wallet_suggestion[g2][a6].get_remainder() == 0


def test_suggestion_remainder_single_group_single_asset():
    w = Wallet()
    g1 = InvestmentGroup('G1', 100.0)
    a1 = Asset('A1', 0, 100.0)
    g1.add_asset(a1)
    w.add_investment_group(g1)
    w.update_asset_values(lambda x: 5)

    wallet_suggestion = WalletInvestmentSuggestion(w, 5)
    assert wallet_suggestion.get_remainder() == 0
    assert wallet_suggestion[g1].get_remainder() == 0
    assert wallet_suggestion[g1][a1].get_remainder() == 0

    wallet_suggestion = WalletInvestmentSuggestion(w, 54)
    assert wallet_suggestion.get_remainder() == 4
    assert wallet_suggestion[g1].get_remainder() == 4
    assert wallet_suggestion[g1][a1].get_remainder() == 4

    wallet_suggestion = WalletInvestmentSuggestion(w, 10.5)
    assert wallet_suggestion.get_remainder() == 0.50
    assert wallet_suggestion[g1].get_remainder() == 0.50
    assert wallet_suggestion[g1][a1].get_remainder() == 0.50

    wallet_suggestion = WalletInvestmentSuggestion(w, 41.5)
    assert wallet_suggestion.get_remainder() == 1.50
    assert wallet_suggestion[g1].get_remainder() == 1.50
    assert wallet_suggestion[g1][a1].get_remainder() == 1.50

    wallet_suggestion = WalletInvestmentSuggestion(w, 0)
    assert wallet_suggestion.get_remainder() == 0
    assert wallet_suggestion[g1].get_remainder() == 0
    assert wallet_suggestion[g1][a1].get_remainder() == 0

    wallet_suggestion = WalletInvestmentSuggestion(w, 1.0)
    assert wallet_suggestion.get_remainder() == 1
    assert wallet_suggestion[g1].get_remainder() == 1
    assert wallet_suggestion[g1][a1].get_remainder() == 1

    wallet_suggestion = WalletInvestmentSuggestion(w, 2.0)
    assert wallet_suggestion.get_remainder() == 2
    assert wallet_suggestion[g1].get_remainder() == 2
    assert wallet_suggestion[g1][a1].get_remainder() == 2

    wallet_suggestion = WalletInvestmentSuggestion(w, 3.0)
    assert wallet_suggestion.get_remainder() == 3
    assert wallet_suggestion[g1].get_remainder() == 3
    assert wallet_suggestion[g1][a1].get_remainder() == 3

    wallet_suggestion = WalletInvestmentSuggestion(w, 4.0)
    assert wallet_suggestion.get_remainder() == 4
    assert wallet_suggestion[g1].get_remainder() == 4
    assert wallet_suggestion[g1][a1].get_remainder() == 4
