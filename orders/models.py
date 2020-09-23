from django.db import models
from django.conf import settings
from products.models import Item
from django.db.models.signals import pre_save, post_save, post_delete
from django.dispatch import receiver
from django.db.models import Sum
import random, string



user = settings.AUTH_USER_MODEL

# Create your models here.


class Shipping_Details(models.Model):
    user = models.ForeignKey(user, on_delete = models.SET_NULL, null=True, related_name='address')
    first_name = models.CharField(max_length=100, blank=True)
    last_name = models.CharField(max_length=100, blank=True)
    email = models.EmailField(blank=True)
    address1 = models.CharField(max_length=200, blank=True)
    address2 = models.CharField(max_length=200, null=True, blank=True)
    phone = models.CharField(max_length=20,blank=True, null=True)
    city = models.CharField(max_length=50, blank=True)
    state =models.CharField(max_length=50, blank=True)
    zipcode = models.CharField(max_length=20, blank=True)

    def __str__(self):
        return self.user.email

class OrderManager(models.Manager):

    def create_new_id(self):
        qs = self.get_queryset()
        while(True):
            x = ''.join(random.choices(
                string.ascii_letters + string.digits, k=8))
            if not qs.filter(order_id=x).exists():
                break
        return x


class Order(models.Model):
    order_id = models.CharField(max_length=10, blank=True)
    customer = models.ForeignKey(
        user, on_delete=models.SET_NULL, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    confirm = models.BooleanField(default=False)
    total = models.DecimalField(decimal_places=2, max_digits=20, default=0, blank=True)
    shipping_details = models.OneToOneField(Shipping_Details, on_delete = models.SET_NULL, null=True)
    is_paid = models.BooleanField(default=False)
    payment_status = models.CharField(max_length=500, blank=True)
    transaction_id = models.CharField(max_length=300, blank=True)
    objects = OrderManager()

    def update_total(self):
        self.total = self.orderitem_set.aggregate(Sum('price_total'))[
            'price_total__sum'] or 0
        self.save()
    def __str__(self):
        return self.customer.email
 


class Orderitem(models.Model):
    item = models.ForeignKey(
        Item, on_delete=models.SET_NULL, null=True)
    size = models.CharField(max_length=20, blank=True)
    color = models.CharField(max_length=100, blank=True)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    item_name = models.CharField(max_length=200, blank=True)
    quantity = models.IntegerField(default=1)
    price_each = models.DecimalField(
        decimal_places=2, max_digits=20, blank=True)
    price_total = models.DecimalField(
        decimal_places=2, max_digits=20, blank=True)


@receiver(pre_save, sender=Orderitem)
def pre_save_OrderItem(sender, instance, *args, **kwargs):
    instance.item_name = instance.item.title
