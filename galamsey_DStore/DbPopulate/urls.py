from django.urls import path
from . import views
from .views import upload_csv

urlpatterns = [
    # CRUD Endpoints
    path('gsites/', views.gsite_data_list, name='gsite-data-list'),

    #  Endpoints
    #Total Galamsey Sites
    path('total-galamsey-sites/', views.total_galamsey_sites, name='total-galamsey-sites'),

    #Average Galamsay Site per Region
    path('average-galamsey-sites-per-region/', views.average_galamsey_sites_per_region, name='average-galamsey-sites-per-region'),

    # Region with Highest Galamsey Sites
    path('region-with-highest-galamsey-sites/', views.region_with_highest_galamsey_sites, name='region-with-highest-galamsey-sites'),

    #Region Above a threshold
    path('regions-above-threshold/', views.regions_with_sites_above_threshold, name='regions_above_threshold'),

    path('upload-csv/', upload_csv, name='upload-csv'),

]