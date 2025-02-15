import io

from django.db.models import Avg, Sum
from django.http import HttpResponse
from django.urls import reverse
from rest_framework.decorators import api_view
from .serializers import SiteRecordsSerializer, UploadedFileSerializer, RecordSiteSerializer, AverageSitesPerRegionSerializer, RegionWithHighestSitesSerializer
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework import status, generics
from .models import UploadedFile, SiteRecords

# Create your views here.

# CRUD Operations
@api_view(['GET'])
def api_root(request, format=None):
    """
    API Root endpoint that provides clickable links to all API endpoints in an HTML-rendered view.
    """
    endpoints = {
        "Get All Site Data": reverse('get-site-data', args=[1]),  # Example file_id=1
        "Average Sites Per Region": reverse('average-sites-per-region', args=[1]),
        "Sites Above Threshold": reverse('sites-above-threshold', args=[1, 5]),  # Example threshold=5
        "Region with Highest Sites": reverse('region-with-highest-site', args=[1]),
    }

    # Generate an HTML response with clickable links
    html_response = '<center><h1>Welcome to the Galamsey Site Analyser API</h1>'
    html_response += '<h3>Below are the available endpoints:</h3>'
    html_response += '<h2>'

    for name, url in endpoints.items():
        full_url = request.build_absolute_uri(url)
        html_response += f'<p><a href="{full_url}">{name}</a></p><br>'

    html_response += '</h2></center>'

    return HttpResponse(html_response)


# 1. All sites that were recorded (GET api/getsitedata [FileID])
@api_view(['GET'])
def get_site_data(request, file_id):
    """
    Retrieve all site records for a specific file.
    """
    try:
        file = UploadedFile.objects.get(ID=file_id)
    except UploadedFile.DoesNotExist:
        return Response({"error": "File not found"}, status=status.HTTP_404_NOT_FOUND)

    sites = SiteRecords.objects.filter(FileID=file)
    serializer = SiteRecordsSerializer(sites, many=True)

    return Response(serializer.data, status=status.HTTP_200_OK)

# 2. Average sites per region (GET api/averagesitesperregion [FileID])
@api_view(['GET'])
def average_sites_per_region(request, file_id):
    """
    Calculate the average number of sites per region for a specific file.
    """
    try:
        file = UploadedFile.objects.get(ID=file_id)
    except UploadedFile.DoesNotExist:
        return Response({"error": "File not found"}, status=status.HTTP_404_NOT_FOUND)

    averages = SiteRecords.objects.filter(FileID=file).values('Region').annotate(average_sites=Avg('Number_of_Galamsay_Sites'))

    serializer = AverageSitesPerRegionSerializer(averages, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

# 3. Regions with Sites above a given threshold (GET api/sitesabovethreshold [FileID, threshold])
@api_view(['GET'])
def sites_above_threshold(request, file_id, threshold):
    """
    Retrieve regions where the total number of galamsay sites exceeds a given threshold.
    Returns Region name and total sites in that region.
    """
    try:
        file = UploadedFile.objects.get(ID=file_id)
    except UploadedFile.DoesNotExist:
        return Response({"error": "File not found"}, status=status.HTTP_404_NOT_FOUND)

    # Aggregate total number of sites per region
    region_totals = (
        SiteRecords.objects
        .filter(FileID=file)
        .values('Region')
        .annotate(total_sites=Sum('Number_of_Galamsay_Sites'))
        .filter(total_sites__gt=threshold)  # Keep only regions above threshold
    )

    if not region_totals:
        return Response({"message": "No regions exceed the threshold"}, status=status.HTTP_404_NOT_FOUND)

    return Response(region_totals, status=status.HTTP_200_OK)

# 4. Region with Highest number of Sites (GET api/regionwithhighestsite [FileID])
@api_view(['GET'])
def region_with_highest_site(request, file_id):
    """
    Find the region with the highest number of galamsay sites for a specific file.
    """
    try:
        file = UploadedFile.objects.get(ID=file_id)
    except UploadedFile.DoesNotExist:
        return Response({"error": "File not found"}, status=status.HTTP_404_NOT_FOUND)

    highest_region = SiteRecords.objects.filter(FileID=file).values('Region').annotate(total_sites=Sum('Number_of_Galamsay_Sites')).order_by('-total_sites').first()

    if not highest_region:
        return Response({"error": "No records found"}, status=status.HTTP_404_NOT_FOUND)

    serializer = RegionWithHighestSitesSerializer(highest_region)
    return Response(serializer.data, status=status.HTTP_200_OK)


class FileUploadView(generics.CreateAPIView):
    queryset = UploadedFile.objects.all()
    serializer_class = UploadedFileSerializer
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request, *args, **kwargs):
        file_obj = request.FILES.get('file')

        if not file_obj:
            return Response({"error": "No file uploaded"}, status=status.HTTP_400_BAD_REQUEST)

        # Save file details in UploadedFile model
        uploaded_file = UploadedFile.objects.create(FileName=file_obj.name)

        # Read and parse CSV content
        try:
            file_stream = io.TextIOWrapper(file_obj, encoding='utf-8')
            for line in file_stream:
                data = line.strip().split(',')
                if len(data) == 3:  # Ensure valid format
                    town, region, sites = data
                    SiteRecords.objects.create(
                        Town=town.strip(),
                        Region=region.strip(),
                        Number_of_Galamsay_Sites=int(sites.strip()),
                        FileID=uploaded_file
                    )
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response({
            "message": "File uploaded and data stored successfully",
            "FileID": uploaded_file.id,
            "FileName": uploaded_file.FileName
        }, status=status.HTTP_201_CREATED)

