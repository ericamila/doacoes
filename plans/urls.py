from django.urls import path

from . import views

app_name = "plans"

urlpatterns = [
    path("", views.lists, name="lists"),
    path("criar", views.new, name="new"),
    path("<int:id>", views.detail, name="detail"),
    path("<int:id>/remover", views.remove, name="remove"),
    path("plano-de-acao/<int:id>/registrar-accountability/", views.registrar_accountability,
         name="registrar_accountability"),
    path('carregar-dados/', views.load_datas, name='load_datas'),
]
