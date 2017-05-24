from __future__ import unicode_literals, division, absolute_import, print_function, unicode_literals

from django.shortcuts import render, redirect
from django.urls import reverse
from urllib.request import urlopen, urlretrieve
from django.contrib import messages
from bs4 import BeautifulSoup

from aparcamientos.models import Aparcamiento


def parsear(query, tipo):
    if tipo == "localizacion":
        resultado = {"NOMBRE-VIA":None,
                        "CLASE-VIAL":None,
                        "TIPO-NUM":None,
                        "NUM":None,
                        "LOCALIDAD": None,
                        "PROVINCIA": None,
                        "CODIGO-POSTAL": -1,
                        "BARRIO":None,
                        "DISTRITO":None,
                        "COORDENADA-X": -1,
                        "COORDENADA-Y": -1,
                        "LATITUD": -1,
                        "LONGITUD": -1
                    }
    elif tipo == "contacto":
        resultado = {
            'TELEFONO': None,
            'EMAIL': None,
        }
    elif tipo == "atributos":
        resultado = {
            "ID-ENTIDAD":None,
            "NOMBRE":None,
            "DESCRIPCION":None,
            "ACCESIBILIDAD":None,
            "CONTENT-URL":None,
            "LOCALIZACION":None,
        }
    else:
        return {}
    datos = query.find_all('atributo')
    for clave1 in resultado:
        for dato in datos:
            if clave1 == dato['nombre']:
                resultado[clave1] = str(dato.string)
                if tipo == "localizacion":
                    if dato['nombre'] == "NOMBRE-VIA":
                        resultado[clave1] = resultado[clave1].replace("&Ntilde;", "Ñ")
                        resultado[clave1] = resultado[clave1].replace("&Uuml;", "Ü")
                    #if isinstance(resultado[clave1], str):
                        #resultado[clave1] = resultado[clave1].title()
    return resultado


def almacenar_aparcamiento(query):
    resultado = False
    if query != None:
        a = parsear(query, "atributos")
        try:
            aparcamiento = Aparcamiento.objects.get(identidad=a['ID-ENTIDAD'])
            return resultado
        except:
            pass
        for child in query.children:
            if child.name == "atributo":
                if child['nombre'] == "LOCALIZACION":
                    l = parsear(query, "localizacion")
                elif child['nombre'] == "DATOSCONTACTOS":
                    d = parsear(child, "contacto")
        aparcamiento = Aparcamiento.objects.create(
                    identidad=a['ID-ENTIDAD'],
                    nombre=a['NOMBRE'],
                    descripcion=a['DESCRIPCION'],
                    accesibilidad=int(a['ACCESIBILIDAD']),
                    url=a['CONTENT-URL'],
                    nombrevia = l['NOMBRE-VIA'],
                    clasevial = l['CLASE-VIAL'],
                    tiponum =  l['TIPO-NUM'],
                    numero = l['NUM'],
                    localidad = l['LOCALIDAD'],
                    provincia = l['PROVINCIA'],
                    cpostal = int(l['CODIGO-POSTAL']),
                    barrio = l['BARRIO'],
                    distrito = l['DISTRITO'],
                    x = int(l['COORDENADA-X']),
                    y = int(l['COORDENADA-Y']),
                    latitud = float(l['LATITUD']),
                    longitud = float(l['LONGITUD']),
                    email=d['EMAIL'],
                    telefono=d['TELEFONO']
                )
        resultado = True
    return resultado


def actualizar_aparcamientos(request):
    url = "http://datos.madrid.es/egob/catalogo/202584-0-aparcamientos-residentes.xml"
    try:
        soup = BeautifulSoup(urlopen(url).read(), "xml")
    except:
        soup = False
    if soup:
        todos = soup.find_all('contenido')
        if todos:
            aparcamientos = []
            existe = False
            num = 0
            for numero in range(len(todos)):
                for tag in todos[numero].children:
                    if tag.name == "atributos":
                        almacenar_aparcamiento(tag)
    else:
        messages.error(request, "No se han podido descargar ni actualizar los aparcamientos")
    return redirect(reverse('index'))

