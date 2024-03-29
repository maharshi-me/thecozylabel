
from django.db import models
from django.shortcuts import reverse
from django.conf import settings
from django.db.models import Sum
from multiselectfield import MultiSelectField
from ecommerce.storage_backends import MediaStorage


# Create your models here.
user = settings.AUTH_USER_MODEL
LABEL_CHOICES = (
    ('N', 'New Arrivals (Show on Top)'),
)

SIZE_CHOICES = (
    ('XS', 'XS'),
    ('S', 'S'),
    ('M', 'M'),
    ('L', 'L'),
    ('XL', 'XL'),
    ('34', '34'),
    ('35', '35'),
    ('36', '36'),
    ('37', '37'),
    ('38', '38'),
    ('39', '39'),
    ('40', '40'),
    ('41', '41'),
    ('42', '42'),
    ('43', '43'),
)

class Color(models.Model):
    colorcode = models.CharField(max_length=50)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name


class Item(models.Model):
    title = models.CharField(max_length=100)
    image = models.FileField(storage=MediaStorage(), upload_to='item_images')
    image_1 = models.FileField(storage=MediaStorage(), upload_to='item_images', blank=True)
    image_2 = models.FileField(storage=MediaStorage(), upload_to='item_images', blank=True)
    image_3 = models.FileField(storage=MediaStorage(), upload_to='item_images', blank=True)
    image_4 = models.FileField(storage=MediaStorage(), upload_to='item_images', blank=True)
    is_in_stock = models.BooleanField(default=True)
    description = models.TextField(blank=True, null=True)
    price = models.FloatField()
    discount_price = models.FloatField(blank=True, null=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='category')
    label = models.CharField(choices=LABEL_CHOICES, max_length=1, blank=True)
    colors = models.ManyToManyField(Color, blank=True)
    sizes = MultiSelectField(choices=SIZE_CHOICES, max_length=100, blank=True)
    stretchability = models.CharField(max_length=1000, blank=True, null=True)
    material = models.CharField(max_length=1000, blank=True, null=True)
    color = models.CharField(max_length=1000, blank=True, null=True)
    disclaimer = models.TextField(blank=True, null=True)


    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("a:item-list")
    
    def get_discount_percentage(self):
        return int(((self.price - self.discount_price)/self.price)*100)


class Cart(models.Model):
    user = models.OneToOneField(user, on_delete=models.CASCADE, related_name='cart')
    ordered = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username

    def get_total_price(self):
        total = 0
        for item in self.cartitem_set.all():
            total += item.get_final_price()
        return total

    def get_items_count(self):
        return self.cartitem_set.all().aggregate(Sum('quantity'))['quantity__sum']


class Cartitem(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    size = models.CharField(choices=SIZE_CHOICES, max_length=100, blank=True)
    color = models.CharField(max_length=100, blank=True)
    quantity = models.IntegerField(default=1)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.quantity} of {self.item.title} for {self.cart.user.username}"

    def get_item_total_price(self):
        return self.item.price * self.quantity

    def get_discount_total_price(self):
        return self.item.discount_price * self.quantity

    def get_item_final_price(self):
        if self.item.discount_price:
            return self.item.discount_price * self.quantity
        else:
            return self.item.price * self.quantity

    def get_item_final_price_single(self):
        if self.item.discount_price:
            return self.item.discount_price
        else:
            return self.item.price

    def get_amount_saved(self):
        return self.get_item_total_price() - self.get_discount_total_price()

    def get_final_price(self):
        if self.item.discount_price:
            return self.get_discount_total_price()
        return self.get_item_total_price()
    
    def increment(self):
        self.quantity = self.quantity + 1

    def decrement(self):
        self.quantity = self.quantity - 1

















