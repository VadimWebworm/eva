from django.urls import path

from . import views

urlpatterns = [
    path("<int:quiz_id>/", views.ApiView.as_view(), name="api"),
]
