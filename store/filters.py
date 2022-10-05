from . models import Box
import django_filters

class BoxFilter(django_filters.FilterSet):
    length = django_filters.NumberFilter()
    length__gt = django_filters.NumberFilter(field_name='length', lookup_expr='gt')
    length__lt = django_filters.NumberFilter(field_name='length', lookup_expr='lt')

    width = django_filters.NumberFilter()
    width__gt = django_filters.NumberFilter(field_name='width', lookup_expr='gt')
    width__lt = django_filters.NumberFilter(field_name='width', lookup_expr='lt')

    height = django_filters.NumberFilter()
    height__gt = django_filters.NumberFilter(field_name='height', lookup_expr='gt')
    height__lt = django_filters.NumberFilter(field_name='height', lookup_expr='lt')

    area = django_filters.NumberFilter()
    area_gt = django_filters.NumberFilter(field_name='area', lookup_expr='gt')
    area_lt = django_filters.NumberFilter(field_name='area', lookup_expr='lt')

    volume = django_filters.NumberFilter()
    volume__gt = django_filters.NumberFilter(field_name='volume', lookup_expr='gt')
    volume__lt = django_filters.NumberFilter(field_name='volume', lookup_expr='lt')

    user = django_filters.NumberFilter
    user__box = django_filters.NumberFilter(field_name='created_by', lookup_expr='pk')

    date = django_filters.DateFilter()
    date__gt = django_filters.DateFilter(field_name='created_on', lookup_expr='gt')
    date__lt = django_filters.DateFilter(field_name='created_on', lookup_expr='lt')

    class Meta:
        model = Box
        fields = []