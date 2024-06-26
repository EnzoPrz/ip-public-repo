# capa de vista/presentación
# si se necesita algún dato (lista, valor, etc), esta capa SIEMPRE se comunica con services_nasa_image_gallery.py

from django.shortcuts import redirect, render, HttpResponse
from .layers.services import services_nasa_image_gallery 
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User
from django.urls import reverse
from .layers.generic import mapper


def signup_view(request):

    if request.method == 'POST':
        Uname= request.POST.get('username')
        email= request.POST.get('email')
        pass1= request.POST.get('password1')
        pass2= request.POST.get('password2')
        #corrobora que las contraseñas coinsidan:
        if pass1 != pass2:
            return HttpResponse("Tus contraseñas no coinciden")
        
        #Crea el user, lo guarda y te redirige al login
        user = User.objects.create_user(username=Uname, email=email, password=pass1)   
        return redirect('login')
        
    return render(request, 'registration/signup.html')


def login_user(request):
    if request.method == "POST":
        username= request.POST['username']
        password= request.POST['password']
        user= authenticate(request, username=username, password=password)
        if user is not None:
            login(request,user)
            return redirect ("home")
        else:
            messages.error(request,'Volve a intentar')
            return redirect ("login")
    else:
        return render(request, 'registration/login.html')   

# función que invoca al template del índice de la aplicación.
def index_page(request):
    return render(request, 'index.html')

# auxiliar: retorna 2 listados -> uno de las imágenes de la API y otro de los favoritos del usuario.
def getAllImagesAndFavouriteList(request):
    images = services_nasa_image_gallery.getAllImages
    if User is not None:
       favourite_list = services_nasa_image_gallery.getAllFavouritesByUser(request)
    else:
       favourite_list =[]
    
    return images, favourite_list

# función principal de la galería.
def home(request):
   
    # llama a la función auxiliar getAllImagesAndFavouriteList() y obtiene 2 listados: uno de las imágenes de la API y otro de favoritos por usuario*.
    # (*) este último, solo si se desarrolló el opcional de favoritos; caso contrario, será un listado vacío [].
    images= services_nasa_image_gallery.getImagesBySearchInputLike("space")
    _, favourite_list = getAllImagesAndFavouriteList(request)
    return render(request, 'home.html', {'images': images, 'favourite_list': favourite_list} )


# función utilizada en el buscador.
def search(request):
    images, favourite_list = getAllImagesAndFavouriteList(request)
    search_msg = request.POST.get('query', '')
    # si el usuario no ingresó texto alguno, debe refrescar la página; caso contrario, debe filtrar aquellas imágenes que posean el texto de búsqueda.
    if (search_msg != ''):
        images_filtered =  services_nasa_image_gallery.getImagesBySearchInputLike(search_msg)
        return render (request, 'home.html',{'images': images_filtered, 'favourite_list': favourite_list} )
    else:
        images_filtered =  services_nasa_image_gallery.getImagesBySearchInputLike("space")
        return render (request, 'home.html',{'images': images_filtered, 'favourite_list': favourite_list} )
      

# las siguientes funciones se utilizan para implementar la sección de favoritos: traer los favoritos de un usuario, guardarlos, eliminarlos y desloguearse de la app.
@login_required
def getAllFavouritesByUser(request):
    favourite_list = services_nasa_image_gallery.getAllFavouritesByUser(request)
    return render(request, 'favourites.html', {'favourite_list': favourite_list})


@login_required
def saveFavourite(request):
    services_nasa_image_gallery.saveFavourite(request)
    return redirect('home')


@login_required
def deleteFavourite(request):
    services_nasa_image_gallery.deleteFavourite(request)
    return redirect('favoritos')


@login_required
def logout_user(request):
    logout(request)
    return redirect('login')

def exit(request):
    pass