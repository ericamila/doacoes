from django.urls import path

from . import views

app_name = "accountability"

urlpatterns = [
    path("", views.lists, name="lists"),
    path("criar", views.new, name="new"),
    path("<int:id>/editar", views.edit, name="edit"),
    path("<int:id>/remover", views.remover_accountability, name="remove"),
    path("<int:accountability_id>/registrar-documento/", views.register_document, name="register_document"),
    path('remover-documento/<int:documento_id>/', views.remove_document, name='remove_document'),
]
