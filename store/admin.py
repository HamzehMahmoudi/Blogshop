from django.contrib import admin
from . import models


class OrderItemInline(admin.TabularInline):
    """
    Admin inline for OrderItem model
    """

    model = models.OrderItem
    fields = (
        "product",
        "qty",
        "price",
    )


@admin.register(models.Order)
class OrderAdmin(admin.ModelAdmin):
    inlines = (OrderItemInline,)
    list_display = (
        "pk",
        "owner",
        "statuse",
    )

    list_display_links = (
        "pk",
        "owner",
    )
    list_editable = ("statuse",)
    search_fields = ("statuse__icontains",)
    list_filter = ("owner", "statuse", "created_on")
    list_per_page = 10
