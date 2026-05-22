import json
import psycopg2
import sys

# =========================
# CONFIGURACIÓN BD
# =========================

DB_CONFIG = {
    "host": "localhost",
    "database": "TFG",
    "user": "postgres",
    "password": "1234",
    "port": 5432
}

JSON_FILE = "bd_reorganizada.json"

# =========================
# MENÚ CMD
# =========================

print("""
=========================
¿QUÉ QUIERES INSERTAR?
=========================

1. Entrenadores
2. Jinetes
3. Propietarios
4. Caballos
5. Carreras
6. Participantes
7. Resultados
8. Todo
""")

opcion = input("Selecciona una opción: ")

# =========================
# CONEXIÓN
# =========================

conn = psycopg2.connect(**DB_CONFIG)
cursor = conn.cursor()

# =========================
# CARGAR JSON
# =========================

with open(JSON_FILE, "r", encoding="utf-8") as f:
    data = json.load(f)

# =========================================================
# FUNCIONES AUXILIARES
# =========================================================

def obtener_mapa(
    tabla,
    id_col,
    nombre_col
):

    cursor.execute(f"""
        SELECT {id_col}, {nombre_col}
        FROM {tabla}
    """)

    return {
        nombre: id_
        for id_, nombre in cursor.fetchall()
    }


def insertar_simple(
    tabla,
    columnas,
    valores,
    unique_col=None
):

    cols_sql = ", ".join(columnas)

    placeholders = ", ".join(
        ["%s"] * len(columnas)
    )

    if unique_col:

        sql = f"""
            INSERT INTO {tabla} ({cols_sql})
            VALUES ({placeholders})

            ON CONFLICT ({unique_col})
            DO NOTHING
        """

    else:

        sql = f"""
            INSERT INTO {tabla} ({cols_sql})
            VALUES ({placeholders})
        """

    cursor.execute(sql, valores)

# =========================================================
# 1. ENTRENADORES
# =========================================================

if opcion == "1" or opcion == "8":

    print("Insertando entrenadores...")

    for e in data.get("entrenadores", []):

        insertar_simple(
            "entrenador",
            [
                "nombre",
                "nacionalidad"
            ],
            [
                e.get("nombre"),
                e.get("nacionalidad")
            ],
            unique_col="nombre"
        )

    conn.commit()

entrenadores_map = obtener_mapa(
    "entrenador",
    "id_entrenador",
    "nombre"
)

# =========================================================
# 2. JINETES
# =========================================================

if opcion == "2" or opcion == "8":

    print("Insertando jinetes...")

    for j in data.get("jinetes", []):

        insertar_simple(
            "jinete",
            [
                "nombre",
                "peso",
                "nacionalidad"
            ],
            [
                j.get("nombre"),
                j.get("peso"),
                j.get("nacionalidad")
            ],
            unique_col="nombre"
        )

    conn.commit()

jinetes_map = obtener_mapa(
    "jinete",
    "id_jinete",
    "nombre"
)

# =========================================================
# 3. PROPIETARIOS
# =========================================================

if opcion == "3" or opcion == "8":

    print("Insertando propietarios...")

    for p in data.get("propietarios", []):

        insertar_simple(
            "propietario",
            [
                "nombre",
                "nacionalidad",
                "equipamiento"
            ],
            [
                p.get("nombre"),
                p.get("nacionalidad"),
                p.get("equipamiento")
            ],
            unique_col="nombre"
        )

    conn.commit()

propietarios_map = obtener_mapa(
    "propietario",
    "id_propietario",
    "nombre"
)

# =========================================================
# 4. CABALLOS
# =========================================================

if opcion == "4" or opcion == "8":

    print("Insertando caballos...")

    for c in data.get("caballos", []):

        id_entrenador = None
        id_propietario = None

        if c.get("entrenador"):

            id_entrenador = entrenadores_map.get(
                c.get("entrenador")
            )

        if c.get("propietario"):

            id_propietario = propietarios_map.get(
                c.get("propietario")
            )

        insertar_simple(
            "caballo",
            [
                "nombre",
                "nacionalidad",
                "sexo",
                "edad",
                "id_entrenador",
                "id_propietario"
            ],
            [
                c.get("nombre"),
                c.get("nacionalidad"),
                c.get("sexo"),
                c.get("edad"),
                id_entrenador,
                id_propietario
            ],
            unique_col="nombre"
        )

    conn.commit()

caballos_map = obtener_mapa(
    "caballo",
    "id_caballo",
    "nombre"
)

# =========================================================
# 5. CARRERAS
# =========================================================

