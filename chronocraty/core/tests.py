from django.test import TestCase
from django.test.client import Client

# Create your tests here.


class TestHealthCheck(TestCase):
    def setUp(self):
        self.assertEqual.__self__.maxDiff = None

    def test_health_check(self):
        client = Client()
        response = client.get('/health-check/', {})
        result = response.content.decode()
        print(result)
        self.assertEqual('Health-check OK', result)



