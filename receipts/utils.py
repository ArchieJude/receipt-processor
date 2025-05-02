# receipts/utils.py
import math
from datetime import time


def calculate_rule_1(receipt_data):
    # Rule 1: One point for every alphanumeric character in the retailer name
    retailer = receipt_data['retailer']
    return sum(c.isalnum() for c in retailer)

def calculate_rule_2(receipt_data):
    # Rule 2: 50 points if the total is a round dollar amount with no cents
    total = float(receipt_data['total'])
    
    if total.is_integer():
        return 50
    return 0
        
def calculate_rule_3(receipt_data):
    # Rule 2: 50 points if the total is a round dollar amount with no cents
    total = float(receipt_data['total'])
    
    if (total * 100) % 25 == 0:
        return 25
    return 0

def calculate_rule_4(receipt_data):
    # Rule 4: 5 points for every two items on the receipt
    items = receipt_data['items']
    return (len(items) // 2) * 5

def calculate_rule_5(receipt_data):
    # Rule 5: If the trimmed length of the item description is a multiple of 3,
    # multiply the price by 0.2 and round up to the nearest integer
    items = receipt_data['items']
    point_to_return = 0
    for item in items:
        description = item['shortDescription'].strip()
        if len(description) % 3 == 0:
            price = float(item['price'])
            point_to_return += math.ceil(price * 0.2)
    return point_to_return

def calculate_rule_6(receipt_data):
    # Rule 6: 6 points if the day in the purchase date is odd
    purchase_date = receipt_data['purchaseDate']  # already a datetime.date
    point_to_return = 0
    if purchase_date.day % 2 == 1:
        point_to_return += 6
    return point_to_return


def calculate_rule_7(receipt_data):
    # Rule 7: 10 points if the time of purchase is after 2:00pm and before 4:00pm
    purchase_time = receipt_data['purchaseTime']  # already a datetime.time object
    if time(14, 0) < purchase_time < time(16, 0):
        return 10
    return 0

            
def calculate_points(receipt_data):
    points = 0

    points += calculate_rule_1(receipt_data)

    points += calculate_rule_2(receipt_data)

    points += calculate_rule_3(receipt_data)

    points += calculate_rule_4(receipt_data)
    
    points += calculate_rule_5(receipt_data)
    
    points += calculate_rule_6(receipt_data)

    points += calculate_rule_7(receipt_data)


    return points
