from django.http import Http404

from .models import Car, Rating
from .serializers import CarSerializer, CreateCarSerializer, RateSerializer, CreateRateSerializer, CarPopularSerializer

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response


class CarListView(APIView):
    serializer_class = CreateCarSerializer

    def get(self, request, format=None):
        cars = Car.objects.all()
        serializer = CarSerializer(cars, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            import requests
            import json
            import objectpath
            make = serializer.data.get('make')
            model = serializer.data.get('model')
            url = 'https://vpic.nhtsa.dot.gov/api/vehicles/getmodelsformake/{make}?format=json'.format(
                make=make.lower()
            )
            r = requests.get(url)
            apidict = json.loads(r.text)
            apidata = objectpath.Tree(apidict)
            apituple = tuple(apidata.execute('$..Model_Name'))
            if model in apituple:
                pass
            else:
                return Response({'Bad Request': "This car doesn't exist"}, status=status.HTTP_400_BAD_REQUEST)

            car = Car(
                make=make.lower().capitalize(),
                model=model,
            )
            car.save()
            return Response(CarSerializer(car).data, status=status.HTTP_201_CREATED)

        return Response({'Bad Request': 'Invalid data...'}, status=status.HTTP_400_BAD_REQUEST)


class CarDetailView(APIView):

    @staticmethod
    def get_object(pk):
        try:
            return Car.objects.get(pk=pk)
        except Car.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        car = self.get_object(pk)
        serializer = CarSerializer(car)
        return Response(serializer.data)

    def delete(self, request, pk, format=None):
        car = self.get_object(pk)
        car.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class PopularCarListView(APIView):
    serializer_class = CarPopularSerializer

    def get(self, request, format=None):
        cars = Car.objects.all()
        serializer = CarPopularSerializer(cars, many=True)
        serializer = sorted(
            serializer.data, key=lambda k: k['rates_number'], reverse=True)
        return Response(serializer)


class RateListView(APIView):
    serializer_class = CreateRateSerializer

    def post(self, request, format=None):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            car_id = serializer.data.get('car_id')
            rating = serializer.data.get('rating')

            if 1 <= rating <= 5:
                pass
            else:
                return Response({'Bad Request': 'Rating should be from 1 to 5'}, status=status.HTTP_400_BAD_REQUEST)

            rate = Rating(
                car_id_id=car_id,
                rating=rating,
            )
            rate.save()
            return Response(RateSerializer(rate).data, status=status.HTTP_201_CREATED)

        return Response({'Bad Request': 'Invalid data...'}, status=status.HTTP_400_BAD_REQUEST)
