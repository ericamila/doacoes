from django.urls import path

from . import views

app_name = "settlement"

urlpatterns = [
    path("", views.lists, name="lists"),
    path("<int:id>", views.detail, name="detail"),
]
