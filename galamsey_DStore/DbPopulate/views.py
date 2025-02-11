import json
import csv
import io
from operator import index

from rest_framework import status
from rest_framework.decorators import api_view, parser_classes
from rest_framework.response import Response
from .models import GSiteData
from .serializers import GSiteDataSerializer, ThresHoldDataSerializer, CSVUploadSerializer
from django.db.models import Avg, Sum
from rest_framework.parsers import MultiPartParser, FormParser


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


@api_view(['POST'])
@parser_classes([MultiPartParser, FormParser])
def upload_csv(request):
    """ Endpoint to upload CSV file and save data to the database. """

    file_serializer = CSVUploadSerializer(data=request.data)

    if file_serializer.is_valid():
        csv_file = request.FILES['file']

        if not csv_file.name.endswith('.csv'):
            return Response({"error": "Only CSV files are accepted"}, status=status.HTTP_400_BAD_REQUEST)

        # Read CSV file
        decoded_file = csv_file.read().decode('utf-8')
        io_string = io.StringIO(decoded_file)
        reader = csv.DictReader(io_string)  # Read CSV with headers

        # Insert data into the database
        new_entries = []
        for index, row in enumerate(reader):
            if index == 0:
                continue  # Skip header row

            try:
                number_of_sites = int(row.get("Number_of_Galamsay_Sites", 0))  # Use dictionary keys

                _, created = GSiteData.objects.get_or_create(
                    Town=row.get("Town"),
                    Region=row.get("Region"),
                    defaults={'Number_of_Galamsay_Sites': number_of_sites}
                )

                if not created:
                    GSiteData.objects.filter(
                        Town=row.get("Town"),
                        Region=row.get("Region")
                    ).update(Number_of_Galamsay_Sites=number_of_sites)

            except ValueError:
                print(f"Skipping row: Town={row.get('Town')}, Region={row.get('Region')}. Invalid number format.")
                continue

        # Bulk create for performance
        GSiteData.objects.bulk_create(new_entries)

        return Response({"message": "CSV data uploaded successfully"}, status=status.HTTP_201_CREATED)

    return Response(file_serializer.errors, status=status.HTTP_400_BAD_REQUEST)