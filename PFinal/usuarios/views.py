from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth.models import User, Permission
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth import authenticate, login, logout
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core import serializers
from django.http import HttpResponse
from django.template import RequestContext
from django.template.loader import get_template

from .forms import RegistroUserForm, EditarEmailForm, EditarSizeForm, EditarTituloForm, EditarColorForm
from .models import PerfilUsuario
from aparcamientos.models import Aparcamiento, Comentario, Seleccion


# devuelve el estado inicial en el que deben encontrarse ciertas variables
def setup_vars(request, var):
    if var == 'actualizar':
        try:
            actualizar = False
            Aparcamiento.objects.all()[0]
        except:
            actualizar = True
        return actualizar
    if var == 'accesibles':
        accesibles = request.GET.get('accesibles')
        if accesibles == '1':
            accesibles = 1
        else:
            accesibles = 0
        return accesibles
    if var == 'busqueda':
        distrito = request.GET.get('distrito')
        return distrito


# Obtiene el color asignado por el usuario autentificado
def color_set(usuario):
    color = False
    try:
        usercolor = PerfilUsuario.objects.get(nombre=usuario)
        color = usercolor.color
    except:
        pass
    return color


# Obtiene el tamaño asignado por el usuario autentificado
def size_set(usuario):
    size = False
    try:
        usersize = PerfilUsuario.objects.get(nombre=usuario)
        size = usersize.size
    except:
        pass
    return size

# Comprueba si el usuario que realiza las peticiones es el mismo que el solicitado
def comprobar_usuario(request, usuario):
    mismo = False
    if request.user.username == usuario:
        mismo = True
    try:
        user = User.objects.get(username=usuario)
        user = PerfilUsuario.objects.get(user=user)
    except:
        user = False
    return (user, mismo)


# Página principal de cada usuario
# Agrega opciones según sea la página pública o privada
def index_view(request, usuario):
    (user, mismo) = comprobar_usuario(request, usuario)
    usercolor = color_set(request.user.username)
    usersize = size_set(request.user.username)
    paginator = False
    actualizar = setup_vars(request, "actualizar")
    accesibles = setup_vars(request, "accesibles")

    try:
        user = User.objects.get(username=usuario)
        usuario = PerfilUsuario.objects.get(user=user)
    except:
        user = False
        usuario= False
    if not actualizar:
        try:
            seleccionados = user.seleccion_usuario.all().order_by('-fecha')
            if accesibles == 1:
                accesibles = []
                for seleccion in seleccionados:
                    if seleccion.aparcamiento.accesibilidad == 1:
                        accesibles.append(seleccion)
                seleccionados = accesibles
            paginator = Paginator(seleccionados, 5)
            page = request.GET.get('page')
            seleccionados = paginator.page(page)
        except PageNotAnInteger:
            seleccionados = paginator.page(1)
        except EmptyPage:
            seleccionados = paginator.page(paginator.num_pages)
        except:
            seleccionados = False
    else:
        seleccionados = False

    try:
        if paginator.num_pages > 1:
            is_paginated = True
        else:
            is_paginated = False
    except:
        is_paginated = False

    context = {
        'actualizar': actualizar,
        'mismo': mismo,
        'usuario': usuario,
        'usercolor': usercolor,
        'usersize': usersize,
        'is_paginated': is_paginated,
        'paginator': paginator,
        'seleccionados': seleccionados,
        'accesibles':accesibles,
    }
    return render(request, 'usuarios/seleccionados.html', context)

"""
Registra a un nuevo usuario y le da permiso para comentar. Una vez registrado NO te loguea.
En caso de que su nickname sea "aparcamientos", "about" o que ya esté cogido,
o que el email ya esté asignado a otro usuario, muestra el error correspondiente
y termina el proceso
"""
def registro_view(request):
    if request.method == 'POST':
        form = RegistroUserForm(request.POST, request.FILES)
        if form.is_valid():
            cleaned_data = form.cleaned_data
            username = cleaned_data.get('username')
            if username != "aparcamientos" and username != "about":
                password = cleaned_data.get('password')
                email = cleaned_data.get('email')
                user_model = User.objects.create_user(username=username, password=password)
                # Permisos para agregar comentarios
                content_type = ContentType.objects.get_for_model(Comentario)
                permiso_comentar = Permission.objects.get(content_type=content_type, codename='add_comentario')
                user_model.user_permissions.add(permiso_comentar)
                user_model.email = email
                user_model.save()
                user_profile = PerfilUsuario(nombre=user_model.username)
                user_profile.user = user_model
                user_profile.save()
                return redirect(reverse('usuarios:gracias', kwargs={'usuario':username}))
            else:
                messages.error(request, "Nombre no permitido")
    else:
        form = RegistroUserForm
    context = {
        'form': form,
    }
    return render(request, 'usuarios/registro.html', context)

# Una vez registrado, renderiza un mensaje de agradecimiento al nuevo usuario
def gracias_view(request, usuario):
    context = {
        'mensaje': "Gracias por registrarte " + usuario
    }
    return render(request, 'usuarios/gracias.html', context)

