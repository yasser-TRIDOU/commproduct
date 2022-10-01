from django.urls import path
from . import views

app_name='frontend'
urlpatterns = [
    path('', views.HomeView.as_view(),name='home'),
    path('product/<slug>/',views.ProductDetailView.as_view(),name='detail'),
    path('summary/', views.OrderSummaryView.as_view(),name='summary'),
    path('add_to_cart/<slug>/',views.add_to_cart,name='addcart'),
    path('remove-single-item/<slug>/',views.remove_order_item,name='remove-single-item'),
    path('shiping-adress/',views.shiping_adr.as_view(),name='shipadress'),
    path('add-coupon/',views.AddCoupon.as_view(),name='add-coupon'),
    path('payment/',views.PaymentView.as_view(),name='payment')
]