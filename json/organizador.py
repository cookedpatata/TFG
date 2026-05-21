import json
import os
import re

# =====================================================
# CARGAR JSONS SI EXISTEN
# =====================================================

san_sebastian = []
zarzuela = []

if os.path.exists("datos_carreras_sansebastian.json"):

    with open(
        "datos_carreras_sansebastian.json",
        "r",
        encoding="utf-8"
    ) as f:

        san_sebastian = json.load(f)

    print("JSON San Sebastián cargado")

else:

    print("No existe datos_carreras_sansebastian.json")


if os.path.exists("datos_carreras_zarzuela.json"):

    with open(
        "datos_carreras_zarzuela.json",
        "r",
        encoding="utf-8"
    ) as f:

        zarzuela = json.load(f)

    print("JSON Zarzuela cargado")

else:

    print("No existe datos_carreras_zarzuela.json")

# =====================================================
# ESTRUCTURA FINAL
# =====================================================

bd = {
    "hipodromos": [],
    "pistas": [],
    "estado_pista": [],
    "carreras": [],
    "entrenadores": [],
    "jinetes": [],
    "propietarios": [],
    "caballos": [],
    "participantes": [],
    "resultados": []
}

# =====================================================
# SETS DUPLICADOS
# =====================================================

hipodromos_set = set()
pistas_set = set()
estado_set = set()

entrenadores_set = set()
jinetes_set = set()
propietarios_set = set()
caballos_set = set()

carreras_set = set()
participantes_set = set()

# =====================================================
# VALORES DESCONOCIDOS
# =====================================================

bd["pistas"].append({
    "tipo": "Desconocido"
})

bd["estado_pista"].append({
    "tipo": "Desconocido"
})

pistas_set.add("Desconocido")
estado_set.add("Desconocido")

# =====================================================
# UNIR CARRERAS
# =====================================================

todas_carreras = san_sebastian + zarzuela

# =====================================================
# COMPROBAR DATOS
# =====================================================

if len(todas_carreras) == 0:

    print("No hay carreras disponibles")

    exit()

# =====================================================
# RECORRER CARRERAS
# =====================================================

