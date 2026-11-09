import pytest

from coupon_validator import (
    coupon_discount,
    best_discount,
    is_expired
)


def test_coupon_discount_all_paths():

    # Empty cart should raise ValueError
    with pytest.raises(ValueError):
        coupon_discount("WELCOME10", 0, True, "mon")

    # WELCOME10 for a new user
    assert coupon_discount(
        "WELCOME10", 200, True, "mon"
    ) == 20

    # WELCOME10 for an existing user
    assert coupon_discount(
        "WELCOME10", 200, False, "mon"
    ) == 0

    # WEEKEND20 on Saturday with cart >= 500
    assert coupon_discount(
        "WEEKEND20", 600, False, "sat"
    ) == 120

    # WEEKEND20 on Sunday with cart < 500
    assert coupon_discount(
        "WEEKEND20", 400, False, "sun"
    ) == 50

    # WEEKEND20 on a weekday
    assert coupon_discount(
        "WEEKEND20", 600, False, "mon"
    ) == 0

    # FLAT100 with cart > 300
    assert coupon_discount(
        "FLAT100", 400, False, "mon"
    ) == 100

    # FLAT100 with cart <= 300
    assert coupon_discount(
        "FLAT100", 300, False, "mon"
    ) == 0

    # Unknown coupon
    assert coupon_discount(
        "UNKNOWN", 400, False, "mon"
    ) == 0


def test_best_discount_all_paths():

    # Empty coupon list
    assert best_discount(
        [], 1000, False, "mon"
    ) == 0

    # A valid discount
    assert best_discount(
        ["WELCOME10"], 200, True, "mon"
    ) == 20

    # Multiple coupons
    assert best_discount(
        ["WELCOME10", "FLAT100"],
        1000, False, "mon"
    ) == 100

    # Discount cap is not exceeded
    assert best_discount(
        ["WEEKEND20"], 1000, False, "sat"
    ) == 200

    # Discount cap is applied
    assert best_discount(
        ["WEEKEND20"], 100, False, "sat"
    ) == 40


def test_is_expired_all_paths():

    # Zero validity
    assert is_expired(10, 5, 0) is True

    # Coupon has expired
    assert is_expired(11, 5, 5) is True

    # Coupon has not expired
    assert is_expired(10, 5, 5) is False