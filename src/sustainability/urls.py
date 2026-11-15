from django.urls import path

from . import views

app_name = "sustainability"

urlpatterns = [
    path("", views.dashboard, name="dashboard"),
    path("impacts/<int:pk>/confirm/", views.confirm_avoided_purchase, name="confirm"),
]
