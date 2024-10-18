from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status


# from django.shortcuts import render

# Create your views here.
@api_view(['POST'])
def enroll(request):
    return Response('enroll', status=status.HTTP_201_CREATED)
