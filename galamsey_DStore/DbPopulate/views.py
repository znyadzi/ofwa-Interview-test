from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import GSiteData
from .serializers import GSiteDataSerializer
from django.db.models import Avg, Sum

# Create your views here.

# CRUD Operations

@api_view(['GET', 'POST'])
def gsite_data_list(request):
    if request.method == 'GET':
        data = GSiteData.objects.all()
        serializer = GSiteDataSerializer(data, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = GSiteDataSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
def gsite_data_detail(request, pk):
    try:
        data = GSiteData.objects.get(pk=pk)
    except GSiteData.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = GSiteDataSerializer(data)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = GSiteDataSerializer(data, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        data.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

# Custom Functions

@api_view(['GET'])
def total_galamsey_sites(request):
    total = GSiteData.objects.aggregate(Sum('Number_of_Galamsay_Sites'))
    return Response({'total_galamsey_sites': total['Number_of_Galamsay_Sites__sum']})

@api_view(['GET'])
def average_galamsey_sites_per_region(request):
    average = GSiteData.objects.values('Region').annotate(avg_sites=Avg('Number_of_Galamsay_Sites'))
    return Response(average)


@api_view(['GET'])
def region_with_highest_galamsey_sites(request):
    # Aggregate the total number of Galamsey sites per region
    regions = GSiteData.objects.values('Region').annotate(total_sites=Sum('Number_of_Galamsay_Sites')).order_by(
        '-total_sites')

    # Get the region with the highest number of Galamsey sites
    if regions:
        highest_region = regions[0]
        return Response({
            'region': highest_region['Region'],
            'total_galamsey_sites': highest_region['total_sites']
        })
    else:
        return Response({'message': 'No data available'}, status=404)
