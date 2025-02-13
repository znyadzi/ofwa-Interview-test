import json
import csv
import io
import logging
from django.urls import reverse
from django.http import JsonResponse, HttpResponse
from django.db import IntegrityError
from django.http import JsonResponse
from django.utils.timezone import now
from rest_framework import status
from rest_framework.decorators import api_view, parser_classes
from rest_framework.response import Response
from .models import GSiteData, CsvFileData
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



@api_view(['GET', 'POST', 'DELETE'])
def gsite_data_list(request):
    if request.method == 'GET':
        """
        Description: Retrieves a list of all GSite data.
        Example Request:
        GET /gsite/
        Example Response:
        [
            {
                "id": 1,
                "City": "Accra",
                "Region": "Greater Accra",
                "Number_of_Galamsay_Sites": 12
            },
            {
                "id": 2,
                "City": "Kumasi",
                "Region": "Ashanti",
                "Number_of_Galamsay_Sites": 20
            }
        ]
        """
        data = GSiteData.objects.all()
        serializer = GSiteDataSerializer(data, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        """
        Description: Adds new GSite data.
        Example Request:
        POST /gsite/
        Body:
        {
            "City": "Accra",
            "Region": "Greater Accra",
            "Number_of_Galamsay_Sites": 15
        }
        Example Response:
        {
            "id": 3,
            "City": "Accra",
            "Region": "Greater Accra",
            "Number_of_Galamsay_Sites": 15
        }
        """
        serializer = GSiteDataSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        """
        Description: Deletes GSite data by ID.
        Example Request:
        DELETE /gsite/
        Body (JSON):
        {
            "id": [1, 2, 3]
        }
        Example Response:
        {
            "deleted": 3
        }
        """
        try:
            data = json.loads(request.body)
            ids_to_delete = data.get('id', [])
            deleted_count = GSiteData.objects.filter(pk__in=ids_to_delete).delete()[0]
            return Response({'deleted': deleted_count}, status=status.HTTP_200_OK)
        except json.JSONDecodeError:
            return Response({'error': 'Invalid JSON payload'}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
def total_galamsey_sites(request):
    """
    Description: Retrieves the total number of Galamsey sites across all regions.
    Example Request:
    GET /total-galamsey-sites/
    Example Response:
    {
        "total_galamsey_sites": 150
    }
    """
    total = GSiteData.objects.aggregate(Sum('Number_of_Galamsay_Sites'))
    return Response({'total_galamsey_sites': total['Number_of_Galamsay_Sites__sum']})

@api_view(['GET'])
def average_galamsey_sites_per_region(request):
    """
    Description: Retrieves the average number of Galamsey sites per region.
    Example Request:
    GET /average-galamsey-sites-per-region/
    Example Response:
    [
        {
            "Region": "Greater Accra",
            "avg_sites": 12.5
        },
        {
            "Region": "Ashanti",
            "avg_sites": 20.0
        }
    ]
    """


    average = GSiteData.objects.values('Region').annotate(avg_sites=Avg('Number_of_Galamsay_Sites'))
    return Response(average)

@api_view(['GET'])
def region_with_highest_galamsey_sites(request):
    """
    Description: Retrieves the region with the highest number of Galamsey sites.
    Example Request:
    GET /region-with-highest-galamsey-sites/
    Example Response:
    {
        "region": "Ashanti",
        "total_galamsey_sites": 50
    }
    In case of no data:
    {
        "message": "No data available"
    }
    """
    regions = GSiteData.objects.values('Region').annotate(total_sites=Sum('Number_of_Galamsay_Sites')).order_by(
        '-total_sites')

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
    """
    Description: Retrieves regions with a number of Galamsey sites greater than the specified threshold.
    Example Request:
    POST /regions-with-sites-above-threshold/
    Body:
    {
        "threshold": 10
    }
    Example Response:
    [
        {
            "id": 1,
            "City": "Kumasi",
            "Region": "Ashanti",
            "Number_of_Galamsay_Sites": 15
        },
        {
            "id": 2,
            "City": "Sunyani",
            "Region": "Bono",
            "Number_of_Galamsay_Sites": 12
        }
    ]
    Error Responses:
    - If no `threshold` is provided:
      {
          "error": "Threshold parameter is required"
      }
    - If the `threshold` value is invalid (non-integer):
      {
          "error": "Threshold must be a valid integer"
      }
    """
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

# @api_view(['POST'])
# @parser_classes([MultiPartParser, FormParser])
# def upload_csv(request):
#     if request.method == 'POST':
#         # Check if a file is included in the request
#         if 'file' not in request.FILES:
#             return JsonResponse({'error': 'No file provided'}, status=400)
#
#         # Retrieve the uploaded file
#         file = request.FILES['file']
#
#         threshold = regions_with_sites_above_threshold(request)
#
#         # Check if the file is a CSV
#         if not file.name.endswith('.csv'):
#             return JsonResponse({'error': 'Invalid file format. Only CSV files are allowed.'}, status=400)
#
#         # Decode and read the file
#         try:
#             data = io.StringIO(file.read().decode('utf-8'))
#         except UnicodeDecodeError:
#             return JsonResponse({'error': 'Unable to decode file. Ensure the file encoding is UTF-8.'}, status=400)
#
#         # Parse the CSV and process data
#         csv_reader = csv.reader(data)
#         next(csv_reader)  # Skip the header row
#
#         duplicate_entries = []
#         invalid_entries = []
#         successful_inserts = 0
#
#         for row in csv_reader:
#             if len(row) != 3:
#                 # Skip rows with incorrect number of columns
#                 invalid_entries.append({'row': row, 'error': 'Invalid row format'})
#                 continue
#
#             town, region, number_of_sites = row
#
#             # Validate `number_of_sites` is an integer
#             try:
#                 number_of_sites = int(number_of_sites)
#             except ValueError:
#                 invalid_entries.append({'row': row, 'error': 'Invalid datatype for Number_of_Galamsay_Sites'})
#                 continue
#
#             # Create entry in the database
#             try:
#                 GSiteData.objects.create(
#                     Town=town.strip(),
#                     Region=region.strip(),
#                     Number_of_Galamsay_Sites=number_of_sites
#                 )
#                 successful_inserts += 1
#             except IntegrityError:
#                 # Skip duplicate entries based on Town and Region uniqueness constraint
#                 duplicate_entries.append({'row': row, 'error': 'Duplicate entry'})
#
#         #frontend requests to get statistics
#         total_g_sites = GSiteData.objects.aggregate(Sum('Number_of_Galamsay_Sites'))
#         average_gsite_p_region = GSiteData.objects.values('Region').annotate(avg_sites=Avg('Number_of_Galamsay_Sites'))
#         highest_galamsay_region = GSiteData.objects.values('Region').annotate(total_sites=Sum('Number_of_Galamsay_Sites')).order_by(
#             '-total_sites')
#
#         # Prepare response with summary of results
#         response = {
#             'status': 'success',
#             'details': {
#                 'successful_inserts': successful_inserts,
#                 'duplicates': len(duplicate_entries),
#                 'invalid_entries': len(invalid_entries),
#                 'skipped_duplicates': duplicate_entries,
#                 'skipped_invalid_entries': invalid_entries,
#             },
#             'analysis_data':{
#                 'total_galamsey_sites': total_g_sites,
#                 'average': average_gsite_p_region,
#                 'threshold': threshold,
#                 'highest_galamsay_region': highest_galamsay_region,
#
#              },
#         }
#         return JsonResponse(response, status=200)
#
#     return JsonResponse({'error': 'Unsupported HTTP method. Use POST instead.'}, status=405)
#

@api_view(['POST'])
@parser_classes([MultiPartParser, FormParser])
def upload_and_analyze_csv(request):
    """
    Handles file upload, performs analysis with data cleaning,
    saves the cleaned data to DB, and returns the analysis results.
    """

    # Step 1: Retrieve file and threshold from the request
    file = request.FILES.get('file', None)
    threshold = request.data.get('threshold', None)

    if not file:
        return Response({"error": "File is required"}, status=status.HTTP_400_BAD_REQUEST)
    if not threshold:
        return Response({"error": "Threshold is required"}, status=status.HTTP_400_BAD_REQUEST)

    # Validate threshold as a number
    try:
        threshold = int(threshold)
    except ValueError:
        return Response({"error": "Threshold must be a number"}, status=status.HTTP_400_BAD_REQUEST)

    # Validate file type
    if not file.name.endswith('.csv'):
        return Response({"error": "Invalid file format. Only CSV files are allowed."},
                        status=status.HTTP_400_BAD_REQUEST)

    # Step 2: Decode and read CSV file
    try:
        data = io.StringIO(file.read().decode('utf-8'))
        csv_reader = csv.reader(data)
        header = next(csv_reader)  # Read header row
        if len(header) != 3 or header != ['Town', 'Region', 'Number_of_Galamsay_Sites']:
            return Response({"error": "Invalid CSV header format."}, status=status.HTTP_400_BAD_REQUEST)
    except UnicodeDecodeError:
        return Response({"error": "Unable to decode file. Ensure the file encoding is UTF-8."},
                        status=status.HTTP_400_BAD_REQUEST)

    # Step 3: Initialize data processing trackers
    duplicate_entries = []
    invalid_entries = []
    successful_inserts = 0
    rows = []

    for row in csv_reader:
        # Validate row length
        if len(row) != 3:
            invalid_entries.append({'row': row, 'error': 'Invalid row format (incorrect column count)'})
            continue

        town, region, number_of_sites = row

        # Validate `Number_of_Galamsay_Sites` as an integer
        try:
            number_of_sites = int(number_of_sites)
        except ValueError:
            invalid_entries.append({'row': row, 'error': 'Invalid datatype for Number_of_Galamsay_Sites'})
            continue

        # Append a processed row to the data list for bulk insert later
        rows.append({
            'Town': town.strip(),
            'Region': region.strip(),
            'Number_of_Galamsay_Sites': number_of_sites
        })

    # Step 4: Save metadata to `CsvFileData`
    csv_file_data = CsvFileData.objects.create(
        filename=file.name,
        createdAt=now().isoformat(),
        Numberofrecords=len(rows)
    )

    # Step 5: Insert rows into `GSiteData` with duplicate checks
    for row in rows:
        try:
            GSiteData.objects.create(
                Town=row['Town'],
                Region=row['Region'],
                Number_of_Galamsay_Sites=row['Number_of_Galamsay_Sites'],
                csvfileid=csv_file_data
            )
            successful_inserts += 1
        except IntegrityError:
            duplicate_entries.append({'row': row, 'error': 'Duplicate entry (Town and Region must be unique)'})

    # Step 6: Perform analysis on the uploaded file's data
    total_sites = GSiteData.objects.filter(csvfileid=csv_file_data).aggregate(
        total_sites=Sum('Number_of_Galamsay_Sites')
    )['total_sites']

    region_with_highest = (
        GSiteData.objects.filter(csvfileid=csv_file_data)
        .values('Region')
        .annotate(total_sites=Sum('Number_of_Galamsay_Sites'))
        .order_by('-total_sites')
        .first()
    )
    region_with_highest_sites = region_with_highest['Region'] if region_with_highest else None

    cities_exceeding_threshold = list(
        GSiteData.objects.filter(
            csvfileid=csv_file_data,
            Number_of_Galamsay_Sites__gt=threshold
        ).values_list('Town', flat=True)
    )

    regional_site_averages = list(
        GSiteData.objects.filter(csvfileid=csv_file_data)
        .values('Region')
        .annotate(avg_sites=Avg('Number_of_Galamsay_Sites'))
    )
    formatted_regional_site_averages = [
        {"region": r['Region'], "avg": r['avg_sites']} for r in regional_site_averages
    ]

    # Step 7: Prepare the final response
    response_data = {
        "id": str(csv_file_data.Id),
        "filename": csv_file_data.filename,
        "totalGalamseySites": total_sites,
        "regionWithHighestGalamseySites": region_with_highest_sites,
        "citiesExceedingThreshold": cities_exceeding_threshold,
        "regionalSiteAverages": formatted_regional_site_averages,
        "threshold": threshold,
        "createdAt": csv_file_data.createdAt,
        "details": {
            "successful_inserts": successful_inserts,
            "duplicates": len(duplicate_entries),
            "invalid_entries": len(invalid_entries),
            "skipped_duplicates": duplicate_entries,
            "skipped_invalid_entries": invalid_entries,
        }
    }

    return Response(response_data, status=status.HTTP_201_CREATED)
