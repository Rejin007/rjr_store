from django.urls import path
from app import views
from django.conf import settings
from django.conf.urls.static import static
from .views import MyProtectedView

app_name = 'app'

urlpatterns = [
    path('',views.homepage, name = 'homepage'),
    path('about',views.about,name = "about"),
    path('contact',views.contact,name = "contact"),
    path('login',views.loginpage,name = "loginpage"),
    path('register',views.register,name = "register"),
    path('forgotpassword',views.forgotpassword,name = "forgotpassword"),
    path('address',views.address,name = "address"),
    path('state/<int:id>',views.states,name = "states"),
    path('district/<int:id>',views.districts,name = "districts"),
    path('products',views.get_products,name = "get_products"),
    path('product/<slug:slug>',views.get_product,name = "get_product"),
    path('verify/<uidb64>/<token>',views.activate,name = "activate"),
    path('refresh',views.refresh,name = "refresh"),
    path('forgotrefresh',views.forgotrefresh,name = "forgotrefresh"),
    path('gsfthagfsdfgs',views.logout,name = "logout"),
    path('adresslist',views.adresslist,name = "adresslist"),
    path('remove_item/<slug:slug>',views.remove_item,name = "remove_item"),
    path('reser_quantity/<slug:slug>',views.reser_quantity,name = "reser_quantity"),
    path('clear_cart',views.clear_cart,name = "clear_cart"),
    path('add_to_cart/<slug:slug>',views.add_to_cart,name = "add_to_cart"),
    path('cart',views.cartload,name = "cartload"),
    path('search_bar/',views.search_bar,name = "search_bar"),
    path('protected',MyProtectedView.as_view(),name = "protected_view")
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
