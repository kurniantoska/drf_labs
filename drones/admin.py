from django.contrib import admin
from drones import models


@admin.register(models.DroneCategory)
class DroneCategoryAdmin(admin.ModelAdmin):
    pass


@admin.register(models.Drone)
class DroneAdmin(admin.ModelAdmin):
    pass


@admin.register(models.Pilot)
class PilotAdmin(admin.ModelAdmin):
    pass


@admin.register(models.Competition)
class CompetitionAdmin(admin.ModelAdmin):
    pass
