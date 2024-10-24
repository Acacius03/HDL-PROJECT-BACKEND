import uuid
from rest_framework import serializers
from .models import Student

class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = '__all__'

class StudentListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        exclude = ['face_img']

