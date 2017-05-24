from django.conf.urls import url
from . import views

app_name = "usuarios"
urlpatterns = [
    url(r'^$', views.index_view, name="index"),
    url(r'^gracias/$', views.gracias_view, name="gracias"),
    url(r'^logout/$', views.logout_view, name="logout"),
    url(r'^editar_email/$', views.editar_email, name='editar_email'),
    url(r'^editar_color/$', views.editar_color, name='editar_color'),
    url(r'^editar_size/$', views.editar_size, name='editar_size'),
    url(r'^editar_titulo/$', views.editar_titulo, name='editar_titulo'),
    url(r'^xml/$', views.xml_view, name='xml')
]