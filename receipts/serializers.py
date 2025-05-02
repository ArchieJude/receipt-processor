from rest_framework import serializers

class ItemSerializer(serializers.Serializer):
    shortDescription = serializers.CharField()
    price = serializers.CharField()

class ReceiptSerializer(serializers.Serializer):
    retailer = serializers.CharField()
    purchaseDate = serializers.DateField()
    purchaseTime = serializers.TimeField()
    total = serializers.CharField()
    items = serializers.ListField(child=ItemSerializer())

    def validate_retailer(self, value):
        if not isinstance(value, str):
            raise serializers.ValidationError("Retailer must be a string.")
        return value

    def validate_purchaseDate(self, value):
        if not hasattr(value, 'day'):  # ensure it's a datetime.date instance
            raise serializers.ValidationError("purchaseDate must be a valid date.")
        return value

    def validate_purchaseTime(self, value):
        if not hasattr(value, 'hour'):  # ensure it's a datetime.time instance
            raise serializers.ValidationError("purchaseTime must be a valid time.")
        return value

    def validate_total(self, value):
        if not isinstance(value, str):
            raise serializers.ValidationError("Total must be a string.")
        try:
            float(value)
        except ValueError:
            raise serializers.ValidationError("Total must be a string representing a decimal number.")
        return value

    def validate_items(self, value):
        if not isinstance(value, list):
            raise serializers.ValidationError("Items must be a list.")
        if not value:
            raise serializers.ValidationError("Items list cannot be empty.")
        return value
