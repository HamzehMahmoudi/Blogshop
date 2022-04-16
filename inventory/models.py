from django.db import models
from django.utils.translation import ugettext as _
from . import enums
import logging

logger = logging.getLogger(__name__)


class Product(models.Model):
    """
    Represents a single product
    """

    name = models.CharField(max_length=200, verbose_name=_("product name"), db_index=True)
    description = models.TextField(verbose_name=_("Description"), help_text=_("product discription"))
    price = models.PositiveIntegerField(default=0, db_index=True, verbose_name=_("product price"))
    qty_in_stock = models.PositiveIntegerField(default=0, verbose_name=_("quantity in stock"))
    is_active = models.BooleanField(default=False, help_text=_("is marketable"), verbose_name=_("is marketable"))
    type = models.CharField(max_length=100, choices=enums.ProductTypes.choices, verbose_name=_("type"))

    def __str__(self) -> str:
        return f"{self.name} {self.type}"

    def can_be_sold(self):
        return self.is_active

    def is_in_stock(self, qty):
        return qty <= self.qty_in_stock

    def deduct_from_stock(self, qty):
        """
        Deducts the qty from self.qty_in_stock
        returns: int
        """
        self.qty_in_stock -= qty
        self.save()
        logger.info(f"{self.name} sold {self.qty_in_stock} left")
        return self.qty_in_stock
