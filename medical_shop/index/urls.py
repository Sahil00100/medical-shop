from django.contrib import admin
from django.urls import path,include

from index.views import index_view,register_view,login_view,logout_view,single_product_view,cart_view
from index.views import cart_adder,orders_view,search_view,delete
from django.conf.urls.static import static
from django.conf import settings
import os


urlpatterns = [
   path('index/',index_view,name='index'),
   path('register/',register_view,name='register'),
   path('login/',login_view,name='login'),
   path('logout/',logout_view,name='logout'),
   path('product/<str:id>/',single_product_view,name='product'),
   path('cart/',cart_view,name='cart'),
   path('cartadd/<str:id>/',cart_adder,name='cartadd'),
   path('orders/',orders_view,name='orders'),
   path('delete/<str:id>/',search_view,name='delete'),
   path('search/',search_view,name='search'),

]+ static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
