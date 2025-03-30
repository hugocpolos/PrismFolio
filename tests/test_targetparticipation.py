from prismfolio.targetparticipation import TargetParticipation
import random
import pytest


def test_valid_initialization():
    for i in range(1, 101):
        TargetParticipation(float(i))


def test_random_values_valid_initialization():
    for _ in range(1000):
        TargetParticipation(random.random()*100)


@pytest.mark.parametrize("non_float_value", [1, 50, 0, "foo", None, True, False, dict(), set()])
def test_non_float_initialization(non_float_value):
    with pytest.raises(TypeError):
        TargetParticipation(non_float_value)


@pytest.mark.parametrize("negative_value", [-5.0, -.0000001, -.0000000001])
def test_negative_value_initialization(negative_value):
    with pytest.raises(ValueError):
        TargetParticipation(negative_value)


def test_zero_value_initialization():
    with pytest.raises(ValueError):
        TargetParticipation(0.0)
    TargetParticipation(0.0000001)


@pytest.mark.parametrize("high_value", [100.00001, 100.00000001, 1000000.0])
def test_high_value_initialization(high_value):
    with pytest.raises(ValueError):
        TargetParticipation(high_value)


@pytest.mark.parametrize("participation_value", [0.001, 2.0, 3.5, 6.0, 50.0, 99.9999, 100.0])
def test_get_participation_value(participation_value):
    _t = TargetParticipation(participation_value)
    assert _t.get_target_participation() == participation_value
