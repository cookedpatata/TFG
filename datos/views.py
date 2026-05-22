from decimal import Decimal
import random
import re

from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Q
from django.db import connection

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
# HOME
# =========================================

def inicio(request):

    carreras = Carrera.objects.exclude(
        estado__iexact='finalizada'
    ).annotate(
        num_participantes=Count('participantes')
    )

    categoria = request.GET.get('categoria')
    distancia = request.GET.get('distancia')
    participantes = request.GET.get('participantes')
    hipodromo = request.GET.get('hipodromo')

    if categoria:

        carreras = carreras.filter(
            categoria=categoria
        )

    if distancia and '-' in distancia:

        minimo, maximo = distancia.split('-')

        carreras = carreras.filter(
            distancia__gte=minimo,
            distancia__lte=maximo
        )

    if participantes:

        carreras = carreras.filter(
            num_participantes__gte=participantes
        )

    if hipodromo:

        carreras = carreras.filter(
            id_hipodromo=hipodromo
        )

    carreras = carreras.order_by(
        'fecha',
        'hora'
    )[:10]

    categorias = Carrera.objects.values_list(
        'categoria',
        flat=True
    ).distinct()

    distancias = Carrera.objects.values_list(
        'distancia',
        flat=True
    ).distinct()

    hipodromos = Hipodromo.objects.all()

    top_usuarios_db = Usuario.objects.annotate(

        total_apostado=Coalesce(
            Sum('user__apuestas__cantidad'),
            Decimal('0.00')
        ),

        total_apuestas=Count('user__apuestas')

    ).order_by('-total_apostado')[:5]

    top_usuarios = []

    usuarios = Usuario.objects.all()

    for usuario in usuarios:

        apuestas_usuario = Apuesta.objects.filter(
            usuario=usuario.user
        )

        total_ganado = Decimal('0.00')

        for apuesta in apuestas_usuario:

            if apuesta.estado == 'ganada':

                total_ganado += (
                    apuesta.cantidad * apuesta.dividendo
                )

            elif apuesta.estado == 'perdida':

                total_ganado -= apuesta.cantidad

        iniciales = (
            usuario.user.username[:2]
        ).upper()

        top_usuarios.append({

            'nombre': usuario.user.username,

            'ganancias': total_ganado,

            'victorias': apuestas_usuario.filter(
                estado='ganada'
            ).count(),

            'iniciales': iniciales
        })

    top_usuarios = sorted(
        top_usuarios,
        key=lambda x: x['ganancias'],
        reverse=True
    )[:5]

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
            'top_jinetes': top_jinetes,
            'categorias': categorias,
            'distancias': distancias,
            'hipodromos': hipodromos
        }
    )


# =========================================
# REGISTER
# =========================================

def registro(request):

    # =========================================
    # REINICIAR SECUENCIAS
    # =========================================

    with connection.cursor() as cursor:

        # Tabla auth_user
        cursor.execute("""
            SELECT setval(
                'auth_user_id_seq',
                COALESCE(
                    (SELECT MAX(id) FROM auth_user),
                    1
                )
            );
        """)

        # Tabla participante
        cursor.execute("""
            SELECT setval(
                'participante_id_participante_seq',
                COALESCE(
                    (SELECT MAX(id_participante) FROM participante),
                    1
                )
            );
        """)

    if request.method == 'POST':

        username = request.POST['username'].strip()
        email = request.POST['email'].strip().lower()
        password = request.POST['password']
        apellidos = request.POST['apellidos'].strip()
        fecha_nac = request.POST['fecha_nac']
        dni = request.POST['dni'].strip().upper()

        errores = False

        if (
            len(password) < 8
            or not any(c.isupper() for c in password)
            or not any(c.isdigit() for c in password)
        ):

            messages.error(
                request,
                'Password must have at least 8 characters, one uppercase letter and one number'
            )

            errores = True

        if not re.match(
            r'^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$',
            email
        ):

            messages.error(
                request,
                'Invalid email'
            )

            errores = True

        if not re.match(
            r'^[0-9]{8}[A-Za-z]$',
            dni
        ):

            messages.error(
                request,
                'Invalid DNI'
            )

            errores = True

        if errores:
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
            'User created successfully'
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

        correo = request.POST['correo']
        password = request.POST['password']

        try:

            user_db = User.objects.get(
                email=correo
            )

            user = authenticate(
                request,
                username=user_db.username,
                password=password
            )

        except User.DoesNotExist:

            user = None

        if user is not None:

            login(request, user)

            if user.is_superuser:
                return redirect('panel_carreras')

            return redirect('perfil')

        messages.error(
            request,
            'Incorrect email or password'
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
# PROFILE
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

    total_ganado = Decimal('0.00')

    for apuesta in apuestas:

        if apuesta.dividendo:

            apuesta.ganancia = (
                apuesta.cantidad * apuesta.dividendo
            )

        else:

            apuesta.ganancia = apuesta.cantidad

        if apuesta.estado == 'ganada':

            total_ganado += (
                apuesta.cantidad * apuesta.dividendo
            )

        elif apuesta.estado == 'perdida':

            total_ganado -= apuesta.cantidad

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
            'total_ganado': total_ganado,
            'victorias': victorias
        }
    )


