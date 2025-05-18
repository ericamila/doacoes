from django.urls import path

from . import views

app_name = "projects"

urlpatterns = [
    path("", views.lists, name="lists"),
    path("criar", views.new, name="new"),
    path("<int:id>", views.detail, name="detail"),
    path("<int:id>/editar", views.edit, name="edit"),
    path("<int:id>/remover", views.remove, name="remove"),
]