if opcion == "5" or opcion == "8":

    print("Insertando carreras...")

    cursor.execute("""
        SELECT id_hipodromo, nombre
        FROM hipodromo
    """)

    hipodromos_map = {
        nombre: id_
        for id_, nombre in cursor.fetchall()
    }

    cursor.execute("""
        SELECT id_pista, tipo
        FROM pista
    """)

    pistas_map = {}

    for id_, tipo in cursor.fetchall():

        tipo = tipo.strip().upper()

        pistas_map[tipo] = id_

        if tipo == "HIERBA":
            pistas_map["H"] = id_

        elif tipo == "ARENA":
            pistas_map["A"] = id_

    cursor.execute("""
        SELECT id_estado_pista, tipo
        FROM estado_pista
    """)

    estado_pista_map = {
        tipo: id_
        for id_, tipo in cursor.fetchall()
    }

    for c in data.get("carreras", []):

        id_hipodromo = hipodromos_map.get(
            c.get("hipodromo")
        )

        id_pista = pistas_map.get(
            str(
                c.get("pista", "")
            ).strip().upper()
        )

        id_estado_pista = estado_pista_map.get(
            c.get("estado_pista")
        )

        sql = """
            INSERT INTO carrera (
                enlace,
                nombre,
                fecha,
                hora,
                distancia,
                orden,
                estado,
                id_hipodromo,
                id_pista,
                id_estado_pista,
                tipo,
                categoria
            )

            VALUES (
                %s,%s,%s,%s,%s,%s,
                %s,%s,%s,%s,%s,%s
            )

            ON CONFLICT (enlace)
            DO NOTHING
        """

        valores = (
            c.get("enlace"),
            c.get("nombre"),
            c.get("fecha"),
            c.get("hora"),
            c.get("distancia"),
            c.get("orden"),
            c.get("estado"),
            id_hipodromo,
            id_pista,
            id_estado_pista,
            c.get("tipo"),
            c.get("categoria")
        )

        cursor.execute(sql, valores)

    conn.commit()

# =========================================================
# MAPA CARRERAS
# =========================================================

cursor.execute("""
    SELECT
        id_carrera,
        enlace
    FROM carrera
""")

carreras_map = {

    enlace: id_

    for id_, enlace
    in cursor.fetchall()
}

# =========================================================
# 6. PARTICIPANTES
# =========================================================

if opcion == "6" or opcion == "8":

    print("Insertando participantes...")

    for p in data.get("participantes", []):

        id_caballo = caballos_map.get(
            p.get("caballo")
        )

        id_jinete = jinetes_map.get(
            p.get("jinete")
        )

        id_carrera = carreras_map.get(
            p.get("carrera")
        )

        if (
            not id_caballo or
            not id_jinete or
            not id_carrera
        ):
            continue

        sql = """
            INSERT INTO participante (
                id_caballo,
                id_carrera,
                id_jinete,
                numero_salida,
                retirado
            )

            VALUES (%s,%s,%s,%s,%s)

            ON CONFLICT ON CONSTRAINT unique_caballo_carrera
            DO NOTHING
        """

        valores = (
            id_caballo,
            id_carrera,
            id_jinete,
            p.get("numero_salida"),
            p.get("retirado")
        )

        cursor.execute(sql, valores)

    conn.commit()

# =========================================================
# 7. RESULTADOS
# =========================================================

if opcion == "7" or opcion == "8":

    print("Insertando resultados...")

    for r in data.get("resultados", []):

        id_caballo = caballos_map.get(
            r.get("caballo")
        )

        id_carrera = carreras_map.get(
            r.get("carrera")
        )

        if (
            not id_caballo or
            not id_carrera
        ):
            continue

        cursor.execute("""
            SELECT id_participante
            FROM participante
            WHERE id_caballo = %s
            AND id_carrera = %s
        """, (
            id_caballo,
            id_carrera
        ))

        participante = cursor.fetchone()

        if not participante:
            continue

        id_participante = participante[0]

        sql = """
            INSERT INTO resultado (
                id_participante,
                posicion,
                duracion,
                distancia
            )

            VALUES (%s,%s,%s,%s)

            ON CONFLICT (id_participante)
            DO NOTHING
        """

        valores = (
            id_participante,
            r.get("posicion"),
            r.get("duracion"),
            r.get("distancia")
        )

        cursor.execute(sql, valores)

    conn.commit()

# =========================================================
# FINALIZAR
# =========================================================

cursor.close()
conn.close()

print("Importación completada correctamente.")