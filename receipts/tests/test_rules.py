import pytest
from receipts.utils import calculate_rule_1, calculate_rule_2, calculate_rule_3, calculate_rule_4, calculate_rule_5, calculate_rule_6, calculate_rule_7
import datetime
from datetime import time

@pytest.mark.parametrize(
    "retailer,expected_points",
    [
        ("ABC123", 6),         # All characters are alphanumeric
        ("A B!C@1", 4),        # A, B, C, 1
        ("!!!", 0),            # No alphanumerics
        ("Shop#Mart 99", 10),  # ShopMart99 (space and # excluded)
        ("", 0),               # Empty string
    ]
)
def test_calculate_rule_1(retailer, expected_points):
    # Rule 1: One point for every alphanumeric character in the retailer name.
    receipt_data = {"retailer": retailer}
    assert calculate_rule_1(receipt_data) == expected_points


@pytest.mark.parametrize(
    "total,expected_points",
    [
        ("20.00", 50),   # round dollar
        ("100.0", 50),   # also round
        ("0", 50),       # edge case: zero dollars
        ("12.34", 0),    # not round
        ("99.99", 0),    # not round
        ("10.50", 0),    # 50 cents not allowed
    ]
)
def test_calculate_rule_2(total, expected_points):
    # Rule 2: 50 points if the total is a round dollar amount with no cents.
    receipt_data = {"total": total}
    assert calculate_rule_2(receipt_data) == expected_points
    
    
@pytest.mark.parametrize(
    "total,expected_points",
    [
        ("1.00", 25),     # 100 % 25 == 0
        ("0.25", 25),     # 25 % 25 == 0
        ("2.75", 25),     # 275 % 25 == 0
        ("10.50", 25),    # 1050 % 25 == 0
        ("0.10", 0),      # 10 % 25 != 0
        ("3.33", 0),      # not divisible by 25
        ("4.99", 0),      # close, but not exact
    ]
)
def test_calculate_rule_3(total, expected_points):
    # Rule 3: 25 points if the total is a multiple of 0.25.
    receipt_data = {"total": total}
    assert calculate_rule_3(receipt_data) == expected_points
    
    
@pytest.mark.parametrize(
    "items,expected_points",
    [
        ([], 0),
        ([{"shortDescription": "A", "price": "1.00"}], 0),
        ([{"shortDescription": "A", "price": "1.00"}, {"shortDescription": "B", "price": "2.00"}], 5),
        ([{"shortDescription": "A", "price": "1.00"}] * 5, 10),  # 2 full pairs
    ]
)
def test_calculate_rule_4(items, expected_points):
    # Rule 4: 5 points for every two items on the receipt.
    receipt_data = {"items": items}
    assert calculate_rule_4(receipt_data) == expected_points


@pytest.mark.parametrize(
    "items,expected_points",
    [
        # desc len = 3 → ceil(1.00 * 0.2) = 1
        ([{"shortDescription": "abc", "price": "1.00"}], 1),
        # desc len = 6 → ceil(5.00 * 0.2) = 1
        ([{"shortDescription": "banana", "price": "5.00"}], 1),
        # desc len = 4 → ignored
        ([{"shortDescription": "milk", "price": "2.00"}], 0),
        # mixed
        ([
            {"shortDescription": "abc", "price": "1.00"},   # 1
            {"shortDescription": "xyz", "price": "3.00"},   # 1
            {"shortDescription": "ice", "price": "2.00"},   # 1
            {"shortDescription": "beef", "price": "6.00"}   # 0
        ], 3),
    ]
)
def test_calculate_rule_5(items, expected_points):
    # Rule 5: If the trimmed length of the item description is a multiple of 3, multiply the price by 0.2 and round up to the nearest integer. The result is the number of points earned.
    receipt_data = {"items": items}
    assert calculate_rule_5(receipt_data) == expected_points


@pytest.mark.parametrize(
    "purchase_date,expected_points",
    [
        (datetime.date(2022, 1, 1), 6),
        (datetime.date(2022, 1, 2), 0),
        (datetime.date(2022, 1, 31), 6),
        (datetime.date(2022, 12, 30), 0),
    ]
)
def test_calculate_rule_6(purchase_date, expected_points):
    # Rule 6: 6 points if the day in the purchase date is odd.
    receipt_data = {"purchaseDate": purchase_date}
    assert calculate_rule_6(receipt_data) == expected_points


@pytest.mark.parametrize(
    "purchase_time,expected_points",
    [
        (time(14, 0), 0),      # Exactly 2:00 PM → excluded
        (time(14, 1), 10),     # After 2:00 PM → included
        (time(15, 59), 10),    # Before 4:00 PM → included
        (time(16, 0), 0),      # Exactly 4:00 PM → excluded
        (time(13, 59), 0),     # Before 2:00 PM → excluded
    ]
)
def test_calculate_rule_7(purchase_time, expected_points):
    # Rule 7: 10 points if the time of purchase is after 2:00pm and before 4:00pm.
    receipt_data = {"purchaseTime": purchase_time}
    assert calculate_rule_7(receipt_data) == expected_points
