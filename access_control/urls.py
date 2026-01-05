from django.urls import path
from .views import AccessLogListCreateView, AccessLogDetailView

urlpatterns = [
    path("logs/", AccessLogListCreateView.as_view()),
    path("logs/<int:pk>/", AccessLogDetailView.as_view()),
]