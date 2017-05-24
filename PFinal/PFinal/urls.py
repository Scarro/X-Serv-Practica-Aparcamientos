from django.conf.urls import url, include
from django.contrib import admin
from . import views as main_views
from usuarios import views as usuario_views
from parseador import views as parseador_views

#app_name = "main"
urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^about/$', main_views.about, name="about"),
    url(r'^aparcamientos/', include('aparcamientos.urls')),
    url(r'registro/$', usuario_views.registro_view, name="registro"),
    url(r'login/$', usuario_views.login_view, name="login"),
    url(r'^parseador/', parseador_views.actualizar_aparcamientos, name="actualizar"),
    url(r'^(?P<usuario>[-\w]+)/', include('usuarios.urls')),
    url(r'^$', main_views.index_view, name='index'),
]
