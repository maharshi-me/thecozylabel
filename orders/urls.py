from django.urls import path
from . import views

app_name = 'orders'

urlpatterns = [
	path('checkout/', views.Checkout.as_view(), name = 'checkout'),
	path('confirm/<int:pk>/', views.ConfirmOrder.as_view(), name = 'confirm-order'),
	path('handlerequest/', views.handlerequest, name= 'handlerequest'),
]