from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
# We'll add viewsets here later

urlpatterns = [
    path('', include(router.urls)),
]