# Logueo a un usuario
def login_view(request):
    # Si el usuario ya está logueado, lo redireccionamos a index_view
    if request.user.is_authenticated():
        user = request.user.username
        return redirect(reverse('main:index', kwargs={'usuario':user}))
    mensaje = ''
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            users = User.objects.all()
            # Cada vez que hago login compruebo que los superuser creados
            # tengan perfildeusuario (se podria mejorar para evitar que siempre
            # haga esta comprobación )
            for u in users:
                if u.is_superuser:
                    PerfilUsuario.objects.get_or_create(user=u, nombre=u.username)
            login(request, user)
            return redirect(reverse('index'))
        mensaje = 'Nombre de usuario o contraseña incorrecta'
    context = {
        'mensaje': mensaje,
    }
    return render(request, 'usuarios/login.html', context)


# Desconecto al usuario 
@login_required
def logout_view(request, usuario):
    logout(request)
    messages.success(request, usuario + ': has sido desconectado con exito.')
    return redirect(reverse('index'))


# INTERFAZ PRIVADA
# ----------------------------------------------------------------------------
@login_required
def editar_email(request, usuario):
    actualizar = setup_vars(request, "actualizar")

    if request.method == 'POST':
        form = EditarEmailForm(request.POST, request=request)
        if form.is_valid():
            request.user.email = form.cleaned_data['email']
            request.user.save()
            messages.success(request, "El email ha sido cambiado con éxito!.")
        direccion = "/" + request.user.username + "/"
        return redirect(direccion)
    else:
        form = EditarEmailForm(
            request=request,
            initial={'email': request.user.email}
            )
        (user, mismo) = comprobar_usuario(request, usuario)
        usercolor = color_set(request.user.username)
        usersize = size_set(request.user.username)
        context = {
            'actualizar': actualizar,
            'form': form,
            'usuario': user,
            'mismo': mismo,
            'usercolor': usercolor,
            'usersize': usersize,
        }
    return render(request, 'usuarios/editar_email.html', context)


@login_required
def editar_size(request, usuario):
    actualizar = setup_vars(request, "actualizar")

    if request.method == "POST":
        form = EditarSizeForm(request.POST, request=request)
        if form.is_valid():
            user = User.objects.get(username=request.user.username)
            user = PerfilUsuario.objects.get(user=user)
            user.size = form['size'].value()
            user.save()
            messages.success(request, "El tamaño ha sido modificado")
        direccion = "/" + request.user.username + "/"
        return redirect(direccion)
    else:
        form = EditarSizeForm(
            request=request
            )
        (user, mismo) = comprobar_usuario(request, usuario)
        usercolor = color_set(request.user.username)
        usersize = size_set(request.user.username)
        context = {
            'actualizar':actualizar,
            'form': form,
            'usuario': user,
            'mismo': mismo,
            'usercolor': usercolor,
            'usersize': usersize,
        }
        return render(request, 'usuarios/editar_size.html', context)


@login_required
def editar_titulo(request, usuario):
    actualizar = setup_vars(request, "actualizar")

    if request.method == "POST":
        form = EditarTituloForm(request.POST, request=request)
        if form.is_valid():
            user = User.objects.get(username=request.user.username)
            user = PerfilUsuario.objects.get(user=user)
            user.titulo = form['titulo'].value()
            user.save()
            messages.success(request, "El título de la página principal ha sido modificado.")
        direccion = "/" + request.user.username + "/"
        return redirect(direccion)
    else:
        form = EditarTituloForm(request=request)
        (user,mismo) = comprobar_usuario(request, usuario)
        usercolor = color_set(request.user.username)
        usersize = size_set(request.user.username)
        context = {
            'actualizar':actualizar,
            'form': form,
            'usuario': user,
            'mismo': mismo,
            'usercolor': usercolor,
            'usersize': usersize,
        }
        return render(request, 'usuarios/editar_titulo.html', context)


@login_required
def editar_color(request, usuario):
    actualizar = setup_vars(request, "actualizar")

    if request.method == "POST":
        form = EditarColorForm(request.POST, request=request)
        if form.is_valid():
            user = User.objects.get(username=request.user.username)
            user = PerfilUsuario.objects.get(user=user)
            user.color = form['color'].value()
            user.save()
            messages.success(request, "El color ha sido modificado. (si no es válido, por defecto se pondrá el blanco")
        direccion = "/" + request.user.username + "/"
        return redirect(direccion)
    else:
        form = EditarColorForm(
            request=request
        )
        (user, mismo) = comprobar_usuario(request, usuario)
        usercolor = color_set(request.user.username)
        usersize = size_set(request.user.username)
        context = {
            'actualizar':actualizar,
            'form':form,
            'usuario':user,
            'mismo': mismo,
            'usercolor': usercolor,
            'usersize': usersize,
        }
        return render(request, 'usuarios/editar_color.html', context)

def xml_view(request, usuario):
    usuario = User.objects.get(username=usuario)
    XML = []
    try:
        seleccionados = usuario.seleccion_usuario.all()
        for seleccionado in seleccionados:
            XML += [seleccionado.aparcamiento]
    except:
        XML = ""
    context = RequestContext(request, {"aparcamientos": XML})
    template = get_template("usuarios/XML.xml")

    return HttpResponse(template.render(context), content_type='application/xml')