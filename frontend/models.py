from django.contrib.auth.models import User
from django.db import models

# Create your models here.
from django.shortcuts import reverse
from django_countries.fields import CountryField

CATEGORY_CHOICES = {
    ('C','Computer'),
    ('M','Mobile'),
    ('T','Tablet')
}
LABEL_CHOICES = {
    ('N','New'),
    ('R','Refurbished'),
    ('U','Used')
}

class Item(models.Model):
    title=models.CharField(max_length=100)
    price =models.FloatField()
    discount_price=models.FloatField(null=True,blank=True)
    category =models.CharField(choices=CATEGORY_CHOICES,max_length=5)
    label=models.CharField(choices=LABEL_CHOICES,max_length=5)
    slug=models.SlugField()
    descreption = models.TextField()
    image=models.ImageField(upload_to='photos/%y/%m/%d')

    def __str__(self):
        return self.title

    def get_discount_percent(self):
        discount=100-(self.discount_price * 100/ self.price)
        return discount

    def get_item_url(self):
        return reverse('frontend:detail',kwargs={
            'slug':self.slug
        })
    def get_add_to_cart(self):
        return reverse('frontend:addcart',kwargs={'slug': self.slug})

    def snip_description(self):
        return self.descreption[:30]+"..."


class OrderItem(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    ordered=models.BooleanField(default=False)
    item=models.ForeignKey(Item,on_delete=models.CASCADE)
    quantity=models.IntegerField(default=1)

    def __str__(self):
        return f"{self.quantity}-{self.item.title} "

    def total_item_price(self):
        return self.quantity * self.item.price

    def total_discount_item_price(self):
        return self.item.discount_price * self.quantity

    def amount_saved(self):
        return self.total_item_price() - self.total_discount_item_price()

    def final_price(self):
        if self.item.discount_price :
            return self.total_discount_item_price()
        else:
            return self.total_item_price()




class Order(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    order_ref = models.CharField(max_length=20)
    items=models.ManyToManyField(OrderItem)
    order_date=models.DateTimeField()
    ordered = models.BooleanField(default=False)
    billing_adress=models.ForeignKey('BelingAdress',on_delete=models.SET_NULL,blank=True,null=True)
    Coupon=models.ForeignKey('Coupon',on_delete=models.SET_NULL,blank=True,null=True)
    payment=models.ForeignKey('Payment',on_delete=models.SET_NULL,blank=True,null=True)
    delivered=models.BooleanField(default=False)
    refund_requested=models.BooleanField(default=False)
    refund_granted=models.BooleanField(default=False)

    def __str__(self):
        return self.user.username

    def total_price(self):
        total=0
        for order_item in self.items.all() :
            total += order_item.final_price()
            if self.Coupon:
                total-=self.Coupon.amount

        return total

class BelingAdress(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    street_adress=models.CharField(max_length=100)
    appartment=models.CharField(max_length=100)
    country=CountryField(max_length=100)
    zip=models.CharField(max_length=10)

    def __str__(self):
        return self.user.username



class Coupon(models.Model):
    code=models.CharField(max_length=100)
    amount=models.FloatField()
    def __str__(self):
        return self.code



class Payment(models.Model):
    stripe_charge_id=models.CharField(max_length=100)
    user=models.ForeignKey(User,on_delete=models.SET_NULL,blank=True,null=True)
    amount=models.FloatField()
    time=models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.user.username


class Refund(models.Model):
    order=models.ForeignKey(Order,on_delete=models.CASCADE)
    reason=models.TextField()
    accepted=models.BooleanField(default=False)


    def __str__(self):
        return f"{self.pk}"





