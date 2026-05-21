
from django.contrib import admin

from .models import *


@admin.register(Carrera)
class CarreraAdmin(admin.ModelAdmin):

    list_display = (
        'nombre',
        'fecha',
        'hora',
        'estado',
        'tipo',
        'categoria'
    )

    list_filter = (
        'estado',
        'fecha',
        'tipo'
    )

    search_fields = (
        'nombre',
    )

@admin.register(Participante)
class ParticipanteAdmin(admin.ModelAdmin):

    list_display = (
        'id_participante',
        'caballo',
        'jinete',
        'peso_jinete',
        'carrera'
    )

    def peso_jinete(self, obj):
        return obj.jinete.peso

    peso_jinete.short_description = 'Peso jinete'


@admin.register(Resultado)
class ResultadoAdmin(admin.ModelAdmin):

    list_display = (
        'participante',
        'posicion',
        'distancia'
    )


admin.site.register(Usuario)
admin.site.register(Entrenador)
admin.site.register(Jinete)
admin.site.register(Caballo)
admin.site.register(Hipodromo)
admin.site.register(Pista)
admin.site.register(EstadoPista)
admin.site.register(TipoApuesta)
admin.site.register(Apuesta)

