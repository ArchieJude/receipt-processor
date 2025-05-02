# receipts/views.py
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .serializers import ReceiptSerializer
from .utils import calculate_points
import uuid

# In-memory store for receipts
receipts_store = {}

@api_view(['POST'])
def process_receipt(request):
    serializer = ReceiptSerializer(data=request.data)
    if serializer.is_valid():
        receipt_data = serializer.validated_data
        points = calculate_points(receipt_data)
        receipt_id = str(uuid.uuid4())
        receipts_store[receipt_id] = points
        return Response({"id": receipt_id}, status=status.HTTP_200_OK)
    return Response({"error": "The receipt is invalid."}, status=status.HTTP_400_BAD_REQUEST)
@api_view(['GET'])
def get_points(request, receipt_id):
    points = receipts_store.get(receipt_id)
    if points is not None:
        return Response({"points": points}, status=status.HTTP_200_OK)
    return Response({"error": "No receipt found for that ID."}, status=status.HTTP_404_NOT_FOUND)
