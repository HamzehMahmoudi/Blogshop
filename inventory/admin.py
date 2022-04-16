from django.contrib import admin
from django.utils.translation import activate
from . import models

admin.site.site_header = "art shop"


@admin.action(description="activate product")
def set_product_active(modeladmin, request, queryset):
    queryset.update(is_active=True)


@admin.action(description="deactivate product")
def set_product_inactive(modeladmin, request, queryset):
    queryset.update(is_active=False)


# Register your models here.
@admin.register(models.Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        "pk",
        "name",
        "description",
        "qty_in_stock",
        "price",
        "is_active",
        "type",
    )

    list_display_links = (
        "pk",
        "name",
    )
    list_editable = (
        "price",
        "qty_in_stock",
    )
    search_fields = ("name", "description__icontains")
    list_filter = (
        "is_active",
        "type",
    )
    actions = [set_product_active, set_product_inactive]
