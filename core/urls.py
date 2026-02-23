from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("noticia/<slug:slug>/", views.noticia_detalhe, name="noticia_detalhe"),

    # ✅ NOVO
    path("buscar/", views.buscar, name="buscar"),
]
