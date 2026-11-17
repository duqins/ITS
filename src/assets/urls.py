from django.urls import path

from . import views

app_name = "assets"

urlpatterns = [
    path("", views.asset_list, name="list"),
    path("register/", views.asset_register, name="register"),
    path("<int:pk>/", views.asset_detail, name="detail"),
    path("<int:pk>/edit/", views.asset_edit, name="edit"),
    path("<int:pk>/confirm/", views.asset_confirm, name="confirm"),
    path("<int:pk>/verify/", views.asset_verify, name="verify"),
    path("<int:pk>/files/<int:file_pk>/", views.asset_file, name="file"),
    path("<int:pk>/list/", views.listing_create, name="listing_create"),
    path("listings/<int:pk>/", views.listing_detail, name="listing"),
    path("listings/<int:pk>/submit/", views.listing_submit, name="listing_submit"),
    path("listings/<int:pk>/decide/", views.listing_decide, name="listing_decide"),
    path("listings/<int:pk>/withdraw/", views.listing_withdraw, name="listing_withdraw"),
    path("search/", views.search, name="search"),
]
