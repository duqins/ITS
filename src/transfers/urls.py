from django.urls import path

from . import views

app_name = "transfers"

urlpatterns = [
    path("", views.transfer_list, name="list"),
    path("approvals/", views.approvals, name="approvals"),
    path("approvals/<int:pk>/", views.approval_detail, name="approval"),
    path("holds/request/", views.hold_request, name="hold_request"),
    path("holds/<int:pk>/decide/", views.hold_decide, name="hold_decide"),
    path("holds/<int:pk>/start/", views.transfer_start, name="start"),
    path("<int:pk>/", views.transfer_detail, name="detail"),
    path("<int:pk>/hand-over/", views.transfer_handover, name="handover"),
    path("<int:pk>/receive/", views.transfer_receive, name="receive"),
    path("<int:pk>/resolve/", views.transfer_resolve, name="resolve"),
    path("<int:pk>/cancel/", views.transfer_cancel, name="cancel"),
]
