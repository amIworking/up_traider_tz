from django.db import models


class Menu(models.Model):
    code = models.CharField(verbose_name="Code", max_length=50, unique=True)
    name = models.CharField(verbose_name="Name", max_length=50)
    parent = models.ForeignKey("menu.Menu", verbose_name="Parent", null=True, blank=True,
                               on_delete=models.PROTECT, related_name='nested_menu')
    main_menu = models.ForeignKey("menu.Menu", verbose_name="Main menu", null=True, blank=True,
                                  on_delete=models.PROTECT, related_name='all_child_menu')
    nested_level = models.SmallIntegerField(verbose_name="Nested Level", default=0)

    class Meta:
        verbose_name = "Menu"

    def __str__(self):
        return f"{self.name}"
