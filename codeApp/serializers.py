from rest_framework import serializers
from .models import LeetcodeProblem

class DataEntrySerializer(serializers.ModelSerializer):
    class Meta:
        model = LeetcodeProblem
        fields = '__all__'