from django.urls import path, re_path

from .views import CarListView, CarDetailView, RateListView, PopularCarListView


urlpatterns = [
    re_path(r'^cars/?$', CarListView.as_view(), name='cars-list'),
    re_path(r'^rate/?$', RateListView.as_view()),
    re_path(r'^popular/?$', PopularCarListView.as_view()),
    path('cars/<int:pk>/', CarDetailView.as_view()),
]
