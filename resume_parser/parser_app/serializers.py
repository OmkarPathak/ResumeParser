from rest_framework import serializers
from .models import UserDetails, Competencies, MeasurableResults, Resume, ResumeDetails

class UserDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserDetails
        fields = '__all__'

class CompetenciesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Competencies
        fields = '__all__'

class MeasurableResultsSerializer(serializers.ModelSerializer):
    class Meta:
        model = MeasurableResults
        fields = '__all__'

class ResumeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Resume
        fields = '__all__'

class ResumeDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ResumeDetails
        fields = '__all__'