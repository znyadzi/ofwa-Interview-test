from django.test import TestCase, Client
from DbPopulate.models import GSiteData


class ApiEndpointsTestCase(TestCase):
    def setUp(self):
        # Initialize the test client
        self.client = Client()

        # Populate test data
        GSiteData.objects.create(Town='TestTown1', Region='TestRegion1', Number_of_Galamsay_Sites=20)
        GSiteData.objects.create(Town='TestTown2', Region='TestRegion1', Number_of_Galamsay_Sites=30)
        GSiteData.objects.create(Town='TestTown3', Region='TestRegion2', Number_of_Galamsay_Sites=50)

    def test_total_galamsey_sites(self):
        # Perform test for total Galamsey sites
        response = self.client.get('/total-galamsey-sites/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {'total_sites': 100})

    def test_average_galamsey_sites_per_region(self):
        # Perform test for average Galamsey sites per region
        response = self.client.get('/average-galamsey-sites-per-region/')
        self.assertEqual(response.status_code, 200)

        avg_data = response.json()
        self.assertIn({'Region': 'TestRegion1', 'avg_sites': 25.0}, avg_data)
        self.assertIn({'Region': 'TestRegion2', 'avg_sites': 50.0}, avg_data)

    def test_region_with_highest_galamsey_sites(self):
        # Perform test for the region with the highest Galamsey sites
        response = self.client.get('/region-with-highest-galamsey-sites/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {'region': 'TestRegion2', 'total_sites': 50})

    def test_regions_above_threshold(self):
        # Perform test for regions above a threshold
        response = self.client.get('/regions-above-threshold/?threshold=20')
        self.assertEqual(response.status_code, 200)

        regions_data = response.json()
        self.assertIn({'Region': 'TestRegion1', 'total_sites': 50}, regions_data)
        self.assertIn({'Region': 'TestRegion2', 'total_sites': 50}, regions_data)

    def test_regions_above_threshold_missing_parameter(self):
        # Test regions-above-threshold endpoint without the required "threshold" parameter
        response = self.client.get('/regions-above-threshold/')
        self.assertEqual(response.status_code, 400)  # Bad Request
        self.assertEqual(response.json(), {'error': 'Threshold parameter is required'})
