from django.urls import path

from . import views

app_name = "resource_requests"

urlpatterns = [
    path("", views.request_list, name="list"),
    path("new/", views.request_create, name="create"),
    path("<int:pk>/", views.request_detail, name="detail"),
    path("<int:pk>/edit/", views.request_edit, name="edit"),
    path("<int:pk>/submit/", views.request_submit, name="submit"),
    path("<int:pk>/cancel/", views.request_cancel, name="cancel"),
    path("<int:pk>/close/", views.request_close, name="close"),
]
