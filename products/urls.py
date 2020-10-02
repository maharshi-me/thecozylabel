from django.urls import path
from . import views

app_name = 'products'

urlpatterns = [
	path('', views.ProductsList.as_view(), name = 'list_products'),
	path('all_product/', views.All_ProductsList.as_view(), name = 'all_products'),

	path('product_detail/<int:pk>/', views.ProductDetail.as_view(), name = 'product_detail'),
	path('cart/', views.CartList.as_view(), name='cart'),
	path('contact/', views.ContactFormPage.as_view(), name='contact-us'),
	path('terms_condition/', views.Terms_Condition, name = 'terms_condition'),
	path('privacy_policy/', views.Privacy_Policy, name = 'privacy_policy'),
	path('about_us/', views.about_us, name = 'about_us'),
	path('shipping_policy/', views.return_refund, name = 'return_refund'),
	path('how_to_buy/', views.how_to_buy, name = 'how_to_buy'),
	path('exchange/', views.exchange, name = 'exchange'),
	path('size_chart/', views.size, name = 'size'),
	path('add-to-cart/', views.AddToCart.as_view(), name = 'add_to_cart'),
	path('increment/<int:pk>/', views.IncrementCart.as_view(), name = 'increment'),
	path('decrement/<int:pk>/', views.DecrementCart.as_view(), name = 'decrement'),
	path('remove-from-cart/<int:pk>/', views.DeleteFromCart.as_view(), name='remove_from_cart'),
]