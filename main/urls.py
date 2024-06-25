from django.contrib import admin
from django.urls import path, include
from nasa_image_gallery import views
urlpatterns = [
   # path('register.html', views.register_view, name='register'),
    path('admin/', admin.site.urls),
    path('', include('nasa_image_gallery.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
    #path('accounts/', include('accounts.urls')),
    path('accounts/login/', views.login_user, name='login'),
    path('accounts/logout/', views.logout_user, name='logout'),
    
]