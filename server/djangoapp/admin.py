from django.contrib import admin
from .models import CarMake, CarModel



# Register your models here.


# CarModelInline class
class CarModelInline(admin.StackedInline):
    model = CarModel
    extra = 3

# CarModelAdmin class
class CarModelAdmin(admin.ModelAdmin):
    fields = ['name', 'make','year', 'model_type', 'dealer_id']

# CarMakeAdmin class with CarModelInline
class CarMakeAdmin(admin.ModelAdmin):
    fields=['name', 'description']
    inlines = [CarModelInline]

# Register models here
admin.site.register(CarModel, CarModelAdmin)
admin.site.register(CarMake, CarMakeAdmin)
