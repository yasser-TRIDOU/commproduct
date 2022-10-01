from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from .forms import ShippingAdressForm,CouponForm
from .models import Item as it, Order
from .models import OrderItem,BelingAdress,Coupon
from django.views.generic import View,DetailView,ListView
# Create your views here.

# def home(request):
#   context={'items':it.objects.all()}
#   return render(request, 'home.html',context=context)


class HomeView(ListView):
    model=it
    paginate_by = 6
    template_name = 'home.html'


class ProductDetailView(DetailView):
    model=it
    template_name = 'detail.html'


@login_required(login_url='../account/login/')
def add_to_cart(request,slug):
    item=get_object_or_404(it,slug=slug)
    order_item,created=OrderItem.objects.get_or_create(
        item=item,
        user=request.user,
        ordered=False
    )
    order_q=Order.objects.filter(user=request.user,ordered=False)

    if order_q.exists():
        order=order_q[0]
        if order.items.filter(item__slug=item.slug).exists():
            order_item.quantity+=1
            order_item.save()
            messages.info(request,message='item added to your cart')
            return redirect('frontend:summary')
        else:
            messages.info(request,message='item added to your cart')
            order.items.add(order_item)
            return redirect('frontend:summary')
    else :
        order_date=timezone.now()
        order=Order.objects.create(user=request.user,order_date=order_date)
        order.items.add(order_item)
        messages.info(request, message='item added to your cart')
        return redirect('frontend:summary')\




@login_required(login_url='../account/login/')
def remove_order_item(request,slug):
    item=get_object_or_404(it,slug=slug)
    order_q=Order.objects.filter(user=request.user,ordered=False)

    if order_q.exists():
        order=order_q[0]
        if order.items.filter(item__slug=item.slug).exists():
            order_item=OrderItem.objects.filter(item=item,user=request.user,ordered=False)[0]
            if order_item.quantity > 1 :
                order_item.quantity-=1
                order_item.save()
            else:
                order.items.remove(order_item)
            messages.info(request, message='cart updeted')
            return redirect('frontend:summary')
        else :
            messages.info(request, message='item was not in your cart')
            return redirect('frontend:detail',slug=slug)
    else:
        messages.info(request, message='you do not have an active order')
        return redirect('frontend:detail',slug=slug)


class OrderSummaryView(LoginRequiredMixin,View):
    def get(self, *args,**kwargs):
        try:
            current_order=Order.objects.get(user=self.request.user,ordered=False)
            context={
                'object':current_order
            }
            return render(self.request,'summary.html',context=context)
        except ObjectDoesNotExist:
            messages.warning(self.request,"you do not have an active order for now")
            return redirect('/')
        return render(self.request,'summary.html',context)


class shiping_adr(View):
    def get(self,*args,**kwargs):
        try:
            order=Order.objects.get(user=self.request.user,ordered=False)
            form=ShippingAdressForm()
            context={
                'form':form,
                'order':order,
                'couponform':CouponForm(),
                'display_coupon_form':True
            }
            return render(self.request, 'shiping-adress.html',context)
        except ObjectDoesNotExist:
            messages.info(self.request, 'you do not have an active order')
            return redirect('frontend:shipadress')
    def post(self,*args,**kwargs):
        form=ShippingAdressForm(self.request.POST or None)
        try:
            order=Order.objects.get(user=self.request.user,ordered=False)
            if form.is_valid():
                street_adress=form.cleaned_data.get('street_adress')
                appartment_adress=form.cleaned_data.get('appartment_adress')
                country=form.cleaned_data.get('country')
                zip_code=form.cleaned_data.get('zip_code')


                billing_adress=BelingAdress(
                    user=self.request.user,
                    street_adress=street_adress,
                    appartment=appartment_adress,
                    country=country,
                    zip=zip_code,
                )
                billing_adress.save()
                order.billing_adress=billing_adress
                order.save()
                messages.info(self.request, "adress addeed to order")
                return redirect('frontend:payment')
        except ObjectDoesNotExist:
            messages.info(self.request ,"No active order")
            return redirect('frontend:summary')

def get_coupon(request,code):
    try:
        coupon=Coupon.objects.get(code=code)
        return coupon
    except ObjectDoesNotExist:
        messages.info(request,'This coupon is not valid')
        return redirect('frontend:summary')





class AddCoupon(View):
    def post(self,*args,**kwargs):
        form=CouponForm(self.request.POST or None)
        if form.is_valid():
            try:
                code=form.cleaned_data.get('code')
                order=Order.objects.get(user=self.request.user,ordered=False)
                order.Coupon=get_coupon(self.request,code)
                order.save()
                messages.success(self.request,'Coupon addded')
                return redirect('frontend:shipadress')
            except ObjectDoesNotExist:
                messages.info(self.request, 'You do not have an active order')
                return redirect('frontend:shipadress')




class PaymentView(View):
    def get(self,*args,**kwargs):
        order=Order.objects.get(user=self.request.user,ordered=False)
        if order.billing_adress :
            context={
                'order':order,
                'diplay_coupon_from':False

            }
            return render(self.request,'payment.html',context)
        else:
            messages.warning(self.request,'Please add your billing adress')
            return redirect('frontend:shipadress')




