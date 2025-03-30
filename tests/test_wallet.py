from prismfolio.wallet import Wallet
from prismfolio.asset import Asset
from prismfolio.investmentgroup import InvestmentGroup
import pytest


def test_wallet_complete_intialization():
    g1 = InvestmentGroup('G1', 60.0)
    a1 = Asset('A1', 0, 100.0)
    g1.add_asset(a1)

    g2 = InvestmentGroup('G2', 40.0)
    a2 = Asset('A2', 10, 20.0)
    a3 = Asset('A3', 0, 80.0)
    g2.add_asset(a2)
    g2.add_asset(a3)

    w = Wallet()
    w.add_investment_group(g1)
    w.add_investment_group(g2)

    w.update_asset_values(lambda _: 1.0)
    w.update_asset_price_earnings(lambda _: 1.0)
