from decimal import Decimal
import random

from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

from django.db import models
from django.db.models import Count, Sum
from django.db.models.functions import Coalesce

from django.shortcuts import (
    render,
    redirect,
    get_object_or_404
)

from .models import *


# =========================================
# INICIO
# =========================================

def inicio(request):

    carreras = Carrera.objects.filter(
        estado__isnull=True
    ).annotate(
        num_participantes=Count('participantes')
    ).order_by('fecha', 'hora')[:10]

    # =========================================
    # TOP USUARIOS
    # =========================================

    top_usuarios_db = Usuario.objects.annotate(

        total_apostado=Coalesce(
            Sum('user__apuestas__cantidad'),
            Decimal('0.00')
        ),

        total_apuestas=Count('user__apuestas')

    ).order_by('-total_apostado')[:5]

    top_usuarios = []

    for usuario in top_usuarios_db:

        iniciales = (
            usuario.user.username[:2]
        ).upper()

        top_usuarios.append({

            'nombre': usuario.user.username,

            'ganancias': usuario.total_apostado,

            'victorias': usuario.total_apuestas,

            'iniciales': iniciales
        })

    # =========================================
    # TOP CABALLOS
    # =========================================

    top_caballos_db = Caballo.objects.annotate(

        carreras=Count('participantes'),

        victorias=Count(
            'participantes__resultado',
            filter=models.Q(
                participantes__resultado__posicion=1
            )
        )

    ).order_by('-victorias')[:5]

    top_caballos = []

    for caballo in top_caballos_db:

        porcentaje = 0

        if caballo.carreras > 0:

            porcentaje = int(
                (caballo.victorias / caballo.carreras) * 100
            )

        top_caballos.append({

            'nombre': caballo.nombre,

            'victorias': caballo.victorias,

            'carreras': caballo.carreras,

            'porcentaje': porcentaje
        })

    # =========================================
    # TOP JINETES
    # =========================================

    top_jinetes_db = Jinete.objects.annotate(

        victorias=Count(
            'participantes__resultado',
            filter=models.Q(
                participantes__resultado__posicion=1
            )
        ),

        carreras=Count('participantes')

    ).order_by('-victorias')[:5]

    top_jinetes = []

    for jinete in top_jinetes_db:

        efectividad = 0

        if jinete.carreras > 0:

            efectividad = int(
                (jinete.victorias / jinete.carreras) * 100
            )

        top_jinetes.append({

            'nombre': jinete.nombre,

            'victorias': jinete.victorias,

            'efectividad': efectividad
        })

    return render(
        request,
        'index.html',
        {
            'carreras': carreras,
            'top_usuarios': top_usuarios,
            'top_caballos': top_caballos,
            'top_jinetes': top_jinetes
        }
    )


# =========================================
# REGISTRO
# =========================================

def registro(request):

    if request.method == 'POST':

        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        apellidos = request.POST['apellidos']
        fecha_nac = request.POST['fecha_nac']
        dni = request.POST['dni']

        if User.objects.filter(
            username=username
        ).exists():

            messages.error(
                request,
                'El usuario ya existe'
            )

            return redirect('registro')

        if User.objects.filter(
            email=email
        ).exists():

            messages.error(
                request,
                'El correo ya existe'
            )

            return redirect('registro')

        if Usuario.objects.filter(
            dni=dni
        ).exists():

            messages.error(
                request,
                'El DNI ya existe'
            )

            return redirect('registro')

        user = User.objects.create_user(

            username=username,

            email=email,

            password=password
        )

        Usuario.objects.create(

            user=user,

            apellidos=apellidos,

            fecha_nac=fecha_nac,

            dni=dni,

            saldo=100
        )

        messages.success(
            request,
            'Usuario creado correctamente'
        )

        return redirect('login')

    return render(
        request,
        'registro.html'
    )


# =========================================
# LOGIN
# =========================================

def iniciar_sesion(request):

    if request.method == 'POST':

        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:

            login(request, user)

            if user.is_superuser:
                return redirect('panel_carreras')

            return redirect('index')

        messages.error(
            request,
            'Usuario o contraseña incorrectos'
        )

        return redirect('login')

    return render(
        request,
        'login.html'
    )


# =========================================
# LOGOUT
# =========================================

def cerrar_sesion(request):

    logout(request)

    return redirect('index')


# =========================================
# PERFIL
# =========================================

@login_required
def perfil(request):

    perfil_usuario, creado = Usuario.objects.get_or_create(

        user=request.user,

        defaults={

            'apellidos': 'Administrador',

            'fecha_nac': '2000-01-01',

            'dni': f'TEMP-{request.user.id}',

            'saldo': 100
        }
    )

    apuestas = Apuesta.objects.filter(
        usuario=request.user
    ).select_related(
        'participante__caballo',
        'participante__carrera'
    ).order_by('-id_apuesta')

    total_apostado = apuestas.aggregate(
        total=Coalesce(
            Sum('cantidad'),
            Decimal('0.00')
        )
    )['total']

    victorias = Resultado.objects.filter(
        posicion=1,
        participante__apuesta__usuario=request.user
    ).count()

    return render(
        request,
        'usuarios/perfil.html',
        {
            'perfil_usuario': perfil_usuario,
            'apuestas': apuestas,
            'total_apostado': total_apostado,
            'victorias': victorias
        }
    )


