# receipts/serializers.py
from rest_framework import serializers

class ItemSerializer(serializers.Serializer):
    shortDescription = serializers.CharField()
    price = serializers.CharField()

class ReceiptSerializer(serializers.Serializer):
    retailer = serializers.CharField()
    purchaseDate = serializers.DateField()
    purchaseTime = serializers.TimeField()
    total = serializers.CharField()
    items = ItemSerializer(many=True)
