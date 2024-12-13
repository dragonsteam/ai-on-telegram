from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import LoginView, PromoteToDriverView

# employee = DefaultRouter()
# employee.register('employee', EmployerViewSet, basename='employee')


urlpatterns = [
    # dj_rest_auth TODO: remove below lines
    # path("_", include("dj_rest_auth.urls")),
    # path("_register/", include("dj_rest_auth.registration.urls")),

]