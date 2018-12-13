from django.contrib import admin
from . models import Toy

@admin.register(Toy)
class ToyAdmin(admin.ModelAdmin):
    pass
