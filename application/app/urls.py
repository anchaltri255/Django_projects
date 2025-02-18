"""
URL configuration for app project.

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
from myapp.views import *
from django.conf import settings

from django.conf.urls.static import static
from django.contrib.auth import views as auth_view
from myapp.forms  import MyPasswordChangeForm, MyPasswordResetForm,MySetPasswordForm

urlpatterns = [
    path('', home, name="home"),
    path('admin/', admin.site.urls),
    path('about/',about,name="about"),
    path('contact/',contact,name="contact"),
    path('register/',register,name="register"),
    path('login/', login_page, name="login_page"),
    path('logout/', logout_page, name="logout_page"),
    path('address/',address,name="address"),
    path('addtocart/',add_to_cart,name='add_to_cart'),
    path('cart/',show_cart,name='showcart'),
    path('checkout/',checkout.as_view(),name='checkout'),
    path('remove_from_cart/',remove_from_cart, name='remove_from_cart'),
    path('place_order/',place_order, name='place_order'),
    path('orders/', orders, name='orders'),
    path('search/',search_view, name='search'),
    path('update_cart_quantity/',update_cart_quantity, name='update_cart_quantity'),
    path('all_category/',all_category,name="all_category"),
    path('profile/',ProfileView.as_view(),name="profile"),
    path('updateAddress/<int:pk>',UpdateAddress.as_view(),name="updateAddress"),
    path("category/<slug:val>", CategoryView.as_view(),name="category"),
    path("category-title/<val>", CategoryTitle.as_view(),name="category-title"),
    path("product-detail/<int:pk>", ProductDetail.as_view(),name="product-detail"),

    #path('logout/', auth_view.LogoutView.as_view(next_page ='login'),name="logout"),
    

    path('passwordchange/',auth_view.PasswordChangeView.as_view(template_name=
    'myapp/changepassword.html',form_class=MyPasswordChangeForm, success_url=
    '/passwordchangedone'), name='passwordchange'),

    path('passwordchangedone/',auth_view.PasswordChangeDoneView.as_view(template_name=
    'myapp/passwordchangedone.html'),name='passwordchangedone'),

    path('password-reset/',auth_view.PasswordResetView.as_view(template_name='myapp/password_reset.html',
    form_class=MyPasswordResetForm),name="password_reset"),

    path('password-reset/done/',auth_view.PasswordChangeDoneView.as_view(template_name='myapp/password_reset_done.html'),
    name="password_reset_done"),

    path('password-reset-confirm/<uidb64>/<token>/',auth_view.PasswordResetConfirmView.as_view(template_name='myapp/password_reset_confirm.html',
    form_class=MySetPasswordForm),name='password_reset_confirm'),
    
    path('password-reset-complete/',auth_view.PasswordResetCompleteView.as_view(template_name="myapp/password_reset_complete.html"),name='password_reset_complete'),

]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
