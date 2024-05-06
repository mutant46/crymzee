from django.urls import path
from django.views.generic import TemplateView
from .views import DashboardView, CreateUserFileView

urlpatterns = [
    path('', TemplateView.as_view(template_name="home.html"), name='home'),
    path('dashboard/', DashboardView.as_view(), name='dashboard'),
    path('dashboard/files/create/', CreateUserFileView.as_view(), name="create_file")
]
