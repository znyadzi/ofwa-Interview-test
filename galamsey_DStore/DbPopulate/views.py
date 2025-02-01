from django.shortcuts import render
from .models import GSiteData
from django.db.models import Avg, Sum

def api_dashboard(request):
    # Fetch data for all APIs
    gsite_data = GSiteData.objects.all()
    total_galamsey_sites = GSiteData.objects.aggregate(Sum('Number_of_Galamsay_Sites'))['Number_of_Galamsay_Sites__sum']
    average_galamsey_sites_per_region = GSiteData.objects.values('Region').annotate(avg_sites=Avg('Number_of_Galamsay_Sites'))

    # Prepare context data
    context = {
        'gsite_data': gsite_data,
        'total_galamsey_sites': total_galamsey_sites,
        'average_galamsey_sites_per_region': average_galamsey_sites_per_region,
    }

    # Render the template with the context data
    return render(request, 'dgapp/api_dashboard.html', context)