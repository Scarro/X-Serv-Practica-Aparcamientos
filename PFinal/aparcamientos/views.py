from django.shortcuts import render, redirect
from django.urls import reverse
from usuarios.views import color_set, size_set
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.decorators import login_required
from django.core.serializers import serialize
from django.http import JsonResponse, HttpResponse
from usuarios.views import setup_vars

from django.contrib.auth.models import User
from usuarios.models import PerfilUsuario
from .models import Aparcamiento, Comentario, Seleccion
from .forms import ComentarioCreateForm


# Pagina principal donde se muestran todos los aparcamientos
# así como un formulario para filtrarlos
def todos_view(request):
    actualizar = setup_vars(request, "actualizar")
    accesibles = setup_vars(request, "accesibles")
    distrito = setup_vars(request, "busqueda")

    is_paginated = False
    paginator = False

    if not actualizar:
        if accesibles == 1:
            aparcamientos = Aparcamiento.objects.filter(accesibilidad=1)
        else:
            aparcamientos = Aparcamiento.objects.all()

        paginator = Paginator(aparcamientos,10)
        page = request.GET.get('page')
        try:
            aparcamientos = paginator.page(page)
        except PageNotAnInteger:
            aparcamientos = paginator.page(1)
        except EmptyPage:
            aparcamientos = paginator.page(paginator.num_page)

        if paginator.num_pages > 1:
            is_paginated = True
        else:
            is_paginated = False
    else:
        aparcamientos = False

    distritos = list(set(Aparcamiento.objects.values_list('distrito',flat=True)))
    try:
        distritos.remove(None)
    except Exception as e:
        print(e)

    template = "aparcamientos/todos.html"

    context = {
        'actualizar': actualizar,
        'buscador': "si",
        'distritos': distritos,
        'usersize': size_set(request.user.username),
        'usercolor': color_set(request.user.username),
        'nombre_btn': 'Filtrar',
        'aparcamientos': aparcamientos,
        'accesibles':accesibles,
        'is_paginated': is_paginated,
        'paginator': paginator,
        'distrito':distrito,
    }
    return render(request, template, context)


# Muestra la información detallada de cada aparcamiento
def detalle_view(request, aparcamiento_identidad):
    actualizar = setup_vars(request, "actualizar")

    try:
        aparcamiento = Aparcamiento.objects.get(identidad=aparcamiento_identidad)
    except:
        return redirect(reverse('aparcamientos:todos'))
    try:
        comentarios = aparcamiento.comentario_aparcamiento.all().order_by('-creado')
    except:
        comentarios = False
    try:
        usuario = User.objects.get(username=request.user.username)
        u = usuario.seleccion_usuario.get(aparcamiento=aparcamiento)
        seleccionado = True
    except:
        seleccionado = False

    localizacion = False
    contacto = False
    if aparcamiento.latitud and aparcamiento.latitud:
        localizacion = True
    if aparcamiento.email or aparcamiento.telefono:
        contacto = True
    url = False
    if aparcamiento.url:
        url=True

    usercolor = color_set(request.user.username)
    usersize = size_set(request.user.username)
    try:
        liked = request.session[aparcamiento_identidad]
    except:
        liked = False
    context = {
        'detalle': True,
        'url': url,
        'liked': liked,
        'actualizar': actualizar,
        'aparcamiento': aparcamiento,
        'comentarios': comentarios,
        'usercolor': usercolor,
        'usersize': usersize,
        'seleccionado': seleccionado,
        'localizacion': localizacion,
        'contacto': contacto,
    }
    return render(request, 'aparcamientos/detalle.html', context)


# Devuelve los aparcamientos filtrados por distrito
def buscar_view(request):
    actualizar = setup_vars(request, "actualizar")
    accesibles = setup_vars(request, "accesibles")

    aparcamientos = []
    if request.method == "POST":
        distrito = request.POST.get('Distrito')
    else:
        distrito = request.GET.get('distrito')
    if accesibles == 1:
        aparcamientos = Aparcamiento.objects.filter(distrito=distrito, accesibilidad=1)
    else:
        aparcamientos = Aparcamiento.objects.filter(distrito=distrito)
    usercolor = color_set(request.user.username)
    usersize = size_set(request.user.username)
    context = {
        'actualizar':actualizar,
        'distrito': distrito,
        'aparcamientos': aparcamientos,
        'usercolor': usercolor,
        'usersize': usersize,
        'accesibles': accesibles,
    }
    return render(request, 'aparcamientos/todos.html', context)


# Permite la creación de comentarios si estás logueado
@login_required
def crear_comentario(request, aparcamiento_identidad):
    form = ComentarioCreateForm
    if request.method == "POST":
        form = ComentarioCreateForm(request.POST, request.FILES)
        if form.is_valid():
            cleaned_data = form.cleaned_data
            user=User.objects.get(username=request.user.username)
            aparcamiento = Aparcamiento.objects.get(identidad=aparcamiento_identidad)
            titulo = cleaned_data.get('titulo')
            cuerpo = cleaned_data.get('cuerpo')
            comentario = Comentario.objects.create(usuario=user, aparcamiento=aparcamiento, titulo = titulo, cuerpo=cuerpo)
            return redirect(reverse('aparcamientos:detalle', args=[aparcamiento_identidad]))
    template = 'aparcamientos/comentario_form.html'
    usercolor = color_set(request.user.username)
    usersize = size_set(request.user.username)
    context = {
        'titulo': "Crear Comentario",
        'nombre_btn': "Crear",
        'form': form,
        'usercolor': usercolor,
        'usersize': usersize,
    }
    return render(request, template, context)

# Permite seleccionar un aparcamiento si estás logueado
@login_required
def seleccion(request, aparcamiento_identidad):
    try:
        accion = request.GET.get('seleccion')
        aparcamiento = Aparcamiento.objects.get(identidad=aparcamiento_identidad)
        nombre = request.user.username
        usuario = User.objects.get(username=nombre)
        if accion == 'anular':
            seleccion = Seleccion.objects.filter(usuario=usuario, aparcamiento=aparcamiento)
            seleccion.delete()
        else:
            seleccion = Seleccion.objects.create(usuario=usuario, aparcamiento=aparcamiento)
    except:
        pass
    return redirect(reverse('aparcamientos:detalle', args=[aparcamiento_identidad]))

# Permite darle a like a un aparcamiento
def likes(request, aparcamiento_identidad):
    try:
        aparcamiento = Aparcamiento.objects.get(identidad=aparcamiento_identidad)
    except:
        aparcarcamiento = None
    if aparcamiento:
        aparcamiento.likes = aparcamiento.likes+1
        aparcamiento.save()
        like = True
        request.session[aparcamiento_identidad] = True
    return redirect(reverse('aparcamientos:detalle', args=[aparcamiento_identidad]))

def json(request, aparcamiento_identidad):
    aparcamiento = Aparcamiento.objects.filter(identidad=aparcamiento_identidad)
    data = serialize("json", aparcamiento)
    return JsonResponse(data, safe=False)