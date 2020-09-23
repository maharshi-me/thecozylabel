from django.urls import path
from . import views

app_name = 'profile'

urlpatterns = [
	path('', views.Profile.as_view(), name="menu"),
	path('your-orders/', views.CustomerOrders.as_view(), name='your-orders'),
	path('your-orders/<int:pk>/', views.CustomerOrderDetail.as_view(), name='your-order-detail'),
]