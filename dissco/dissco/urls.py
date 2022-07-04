from django.conf import settings
from django.contrib import admin
from django.http import HttpRequest
from django.urls import path, include, re_path
from django.views import static
from django.views.defaults import page_not_found
from rest_framework import routers

from common.api_views import InstitutionViewSet, whoami
from policy import api_views as public_policy_views
from qa import api as pack_api

# setup the api router and add the viewsets
router = routers.DefaultRouter()
router.register('institution', InstitutionViewSet)
router.register('service', public_policy_views.ServiceViewSet)
router.register('policy', public_policy_views.PolicyAreaViewSet)

# frontend document root location
FRONTEND_ROOT: Path = settings.BASE_DIR / 'static' / 'frontend'


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
    path('', static.serve, {'document_root': FRONTEND_ROOT, 'path': 'index.html'}),
    # catch all other paths and serve static content, this should let the SPA work as expected
    re_path('^(?P<path>.*)/$', static.serve, {'document_root': FRONTEND_ROOT}),
]


def handler404(request: HttpRequest, *args, **kwargs):
    """
    404 handler which ensures invalid django paths are routed to the Vue app.
    """
    # if the path starts with any of our known non-SPA paths, use the default django 404 function
    non_spa_paths = {'/api/', '/admin/', '/auth/'}
    if any(request.path.startswith(non_spa_path) for non_spa_path in non_spa_paths):
        return page_not_found(request, *args, **kwargs)

    # otherwise, serve the index.html
    return static.serve(request, path='index.html', document_root=FRONTEND_ROOT)
