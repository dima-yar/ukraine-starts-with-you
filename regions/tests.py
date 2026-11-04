from django.test import TestCase
from django.urls import reverse
from core.models import Regions, Record


class PagesTest(TestCase):
    def test_main(self):
        self.assertEqual(self.client.get(reverse('main')).status_code, 200)

    def test_region_without_background(self):
        r = Regions.objects.create(region='Test', image='upload/x.png')
        Record.objects.create(record_holders_region=r)
        resp = self.client.get(reverse('local_records:region', args=[r.pk]))
        self.assertEqual(resp.status_code, 200)

    def test_region_404(self):
        self.assertEqual(self.client.get(reverse('local_records:region', args=[9999])).status_code, 404)
