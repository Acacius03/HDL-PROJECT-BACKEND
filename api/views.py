from django.db import transaction
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from .models import Student
from .serializer import StudentListSerializer, StudentSerializer
from FaceRecognition import FR

# Create your views here.
@api_view(['GET'])
def get_students(request):
    students = Student.objects.all()
    serializer = StudentListSerializer(students, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['POST'])
def enroll(request):
    student = StudentSerializer(data=request.data)
    if not student.is_valid(): 
        return Response(student.errors, status=status.HTTP_400_BAD_REQUEST)
    student.save()
    print(student.data['face_img'])
    if not FR.encode_new_face(f".{student.data['face_img']}"):
        Student.objects.filter(id=student.data['id']).delete()
        return Response({'error': 'Failed to encode face'}, status=status.HTTP_400_BAD_REQUEST)
    return Response(student.data, status=status.HTTP_201_CREATED)

def find_user(pk):
    try:
        student = Student.objects.get(pk=pk)
    except Student.DoesNotExist:
        return None
    return student

@api_view(['GET'])
def get_user(request, pk):
    student = find_user(pk)
    if not student:
        return Response(status=status.HTTP_400_NOT_FOUND)
    student = StudentSerializer(student)
    return Response(student.data)

@api_view(['PUT'])
def update_user(request, pk):
    student = find_user(pk)
    if not student:
        return Response(status=status.HTTP_400_NOT_FOUND)
    student = StudentSerializer(student)
    if not student.is_valid(): 
        return Response(student.errors, status=status.HTTP_400_BAD_REQUEST)
    student.save()
    return Response(student.data)

@api_view(['DELETE'])
def delete_user(request, pk):
    student = find_user(pk)
    if not student:
        return Response(status=status.HTTP_400_NOT_FOUND)
    student = StudentSerializer(student)
    if not student.is_valid(): 
        return Response(student.errors, status=status.HTTP_400_BAD_REQUEST)
    student.save()
    return Response(student.data)

@api_view(['POST'])
def login(request):
    print(FR.recognize_faces(request.data['face_img']))
    return Response({'msg': 'Not yet finished'}, status=status.HTTP_200_OK)
