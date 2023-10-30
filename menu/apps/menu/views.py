from collections import defaultdict

from django.db.models import Q, F
from django.views.generic import TemplateView, View

from apps.menu.models import Menu


class MenuBuilder:
    def __init__(self, menu_qs, code=None, main=None, target=None):
        self.menu_qs = menu_qs
        self.main = main
        self.target = target
        self.menu_map = {i.id: i for i in menu_qs}
        self.relation_map = defaultdict(list)
        for menu in self.menu_qs:
            if self.target is None and menu.code == code:
                self.target = menu
            if self.main is None and menu.parent is None:
                self.main = menu
            self.relation_map[menu.parent_id].append(menu.id)

        if self.main is None:
            raise Exception('Main menu not found')
        if self.target is None:
            raise Exception('Target menu not found')

        if self.target is not self.main:
            self.max_depth = self.calc_depth(self.target)
        else:
            self.max_depth = 0

    def calc_depth(self, menu_to_calc):
        parent = self.menu_map.get(menu_to_calc.parent_id)
        if parent.id == self.main.id:
            return 1
        return self.calc_depth(parent) + 1

    @classmethod
    def build_hidden(cls, link):
        return {
            "name": "...",
            "link": link,
            "childs": [],
        }

    def build(self, menu, current_depth=0):
        data = {
            "name": menu.name,
            "link": f"/menu/?code={menu.code}",
            "childs": [],
        }
        child_ids = self.relation_map.get(menu.id)
        if child_ids is None:
            return data
        if current_depth >= self.max_depth:
            data["childs"].append(
                self.build_hidden(link=f"/menu/?code={self.menu_map.get(child_ids[0]).code}")
            )
        else:
            for child_id in child_ids:
                child = self.menu_map.get(child_id)
                data["childs"].append(self.build(child, current_depth + 1))
        return data

    def build_all(self):
        return self.build(self.main)


class MenuView(TemplateView):
    template_name = 'menu/main.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        code = self.request.GET.get('code')

        main = target = None

        if code:
            menu_qs = Menu.objects.filter(
                # либо указанное меню является корнем и надо найти
                # все меню с этим кодом либо все меню у которых родитель с этим кодом
                Q(main_menu__code=code) | Q(code=code)
                # либо указанное меню является узлом дерева и надо найти все узлы
                # у которых родитель тоже имеет связь с элементым с текущим кодом
                | Q(main_menu__all_child_menu__code=code) | Q(all_child_menu__code=code)
            ).distinct()
            menu_qs = list(menu_qs)
        else:
            # если не указано конкретное меню - выводим все корни (главное меню) + ссылки на детей
            menu_qs = Menu.objects.filter(Q(main_menu=None) | Q(main_menu=F('parent')))
            menu_qs = list(menu_qs)
            main = target = next((i for i in menu_qs if i.parent is None), None)

        builder = MenuBuilder(menu_qs, code, main, target)
        if code is None:
            context["menu"] = [builder.build(i) for i in menu_qs if i.parent is None]
        else:
            context["menu"] = [
                builder.build_hidden('/menu/'),
                builder.build_all(),
            ]
        return context
