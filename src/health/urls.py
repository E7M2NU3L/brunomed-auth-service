from django.urls import path
from health.views import Health

urlpatterns = [
    path('', Health.as_view(), name="health")
]
