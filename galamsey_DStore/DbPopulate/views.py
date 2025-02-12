import json
import csv
import io
import logging
from django.urls import reverse
from django.http import JsonResponse, HttpResponse
from django.db import IntegrityError
from django.http import JsonResponse
from rest_framework import status
from rest_framework.decorators import api_view, parser_classes
from rest_framework.response import Response
from .models import GSiteData
from .serializers import GSiteDataSerializer, ThresHoldDataSerializer, CSVUploadSerializer
from django.db.models import Avg, Sum
from rest_framework.parsers import MultiPartParser, FormParser


# Create your views here.

# CRUD Operations
@api_view(['GET'])
def api_root(request):
    """
    API Root endpoint that provides clickable links to all API endpoints in an HTML-rendered view.
    """
    endpoints = {
        "GSite Data List (CRUD)": reverse('gsite-data-list'),
        "Total Galamsey Sites": reverse('total-galamsey-sites'),
        "Average Galamsey Sites Per Region": reverse('average-galamsey-sites-per-region'),
        "Region with Highest Galamsey Sites": reverse('region-with-highest-galamsey-sites'),
        "Regions Above a Threshold": reverse('regions_above_threshold'),
        "Upload CSV File": reverse('upload-csv'),
    }

    # Generate an HTML response with clickable links
    html_response = '<center><h1>Welcome to the Galamsey Site Analyser API  Page</h1><center>'
    html_response += '<h3>Below are the available endpoints:</h3>'
    html_response += '<h2>'
    for name, url in endpoints.items():
        full_url = request.build_absolute_uri(url)
        html_response += f'<p><a href="{full_url}">{name}</a></p><br>'
    html_response += '</h2>'

    return HttpResponse(html_response)



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

    elif request.method == 'DELETE':
        try:
            data = json.loads(request.body)
            ids_to_delete = data.get('id', [])  # Get IDs, default to empty list if not found
            deleted_count = GSiteData.objects.filter(pk__in=ids_to_delete).delete()[0] #returns a tuple (rows_affected,row_ids)
            return Response({'deleted': deleted_count}, status=status.HTTP_200_OK) #or status.HTTP_204_NO_CONTENT if you don't want to return the count
        except json.JSONDecodeError:
            return Response({'error': 'Invalid JSON payload'}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


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
def regions_with_sites_above_threshold(request):
    # Get the threshold value from request data
    threshold = request.data.get('threshold', None)

    if threshold is None:
        return Response({'error': 'Threshold parameter is required'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        threshold = int(threshold)  # Convert threshold to an integer
    except ValueError:
        return Response({'error': 'Threshold must be a valid integer'}, status=status.HTTP_400_BAD_REQUEST)

    # Query the database for regions with sites above the threshold
    sites_above_threshold = GSiteData.objects.filter(Number_of_Galamsay_Sites__gt=threshold)

    # Serialize the filtered results
    serializer = GSiteDataSerializer(sites_above_threshold, many=True)

    return Response(serializer.data, status=status.HTTP_200_OK)


logger = logging.getLogger(__name__)

@api_view(['POST'])
@parser_classes([MultiPartParser, FormParser])
def upload_csv(request):
    if request.method == 'POST':
        # Check if a file is included in the request
        if 'file' not in request.FILES:
            return JsonResponse({'error': 'No file provided'}, status=400)

        # Retrieve the uploaded file
        file = request.FILES['file']

        # Check if the file is a CSV
        if not file.name.endswith('.csv'):
            return JsonResponse({'error': 'Invalid file format. Only CSV files are allowed.'}, status=400)

        # Decode and read the file
        try:
            data = io.StringIO(file.read().decode('utf-8'))
        except UnicodeDecodeError:
            return JsonResponse({'error': 'Unable to decode file. Ensure the file encoding is UTF-8.'}, status=400)

        # Parse the CSV and process data
        csv_reader = csv.reader(data)
        next(csv_reader)  # Skip the header row

        duplicate_entries = []
        invalid_entries = []
        successful_inserts = 0

        for row in csv_reader:
            if len(row) != 3:
                # Skip rows with incorrect number of columns
                invalid_entries.append({'row': row, 'error': 'Invalid row format'})
                continue

            town, region, number_of_sites = row

            # Validate `number_of_sites` is an integer
            try:
                number_of_sites = int(number_of_sites)
            except ValueError:
                invalid_entries.append({'row': row, 'error': 'Invalid datatype for Number_of_Galamsay_Sites'})
                continue

            # Create entry in the database
            try:
                GSiteData.objects.create(
                    Town=town.strip(),
                    Region=region.strip(),
                    Number_of_Galamsay_Sites=number_of_sites
                )
                successful_inserts += 1
            except IntegrityError:
                # Skip duplicate entries based on Town and Region uniqueness constraint
                duplicate_entries.append({'row': row, 'error': 'Duplicate entry'})

        # Prepare response with summary of results
        response = {
            'status': 'success',
            'details': {
                'successful_inserts': successful_inserts,
                'duplicates': len(duplicate_entries),
                'invalid_entries': len(invalid_entries),
                'skipped_duplicates': duplicate_entries,
                'skipped_invalid_entries': invalid_entries,
            },
        }
        return JsonResponse(response, status=200)

    return JsonResponse({'error': 'Unsupported HTTP method. Use POST instead.'}, status=405)
