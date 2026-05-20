from django.db import models
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User


# =========================================
# USUARIO
# =========================================

class Usuario(models.Model):

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='perfil'
    )

    apellidos = models.CharField(max_length=150)

    fecha_nac = models.DateField()

    dni = models.CharField(
        max_length=20,
        unique=True
    )

    saldo = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0
    )

    class Meta:
        db_table = 'usuario'

    def __str__(self):
        return self.user.username


# =========================================
# ENTRENADOR
# =========================================

class Entrenador(models.Model):
    id_entrenador = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)
    nacionalidad = models.CharField(max_length=100)

    class Meta:
        db_table = 'entrenador'

    def __str__(self):
        return self.nombre


# =========================================
# PROPIETARIO
# =========================================

class Propietario(models.Model):
    id_propietario = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)
    nacionalidad = models.CharField(max_length=100)
    equipamiento = models.CharField(max_length=150)

    class Meta:
        db_table = 'propietario'

    def __str__(self):
        return self.nombre


# =========================================
# JINETE
# =========================================

class Jinete(models.Model):
    id_jinete = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)
    nacionalidad = models.CharField(max_length=100)

    class Meta:
        db_table = 'jinete'

    def __str__(self):
        return self.nombre


# =========================================
# CABALLO
# =========================================

class Caballo(models.Model):
    id_caballo = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)
    nacionalidad = models.CharField(max_length=100)
    sexo = models.CharField(max_length=20)
    edad = models.IntegerField()

    entrenador = models.ForeignKey(
        Entrenador,
        on_delete=models.PROTECT,
        db_column='id_entrenador'
    )

    propietario = models.ForeignKey(
        Propietario,
        on_delete=models.PROTECT,
        db_column='id_propietario'
    )

    class Meta:
        db_table = 'caballo'

    def __str__(self):
        return self.nombre


# =========================================
# HIPODROMO
# =========================================

class Hipodromo(models.Model):
    id_hipodromo = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)
    direccion = models.CharField(max_length=200)

    class Meta:
        db_table = 'hipodromo'

    def __str__(self):
        return self.nombre


# =========================================
# PISTA
# =========================================

class Pista(models.Model):
    id_pista = models.AutoField(primary_key=True)
    tipo = models.CharField(max_length=100)

    class Meta:
        db_table = 'pista'

    def __str__(self):
        return self.tipo


# =========================================
# ESTADO PISTA
# =========================================

class EstadoPista(models.Model):
    id_estado_pista = models.AutoField(primary_key=True)
    tipo = models.CharField(max_length=100)

    class Meta:
        db_table = 'estado_pista'

    def __str__(self):
        return self.tipo


# =========================================
# CARRERA
# =========================================

class Carrera(models.Model):
    id_carrera = models.AutoField(primary_key=True)

    enlace = models.CharField(max_length=200)
    nombre = models.CharField(max_length=100)

    fecha = models.DateField()
    hora = models.TimeField()

    distancia = models.IntegerField()

    orden = models.IntegerField()

    estado = models.CharField(
        max_length=50,
        blank=True,
        null=True
    )

    id_hipodromo = models.ForeignKey(
        'Hipodromo',
        on_delete=models.RESTRICT,
        db_column='id_hipodromo'
    )

    id_pista = models.ForeignKey(
        'Pista',
        on_delete=models.RESTRICT,
        db_column='id_pista'
    )

    id_estado_pista = models.ForeignKey(
        'EstadoPista',
        on_delete=models.RESTRICT,
        db_column='id_estado_pista'
    )

    tipo = models.CharField(
        max_length=50,
        blank=True,
        null=True
    )

    categoria = models.CharField(
        max_length=50,
        blank=True,
        null=True
    )

    class Meta:
        db_table = 'carrera'

    def __str__(self):
        return self.nombre




# =========================================
# PARTICIPANTE
# =========================================

class Participante(models.Model):
    id_participante = models.AutoField(primary_key=True)

    caballo = models.ForeignKey(
        Caballo,
        on_delete=models.CASCADE,
        db_column='id_caballo',
        related_name='participantes'
    )

    carrera = models.ForeignKey(
        Carrera,
        on_delete=models.CASCADE,
        db_column='id_carrera',
        related_name='participantes'
    )

    jinete = models.ForeignKey(
        Jinete,
        on_delete=models.CASCADE,
        db_column='id_jinete',
        related_name='participantes'
    )

    numero_salida = models.IntegerField()

    retirado = models.BooleanField(default=False)

    peso = models.DecimalField(max_digits=5, decimal_places=2)

    def clean(self):

        if Participante.objects.filter(
            jinete=self.jinete,
            carrera=self.carrera
        ).exclude(pk=self.pk).exists():
            raise ValidationError(
                "Este jinete ya participa en esta carrera."
            )

        if Participante.objects.filter(
            caballo=self.caballo,
            carrera=self.carrera
        ).exclude(pk=self.pk).exists():
            raise ValidationError(
                "Este caballo ya participa en esta carrera."
            )

        if Participante.objects.filter(
            numero_salida=self.numero_salida,
            carrera=self.carrera
        ).exclude(pk=self.pk).exists():
            raise ValidationError(
                "Ese número de salida ya existe en la carrera."
            )

    class Meta:
        db_table = 'participante'

        constraints = [
            models.UniqueConstraint(
                fields=['jinete', 'carrera'],
                name='unique_jinete_carrera'
            ),

            models.UniqueConstraint(
                fields=['caballo', 'carrera'],
                name='unique_caballo_carrera'
            ),

            models.UniqueConstraint(
                fields=['numero_salida', 'carrera'],
                name='unique_salida_carrera'
            ),
        ]

    def __str__(self):
        return f"{self.caballo} - {self.carrera}"


# =========================================
# RESULTADO
# =========================================

class Resultado(models.Model):
    id_resultado = models.AutoField(primary_key=True)

    participante = models.OneToOneField(
        Participante,
        on_delete=models.CASCADE,
        db_column='id_participante'
    )

    posicion = models.IntegerField()
    duracion = models.TimeField()
    distancia = models.CharField(max_length=20)

    class Meta:
        db_table = 'resultado'

    def __str__(self):
        return f"{self.participante} - {self.posicion}"


# =========================================
# TIPO APUESTA
# =========================================

class TipoApuesta(models.Model):
    id_tipo_apuesta = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=50, unique=True)

    class Meta:
        db_table = 'tipos_apuesta'

    def __str__(self):
        return self.nombre


# =========================================
# APUESTA
# =========================================

class Apuesta(models.Model):
    id_apuesta = models.AutoField(primary_key=True)

    cantidad = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    tipo_apuesta = models.ForeignKey(
        TipoApuesta,
        on_delete=models.PROTECT,
        db_column='id_tipo_apuesta'
    )

    usuario = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        db_column='id_usuario',
        related_name='apuestas'
    )

    participante = models.ForeignKey(
        Participante,
        on_delete=models.CASCADE,
        db_column='id_participante'
    )

    class Meta:
        db_table = 'apuesta'

    def __str__(self):
        return f"Apuesta {self.id_apuesta}"