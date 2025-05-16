from django.urls import path
from . import views

app_name = "superadmin"

urlpatterns = [
    path("", views.login_view, name="login"),
    path("register/", views.register, name="register"),
    path("dashboard/", views.dashboard, name="dashboard"),
    path("accept/<str:id>", views.accept_post, name="accept"),
    path("reject/<str:id>", views.reject_post, name="reject"),
    path("logout/", views.logout_view, name="logout"),
]