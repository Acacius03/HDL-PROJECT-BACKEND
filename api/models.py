from django.db import models
import uuid

# Create your models here.

def student_directory_path(instance, filename):
    return "fingerprints/{0}/{1}".format(instance.uuid, filename)

class Student(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    face_img = models.ImageField(upload_to=student_directory_path, blank=True, null=True)
    # birth_date = models.DateField()
    # email =  models.EmailField()

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
    