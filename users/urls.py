from django.urls import path
from django.contrib.auth import views as auth_views

from . import views
from .forms import UsuarioLoginForm, PasswordResetForm, SetPasswordForm

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
         auth_views.PasswordResetView.as_view(
             template_name="registration/password_reset_form.html",
             form_class=PasswordResetForm,
             email_template_name="registration/password_reset_email.html",
             success_url="/users/recuperar-senha/enviado/"
         ), 
         name="password_reset"),
    
    path("recuperar-senha/enviado/", 
         auth_views.PasswordResetDoneView.as_view(
             template_name="registration/password_reset_done.html"
         ), 
         name="password_reset_done"),
    
    path("recuperar-senha/<uidb64>/<token>/", 
         auth_views.PasswordResetConfirmView.as_view(
             template_name="registration/password_reset_confirm.html",
             form_class=SetPasswordForm,
             success_url="/users/recuperar-senha/concluido/"
         ), 
         name="password_reset_confirm"),
    
    path("recuperar-senha/concluido/", 
         auth_views.PasswordResetCompleteView.as_view(
             template_name="registration/password_reset_complete.html"
         ), 
         name="password_reset_complete"),
]
