from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from .models import Student
from .serializer import StudentListSerializer, StudentSerializer

# Create your views here.
@api_view(['GET'])
def get_students(request):
    students = Student.objects.all()
    serializer = StudentListSerializer(students, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['POST'])
def enroll(request):
    student = StudentSerializer(data=request.data)
    if not student.is_valid(): return Response(student.errors, status=status.HTTP_400_BAD_REQUEST)
    student.save()
    return Response(student.data, status=status.HTTP_201_CREATED)

@api_view(['POST'])
def login(request):
    if 'fingerprint' not in request.FILES:
        return Response({'error': 'Fingerprint file is required.'}, status=status.HTTP_400_BAD_REQUEST)
    
    # fingerprint = request.FILES['fingerprint']

    # Implement your fingerprint matching logic here
    # If match found:
    # return Response('success', status=status.HTTP_200_OK)

    return Response({'error': 'Fingerprint not recognized.'}, status=status.HTTP_400_BAD_REQUEST)