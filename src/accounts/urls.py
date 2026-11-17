from django.urls import path

from . import views

app_name = "accounts"

urlpatterns = [
    path("sign-in/", views.sign_in, name="login"),
    path("sign-out/", views.sign_out, name="logout"),
    path("switch-role/", views.switch_role, name="switch_role"),
    path("settings/", views.preferences, name="settings"),
    path("settings/theme/", views.set_theme, name="set_theme"),
    path("settings/language/", views.set_language, name="set_language"),
]
