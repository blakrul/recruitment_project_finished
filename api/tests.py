from django.urls import reverse

from rest_framework import status
from rest_framework.test import APITestCase

from .models import Car


class CreateCarTest(APITestCase):
    def setUp(self):
        self.goodcar = Car.objects.create(make="Honda", model="VTX1300S")
        self.data = {'make': 'Honda', 'model': 'VTX1300S'}

    def test_can_read_car_list(self):
        response = self.client.post(reverse('cars-list'), self.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


class ReadCarTest(APITestCase):
    def setUp(self):
        self.goodcar = Car.objects.create(make="Honda", model="VTX1300S")

    def test_can_read_car_list(self):
        response = self.client.get(reverse('cars-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
