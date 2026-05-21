from django.urls import path
from . import views

urlpatterns = [

    path('', views.inicio, name='index'),

    path('registro/', views.registro, name='registro'),

    path('login/', views.iniciar_sesion, name='login'),

    path('logout/', views.cerrar_sesion, name='logout'),

    path('perfil/', views.perfil, name='perfil'),

    path(
        'carrera/<int:carrera_id>/',
        views.detalle_carrera,
        name='detalle_carrera'
    ),

    path(
        'apostar/<int:participante_id>/',
        views.apostar,
        name='apostar'
    ),

    path(
        'panel-carreras/',
        views.panel_carreras,
        name='panel_carreras'
    ),

    path(
        'finalizar-carrera/<int:carrera_id>/',
        views.finalizar_carrera,
        name='finalizar_carrera'
    ),

    path(
        'resultado-aleatorio/<int:carrera_id>/',
        views.resultado_aleatorio,
        name='resultado_aleatorio'
    ),

    path(
        'caballos/',
        views.caballos,
        name='caballos'
    ),

    path(
        'jinetes/',
        views.jinetes
        , name='jinetes'
    ),
]