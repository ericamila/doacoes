from django.urls import path

from . import views

app_name = "proposals"

urlpatterns = [
    path("", views.lists, name="lists"),
    path("criar", views.new, name="new"),
    path("<int:id>", views.detail, name="detail"),
    path("<int:id>/editar", views.edit, name="edit"),
    path("proposta/<int:id>/registrar-ciencia/", views.registrar_ciencia, name="registrar_ciencia"),
    path("proposta/<int:id>/remover-ciencia/", views.remover_ciencia, name="remover_ciencia"),
    path("<int:id>/remover", views.remove, name="remove"),
]
