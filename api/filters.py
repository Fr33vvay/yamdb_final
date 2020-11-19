from django_filters import rest_framework as filters

from content.models import Title


class TitleFilter(filters.FilterSet):
    """
    Фильтрация произведений по названию, категории, жанру или году
    """
    name = filters.CharFilter(field_name='name', lookup_expr='contains')
    category = filters.CharFilter(field_name='category__slug',
                                  lookup_expr='exact')
    genre = filters.CharFilter(field_name='genre__slug', lookup_expr='exact')

    class Meta:
        model = Title
        fields = ['name', 'category', 'genre', 'year', ]
