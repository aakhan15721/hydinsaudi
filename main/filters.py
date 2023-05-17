import django_filters
from expads.models import Expatad

class Expatadfilter(django_filters.FilterSet):
    fullname = django_filters.CharFilter(lookup_expr='icontains')
    Description = django_filters.CharFilter(lookup_expr='icontains')
    landmark = django_filters.CharFilter(lookup_expr='icontains')
    purpose__name = django_filters.CharFilter(lookup_expr='icontains')
    citycode__name = django_filters.CharFilter(lookup_expr='icontains')
    countrycode__name = django_filters.CharFilter(lookup_expr='icontains')
    price=django_filters.RangeFilter()

    class Meta:
        model : Expatad
        fields = {
            'fullname' : ['icontains'],
            'Description' : ['icontains'],
            'landmark' : ['icontains'],
            'purpose__name' : ['icontains'],
            'citycode__name' : ['icontains'],
            'countrycode__name' : ['icontains']
            #'price': ['lt','gt'],
        }


