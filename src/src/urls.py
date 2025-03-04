from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('health.urls')), 
    path('api/v1/auth/', include('auth_service.urls'))
]
