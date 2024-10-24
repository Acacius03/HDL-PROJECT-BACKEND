from django.urls import path
from .views import enroll, get_students, login
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('students/', get_students, name='get_students'),
    path('enroll/', enroll, name='enroll'),
    path('login/', login, name='login'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)