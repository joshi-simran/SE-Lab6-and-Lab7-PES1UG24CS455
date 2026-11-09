from datetime import date
import math


def split_code(code):

    # Validate input type
    if not isinstance(code, str):
        raise ValueError("Coupon code must be a string")

    parts = code.strip().split("-")

    # Ensure exactly two parts
    if len(parts) != 2:
        raise ValueError("Invalid coupon code format")

    prefix, value_text = parts

    # Ensure neither part is empty
    if not prefix or not value_text:
        raise ValueError("Coupon prefix and value cannot be empty")

    try:
        value = int(value_text)
    except ValueError:
        raise ValueError("Coupon value must be an integer") from None

    # Reject negative values
    if value < 0:
        raise ValueError("Coupon value cannot be negative")

    return prefix.upper(), value


def most_expensive(prices_csv):

    # Validate input type
    if not isinstance(prices_csv, str):
        raise ValueError("Prices must be provided as a string")

    parts = prices_csv.split(",")

    # Reject empty input or empty elements
    if not parts or any(not p.strip() for p in parts):
        raise ValueError("Price list cannot be empty")

    try:
        prices = [float(p.strip()) for p in parts]
    except ValueError:
        raise ValueError("All prices must be numeric") from None

    # Reject NaN and infinity
    if not all(math.isfinite(p) for p in prices):
        raise ValueError("Prices must be finite numbers")

    return max(prices)


def expiry_days(date_text):

    # Validate input type
    if not isinstance(date_text, str):
        raise ValueError("Date must be a string")

    try:
        parsed_date = date.fromisoformat(date_text)
    except ValueError:
        raise ValueError("Date must be a valid YYYY-MM-DD date") from None

    # Enforce exact YYYY-MM-DD format
    if parsed_date.isoformat() != date_text:
        raise ValueError("Date must use YYYY-MM-DD format")

    year = parsed_date.year
    month = parsed_date.month
    day = parsed_date.day

    return (
        (year - 2024) * 365
        + (month - 1) * 30
        + day
    )


def main():

    print("==== Running split_code ====")
    user_input = input("Enter a coupon code (e.g. save-20): ")
    result = split_code(user_input)
    print("Prefix and Value:", result)

    print("\n==== Running most_expensive ====")
    user_input = input(
        "Enter item prices as CSV (e.g. 199,49.5,320): "
    )
    result = most_expensive(user_input)
    print("Most Expensive Item:", result)

    print("\n==== Running expiry_days ====")
    user_input = input("Enter an expiry date as YYYY-MM-DD: ")
    result = expiry_days(user_input)
    print("Days Since 2024:", result)


if __name__ == "__main__":
    main()