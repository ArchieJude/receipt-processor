import pytest
from django.urls import reverse
from rest_framework.test import APIClient
import uuid

@pytest.fixture
def client():
    return APIClient()


def test_process_receipt(client):
    url = reverse("process_receipt")
    payload = {
        "retailer": "Target",
        "purchaseDate": "2022-01-01",
        "purchaseTime": "13:01",
        "items": [
            {"shortDescription": "Mountain Dew 12PK", "price": "6.49"},
            {"shortDescription": "Emils Cheese Pizza", "price": "12.25"},
        ],
        "total": "18.74",
    }
    response = client.post(url, payload, format="json")
    assert response.status_code == 200
    assert "id" in response.data


@pytest.mark.parametrize(
    "payload,expected_points",
    [
        # Test case, example 1
        (
            {
                "retailer": "Target",
                "purchaseDate": "2022-01-01",
                "purchaseTime": "13:01",
                "items": [
                    {"shortDescription": "Mountain Dew 12PK", "price": "6.49"},
                    {"shortDescription": "Emils Cheese Pizza", "price": "12.25"},
                    {"shortDescription": "Knorr Creamy Chicken", "price": "1.26"},
                    {"shortDescription": "Doritos Nacho Cheese", "price": "3.35"},
                    {
                        "shortDescription": "   Klarbrunn 12-PK 12 FL OZ  ",
                        "price": "12.00",
                    },
                ],
                "total": "35.35",
            },
            28, # expected point
        ),
        # Test case, example 2
        (
            {
                "retailer": "M&M Corner Market",
                "purchaseDate": "2022-03-20",
                "purchaseTime": "14:33",
                "items": [
                    {"shortDescription": "Gatorade", "price": "2.25"},
                    {"shortDescription": "Gatorade", "price": "2.25"},
                    {"shortDescription": "Gatorade", "price": "2.25"},
                    {"shortDescription": "Gatorade", "price": "2.25"},
                ],
                "total": "9.00",
            },
            109, # expected point
        ),

    ],
)
def test_receipt_points(client, payload, expected_points):
    process_url = reverse("process_receipt")
    response = client.post(process_url, payload, format="json")
    assert response.status_code == 200
    receipt_id = response.data["id"]

    points_url = reverse("get_points", args=[receipt_id])
    points_response = client.get(points_url)

    assert points_response.status_code == 200
    assert points_response.data["points"] == expected_points


def test_process_receipt_missing_items(client):
    payload = {
        "retailer": "Target",
        "purchaseDate": "2022-01-01",
        "purchaseTime": "13:01",
        "total": "35.35"
        # 'items' field is missing
    }
    response = client.post(reverse("process_receipt"), payload, format="json")
    assert response.status_code == 400
    assert "The receipt is invalid." in response.data.get("error", "")

@pytest.mark.parametrize(
    "bad_payload,invalid_field",
    [
        # retailer should be string
        ({"retailer": 12345, "purchaseDate": "2022-01-01", "purchaseTime": "13:01", "items": [], "total": "10.00"}, "retailer"),
        
        # purchaseDate should be string (formatted date)
        ({"retailer": "Target", "purchaseDate": 20220101, "purchaseTime": "13:01", "items": [], "total": "10.00"}, "purchaseDate"),

        # purchaseTime should be string (formatted time)
        ({"retailer": "Target", "purchaseDate": "2022-01-01", "purchaseTime": 1301, "items": [], "total": "10.00"}, "purchaseTime"),

        # items should be a list
        ({"retailer": "Target", "purchaseDate": "2022-01-01", "purchaseTime": "13:01", "items": "not-a-list", "total": "10.00"}, "items"),

        # total should be string (representing a decimal)
        ({"retailer": "Target", "purchaseDate": "2022-01-01", "purchaseTime": "13:01", "items": [], "total": "ten"}, "total"),
        
        # total should be string (representing a decimal)
        ({"retailer": "Target", "purchaseDate": "2022-01-01", "purchaseTime": "13:01", "items": [], "total": 10}, "total"),
        
    ]
)
def test_process_receipt_with_invalid_field_types(client, bad_payload, invalid_field):
    url = reverse("process_receipt")
    response = client.post(url, bad_payload, format="json")

    assert response.status_code == 400
    assert "The receipt is invalid." in response.data.get("error", "") or "The receipt is invalid." in str(response.data)

def test_get_points_receipt_not_found(client):
    fake_receipt_id = str(uuid.uuid4())
    url = reverse("get_points", args=[fake_receipt_id])
    response = client.get(url)

    assert response.status_code == 404
    assert "No receipt found for that ID." in response.data.get("error", "")
