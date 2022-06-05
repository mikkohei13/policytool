from django.contrib import admin
from django.urls import path, include
from rest_framework import routers

# setup the api router
router = routers.DefaultRouter()

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('common.urls')),
    path('api/', include(router.urls)),
]
