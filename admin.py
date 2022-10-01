from django.contrib import admin
from .models import Item,OrderItem,Order,BelingAdress,Coupon,Payment,Refund


# Register your models here.
admin.site.register(Item)
admin.site.register(OrderItem)
admin.site.register(Order)
admin.site.register(BelingAdress)
admin.site.register(Coupon)
admin.site.register(Payment)
admin.site.register(Refund)