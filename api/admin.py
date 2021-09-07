from django.contrib import admin
from.models import Car


@admin.register(Car)
class CarAdmin(admin.ModelAdmin):
    fields = (
        'make',
        'model',
        'avg_rating',
    )

    readonly_fields = ('avg_rating',)
