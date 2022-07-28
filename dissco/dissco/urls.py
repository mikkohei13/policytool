from pathlib import Path

from django.conf import settings
from django.contrib import admin
from django.http import HttpRequest
from django.urls import path, include, re_path
from django.views import static
from django.views.defaults import page_not_found

from common.api_views import whoami
from maturity.api_views import ResponderAPIView
from policy import api_views as policy_views
from qa import api as pack_api

# frontend document root location
STATIC_ROOT: Path = settings.BASE_DIR / 'static'
FRONTEND_ROOT: Path = STATIC_ROOT / 'frontend'

# change the admin login title
admin.site.site_header = 'DiSSCo Admin Login'

urlpatterns = [
    # admin site
    path('admin/', admin.site.urls),

    # openapi landing page and definition
    path('api/', static.serve, {'document_root': STATIC_ROOT, 'path': 'openapi.html'}),
    path('openapi.yaml', static.serve, {'document_root': STATIC_ROOT, 'path': 'openapi.yaml'}),

    # endpoints for web app token auth
    path('auth/', include('dj_rest_auth.urls')),

    # authed api endpoints
    path('api/whoami/', whoami),
    path('api/<str:pack_type>/<int:responder_id>/pack/', pack_api.get_packs),
    path('api/<str:pack_type>/<int:responder_id>/pack/<int:pack_id>/', pack_api.get_pack),
    path('api/<str:pack_type>/<int:responder_id>/pack/<int:pack_id>/finish', pack_api.finish_pack),
    path('api/<str:pack_type>/<int:responder_id>/pack/<int:pack_id>/<int:question_id>/',
         pack_api.handle_answer),

    path('api/policy/', policy_views.InstitutionPolicyAreaAPIView.as_view()),
    path('api/policy/alignment/', policy_views.get_institution_alignment),
    path('api/policy/alignment/<int:mapping_id>/', policy_views.get_institution_alignment_mapping),
    path('api/maturity/responder', ResponderAPIView.as_view()),
    path('api/maturity/responder/<int:responder_id>', ResponderAPIView.as_view()),

    # public api endpoints
    path('api/institution/policy/', policy_views.get_institution_public_policy_list),
    path('api/dissco/service/', policy_views.get_dissco_service_list),
    path('api/dissco/service/<int:service_id>/', policy_views.get_dissco_service),
    path('api/dissco/policy/', policy_views.get_dissco_policy_list),

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
