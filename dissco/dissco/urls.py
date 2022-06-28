from django.conf import settings
from django.contrib import admin
from django.urls import path, include, re_path
from django.views import static
from rest_framework import routers

from common.api_views import InstitutionViewSet, whoami
from policy import api_views as public_policy_views
from qa import api as pack_api

# setup the api router and add the viewsets
router = routers.DefaultRouter()
router.register('institution', InstitutionViewSet)
router.register('service', public_policy_views.ServiceViewSet)
router.register('policy', public_policy_views.PolicyAreaViewSet)

urlpatterns = [
    # admin site
    path('admin/', admin.site.urls),

    # endpoints for web app token auth
    path('auth/', include('dj_rest_auth.urls')),

    # authed api endpoints
    path('api/whoami', whoami),
    path('api/<str:pack_type>/pack', pack_api.get_packs),
    path('api/<str:pack_type>/pack/<int:pack_id>', pack_api.get_pack),
    path('api/<str:pack_type>/pack/answer/<int:question_id>', pack_api.handle_answer),

    # public api endpoints
    path('api/institution/<int:institution_id>/policies',
         public_policy_views.InstitutionPolicyAreaAPIView.as_view()),
    path('api/institution/<int:institution_id>/components',
         public_policy_views.InstitutionPolicyComponentAPIView.as_view()),
    path('api/', include(router.urls)),

    # catch the base URL at / and serve the Vite generated index.html
    path('', static.serve, {
        'document_root': settings.BASE_DIR / 'static',
        'path': 'index.html',
    }, name='static.file.serve'),
    # catch all other paths and serve static content, this should let the SPA work as expected
    re_path('^(?P<path>.*)/$', static.serve, {
        'document_root': settings.BASE_DIR / 'static',
    }, name='static.file.serve'),
]
