import json
from datetime import datetime

# =====================================================
# CARGAR JSONS
# =====================================================

with open("datos_carreras_sansebastian.json", "r", encoding="utf-8") as f:
    san_sebastian = json.load(f)

with open("datos_carreras_zarzuela.json", "r", encoding="utf-8") as f:
    zarzuela = json.load(f)

# =====================================================
# ESTRUCTURA FINAL SEGÚN LA BD
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
# SETS PARA EVITAR DUPLICADOS
# =====================================================

hipodromos_set = set()
pistas_set = set()
estados_set = set()
entrenadores_set = set()
jinetes_set = set()
propietarios_set = set()
caballos_set = set()

# =====================================================
# IDS TEMPORALES
# =====================================================

id_carrera = 1
id_participante = 1

# =====================================================
# FUNCIONES AUXILIARES
# =====================================================

def agregar_unico(tabla, conjunto, valor, datos):

    if valor and valor not in conjunto:
        conjunto.add(valor)
        tabla.append(datos)

# =====================================================
# SAN SEBASTIÁN
# =====================================================

for carrera in san_sebastian:

    datos_carrera = carrera.get("datos_carrera", {})

    hipodromo_nombre = "Hipódromo de San Sebastián"
    pista = datos_carrera.get("Pista", "")
    estado = datos_carrera.get("Estado", "")

    # =================================================
    # HIPODROMO
    # =================================================

    agregar_unico(
        bd["hipodromos"],
        hipodromos_set,
        hipodromo_nombre,
        {
            "nombre": hipodromo_nombre,
            "direccion": "San Sebastián"
        }
    )

    # =================================================
    # PISTA
    # =================================================

    agregar_unico(
        bd["pistas"],
        pistas_set,
        pista,
        {
            "tipo": pista
        }
    )

    # =================================================
    # ESTADO PISTA
    # =================================================

    agregar_unico(
        bd["estado_pista"],
        estados_set,
        estado,
        {
            "tipo": estado
        }
    )

    # =================================================
    # FORMATEAR FECHA
    # =================================================

    fecha = carrera.get("fecha", "")

    try:
        fecha = datetime.strptime(fecha, "%Y%m%d").strftime("%Y-%m-%d")
    except:
        pass

    participantes = carrera.get("tabla_participantes", [])
    resultados = carrera.get("tabla_resultados", [])

    # =================================================
    # CARRERA
    # =================================================

    bd["carreras"].append({
        "id_carrera": id_carrera,
        "enlace": carrera.get("url", ""),
        "nombre": carrera.get("nombre", ""),
        "fecha": fecha,
        "hora": datos_carrera.get("Hora", ""),
        "distancia": datos_carrera.get("Distancia", ""),
        "tipo": datos_carrera.get("Tipo", ""),
        "categoria": datos_carrera.get("Categoría", ""),
        "orden": id_carrera,
        "estado": "Finalizada" if len(resultados) > 0 else "Pendiente",
        "hipodromo": hipodromo_nombre,
        "pista": pista,
        "estado_pista": estado
    })

    # =================================================
    # MAPA RESULTADOS
    # =================================================

    mapa_resultados = {}

    for resultado in resultados:

        nombre_caballo = resultado.get("caballo", "")

        mapa_resultados[nombre_caballo] = resultado

    # =================================================
    # PARTICIPANTES
    # =================================================

    for participante in participantes:

        caballo = participante.get("caballo", "")
        nacionalidad = participante.get("nacionalidad", "")
        entrenador = participante.get("Entrenador", "")
        jinete = participante.get("jockey", "")
        propietario = participante.get("Propietario", "")

        # =============================================
        # ENTRENADOR
        # =============================================

        agregar_unico(
            bd["entrenadores"],
            entrenadores_set,
            entrenador,
            {
                "nombre": entrenador,
                "nacionalidad": ""
            }
        )

        # =============================================
        # JINETE
        # =============================================

        agregar_unico(
            bd["jinetes"],
            jinetes_set,
            jinete,
            {
                "nombre": jinete,
                "peso": None,
                "nacionalidad": ""
            }
        )

        # =============================================
        # PROPIETARIO
        # =============================================

        agregar_unico(
            bd["propietarios"],
            propietarios_set,
            propietario,
            {
                "nombre": propietario,
                "nacionalidad": "",
                "equipamiento": ""
            }
        )

        # =============================================
        # CABALLO
        # =============================================

        agregar_unico(
            bd["caballos"],
            caballos_set,
            caballo,
            {
                "nombre": caballo,
                "nacionalidad": nacionalidad,
                "sexo": participante.get("sexo", ""),
                "edad": participante.get("edad", ""),
                "propietario": propietario,
                "entrenador": entrenador
            }
        )

        # =============================================
        # PARTICIPANTE
        # =============================================

        bd["participantes"].append({
            "id_participante": id_participante,
            "numero_salida": participante.get("numero", ""),
            "caballo": caballo,
            "jinete": jinete,
            "carrera": id_carrera,
            "retirado": False
        })

        # =============================================
        # RESULTADO
        # =============================================

        resultado = mapa_resultados.get(caballo)

        if resultado:

            bd["resultados"].append({
                "participante": id_participante,
                "posicion": resultado.get("posicion", ""),
                "duracion": "00:00:00",
                "distancia": resultado.get("Distancia", "")
            })

        id_participante += 1

    id_carrera += 1

