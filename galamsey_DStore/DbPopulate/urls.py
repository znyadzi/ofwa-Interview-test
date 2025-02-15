from django.urls import path
from .views import UploadedFileListView, FileUploadView,api_root, get_site_data, average_sites_per_region, sites_above_threshold, region_with_highest_site

urlpatterns = [
    path('', api_root, name='api-root'),
    path('getsitedata/<int:file_id>/', get_site_data, name='get-site-data'),
    path('averagesitesperregion/<int:file_id>/', average_sites_per_region, name='average-sites-per-region'),
    path('sitesabovethreshold/<int:file_id>/<int:threshold>/', sites_above_threshold, name='sites-above-threshold'),
    path('regionwithhighestsite/<int:file_id>/', region_with_highest_site, name='region-with-highest-site'),
    path('upload/', FileUploadView.as_view(), name='file-upload'),
    path('uploadedfiles/', UploadedFileListView.as_view(), name='uploaded-files-list'),
]
