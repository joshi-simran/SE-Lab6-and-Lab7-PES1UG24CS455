import pytest

from coupon_validator import (
    coupon_discount,
    best_discount,
    is_expired
)


def test_coupon_discount_all_branches():

    # Invalid cart
    with pytest.raises(ValueError):
        coupon_discount("WELCOME10", 0, True, "mon")

    # WELCOME10: True and False branches
    assert coupon_discount(
        "WELCOME10", 200, True, "mon"
    ) == 20

    assert coupon_discount(
        "WELCOME10", 200, False, "mon"
    ) == 0

    # WEEKEND20: Weekend and weekday branches
    assert coupon_discount(
        "WEEKEND20", 600, False, "sat"
    ) == 120

    assert coupon_discount(
        "WEEKEND20", 400, False, "sun"
    ) == 50

    assert coupon_discount(
        "WEEKEND20", 600, False, "mon"
    ) == 0

    # FLAT100: True and False branches
    assert coupon_discount(
        "FLAT100", 400, False, "mon"
    ) == 100

    assert coupon_discount(
        "FLAT100", 300, False, "mon"
    ) == 0

    # Unknown coupon
    assert coupon_discount(
        "UNKNOWN", 400, False, "mon"
    ) == 0


def test_best_discount_all_branches():

    # Empty list: loop does not execute
    assert best_discount(
        [], 1000, False, "mon"
    ) == 0

    # Loop executes and discount is updated
    assert best_discount(
        ["WELCOME10"], 200, True, "mon"
    ) == 20

    # Discount is not updated when value is zero
    assert best_discount(
        ["WELCOME10"], 200, False, "mon"
    ) == 0

    # Multiple coupons
    assert best_discount(
        ["WELCOME10", "FLAT100"],
        1000, False, "mon"
    ) == 100

    # Cap condition: False
    assert best_discount(
        ["WEEKEND20"], 1000, False, "sat"
    ) == 200

    # Cap condition: True
    assert best_discount(
        ["WEEKEND20"], 100, False, "sat"
    ) == 40


def test_is_expired_all_branches():

    # days_valid <= 0
    assert is_expired(10, 5, 0) is True

    # Expiry condition: True
    assert is_expired(11, 5, 5) is True

    # Expiry condition: False
    assert is_expired(10, 5, 5) is False