"""
URL configuration for setup project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.contrib import admin
from django.urls import include, path
from django.conf.urls.static import static

from projects import views


handler404 = "utils.views.view_404"

urlpatterns = [
    path("admin/", admin.site.urls),
    path("users/", include("users.urls")),
    path("", views.lists, name="lists"),
    path("projects/", include("projects.urls")),
    path("proposals/", include("proposals.urls")),
    path("plans/", include("plans.urls")),
    path("accountability/", include("accountability.urls")),
    path("commitments/", include("commitments.urls")),
    path("settlement/", include("settlement.urls")),
    path("payment/", include("payment.urls")),
    path("utils/", include("utils.urls")),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


