from django.urls import path
from . import views

urlpatterns = [
    # CRUD Endpoints
#    path('gsites/', views.gsite_data_list, name='gsite-data-list'),
    path('gsites/<int:pk>/', views.gsite_data_detail, name='gsite-data-detail'),

    # Custom Function Endpoints
#    path('total-galamsey-sites/', views.total_galamsey_sites, name='total-galamsey-sites'),
    path('average-galamsey-sites-per-region/', views.average_galamsey_sites_per_region, name='average-galamsey-sites-per-region'),

    # Dashboard Endpoint
    path('dashboard/', views.api_dashboard, name='api-dashboard'),
]