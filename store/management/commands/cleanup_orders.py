from django.core.management import BaseCommand
from store.models import Order
from store.enums import OrederStatuses
import jdatetime
import pytz


class Command(BaseCommand):
    help = "cancels un-compeleted orders"

    def handle(self, *args, **options):
        qs = Order.objects.filter(statuse=OrederStatuses.CREATED)
        today = jdatetime.datetime.now(tz=pytz.timezone("asia/Tehran"))
        for order in qs:
            dif = today - order.created_on
            if dif.days > 1:
                order.set_as_canceled()
                print(f"Order #{order.pk} canceled.")
            else:
                print(f"Order #{order.pk} is less than 1 days old.")
