from django.conf.urls import url

from . import views


app_name="aparcamientos"
urlpatterns = [
    url(r'^$', views.todos_view, {}, name="todos"),
    url(r'^buscar/$', views.buscar_view, name="buscar"),
    #url(r'^buscar/(?P<alojamiento_id>[-\w]+)$', views.detalle_view, name="buscar"),
    url(r'^crear_comentario/(?P<aparcamiento_identidad>[-\w]+)/$', views.crear_comentario, name='crear_comentario'),
    url(r'^seleccionar/(?P<aparcamiento_identidad>[-\w]+)/', views.seleccion, name="seleccion"),
    url(r'^likes/(?P<aparcamiento_identidad>[-\w]+)/$', views.likes, name="likes"),
    url(r'^(?P<aparcamiento_identidad>[-\w]+)/aparcamiento.json$', views.json, name='json'),
    url(r'^(?P<aparcamiento_identidad>[-\w]+)$', views.detalle_view, name='detalle'),
]