from django.urls import path
from customer import views

urlpatterns=[
    path("register",views.SignUpView.as_view(),name="register"),
    path("customers/login",views.SigninView.as_view(),name="signin"),
    path("customers/home",views.HomeView.as_view(),name="user-home"),
    path("products/details/<int:id>",views.ProductDetailView.as_view(),name="product-detail"),
    path("products/carts/<int:id>/add",views.add_to_cart,name="add-cart"),
    path("carts/all",views.CartListView.as_view(),name="cart-list")
]  
