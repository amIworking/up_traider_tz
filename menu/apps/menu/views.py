from collections import defaultdict

from django.db.models import Q, F
from django.views.generic import TemplateView, View

from apps.menu.models import Menu


class MenuView(TemplateView):
    template_name = 'menu/main.html'

    def proccess_menu(self, menu: Menu):
        return {
            "name": menu.name,
            "id": menu.pk,
            "nested": [],
        }

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        code = self.request.GET.get('code')

        menu_qs = Menu.objects.filter(
            Q(main_menu__all_child_menu__code=code) | Q(all_child_menu__code=code)).distinct()

        main = None
        pref = defaultdict(list)
        for menu in menu_qs:
            if menu.parent is None:
                main = menu
                continue
            pref[menu.parent_id].append(menu.id)

        if main is None:
            raise Exception("No main menu")

        menu_map = {i.id: i for i in menu_qs}

        def build(obj):
            data = {
                "name": obj.name,
                "link": f"/menu/?code={id}",
                "child": [],
            }
            child_ids = pref.get(obj.id)
            if child_ids is None:
                return data
            for child_id in child_ids:
                child = menu_map.get(child_id)
                data["child"].append(build(child))
            return data

        context["menu"] = build(main)
        context["target_code"] = code
        return context
