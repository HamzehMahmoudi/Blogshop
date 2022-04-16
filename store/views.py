from django.contrib.auth import login
from store import models, serializer
from django.contrib import messages
from django.shortcuts import redirect, render, get_object_or_404
from inventory.models import Product
from .models import Order, OrderItem
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from rest_framework import viewsets
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
import logging
# import weasyprint
from django.http import HttpRequest, HttpResponse
from rest_framework import permissions, status
from .permisssion import IsOwnerOrReadOnly
from rest_framework.exceptions import NotAuthenticated
from rest_framework.decorators import action

logger = logging.getLogger(__name__)
# Create your views here.


def add_to_cart(request):
    product_id = request.GET.get("product_id")
    product = get_object_or_404(Product, pk=product_id)
    if not product.can_be_sold():
        messages.error(request, "we can't sell this item right now")
        return redirect("products")
    if not product.is_in_stock(1):
        messages.error(request, "we dont havae enough item")
        return redirect("products")
    if "cart" not in request.session.keys():
        request.session["cart"] = {}

    if str(product.pk) in request.session["cart"].keys():
        request.session["cart"][str(product.pk)] += 1
    else:
        request.session["cart"][str(product.pk)] = 1

    request.session.save()
    messages.success(request, f"{product.name} added to ypur cart")
    return redirect("products")


def cart_view(request):
    object_list = []
    for item in request.session.get("cart", []):
        object_list += [{"product": Product.objects.get(
            pk=int(item)), "qty": request.session["cart"][item]}]
    return render(request, "store/cart.html", context={"object_list": object_list})


def delete_row(request, product_id):
    request.session["cart"].pop(str(product_id), None)
    request.session.save()
    messages.success(request, "deleted")
    return redirect("cart")


@require_POST
@csrf_exempt
def deduct_from_cart(request):
    """
    Deducts one from product's qty in the cart
    """
    product_id = request.POST.get("product_id", None)

    # What if there were not product_id provided?
    if not product_id:
        return JsonResponse({"success": False, "error": "Invalid data."}, status=400)

    # Try to deduct from qty
    try:
        request.session["cart"][product_id] -= 1
        request.session.modified = True
        return JsonResponse({"success": True, "qty": request.session["cart"][product_id]}, status=200)
    except KeyError:
        # What if the product is not in the cart?
        return JsonResponse({"success": False, "error": "Invalid data. Not in the cart."}, status=400)


@login_required
def order(request):
    cart = request.session.get("cart", None)
    if not cart:
        messages.error(request, "your cart is empty")
        return redirect("inventory:list")
    order = Order.objects.create(owner=request.user)
    for item in cart:
        product = Product.objects.get(pk=int(item))
        qty = cart[item]
        if not product.is_in_stock(qty):
            messages.success(request, "we dont have enough item")
            return redirect("store:view-cart")
        OrderItem.objects.create(
            order=order, product=product, qty=qty, price=product.price * qty)
        product.deduct_from_stock(qty)
    messages.success(request, "ordered")
    request.session.pop("cart")
    request.session.save()
    logger.info(f"User #{request.user.pk} placed the order #{order.pk}.")

    return redirect("orders")


"""
DRF VIEW
"""


class OrderViewSet(viewsets.ModelViewSet):
    """
    viweset for order
    """

    queryset = models.Order.objects.all()
    serializer_class = serializer.OrderSerializer
    permission_classes = [IsOwnerOrReadOnly]

    def get_queryset(self):
        qs = super().get_queryset()
        if self.request.user.is_anonymous:
            raise NotAuthenticated()
        return qs.filter_by_owner(self.request.user)

    @action(detail=True, description='Cancels an order')
    def cancel_order(self, request, *args, **kwargs):
        """
        Cancels an order
        """
        order_instance = self.get_object()
        order_instance.set_as_canceled()
        order_serializer = self.get_serializer(instance=order_instance)
        return JsonResponse(order_serializer.data, status=status.HTTP_202_ACCEPTED)


class OrderView(LoginRequiredMixin, generic.ListView):
    template_name = "store/orders.html"
    paginate_by = 10

    def get_queryset(self, *args, **kwargs):
        return Order.objects.filter(owner=self.request.user)

    class Meta:
        ordering = ["-created_on"]


class PrintOrder(generic.DetailView):
    model = Order
    template_name = "store/order_detail.html"

    # def get(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
    #     g = super().get(request, *args, **kwargs)
    #     rendered_content = g.rendered_content
    #     pdf = weasyprint.HTML(string=rendered_content,
    #                           base_url="http://127.0.0.1:8000").write_pdf()

    #     # Create a new http response with pdf mime type
    #     response = HttpResponse(pdf, content_type="application/pdf")
    #     return response


class OrderItemViewSet(viewsets.ModelViewSet):
    queryset = models.OrderItem.objects.all()
    serializer_class = serializer.OrderItemSerializer
    permission_classes = [permissions.IsAuthenticated]
