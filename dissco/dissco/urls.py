from django.contrib import admin
from django.urls import path, include
from rest_framework import routers

from common.api_views import InstitutionViewSet, current_user

# setup the api router and add the viewsets
router = routers.DefaultRouter()
router.register(r'institutions', InstitutionViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('common.urls')),
    path('auth/', include('dj_rest_auth.urls')),
    path('api/user', current_user),
    path('api/', include(router.urls)),
]
