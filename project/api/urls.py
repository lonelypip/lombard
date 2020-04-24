from django.urls import path
from .views import CheckViewSet


urlpatterns = [
    path('check/products/', CheckViewSet.as_view({'post':'products'}))
]


