from rest_framework import serializers
from .models import UploadedFile, SiteRecords

class SiteRecordsSerializer(serializers.ModelSerializer):
    class Meta:
        model = SiteRecords
        fields = ['ID', 'Town', 'Region', 'Number_of_Galamsay_Sites']

class AverageSitesPerRegionSerializer(serializers.Serializer):
    Region = serializers.CharField()
    average_sites = serializers.FloatField()

class RegionWithHighestSitesSerializer(serializers.Serializer):
    Region = serializers.CharField()
    total_sites = serializers.IntegerField()
