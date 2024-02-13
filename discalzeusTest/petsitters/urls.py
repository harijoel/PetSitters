from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("petsitter/<int:petsitter_id>", views.petsitter, name="petsitter"),
    path("user/<str:username>", views.userProfile, name="user"),
    path("register", views.register, name="register"),
    path("search", views.search, name="search")
]