# =========================================
# DETALLE CARRERA
# =========================================

@login_required
def detalle_carrera(request, carrera_id):

    carrera = get_object_or_404(
        Carrera,
        pk=carrera_id
    )

    participantes = Participante.objects.filter(
        carrera=carrera
    ).select_related(
        'caballo',
        'jinete'
    )

    tipos_apuesta = TipoApuesta.objects.all()

    total_apostado = Apuesta.objects.filter(
        participante__carrera=carrera
    ).aggregate(
        total=Coalesce(
            Sum('cantidad'),
            Decimal('0.00')
        )
    )['total']

    for participante in participantes:

        total_participante = Apuesta.objects.filter(
            participante=participante
        ).aggregate(
            total=Coalesce(
                Sum('cantidad'),
                Decimal('0.00')
            )
        )['total']

        if total_participante > 0:

            participante.dividendo = round(
                float(total_apostado / total_participante),
                2
            )

        else:

            participante.dividendo = 0

    return render(
        request,
        'usuarios/detalle_carrera.html',
        {
            'carrera': carrera,
            'participantes': participantes,
            'tipos_apuesta': tipos_apuesta,
            'total_apostado': total_apostado
        }
    )


# =========================================
# APOSTAR
# =========================================

@login_required
def apostar(request, participante_id):

    participante = get_object_or_404(
        Participante,
        pk=participante_id
    )

    if request.method == 'POST':

        cantidad = Decimal(
            request.POST['cantidad']
        )

        if cantidad <= 0:

            messages.error(
                request,
                'Cantidad inválida'
            )

            return redirect(
                'detalle_carrera',
                participante.carrera.id_carrera
            )

        perfil_usuario = request.user.perfil

        if perfil_usuario.saldo < cantidad:

            messages.error(
                request,
                'Saldo insuficiente'
            )

            return redirect(
                'detalle_carrera',
                participante.carrera.id_carrera
            )

        tipo_apuesta = TipoApuesta.objects.get(
            pk=request.POST['tipo_apuesta']
        )

        Apuesta.objects.create(

            cantidad=cantidad,

            tipo_apuesta=tipo_apuesta,

            usuario=request.user,

            participante=participante
        )

        perfil_usuario.saldo -= cantidad

        perfil_usuario.save()

        messages.success(
            request,
            'Apuesta realizada correctamente'
        )

    return redirect(
        'detalle_carrera',
        participante.carrera.id_carrera
    )


# =========================================
# PANEL ADMIN
# =========================================

@staff_member_required
def panel_carreras(request):

    carreras = Carrera.objects.all().order_by(
        'fecha',
        'hora'
    )

    return render(
        request,
        'usuarios/admin_carreras.html',
        {
            'carreras': carreras
        }
    )


# =========================================
# FINALIZAR CARRERA
# =========================================

@staff_member_required
def finalizar_carrera(request, carrera_id):

    carrera = get_object_or_404(
        Carrera,
        pk=carrera_id
    )

    participantes = Participante.objects.filter(
        carrera=carrera
    ).select_related(
        'caballo'
    )

    if request.method == 'POST':

        posiciones = []

        for participante in participantes:

            posicion = int(
                request.POST.get(
                    f'posicion_{participante.id_participante}'
                )
            )

            if posicion in posiciones:

                messages.error(
                    request,
                    'No puede haber posiciones repetidas'
                )

                return redirect(
                    'finalizar_carrera',
                    carrera.id_carrera
                )

            posiciones.append(posicion)

        for participante in participantes:

            posicion = request.POST.get(
                f'posicion_{participante.id_participante}'
            )

            distancia = request.POST.get(
                f'distancia_{participante.id_participante}'
            )

            Resultado.objects.update_or_create(

                participante=participante,

                defaults={

                    'posicion': posicion,

                    'distancia': distancia,

                    'duracion': '00:00:00'
                }
            )

        carrera.estado = 'Finalizada'

        carrera.save()

        messages.success(
            request,
            'Carrera finalizada correctamente'
        )

        return redirect('panel_carreras')

    return render(
        request,
        'usuarios/finalizar_carrera.html',
        {
            'carrera': carrera,
            'participantes': participantes
        }
    )


# =========================================
# RESULTADO ALEATORIO
# =========================================

@staff_member_required
def resultado_aleatorio(request, carrera_id):

    carrera = get_object_or_404(
        Carrera,
        pk=carrera_id
    )

    participantes = list(
        Participante.objects.filter(
            carrera=carrera
        )
    )

    random.shuffle(participantes)

    for i, participante in enumerate(participantes):

        Resultado.objects.update_or_create(

            participante=participante,

            defaults={

                'posicion': i + 1,

                'distancia': f'{random.randint(1,20)} cuerpos',

                'duracion': '00:00:00'
            }
        )

    carrera.estado = 'Finalizada'

    carrera.save()

    messages.success(
        request,
        'Resultado aleatorio generado'
    )

    return redirect('panel_carreras')