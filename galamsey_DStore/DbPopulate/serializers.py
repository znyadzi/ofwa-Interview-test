from rest_framework import serializers
from .models import GSiteData

class GSiteDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = GSiteData
        fields = ['id', 'Town', 'Region', 'Number_of_Galamsay_Sites']

class HighestRegionSerializer(serializers.Serializer):
    region = serializers.CharField()
    total_galamsey_sites = serializers.IntegerField()