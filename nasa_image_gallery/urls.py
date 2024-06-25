from django.contrib import admin
from django.urls import path, include
from . import views


urlpatterns = [
    path('accounts/', include('django.contrib.auth.urls')),
  #  path('register.html', views.register_view, name='register'),
    path('admin/', admin.site.urls),
    path('', include('django.contrib.auth.urls')),
    path('', views.index_page, name='index-page'),
    path('accounts/login/', views.login_user, name='login'),
    path('home/', views.home, name='home'),
    path('buscar/', views.search, name='buscar'),
    path('favourites/', views.getAllFavouritesByUser, name='favoritos'),
    path('favourites/add/', views.saveFavourite, name='agregar-favorito'),
    path('favourites/delete/', views.deleteFavourite, name='borrar-favorito'),

    path('accounts/logout/', views.logout_user, name='logout'),
   
]
