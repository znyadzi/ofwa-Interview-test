import csv
from django.shortcuts import render
from rest_framework.parsers import FileUploadParser, MultiPartParser
from io import TextIOWrapper
from rest_framework import status
from rest_framework.decorators import api_view, parser_classes
from rest_framework.response import Response
from .models import GSiteData
from .serializers import GSiteDataSerializer
from django.db.models import Avg, Sum
from .forms import CSVUploadForm
from django.http import JsonResponse

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

@api_view(['POST'])
@parser_classes([MultiPartParser])
def upload_csv(request):
    try:  # Enclose the entire file processing within the try block
        if 'file' not in request.FILES:
            return Response({'error': 'No file uploaded'}, status=status.HTTP_400_BAD_REQUEST)

        csv_file = request.FILES['file']
        decoded_file = TextIOWrapper(csv_file.file, encoding='utf-8')
        reader = csv.DictReader(decoded_file)

        # Validate CSV headers (case-insensitive)
        required_headers = ['Town', 'Region', 'Number_of_Galamsay_Sites']
        if not all(header.lower() in map(str.lower, reader.fieldnames) for header in required_headers):
            missing_headers = set(required_headers) - set(map(str.lower, reader.fieldnames))
            return Response({'error': f'CSV file is missing required headers: {", ".join(missing_headers)}'}, status=status.HTTP_400_BAD_REQUEST)

        serializer = GSiteDataSerializer(data=[row for row in reader], many=True)

        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'CSV data uploaded successfully', 'data': serializer.data}, status=status.HTTP_201_CREATED)
        else:
            return Response({'error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    except (csv.Error, UnicodeDecodeError) as e:  # Handle CSV and Unicode errors
        return Response({'error': f'Error processing CSV file: {str(e)}'}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e: # Catch any other exceptions during processing
        return Response({'error': f'An unexpected error occurred: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

