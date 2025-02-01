from django.urls import path
from . import views

urlpatterns = [
    # CRUD Endpoints
    path('gsites/', views.gsite_data_list, name='gsite-data-list'),
    path('gsites/<int:pk>/', views.gsite_data_detail, name='gsite-data-detail'),

    #  Endpoints
    path('total-galamsey-sites/', views.total_galamsey_sites, name='total-galamsey-sites'),
    path('average-galamsey-sites-per-region/', views.average_galamsey_sites_per_region, name='average-galamsey-sites-per-region'),

    # New Endpoint: Region with Highest Galamsey Sites
    path('region-with-highest-galamsey-sites/', views.region_with_highest_galamsey_sites, name='region-with-highest-galamsey-sites'),

    # CSV Upload Endpoint
    path('upload-csv/', views.upload_csv, name='upload-csv'),
]