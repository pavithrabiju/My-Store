from django.shortcuts import render,redirect
from django.views.generic import CreateView,FormView,TemplateView,ListView,DetailView
from django.urls import reverse_lazy
from customer.forms import RegistrationForms,LoginForm
from django.urls import reverse_lazy
from django.contrib import messages                                       
from django.contrib.auth import authenticate,login,logout
from api.models import Products,carts
from django.db.models import Sum

class SignUpView(CreateView):
    template_name="signup.html"
    form_class=RegistrationForms
    success_url=reverse_lazy("signin")

    def form_valid(self, form):
        messages.sucess(self.request,"account created successfully")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.sucess(self.request,"account creation failed")
        return super().form_invalid(form)

class SigninView(FormView):
    template_name="cust-login.html"
    form_class=LoginForm


    def post(self, request,*args,**kwargs):
        form=LoginForm(request.POST)
        if form.is_valid():
            uname = form.cleaned_data.get("username")
            pwd = form.cleaned_data.get("password")
            usr=authenticate(request,username=uname,password=pwd)
            if usr:
                login(request,usr)
                return redirect("user-home")
            else:
                messages.error(request,"invalid credentials")
                return render(request,"cust-login.html",{"form":form})


class HomeView(ListView):
    template_name="cust-index.html"
    context_object_name="products"
    model=Products

class ProductDetailView(DetailView):
    template_name="cust-productdetail.html"
    context_object_name="product"
    pk_url_kwarg="id"
    model=Products            

def add_to_cart(request,*args,**kwargs):
    id=kwargs.get("id")
    prdct=Products.objects.get(id=id)
    usr=request.user
    carts.objects.create(user=usr,product=prdct)
    messages.success(request,"item succesfully added to cart")
    return redirect("user-home")
                                                                         
class CartListView(ListView):
    template_name="cart-list.html"                  
    model=carts
    context_object_name="carts"

    def get(self,request,*args,**kwargs):
        qs=carts.objects.filter(user=request.user)
        total=carts.objects.filter(user=request.user).aggregate(tot=Sum("product__price"))
        return render(request,"cart-list.html",{"carts":qs,"total":total})


