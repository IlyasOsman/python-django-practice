from rest_framework.response import Response
from rest_framework.decorators import api_view
from base.models import Item  # Make sure you import the Item model correctly
from .serializers import ItemSerializer

@api_view(['GET'])
def getData(request):  # Add the 'request' parameter here
    items = Item.objects.all()  # Correct the variable name to 'Item'
    serializer = ItemSerializer(items, many=True)
    return Response(serializer.data)

@api_view(['POST'])
def addItem(request):
    serializer = ItemSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
    return Response(serializer.data)