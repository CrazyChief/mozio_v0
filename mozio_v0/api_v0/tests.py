from faker import Faker
from rest_framework import status
from rest_framework.test import APITestCase

from providers.models import Provider, ServiceArea
from .serializers import ProviderSerializer, ServiceAreaSerializer


class ProviderTests(APITestCase):
    """
    Provide tests for Provider model:
    1) creation of Provider object;
    2) getting details of Provider object;
    3) updating Provider object;
    """

    def create_provider(self):
        faker = Faker()
        provider = Provider.objects.create(
            name=faker.first_name(),
            email=faker.email(),
            phone_number='+380932812462',
            language='en',
            currency='USD'
        )
        provider.save()

        return provider

    def test_create_provider(self):
        provider_url = r'/api/v0/providers/'
        provider_data = {
            'name': 'qwerty',
            'email': 'qwerty123@qwerty.com',
            'phone_number': '+380932812462',
            'language': 'en',
            'currency': 'USD'
        }
        response = self.client.post(
            provider_url, provider_data, format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Provider.objects.count(), 1)
        self.assertEqual(Provider.objects.get().name, 'qwerty')

    def test_can_get_provider(self):
        provider = self.create_provider()
        response = self.client.get(f'/api/v0/providers/{provider.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            (response.data['name'],
             response.data['email']),
            (ProviderSerializer(instance=provider)['name'].value,
             ProviderSerializer(instance=provider)['email'].value))

    def test_can_update_provider(self):
        provider = self.create_provider()
        response = self.client.patch(
            f'/api/v0/providers/{provider.id}/',
            data={
                'name': 'QWERTY'
            }, format='json'
        )
        provider.refresh_from_db()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(provider.name, 'QWERTY')


class ServiceAreaTests(APITestCase):
    """
    Provide tests for ServiceArea model:
    1) getting details of ServiceArea object;
    2) updating of ServiceArea object;
    """

    def create_provider(self):
        faker = Faker()
        provider = Provider.objects.create(
            name=faker.first_name(),
            email=faker.email(),
            phone_number='+380932812462',
            language='en',
            currency='USD'
        )
        provider.save()

        return provider

    def create_service_area(self):
        faker = Faker()
        provider = self.create_provider()
        service_area = ServiceArea.objects.create(
            provider=provider,
            polygon_name=faker.name(),
            price=20,
            polygon=[
                [51.01564224011381, 29.76750033024507],
                [50.403427717842696, 29.59171908024507],
                [50.13658746370076, 30.84416048649507]
            ]
        )
        service_area.save()

        return service_area

    def test_can_get_service_area(self):
        service_area = self.create_service_area()
        response = self.client.get(
            f'/api/v0/service-areas/{service_area.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            (response.data['polygon_name'],
             response.data['price']),
            (ServiceAreaSerializer(
                instance=service_area)['polygon_name'].value,
             ServiceAreaSerializer(
                 instance=service_area)['price'].value))

    def test_can_update_service_area(self):
        faker = Faker()
        service_area = self.create_service_area()
        new_polygon_name = faker.first_name()
        response = self.client.patch(
            f'/api/v0/service-areas/{service_area.id}/',
            data={
                'polygon_name': new_polygon_name
            },
            format='json'
        )
        service_area.refresh_from_db()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(service_area.polygon_name, new_polygon_name)
