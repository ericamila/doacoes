from django.urls import path
from django.contrib.auth import views as auth_views

from . import views
from .forms import UsuarioLoginForm, PasswordChangeForm, PasswordResetForm, SetPasswordForm

app_name = "users"

urlpatterns = [
    path("entrar/", auth_views.LoginView.as_view(form_class=UsuarioLoginForm, template_name="users/login.html"), name="login"),
    path("cadastrar/", views.signup_view, name="signup"),
    path("sair/", auth_views.LogoutView.as_view(), name="logout"),
    path("perfil/", views.profile_view, name="profile"),
    path("alterar-senha/", views.password_change_view, name="password_change"),
    path("usuarios/", views.lists, name="lists"),
    path("usuarios/<int:pk>/", views.detail, name="detail"),
    path("usuarios/<int:pk>/editar/", views.edit, name="edit"),
    path("usuarios/<int:pk>/deletar/", views.remove, name="remove"),
    
    # Rotas para reset de senha
    path("recuperar-senha/", 
         views.CustomPasswordResetView.as_view(), 
         name="password_reset"),
    
    path("recuperar-senha/enviado/", 
         views.CustomPasswordResetDoneView.as_view(), 
         name="password_reset_done"),
    
    path("recuperar-senha/<uidb64>/<token>/", 
         views.CustomPasswordResetConfirmView.as_view(), 
         name="password_reset_confirm"),
    
    path("recuperar-senha/concluido/", 
         views.CustomPasswordResetCompleteView.as_view(), 
         name="password_reset_complete"),
]
