from django.urls import path, include
from rest_framework import routers

from .views import TasksViewSet

router = routers.DefaultRouter()
router.register(r'tasks', TasksViewSet)

urlpatterns = [
    path('', include(router.urls)),
]