for carrera in todas_carreras:

    url_carrera = carrera.get(
        "url",
        ""
    ).strip()

    # ================================================
    # EVITAR CARRERAS DUPLICADAS
    # ================================================

    if not url_carrera:

        continue

    if url_carrera in carreras_set:

        continue

    carreras_set.add(url_carrera)

    # ================================================
    # DATOS GENERALES
    # ================================================

    hipodromo = (
        carrera.get(
            "hipodromo",
            "Desconocido"
        ) or "Desconocido"
    ).strip()

    pista = (
        carrera.get(
            "pista",
            "Desconocido"
        ) or "Desconocido"
    ).strip()

    estado_pista = (
        carrera.get(
            "estado_pista",
            "Desconocido"
        ) or "Desconocido"
    ).strip()

    participantes = carrera.get(
        "participantes",
        []
    )

    resultados = carrera.get(
        "resultados",
        []
    )

    # =================================================
    # LIMPIAR DISTANCIA
    # =================================================

    distancia_raw = str(
        carrera.get("distancia", "0")
    )

    distancia_numeros = "".join(
        c for c in distancia_raw
        if c.isdigit()
    )

    distancia = (
        int(distancia_numeros)
        if distancia_numeros
        else 0
    )

    # =================================================
    # LIMPIAR ORDEN
    # =================================================

    orden_raw = str(
        carrera.get("orden", "0")
    ).strip()

    match_orden = re.search(
        r"\d+",
        orden_raw
    )

    orden = (
        int(match_orden.group())
        if match_orden
        else 0
    )

    # =================================================
    # HIPODROMOS
    # =================================================

    if hipodromo not in hipodromos_set:

        hipodromos_set.add(hipodromo)

        bd["hipodromos"].append({
            "nombre": hipodromo,

            "direccion": (
                "Madrid"
                if "Zarzuela" in hipodromo
                else "San Sebastián"
            )
        })

    # =================================================
    # PISTAS
    # =================================================

    if pista not in pistas_set:

        pistas_set.add(pista)

        bd["pistas"].append({
            "tipo": pista
        })

    # =================================================
    # ESTADO PISTA
    # =================================================

    if estado_pista not in estado_set:

        estado_set.add(estado_pista)

        bd["estado_pista"].append({
            "tipo": estado_pista
        })

    # =================================================
    # CARRERA
    # =================================================

    bd["carreras"].append({

        "enlace": url_carrera,

        "nombre": carrera.get(
            "nombre",
            ""
        ),

        "fecha": carrera.get(
            "fecha",
            ""
        ),

        "hora": carrera.get(
            "hora",
            "00:00:00"
        ),

        "distancia": distancia,

        "orden": orden,

        "estado": (
            "Finalizada"
            if len(resultados) > 0
            else "Pendiente"
        ),

        "hipodromo": hipodromo,

        "pista": pista,

        "estado_pista": estado_pista,

        "tipo": carrera.get(
            "tipo",
            ""
        ),

        "categoria": carrera.get(
            "categoria",
            ""
        )
    })

    # =================================================
    # MAPA RESULTADOS
    # =================================================

    mapa_resultados = {}

    for resultado in resultados:

        caballo_resultado = resultado.get(
            "caballo",
            ""
        ).strip()

        if caballo_resultado:

            mapa_resultados[
                caballo_resultado
            ] = resultado

    # =================================================
    # PARTICIPANTES
    # =================================================

    for participante in participantes:

        caballo = participante.get(
            "caballo",
            ""
        ).strip()

        if not caballo:

            continue

        nacionalidad = participante.get(
            "nacionalidad",
            ""
        ).strip()

        entrenador = participante.get(
            "entrenador",
            ""
        ).strip()

        jinete = participante.get(
            "jinete",
            ""
        ).strip()

        propietario = participante.get(
            "propietario",
            ""
        ).strip()

        # =============================================
        # ENTRENADORES
        # =============================================

        if (
            entrenador and
            entrenador not in entrenadores_set
        ):

            entrenadores_set.add(
                entrenador
            )

            bd["entrenadores"].append({
                "nombre": entrenador,
                "nacionalidad": ""
            })

        # =============================================
        # JINETES
        # =============================================

        if (
            jinete and
            jinete not in jinetes_set
        ):

            jinetes_set.add(
                jinete
            )

            bd["jinetes"].append({
                "nombre": jinete,

                "peso": participante.get(
                    "peso"
                ),

                "nacionalidad": ""
            })

        # =============================================
        # PROPIETARIOS
        # =============================================

        if (
            propietario and
            propietario not in propietarios_set
        ):

            propietarios_set.add(
                propietario
            )

            bd["propietarios"].append({

                "nombre": propietario,

                "nacionalidad": "",

                "equipamiento": ""
            })

        # =============================================
        # CABALLOS
        # =============================================

        if caballo not in caballos_set:

            caballos_set.add(
                caballo
            )

            bd["caballos"].append({

                "nombre": caballo,

                "nacionalidad": nacionalidad,

                "sexo": participante.get(
                    "sexo",
                    ""
                ),

                "edad": participante.get(
                    "edad"
                ),

                "entrenador": entrenador,

                "propietario": propietario
            })

        # =============================================
        # PARTICIPANTE
        # =============================================

        clave_participante = (
            caballo,
            url_carrera,
            jinete
        )

        if (
            clave_participante
            in participantes_set
        ):

            continue

        participantes_set.add(
            clave_participante
        )

        participante_final = {

            "caballo": caballo,

            "carrera": url_carrera,

            "jinete": jinete,

            "numero_salida": participante.get(
                "numero",
                0
            ),

            "retirado": participante.get(
                "retirado",
                False
            )
        }

        bd["participantes"].append(
            participante_final
        )

        # =============================================
        # RESULTADOS
        # =============================================

        resultado = mapa_resultados.get(
            caballo
        )

        if resultado:

            bd["resultados"].append({

                "carrera": url_carrera,

                "caballo": caballo,

                "posicion": resultado.get(
                    "posicion",
                    0
                ),

                "duracion": resultado.get(
                    "duracion",
                    "00:00:00"
                ),

                "distancia": resultado.get(
                    "distancia",
                    ""
                )
            })

# =====================================================
# GUARDAR JSON
# =====================================================

with open(
    "bd_reorganizada.json",
    "w",
    encoding="utf-8"
) as f:

    json.dump(
        bd,
        f,
        ensure_ascii=False,
        indent=4
    )

print("JSON reorganizado correctamente")