# =========================================
# RACE DETAIL
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

        participante.apuesta_usuario = Apuesta.objects.filter(
            participante=participante,
            usuario=request.user
        ).first()

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
# BET
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
                    'Invalid amount'
                )

            return redirect(
                'detalle_carrera',
                participante.carrera.id_carrera
            )

        perfil_usuario = request.user.perfil

        if perfil_usuario.saldo < cantidad:

            messages.error(
                request,
                'Insufficient balance'
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
            'Bet placed successfully'
        )

    return redirect(
        'detalle_carrera',
        participante.carrera.id_carrera
    )

# =========================================
# CANCEL BET
# =========================================

@login_required
def cancelar_apuesta(request, apuesta_id):

    apuesta = get_object_or_404(
        Apuesta,
        pk=apuesta_id,
        usuario=request.user
    )

    if apuesta.estado != 'pendiente':

        messages.error(
            request,
            'Only pending bets can be cancelled'
        )

        return redirect('perfil')

    perfil_usuario = request.user.perfil

    perfil_usuario.saldo += apuesta.cantidad

    perfil_usuario.save()

    apuesta.delete()

    messages.success(
        request,
        'Bet cancelled successfully'
    )

    return redirect('perfil')

# =========================================
# ADMIN PANEL
# =========================================

