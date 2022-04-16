from django.db import models
from django.contrib.auth import get_user_model
from django_jalali.db import models as jmodels
from django.utils.translation import ugettext_lazy as _
from . import enums
from .signals import order_placed
from django.db.models import Sum
import logging

logger = logging.getLogger(__name__)
# Create your models here.


class OrderQuerySetManager(models.QuerySet):
    def filter_by_owner(self, user):
        return self.filter(owner=user)


class Order(models.Model):
    owner = models.ForeignKey(get_user_model(), on_delete=models.PROTECT)
    created_on = jmodels.jDateTimeField(auto_now_add=True)
    statuse = models.CharField(
        max_length=20,
        verbose_name=_("status"),
        choices=enums.OrederStatuses.choices,
        default=enums.OrederStatuses.CREATED,
    )

    objects = OrderQuerySetManager.as_manager()

    def __str__(self):
        return f"{self.owner} order"

    def set_as_canceled(self):
        self.statuse = enums.OrederStatuses.CANCELED
        self.save()
        logger.info(f"Order #{self.pk} canceled")

    def save(self, **kwargs):
        if self.pk is None:
            _created = True
        else:
            _created = False
        super().save()
        order_placed.send(sender=self.__class__, instance=self, created=_created)

    def get_total_qty(self):
        return self.orderitem_set.aggregate(Sum("qty")).get("qty__sum", 0)

    def get_total_price(self):
        return self.orderitem_set.aggregate(Sum("price")).get("price__sum", 0)


class OrderItem(models.Model):
    order = models.ForeignKey("store.Order", on_delete=models.CASCADE)
    product = models.ForeignKey("inventory.Product", on_delete=models.PROTECT)
    qty = models.PositiveIntegerField(default=1)
    discount = models.FloatField(default=0)
    price = models.PositiveIntegerField()

    def get_total(self):
        return self.qty * self.price
