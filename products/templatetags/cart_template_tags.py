from django import template
from products.models import Cart
register = template.Library()


@register.filter
def cart_item_count(user):
	if user.is_authenticated:
		cart, created = Cart.objects.get_or_create(user=user)
		return cart.get_items_count()