# =====================================================
# ZARZUELA
# =====================================================

for fecha in zarzuela:

    carreras = fecha.get("carreras", [])

    for carrera in carreras:

        hipodromo_nombre = "Hipódromo de la Zarzuela"

        agregar_unico(
            bd["hipodromos"],
            hipodromos_set,
            hipodromo_nombre,
            {
                "nombre": hipodromo_nombre,
                "direccion": "Madrid"
            }
        )

        resultados = carrera.get("resultados", [])
        participantes = carrera.get("participantes", [])

        # =================================================
        # CARRERA
        # =================================================

        bd["carreras"].append({
            "id_carrera": id_carrera,
            "enlace": carrera.get("url", ""),
            "nombre": carrera.get("nombre", ""),
            "fecha": carrera.get("fecha", ""),
            "hora": carrera.get("hora", ""),
            "distancia": carrera.get("distancia", ""),
            "tipo": carrera.get("tipo", ""),
            "categoria": carrera.get("categoria", ""),
            "orden": id_carrera,
            "estado": "Finalizada" if len(resultados) > 0 else "Pendiente",
            "hipodromo": hipodromo_nombre,
            "pista": "",
            "estado_pista": ""
        })

        # =================================================
        # MAPA RESULTADOS
        # =================================================

        mapa_resultados = {}

        for resultado in resultados:

            caballo_resultado = resultado.get("caballo", "")
            mapa_resultados[caballo_resultado] = resultado

        # =================================================
        # PARTICIPANTES
        # =================================================

        for participante in participantes:

            caballo = participante.get("caballo", "")
            nacionalidad = participante.get("nacionalidad", "")
            entrenador = participante.get("entrenador", "")
            jinete = participante.get("jockey", "")
            propietario = participante.get("propietario", "")

            # =============================================
            # ENTRENADOR
            # =============================================

            agregar_unico(
                bd["entrenadores"],
                entrenadores_set,
                entrenador,
                {
                    "nombre": entrenador,
                    "nacionalidad": ""
                }
            )

            # =============================================
            # JINETE
            # =============================================

            agregar_unico(
                bd["jinetes"],
                jinetes_set,
                jinete,
                {
                    "nombre": jinete,
                    "peso": None,
                    "nacionalidad": ""
                }
            )

            # =============================================
            # PROPIETARIO
            # =============================================

            agregar_unico(
                bd["propietarios"],
                propietarios_set,
                propietario,
                {
                    "nombre": propietario,
                    "nacionalidad": "",
                    "equipamiento": ""
                }
            )

            # =============================================
            # CABALLO
            # =============================================

            agregar_unico(
                bd["caballos"],
                caballos_set,
                caballo,
                {
                    "nombre": caballo,
                    "nacionalidad": nacionalidad,
                    "sexo": "",
                    "edad": participante.get("edad", ""),
                    "propietario": propietario,
                    "entrenador": entrenador
                }
            )

            # =============================================
            # PARTICIPANTE
            # =============================================

            bd["participantes"].append({
                "id_participante": id_participante,
                "numero_salida": participante.get("numero", ""),
                "caballo": caballo,
                "jinete": jinete,
                "carrera": id_carrera,
                "retirado": False
            })

            # =============================================
            # RESULTADO
            # =============================================

            resultado = mapa_resultados.get(caballo)

            if resultado:

                bd["resultados"].append({
                    "participante": id_participante,
                    "posicion": resultado.get("posicion", ""),
                    "duracion": "00:00:00",
                    "distancia": resultado.get("distancia", "")
                })

            id_participante += 1

        id_carrera += 1

# =====================================================
# GUARDAR JSON FINAL
# =====================================================

with open("bd_reorganizada.json", "w", encoding="utf-8") as f:
    json.dump(bd, f, ensure_ascii=False, indent=4)

print("JSON reorganizado correctamente")
