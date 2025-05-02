from django.contrib import admin
from .models import *
# Register your models here.
class CountriesAdmin(admin.ModelAdmin):
    list_display = ('id', 'country_name')
    search_fields = ('country_name',)
    list_filter = ('country_name',)

class StatesAdmin(admin.ModelAdmin):
    list_display = ('id', 'state_name')
    search_fields = ('state_name',)
    list_filter = ('state_name',)

class DistrictsAdmin(admin.ModelAdmin):
    list_display = ('id', 'district_name')
    search_fields = ('district_name',)
    list_filter = ('district_name',)

class ProductsAdmin(admin.ModelAdmin):
    list_display = ('id', 'product_name', 'product_price', 'product_image', 'is_active','product_description','product_mrp','product_offer')
    search_fields = ('product_name',)
    list_filter = ('is_active',)
    prepopulated_fields = {'slug': ('product_name',)}
    list_editable = ('product_price', 'is_active','product_image','product_description','product_offer','product_mrp','product_name',)  # Make editable in the list view
admin.site.register(Countries, CountriesAdmin)
admin.site.register(States, StatesAdmin)
admin.site.register(Districts, DistrictsAdmin)
admin.site.register(Products, ProductsAdmin)
