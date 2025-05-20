from django.urls import path
from .views import RestaurantListView, FoodSearchView, SmartSearchView, SetCityView


urlpatterns = [
    path('', RestaurantListView.as_view(), name='restaurant_list'),
    path('foods/', FoodSearchView.as_view(), name='food_search'),
    path('search/', SmartSearchView.as_view(), name='smart_search'),
    path('set-location/', SetCityView.as_view(), name='set_city'),
]