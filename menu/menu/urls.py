from django.contrib import admin
from django.urls import path

from apps.menu.views import MenuView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('menu/', MenuView.as_view())
]
