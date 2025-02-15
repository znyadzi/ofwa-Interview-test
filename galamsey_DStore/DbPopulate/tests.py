from django.test import TestCase
from rest_framework.test import APIClient
from .models import UploadedFile, SiteRecords

class SiteRecordsTestCase(TestCase):
    def setUp(self):
        # Create sample file and site record
        self.file = UploadedFile.objects.create(FileName="test.csv")
        self.site1 = SiteRecords.objects.create(
            Town="Accra",
            Region="Greater Accra",
            Number_of_Galamsay_Sites=5,
            FileID=self.file
        )
        self.site2 = SiteRecords.objects.create(
            Town="Kumasi",
            Region="Ashanti",
            Number_of_Galamsay_Sites=10,
            FileID=self.file
        )
        self.client = APIClient()

    def test_get_all_sites(self):
        response = self.client.get(f'/api/getsitedata/{self.file.ID}/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 2)

    def test_average_sites_per_region(self):
        response = self.client.get(f'/api/averagesitesperregion/{self.file.ID}/')
        self.assertEqual(response.status_code, 200)

    def test_sites_above_threshold(self):
        response = self.client.get(f'/api/sitesabovethreshold/{self.file.ID}/7/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)  # Only Kumasi has >7 sites

    def test_region_with_highest_sites(self):
        response = self.client.get(f'/api/regionwithhighestsite/{self.file.ID}/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['Region'], 'Ashanti')  # Highest sites in Ashanti

