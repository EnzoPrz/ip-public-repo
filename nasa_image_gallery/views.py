# capa de vista/presentación
# si se necesita algún dato (lista, valor, etc), esta capa SIEMPRE se comunica con services_nasa_image_gallery.py

from django.shortcuts import redirect, render
from .layers.services import services_nasa_image_gallery
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
#from django.contrib.auth.forms import UserCreationForm

def register_view(request):
   # form= UserCreationForm()
    pass
    #return render(request,'accounts/register.html',{'form':form})

def login_user(request):
    if request.method == "POST":
        username= request.POST['username']
        password= request.POST['password']
        user= authenticate(request, username=username, password=password)
        if user is not None:
            login(request,user)
            return redirect ("home")
        else:
            messages.success(request,('Volve a intentar'))
            return redirect ("login")
    else:
        return render(request, 'login.html', {} )   

# función que invoca al template del índice de la aplicación.
def index_page(request):
    return render(request, 'index.html')

# auxiliar: retorna 2 listados -> uno de las imágenes de la API y otro de los favoritos del usuario.
def getAllImagesAndFavouriteList(request):
    images = []
    favourite_list = saveFavourite(request)
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
    favourite_list = []
    return render(request, 'favourites.html', {'favourite_list': favourite_list})


@login_required
def saveFavourite(request):
    pass


@login_required
def deleteFavourite(request):
    pass


@login_required
def logout_user(request):
    logout(request)
    return redirect('login')

def exit(request):
    pass