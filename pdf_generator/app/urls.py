from django.urls.conf import include, path
from rest_framework.routers import DefaultRouter

from .api import PDFActions

api_router = DefaultRouter()
api_router.register('pdf-actions', PDFActions, basename='pdf-actions')
print(api_router.urls)


urlpatterns = [
    path('', include(api_router.urls))
]
