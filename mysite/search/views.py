from django.views.generic import ListView, TemplateView
from .models import Restaurant, MenuItem
from django.db.models import Q
from django.views import View
from django.shortcuts import redirect, render


class SetCityView(View):
    def get(self, request):
        return render(request, 'search/set_city.html')

    def post(self, request):
        city = request.POST.get('city')
        if city:
            request.session['user_city'] = city
        return redirect('restaurant_list')


class RestaurantListView(ListView):
    model = Restaurant
    template_name = 'search/restaurant_list.html'
    context_object_name = 'restaurants'
    paginate_by = 10

    def get(self, request, *args, **kwargs):
        if not request.session.get('user_city'):
            return redirect('set_city')
        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        query = self.request.GET.get('q')
        user_city = self.request.session.get('user_city')

        queryset = Restaurant.objects.all()

        if user_city:
            queryset = queryset.filter(city__icontains=user_city)

        if query:
            queryset = queryset.filter(
                Q(name__icontains=query) |
                Q(cuisines__icontains=query)
            ).distinct()
        return queryset


class FoodSearchView(ListView):
    model = MenuItem
    template_name = 'search/food_search_results.html'
    context_object_name = 'menu_items'
    paginated_by = 10

    def get_queryset(self):
        query = self.request.GET.get('q')
        queryset = MenuItem.objects.all()

        if query:
            queryset = queryset.filter(name__icontains=query)
        return queryset


class SmartSearchView(TemplateView):
    template_name = 'search/search_results.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        query = self.request.GET.get('q')

        if query:
            context['restaurants'] = Restaurant.objects.filter(
                Q(name__icontains=query) |
                Q(city__icontains=query) |
                Q(cuisines__icontains=query)
            ).distinct()

            context['menu_items'] = MenuItem.objects.filter(
                name__icontains=query
            ).select_related('restaurant')

        else:
            context['restaurants'] = []
            context['menu_items'] = []

        context['query'] = query
        return context