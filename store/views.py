from . models import Box
from . filters import BoxFilter
from . serializers import BoxSerializer, AdminBoxSerializer
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.parsers import JSONParser
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAdminUser
from . Validation import check_validity

"""
Create New Box API
"""
@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAdminUser])
def create_box(request):
    box = Box(created_by=request.user)
    data = JSONParser().parse(request)
    serializer = AdminBoxSerializer(box, data=data, partial=True)
    if serializer.is_valid() and check_validity(request.user, request, data):
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(data={"reason":"Forbidden due to constraints"}, status=status.HTTP_409_CONFLICT)

"""
List All Box API
"""
@api_view(['GET'])
@authentication_classes([TokenAuthentication])
def list_box(request):
    box_queryset = Box.objects.all()
    boxes = BoxFilter(request.GET, queryset=box_queryset).qs
    if request.user == IsAdminUser:
        serializer = AdminBoxSerializer(boxes, many=True)
    else:
        serializer = BoxSerializer(boxes, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

"""
List My Boxes API 
"""
@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAdminUser])
def my_list_box(request):
    box_queryset = Box.objects.filter(created_by=request.user)
    boxes = BoxFilter(request.GET,queryset=box_queryset).qs
    serializer = AdminBoxSerializer(boxes, many=True)
    return Response(serializer.data,status=status.HTTP_200_OK)


"""
Update Box with User ID
"""
@api_view(['PUT'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAdminUser])
def update_box(request, pk):
    try:
        box = Box.objects.get(pk=pk)
    except Box.DoesNotExist:
        data = {
            "reason" : "No such box exists in database"
        }
        return Response(data, status=status.HTTP_404_NOT_FOUND)
    
    data = JSONParser().parse(request)
    serializer = AdminBoxSerializer(instance=box, data=data, partial=True)
    if serializer.is_valid() and check_validity(request.user, request, data, pk):
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(data={"reason":"Forbidden due to constraints"}, status=status.HTTP_409_CONFLICT)

"""
Delete Box With Given ID
"""
@api_view(['DELETE'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAdminUser])
def delete_box(request, pk):

    try:
        box = Box.objects.get(pk=pk)
        if request.user == box.created_by:
            data = {
                "delete" : "successful"
            }
            box.delete()
        else:
            data = {
            "reason" : "You must be creator of the Box."
            }
            return Response(data, status=status.HTTP_403_FORBIDDEN)
        return Response(data, status=status.HTTP_200_OK)

    except Box.DoesNotExist:
        data = {
            "reason" : "No such box exists in database"
            }
        return Response(data,status=status.HTTP_404_NOT_FOUND)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)