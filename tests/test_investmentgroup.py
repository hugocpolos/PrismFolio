from prismfolio.targetparticipation import TargetParticipation
from prismfolio.asset import Asset, AssetWithNoPrice
from prismfolio.investmentgroup import InvestmentGroup
import random
import pytest
import json


@pytest.mark.parametrize("name,participation",
                         [("TEST", 10.0),
                          ("test", 10.0),
                          ("tEsT", 10.0),
                          ("TEST", 10.0),
                          ("TEST", 10.0),
                          ("TEST", 0.1),
                          ("TEST", 100.0),
                          ("TEST", 5.0),
                          ("TEST", 10.0),
                          ("FOO", 10.0),
                          ("BAR", 10.0),
                          ("12345", 10.0),
                          (".8*21&", 10.0),
                          (".", 10.0),
                          ("VERYL000nG!!$TRINGWITH$p&ci4LCHARS\t\t##"*10, 10.0),
                          ("VERYLONGSTRINGVALUEWITHONLYCHARACTERS"*10, 10.0)])
def test_valid_initialization(name, participation):
    ig = InvestmentGroup(name, participation)
    assert ig.get_name() == name
    assert ig.get_target_participation() == participation


@pytest.mark.parametrize("name,expected_error",
                         [(0, TypeError),
                          (10, TypeError),
                          (None, TypeError),
                          ({}, TypeError),
                          (set(), TypeError),
                          (dict(), TypeError),
                          (list(), TypeError),
                          (0.0, TypeError),
                          (50.0, TypeError),
                          (True, TypeError),
                          (False, TypeError),
                          ("", ValueError)])
def test_invalid_name(name, expected_error):
    with pytest.raises(expected_error):
        InvestmentGroup(name, 10.0)


@pytest.mark.parametrize("invalid_dict",
                         [{'name': 'TEST'},
                          {'target_participation': 50.0},
                          {'assets': []},
                          {'assets': None},
                          {'assets': 1},
                          {'assets': dict()},
                          {None},
                          1,
                          "foo",
                          True,
                          False,
                          [],
                          {}])
def test_investment_group_from_invalid_dict(invalid_dict):
    with pytest.raises(TypeError):
        InvestmentGroup.from_dict(invalid_dict)


@pytest.mark.parametrize("invalid_json,expected_error",
                         [("", json.decoder.JSONDecodeError),
                          ("foo", json.decoder.JSONDecodeError),
                          ("{}", TypeError),
                          (set(), TypeError),
                          (1, TypeError),
                          (10.2, TypeError),
                          (True, TypeError),
                          (False, TypeError),
                          ([], TypeError),
                          ({}, TypeError)])
def test_asset_from_invalid_json(invalid_json, expected_error):
    with pytest.raises(expected_error):
        InvestmentGroup.from_json(invalid_json)


def test_total_participation_greater_than_100_should_trigger_log(caplog):
    d = {'name': "Investment Group with bad total asset participation",
         'target_participation': 100.0,
         'assets': [
             {'code': 'test', 'quantity': 10, 'target_participation': 60.0},
             {'code': 'test2', 'quantity': 10, 'target_participation': 70.0}
         ]
         }
    ig = InvestmentGroup.from_dict(d)
    assert 'WARNING' in caplog.text
    assert 'is 130.00%, which is greater than 100%.' in caplog.text
    assert ig is not None
    assert ig.get_name() == "Investment Group with bad total asset participation"


def test_total_participation_lower_than_95_should_trigger_log(caplog):
    d = {'name': "Investment Group with bad total asset participation",
         'target_participation': 100.0,
         'assets': [
             {'code': 'test', 'quantity': 10, 'target_participation': 40.0},
             {'code': 'test2', 'quantity': 10, 'target_participation': 40.0}
         ]
         }
    ig = InvestmentGroup.from_dict(d)
    assert 'WARNING' in caplog.text
    assert 'is 80.00%, which is lower than 100%.' in caplog.text
    assert ig is not None
    assert ig.get_name() == "Investment Group with bad total asset participation"


def test_empty_assets_dict():
    d = {'name': "Investment Group with no assets",
         'target_participation': 100.0,
         'assets': []
         }
    ig = InvestmentGroup.from_dict(d)
    assert not ig.has_asset()
    ig.add_asset(Asset('Test', 0, 10.0))
    assert ig.has_asset()


def test_pricing():
    d = {'name': "Good group",
         'target_participation': 100.0,
         'assets': [
             {'code': 'test', 'quantity': 5, 'target_participation': 10.0},
             {'code': 'test2', 'quantity': 10, 'target_participation': 10.0}
         ]
         }
    ig = InvestmentGroup.from_dict(d)
    with pytest.raises(AssetWithNoPrice):
        ig.get_total_amount()

    ig.update_asset_values(lambda x: 1.0)
    assert ig.get_total_amount() == 5*1.0 + 10 * 1.0
    ig.update_asset_values(lambda x: 2.0)
    assert ig.get_total_amount() == 5*2.0 + 10 * 2.0

    ig.update_asset_values(lambda x: 1.0 if x == "test" else 10.0)
    assert ig.get_total_amount() == 5*1.0 + 10 * 10.0

    ig.update_asset_values(lambda x: 0.0 if x == "test" else 10.0)
    assert ig.get_total_amount() == 5*0.0 + 10 * 10.0


def test_pricing_with_assets_with_no_initial_quantity():
    d = {'name': "first buying group",
         'target_participation': 100.0,
         'assets': [
             {'code': 'test', 'quantity': 0, 'target_participation': 60.0},
             {'code': 'test2', 'quantity': 0, 'target_participation': 40.0}
         ]
         }
    ig = InvestmentGroup.from_dict(d)
    with pytest.raises(AssetWithNoPrice):
        ig.get_total_amount()

    ig.update_asset_values(lambda x: 1.0)
    assert ig.get_total_amount() == 0.0
    ig.update_asset_values(lambda x: 2.0)
    assert ig.get_total_amount() == 0.0

    ig.update_asset_values(lambda x: 1.0 if x == "test" else 10.0)
    assert ig.get_total_amount() == 0.0

    ig.update_asset_values(lambda x: 0.0 if x == "test" else 10.0)
    assert ig.get_total_amount() == 0.0
