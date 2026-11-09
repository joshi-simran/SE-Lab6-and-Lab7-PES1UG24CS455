import math
from datetime import date

import pytest
from hypothesis import given, strategies as st

from coupon_validator import (
    split_code,
    most_expensive,
    expiry_days
)


# Test 1: Fuzz split_code()
@given(st.one_of(st.text(), st.none()))
def test_split_code_no_crash(s):

    try:
        result = split_code(s)

    except ValueError:
        return

    except Exception as e:
        pytest.fail(
            f"split_code crashed with {s!r}: {e}"
        )

    assert isinstance(result, tuple)
    assert len(result) == 2

    prefix, value = result

    assert isinstance(prefix, str)
    assert prefix != ""
    assert isinstance(value, int)
    assert value >= 0


# Test 2: Fuzz most_expensive()
@given(st.one_of(st.text(), st.none()))
def test_most_expensive_no_crash(s):

    try:
        result = most_expensive(s)

    except ValueError:
        return

    except Exception as e:
        pytest.fail(
            f"most_expensive crashed with {s!r}: {e}"
        )

    try:
        prices = [
            float(p.strip())
            for p in s.split(",")
        ]

        assert prices
        assert all(math.isfinite(p) for p in prices)

    except (ValueError, TypeError, AttributeError):
        pytest.fail(
            f"most_expensive accepted invalid input: {s!r}"
        )

    assert math.isfinite(result)
    assert result == max(prices)


# Test 3: Fuzz expiry_days()
@given(st.one_of(st.text(), st.none()))
def test_expiry_days_no_crash(s):

    try:
        result = expiry_days(s)

    except ValueError:
        return

    except Exception as e:
        pytest.fail(
            f"expiry_days crashed with {s!r}: {e}"
        )

    try:
        parsed_date = date.fromisoformat(s)

    except (ValueError, TypeError):
        pytest.fail(
            f"expiry_days accepted invalid date: {s!r}"
        )

    expected = (
        (parsed_date.year - 2024) * 365
        + (parsed_date.month - 1) * 30
        + parsed_date.day
    )

    assert result == expected