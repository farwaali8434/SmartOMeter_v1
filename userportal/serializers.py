from django.contrib.auth.models import User, Group
from rest_framework import serializers

from userportal.models import City, Area


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('url', 'username', 'email', 'groups')


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ('url', 'name')


class CitySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = City
        fields = ('postal_code', 'city_name')


class AreaSerializer(serializers.HyperlinkedModelSerializer):
    city = CitySerializer()

    class Meta:
        model = Area
        fields = ('city', 'area_name', 'zone')
