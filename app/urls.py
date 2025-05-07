from django.urls import path
from app import views
from django.conf import settings
from django.conf.urls.static import static
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
    path('verify/<uidb64>/<token>',views.activate,name="activate"),
    path('refresh',views.refresh,name="refresh"),
    path('forgotrefresh',views.forgotrefresh,name="forgotrefresh"),
    path('gsfthagfsdfgs',views.logout,name="logout"),
    
    path('cart',views.cartload,name="cartload"),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)