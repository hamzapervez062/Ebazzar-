"""
URL configuration for Ebazzar project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from Account import views
from Products import views as product_views
from Cart import views as cart_views
from Order import views as order_views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('signup/', views.sign_up, name='signup'),
    path('login/', views.log_in, name='login'),
    path('profile/', views.profile, name='profile'),
    path('logout/', views.user_logout, name='logout'),
    ##product
    path('', product_views.homeListView.as_view(), name='homelist'),
    # path('store/', product_views.Store, name='store'),
    path('store/', product_views.Store.as_view(), name='store'),
    path('store/category/<slug:post>/', product_views.storeListView.as_view(), name='storeview'),
    # path('store/category/<slug:post>/', product_views.storeRedirectView.as_view(), ),
    path('search/', product_views.SearchItem, name='search'),
    path('price_range/', product_views.PriceRange, name='price_range'),

    #product detail
    path('store/category/<slug:post>/<slug:slug>/', product_views.ProductDetails.as_view(), name='productdetail'),

    #review
    path('store/category/<slug:post>/<slug:slug>/review/', product_views.ReviewSubmit, name='reviewd'),
    path('store/category/<slug:post>/<slug:slug>/review/delete/', product_views.deleteReview, name='deletereview'),

    #cart
    path('cart/<int:id>', cart_views.AddToCart, name='cart'), 
    # path('cart/<int:id>', cart_views.AddtoCart.as_view(), name='cart'),
    path('cart/', cart_views.CartView, name='cartview'),
    path('cart/delete/<int:id>', cart_views.DeleteCart, name='deletecart'),
    path('cart/update/<int:id>', cart_views.UpdateCart, name='updatecart'),
    path('Quantityup/<int:id>', cart_views.QuantityUp, name='quantityup'),
    path('Quantitydown/<int:id>', cart_views.QuantityDown, name='quantitydown'),

    #checkout
    path('checkout/', order_views.checkout, name='checkout'),
   

    #order
    path('placeorder/', order_views.placeorder, name='placeorder'),
    path('editshippinginfo/', order_views.editshippinginfo, name='editinfo'),

    path('orders/', order_views.order_processing, name='orderprocessing'),

    #order complete
    path('ordercomplete/<int:id>/<slug:slug>/', order_views.order_complete, name='ordercomplete'),

    #dashboard
    path('dashboard/' , views.dashboard, name='dashboard'),
    path('activate/<uidb64>/<token>/', views.activate, name='activate'),
    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
