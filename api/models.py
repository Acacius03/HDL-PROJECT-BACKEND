from django.core.validators import MaxValueValidator, MinLengthValidator
from django.db import models
import uuid

# Create your models here.

SUFFIX_CHOICES = [
    ('Jr.', 'Jr.'),
    ('Sr.', 'Sr.'),
    ('II', 'II'),
    ('III', 'III'),
    ('IV', 'IV'),
    ('None', 'None')  # Option for no suffix
]

def student_directory_path(instance, filename):
    return "faces/{0}/{1}".format(instance.uuid, filename)

class Student(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    first_name = models.CharField(max_length=30)
    middle_initial = models.CharField(max_length=1)
    last_name = models.CharField(max_length=30)
    suffix = models.CharField(max_length=5, choices=SUFFIX_CHOICES, default='None')
    LRN = models.CharField(max_length=12, validators=[MinLengthValidator(12)], unique=True)
    birth_date = models.DateField()
    phone_number = models.CharField(null=True, max_length=15, validators=[MinLengthValidator(10)], unique=True)
    email =  models.EmailField(null=True, unique=True)
    last_login = models.DateTimeField(null=True)
    last_logout = models.DateTimeField(null=True)
    face_img = models.ImageField(upload_to=student_directory_path, blank=True, null=True)
    average_grade = models.DecimalField(null=True, max_digits=4, decimal_places=2)
    absences = models.SmallIntegerField(default=0, validators=[MaxValueValidator(5)])

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
    
class Guardian(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=30)
    middle_initial = models.CharField(x_length=1)
    last_name = models.CharField(max_length=30)
    suffix = models.CharField(max_length=5, choices=SUFFIX_CHOICES, default='None')
    phone_number = models.CharField(max_length=15, null=True, unique=True)
    email =  models.EmailField(null=True, unique=True)
    