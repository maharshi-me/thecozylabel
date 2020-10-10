from django.urls import path
from . import views

app_name = 'a'

urlpatterns = [
	path('dashboard/', views.Orders.as_view(), name = 'dashboard'),
	path('orders/<int:pk>/', views.OrdersDetail.as_view(), name = 'orders-detail'),
	path('create-item/', views.Items.as_view(), name='item-create'),
	path('items/', views.ItemsDisplay.as_view(), name='item-list'),
	path('items/edit/<int:pk>/', views.ItemUpdate.as_view(), name='item-edit'),
	path('items/delete/<int:pk>/', views.ItemDelete.as_view(), name='item-delete'),
	path('contacts/', views.ContactsList.as_view(), name='contacts-list'),
	path('contacts/<int:pk>/', views.ContactsDetail.as_view(), name = 'contacts-detail'),
	path('add-color/', views.AddColor.as_view(), name = 'color-create'),
	path('colors/', views.Colors.as_view(), name = 'colors'),





]