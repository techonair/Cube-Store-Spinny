from rest_framework import serializers
from . models import Box

class AdminBoxSerializer(serializers.ModelSerializer):
    class Meta:
        model = Box
        fields = ['length', 'width', 'height', 'area', 'volume', 'created_by', 'updated_on']

class BoxSerializer(serializers.ModelSerializer):
    class Meta:
        model = Box
        fields = ['length', 'width', 'height', 'area', 'volume']