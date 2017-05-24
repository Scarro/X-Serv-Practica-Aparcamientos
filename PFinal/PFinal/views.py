from django.shortcuts import render
from django.db.models import Count
from usuarios.views import color_set, size_set
from django.template import RequestContext
from django.template.loader import get_template
from django.http import HttpResponse, JsonResponse
from django.core.serializers import serialize

from aparcamientos.models import Aparcamiento, Comentario, Seleccion
from usuarios.models import PerfilUsuario
from usuarios.views import setup_vars


def index_view(request):
    actualizar = setup_vars(request, "actualizar")
    accesibles = setup_vars(request, "accesibles")

    tipo = request.GET.get("archivo")

    if not actualizar:
        aparcamientos = Aparcamiento.objects.filter(comentario_aparcamiento__isnull=False)
        if request.GET.get('accesibles') == '1':
            accesibles = 1
            aparcamientos = aparcamientos.filter(accesibilidad=1)
        else:
            accesibles = 0
        aparcamientos = aparcamientos.annotate(num_comentarios= Count('comentario_aparcamiento'))
        aparcamientos = aparcamientos.order_by('-num_comentarios')[:5]
        # Si no hay aparcamientos con comentarios:
        if aparcamientos.count() == 0:
            aparcamientos = False
        if tipo == 'xml':
            context = RequestContext(request, {"aparcamientos": aparcamientos})
            template = get_template("usuarios/XML.xml")
            return HttpResponse(template.render(context), content_type='application/xml')
        elif tipo == 'json':
            data = serialize("json", aparcamientos)
            return JsonResponse(data, safe=False)
    else:
        aparcamientos = False

    try:
        usuarios = PerfilUsuario.objects.all()
    except:
        usuarios = False

    user_color = color_set(request.user.username)
    user_size = size_set(request.user.username)
    context = {
        'actualizar': actualizar,
        'aparcamientos':aparcamientos,
        'usuarios': usuarios,
        'usercolor':user_color,
        'usersize':user_size,
        'accesibles': accesibles,
    }
    return render(request, 'principal.html', context)

def about(request):
    user_color = color_set(request.user.username)
    user_size = size_set(request.user.username)
    context={
        'usercolor':user_color,
        'usersize':user_size,
    }
    template = "about.html"
    return render(request, template, context)