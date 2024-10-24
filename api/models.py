from django.db import models
import uuid

# Create your models here.

def student_directory_path(instance, filename):
    return "faces/{0}/{1}".format(instance.uuid, filename)

class Student(models.Model):
    SUFFIX_CHOICES = [
        ('Jr.', 'Jr.'),
        ('Sr.', 'Sr.'),
        ('II', 'II'),
        ('III', 'III'),
        ('IV', 'IV'),
        ('None', 'None')  # Option for no suffix
    ]
    uuid = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    first_name = models.CharField(max_length=30)
    middle_initial = models.CharField(max_length=1)
    last_name = models.CharField(max_length=30)
    suffix = models.CharField(max_length=5, choices=SUFFIX_CHOICES, default='None')
    LRN = models.CharField(max_length=50)
    birth_date = models.DateField()
    phone_number = models.CharField(max_length=15)
    email =  models.EmailField()
    last_login = models.DateTimeField()
    last_logout = models.DateTimeField()
    face_img = models.ImageField(upload_to=student_directory_path, blank=True, null=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
    