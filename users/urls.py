from django.urls import path
from django.contrib.auth import views as auth_views

from . import views
from .forms import UsuarioLoginForm, PasswordChangeForm

app_name = "users"

urlpatterns = [
    path("entrar/", auth_views.LoginView.as_view(form_class=UsuarioLoginForm, template_name="users/login.html"), name="login"),
    path("cadastrar/", views.signup_view, name="signup"),
    path("sair/", auth_views.LogoutView.as_view(), name="logout"),
    path("perfil/", views.profile_view, name="profile"),
    path("alterar-senha/", views.password_change_view, name="password_change"),
]
