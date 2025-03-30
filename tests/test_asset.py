from prismfolio.asset import Asset, AssetPricingError, AssetWithNoPrice
import json
import pytest
import requests


@pytest.mark.parametrize("code,quantity,participation",
                         [("TEST", 0, 10.0),
                          ("test", 1, 10.0),
                          ("tEsT", 1, 10.0),
                          ("TEST", 1, 10.0), ("TEST", 1000, 10.0),
                          ("TEST", 0, 0.1),
                          ("TEST", 0, 100.0),
                          ("TEST", 0, 5.0),
                          ("TEST", 10000, 10.0),
                          ("FOO", 0, 10.0),
                          ("BAR", 0, 10.0),
                          ("12345", 0, 10.0),
                          (".8*21&", 0, 10.0),
                          (".", 0, 10.0),
                          ("VERYL000nG!!$TRINGWITH$p&ci4LCHARS\t\t##"*10, 1000, 10.0),
                          ("VERYLONGSTRINGVALUEWITHONLYCHARACTERS"*10, 1000, 10.0)])
def test_valid_initialization(code, quantity, participation):
    a = Asset(code, quantity, participation)
    assert a.get_code() == code
    assert a.get_quantity() == quantity
    assert a.get_target_participation() == participation


@pytest.mark.parametrize("code,expected_error",
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
def test_invalid_code(code, expected_error):
    with pytest.raises(expected_error):
        Asset(code, 0, 10.0)


@pytest.mark.parametrize("quantity,expected_error",
                         [("", TypeError),
                          ("foo", TypeError),
                          (None, TypeError),
                          ({}, TypeError),
                          (set(), TypeError),
                          (dict(), TypeError),
                          (list(), TypeError),
                          (0.0, TypeError),
                          (50.0, TypeError),
                          (True, TypeError),
                          (False, TypeError),
                          (-1, ValueError)])
def test_invalid_quantity(quantity, expected_error):
    with pytest.raises(expected_error):
        Asset("TEST", quantity, 10.0)


def test_buy_asset():
    a = Asset("Test", 0, 10.0)
    a.buy(10)
    assert a.get_quantity() == 10
    a.buy(10)
    assert a.get_quantity() == 20
    a.buy(50)
    assert a.get_quantity() == 70
    a.buy(0)
    assert a.get_quantity() == 70
    a.buy(1)
    assert a.get_quantity() == 71

    with pytest.raises(ValueError):
        a.buy(-10)

    with pytest.raises(TypeError):
        a.buy(None)


def test_asset_from_dict():
    a = Asset.from_dict({'code': 'TEST', 'quantity': 100, 'target_participation': 50.0})
    assert a.get_code() == 'TEST'
    assert a.get_quantity() == 100
    assert a.get_target_participation() == 50.0

    a = Asset.from_dict({'code': 'test', 'quantity': 0, 'target_participation': 20.5,
                         'extra_fields': 'Make no difference'})
    assert a.get_code() == 'test'
    assert a.get_quantity() == 0
    assert a.get_target_participation() == 20.5


@pytest.mark.parametrize("invalid_dict",
                         [{'code': 'TEST', 'quantity': 100},
                          {'code': 'TEST', 'target_participation': 50.0},
                          {'quantity': 100, 'target_participation': 50.0},
                          {'code': 't'},
                          {'quantity': 100},
                          {'target_participation': 50.0},
                          {None},
                          1,
                          "foo",
                          True,
                          False,
                          [],
                          {}])
def test_asset_from_invalid_dict(invalid_dict):
    with pytest.raises(TypeError):
        Asset.from_dict(invalid_dict)


def test_asset_from_json():
    a = Asset.from_json('{"code": "TST123", "quantity": 14, "target_participation": 0.5}')
    assert a.get_code() == 'TST123'
    assert a.get_quantity() == 14
    assert a.get_target_participation() == 0.5

    a = Asset.from_json('{"code": "tst321", "quantity": 10000, "target_participation": 1.0,'
                        '"extra_fields": "Make no difference"}')
    assert a.get_code() == 'tst321'
    assert a.get_quantity() == 10000
    assert a.get_target_participation() == 1.0


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
        Asset.from_json(invalid_json)


def test_asset_has_no_price_yet():
    a = Asset('test', 0, 10.0)
    assert not a.has_current_price()

    with pytest.raises(AssetWithNoPrice):
        a.get_total_amount()

    with pytest.raises(AssetWithNoPrice):
        a.get_price()


def test_asset_pricing():
    a = Asset('test', 0, 10.0)
    assert a.update_price(lambda x: 10) == 10
    assert a.update_price(lambda x: 0) == 0
    assert a.update_price(lambda x: 5.3) == 5.3
    assert a.update_price(lambda x: 10.2) == 10.2
    assert a.update_price(lambda x: 0.0) == 0.0


def test_total_amount():
    a = Asset('test', 0, 10.0)
    a.update_price(lambda x: 10)
    assert a.get_total_amount() == 0

    a = Asset('test', 10, 10.0)
    a.update_price(lambda x: 10)
    assert a.get_total_amount() == 100
    a.update_price(lambda x: 1.0)
    assert a.get_total_amount() == 10.0


def test_asset_error_on_pricing():
    a = Asset('test', 0, 10.0)

    def http_error(*args):
        raise requests.HTTPError()

    with pytest.raises(AssetPricingError):
        a.update_price(http_error)