@staff_member_required
def panel_carreras(request):

    carreras = Carrera.objects.exclude(
        estado__iexact='finalizada'
    ).order_by(
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
# FINISH RACE
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

            # =========================================
            # VALIDAR RANGO
            # =========================================

            if posicion < 1 or posicion > participantes.count():

                messages.error(
                    request,
                    f'Positions must be between 1 and {participantes.count()}'
                )

                return redirect(
                    'finalizar_carrera',
                    carrera.id_carrera
                )

            # =========================================
            # VALIDAR REPETIDAS
            # =========================================

            if posicion in posiciones:

                messages.error(
                    request,
                    'There cannot be duplicate positions'
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

        # =========================================
        # CALCULAR DIVIDENDOS
        # =========================================

        total_apostado = Apuesta.objects.filter(
            participante__carrera=carrera
        ).aggregate(
            total=Coalesce(
                Sum('cantidad'),
                Decimal('0.00')
            )
        )['total']

        usuarios_distintos = Apuesta.objects.filter(
            participante__carrera=carrera
        ).values(
            'usuario'
        ).distinct().count()

        participantes_apostados = Apuesta.objects.filter(
            participante__carrera=carrera
        ).values(
            'participante'
        ).distinct().count()

        if (
            usuarios_distintos <= 1
            or participantes_apostados <= 1
        ):

            apuestas = Apuesta.objects.filter(
                participante__carrera=carrera
            )

            for apuesta in apuestas:

                perfil = apuesta.usuario.perfil

                perfil.saldo += apuesta.cantidad

                perfil.save()

                apuesta.estado = 'insuficiente'

                apuesta.dividendo = 1

                apuesta.save()

            carrera.estado = 'Finalizada'

            carrera.save()

            messages.warning(
                request,
                'Not enough valid bets'
            )

            return redirect('panel_carreras')

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

                dividendo = round(
                    float(total_apostado / total_participante),
                    2
                )

            else:

                dividendo = 0

            apuestas = Apuesta.objects.filter(
                participante=participante
            )

            resultado = Resultado.objects.get(
                participante=participante
            )

            for apuesta in apuestas:

                apuesta.dividendo = dividendo

                tipo = apuesta.tipo_apuesta.nombre.lower()

                ganada = False

                if tipo == 'ganador':

                    ganada = resultado.posicion == 1

                elif tipo == 'colocado':

                    ganada = resultado.posicion <= 3

                elif tipo == 'exacta':

                    ganada = resultado.posicion <= 2

                elif tipo == 'trifecta':

                    ganada = resultado.posicion <= 3

                elif tipo == 'quiniela':

                    ganada = resultado.posicion <= 2

                if ganada:

                    apuesta.estado = 'ganada'

                    ganancia = (
                        (apuesta.cantidad * Decimal(dividendo))
                        - apuesta.cantidad
                    )

                    perfil = apuesta.usuario.perfil

                    perfil.saldo += ganancia

                    perfil.save()

                else:

                    apuesta.estado = 'perdida'

                apuesta.save()

        carrera.estado = 'Finalizada'

        carrera.save()

        messages.success(
            request,
            'Race finished successfully'
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
# RANDOM RESULT
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
    
    # =========================================
    # CALCULAR DIVIDENDOS
    # =========================================

    total_apostado = Apuesta.objects.filter(
        participante__carrera=carrera
    ).aggregate(
        total=Coalesce(
            Sum('cantidad'),
            Decimal('0.00')
        )
    )['total']

    usuarios_distintos = Apuesta.objects.filter(
        participante__carrera=carrera
    ).values(
        'usuario'
    ).distinct().count()

    if usuarios_distintos <= 1:

        apuestas = Apuesta.objects.filter(
            participante__carrera=carrera
        )

        for apuesta in apuestas:

            perfil = apuesta.usuario.perfil

            perfil.saldo += apuesta.cantidad

            perfil.save()

            apuesta.estado = (
                'insuficiente'
            )

            apuesta.dividendo = 1

            apuesta.save()

        carrera.estado = 'Finalizada'

        carrera.save()

        messages.warning(
            request,
            'Not enough bettors'
        )

        return redirect('panel_carreras')

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

            dividendo = round(
                float(total_apostado / total_participante),
                2
            )

        else:

            dividendo = 0

        apuestas = Apuesta.objects.filter(
            participante=participante
        )

        resultado = Resultado.objects.get(
            participante=participante
        )

        for apuesta in apuestas:

            apuesta.dividendo = dividendo

            tipo = apuesta.tipo_apuesta.nombre.lower()

            ganada = False

            if tipo == 'ganador':

                ganada = resultado.posicion == 1

            elif tipo == 'colocado':

                ganada = resultado.posicion <= 3

            elif tipo == 'exacta':

                ganada = resultado.posicion <= 2

            elif tipo == 'trifecta':

                ganada = resultado.posicion <= 3

            elif tipo == 'quiniela':

                ganada = resultado.posicion <= 2

            if ganada:

                apuesta.estado = 'ganada'

                ganancia = (
                    (apuesta.cantidad * Decimal(dividendo))
                    - apuesta.cantidad
                )

                perfil = apuesta.usuario.perfil

                perfil.saldo += ganancia

                perfil.save()

            else:

                apuesta.estado = 'perdida'

            apuesta.save()

    carrera.estado = 'Finalizada'

    carrera.save()

    messages.success(
        request,
        'Random result generated'
    )

    return redirect('panel_carreras')

# =========================================
# RACE OPTIONS PANEL
# =========================================

@staff_member_required
def admin_detalle_carrera(request, carrera_id):

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

        participante.apuestas = Apuesta.objects.filter(
            participante=participante
        ).select_related(
            'usuario',
            'tipo_apuesta'
        )

    return render(
        request,
        'usuarios/admin_detalle_carrera.html',
        {
            'carrera': carrera,
            'participantes': participantes,
            'total_apostado': total_apostado
        }
    )

# =========================================
# GENERATE RANDOM BETS
# =========================================

@staff_member_required
def generar_apuestas(request, carrera_id):

    carrera = get_object_or_404(
        Carrera,
        pk=carrera_id
    )

    if request.method == 'POST':

        cantidad_apuestas = int(
            request.POST.get(
                'cantidad_apostantes',
                1
            )
        )

        participantes = list(
            Participante.objects.filter(
                carrera=carrera
            )
        )

        usuarios = list(
            User.objects.filter(
                is_superuser=False
            )
        )

        tipos_apuesta = list(
            TipoApuesta.objects.all()
        )

        if not participantes or not usuarios:

            messages.error(
                request,
                'No participants or users'
            )

            return redirect(
                'admin_detalle_carrera',
                carrera.id_carrera
            )

        apuestas_creadas = 0
        intentos = 0
        max_intentos = cantidad_apuestas * 20

        while (
            apuestas_creadas < cantidad_apuestas
            and intentos < max_intentos
        ):

            intentos += 1

            usuario = random.choice(
                usuarios
            )

            perfil = usuario.perfil

            # =====================================
            # PARTICIPANTES DISPONIBLES
            # =====================================

            participantes_disponibles = []

            for participante in participantes:

                existe = Apuesta.objects.filter(
                    usuario=usuario,
                    participante=participante,
                    estado='pendiente'
                ).exists()

                if not existe:

                    participantes_disponibles.append(
                        participante
                    )

            # Si ya apostó a todos
            if not participantes_disponibles:
                continue

            # =====================================
            # CANTIDAD ALEATORIA
            # =====================================

            max_apuesta = min(
                int(perfil.saldo),
                100
            )

            if max_apuesta < 5:
                continue

            cantidad = Decimal(
                random.randint(
                    5,
                    max_apuesta
                )
            )

            participante = random.choice(
                participantes_disponibles
            )

            tipo_apuesta = random.choice(
                tipos_apuesta
            )

            # =====================================
            # CREAR APUESTA
            # =====================================

            Apuesta.objects.create(

                cantidad=cantidad,

                tipo_apuesta=tipo_apuesta,

                usuario=usuario,

                participante=participante
            )

            perfil.saldo -= cantidad

            perfil.save()

            apuestas_creadas += 1

        messages.success(
            request,
            f'Added {apuestas_creadas} bets'
        )

    return redirect(
        'admin_detalle_carrera',
        carrera.id_carrera
    )

def caballos(request):

    buscar = request.GET.get('buscar')

    caballos = Caballo.objects.all()

    if buscar:

        caballos = caballos.filter(
            Q(nombre__icontains=buscar)
        )

    return render(
        request,
        'caballos.html',
        {
            'caballos': caballos
        }
    )


def jinetes(request):

    buscar = request.GET.get('buscar')

    jinetes = Jinete.objects.all()

    if buscar:

        jinetes = jinetes.filter(
            Q(nombre__icontains=buscar)
        )

    return render(
        request,
        'jinetes.html',
        {
            'jinetes': jinetes
        }
    )

# =========================================
# HORSE DETAIL
# =========================================

def detalle_caballo(request, caballo_id):

    caballo = get_object_or_404(
        Caballo,
        pk=caballo_id
    )

    participantes = Participante.objects.filter(
        caballo=caballo
    ).select_related(
        'carrera',
        'jinete'
    )

    victorias = 0
    derrotas = 0

    for participante in participantes:

        resultado = Resultado.objects.filter(
            participante=participante
        ).first()

        participante.resultado = resultado

        if resultado:

            if resultado.posicion == 1:

                victorias += 1

            else:

                derrotas += 1

    return render(
        request,
        'detalle_caballo.html',
        {
            'caballo': caballo,
            'participantes': participantes,
            'victorias': victorias,
            'derrotas': derrotas
        }
    )


# =========================================
# JOCKEY DETAIL
# =========================================

def detalle_jinete(request, jinete_id):

    jinete = get_object_or_404(
        Jinete,
        pk=jinete_id
    )

    participantes = Participante.objects.filter(
        jinete=jinete
    ).select_related(
        'carrera',
        'caballo'
    )

    victorias = 0
    derrotas = 0

    for participante in participantes:

        resultado = Resultado.objects.filter(
            participante=participante
        ).first()

        participante.resultado = resultado

        if resultado:

            if resultado.posicion == 1:

                victorias += 1

            else:

                derrotas += 1

    return render(
        request,
        'detalle_jinete.html',
        {
            'jinete': jinete,
            'participantes': participantes,
            'victorias': victorias,
            'derrotas': derrotas
        }
    )