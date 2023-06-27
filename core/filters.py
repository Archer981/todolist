import django_filters

from core.models import User


class UserModelFilter(django_filters.rest_framework.FilterSet):
    first_name = django_filters.CharFilter(field_name='first_name', lookup_expr='icontains')
    last_name = django_filters.CharFilter(field_name='last_name', lookup_expr='icontains')
    username = django_filters.CharFilter(field_name='username', lookup_expr='icontains')

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'is_staff',)
