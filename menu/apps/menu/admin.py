from django.contrib import admin

from apps.menu.models import Menu


@admin.register(Menu)
class MenuAdmin(admin.ModelAdmin):
    list_display = ("code", "name", "parent", "main_menu", "nested_level")
