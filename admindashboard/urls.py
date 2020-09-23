from django.urls import path
from . import views

app_name = 'a'

urlpatterns = [
	path('dashboard/', views.Orders.as_view(), name = 'dashboard'),
	path('orders/<int:pk>/', views.OrdersDetail.as_view(), name = 'orders-detail'),
	path('create-item/', views.Items.as_view(), name='item-create'),
	path('create-carousel/', views.CarouselCreate.as_view(), name='carousel-create'),
	path('items/', views.ItemsDisplay.as_view(), name='item-list'),
	path('carousels/', views.CarouselsDisplay.as_view(), name='carousel-list'),
	path('items/edit/<int:pk>/', views.ItemUpdate.as_view(), name='item-edit'),
	path('carousels/edit/<int:pk>/', views.CarouselUpdate.as_view(), name='carousel-edit'),	
	path('items/delete/<int:pk>/', views.ItemDelete.as_view(), name='item-delete'),
	path('carousels/delete/<int:pk>/', views.CarouselDelete.as_view(), name='carousel-delete'),
	path('contacts/', views.ContactsList.as_view(), name='contacts-list'),
	path('contacts/<int:pk>/', views.ContactsDetail.as_view(), name = 'contacts-detail'),





]