from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime
import json
import re

# =========================================================
# CONFIG
# =========================================================

BASE_URL = "https://www.hipodromodelazarzuela.es/carreras/jornada/"

# =========================================================
# FECHAS
# =========================================================

def fechas_mes_actual():

    año = datetime.now().strftime("%Y")
    mes = datetime.now().strftime("%m")

    fechas = []

    for d in range(1, 32):

        dia = str(d).zfill(2)

        fechas.append(año + mes + dia)

    return fechas

# =========================================================
# LIMPIEZA
# =========================================================

def limpiar_distancia(valor):

    numeros = re.findall(r"\d+", str(valor))

    return int(numeros[0]) if numeros else 0


def limpiar_hora(hora):

    hora = hora.replace("h", "").replace(".", ":").strip()

    if len(hora) == 5:
        hora += ":00"

    return hora


def limpiar_peso(valor):

    if not valor:
        return None

    valor = valor.replace(",", ".").strip()

    # =====================================================
    # SI VIENE:
    # 66.00-67.00
    # NOS QUEDAMOS CON:
    # 66.00
    # =====================================================

    valor = valor.split("-")[0].strip()

    numeros = re.findall(r"\d+(?:\.\d+)?", valor)

    try:

        if numeros:
            return float(numeros[0])

        return None

    except:
        return None


def limpiar_edad(valor):

    try:

        numeros = re.findall(r"\d+", str(valor))

        if numeros:
            return int(numeros[0])

        return None

    except:
        return None

def obtener_tipo_pista_participantes(driver):

    try:

        texto = driver.execute_script("""
            return Array.from(
                document.querySelectorAll(".table-head")
            )
            .map(e => e.textContent)
            .join(" ");
        """)

        texto = texto.upper()

        indice_hora = texto.find("HORA")

        if indice_hora > 0:

            anterior = texto[
                indice_hora - 1
            ]

            if anterior in ["H", "A", "C"]:

                return anterior

    except:
        pass

    return "Desconocido"


def obtener_tipo_pista_resultados(driver):

    try:

        texto = driver.execute_script("""
            return document
                .querySelector(".info-container")
                .querySelector("table")
                .querySelectorAll("td")[2]
                .textContent;
        """)

        texto = texto.upper()

        match = re.search(
            r"PISTA:\s*([A-Z])",
            texto
        )

        if match:

            return match.group(1)

    except:
        pass

    return "Desconocido"

# =========================================================
# TD
# =========================================================

def obtener_valor_td(driver, td):

    try:

        strong = td.find_element(By.TAG_NAME, "strong")

        valor = driver.execute_script("""
            let node = arguments[0].nextSibling;
            let text = '';

            while(node){

                if(node.nodeType === Node.TEXT_NODE){
                    text += node.textContent;
                }

                node = node.nextSibling;
            }

            return text.trim();
        """, strong)

        return valor

    except:

        return td.text.strip()

# =========================================================
# CABALLOS
# =========================================================

def parsear_caballo(texto):

    patron = r"^(.*?)\s*\(([A-Z]+)\)$"

    match = re.search(patron, texto)

    if match:

        return {
            "caballo": match.group(1).strip(),
            "nacionalidad": match.group(2).strip()
        }

    return {
        "caballo": texto.strip(),
        "nacionalidad": "ESP"
    }

# =========================================================
# NOMBRE CARRERA
# =========================================================

def limpiar_nombre_carrera(texto):

    return texto.split("(")[0].strip()

# =========================================================
# DRIVER
# =========================================================

options = Options()
options.add_argument("--headless=new")
options.add_argument("--headless")
options.add_argument("--disable-gpu")
options.add_argument("--window-size=1920,1080")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")

driver = webdriver.Chrome(options=options)

# =========================================================
# ARRAY FINAL
# =========================================================

datos_fechas = []

# =========================================================
# RECORRER FECHAS
# =========================================================

for fecha in fechas_mes_actual():

    url = BASE_URL + fecha

    print(f"\nBuscando jornada: {url}")

    driver.get(url)

    carreras_fecha = []

    try:

        tabla_jornada = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.ID, "datatable-jornada"))
        )

        tbody = tabla_jornada.find_element(By.TAG_NAME, "tbody")

        filas = tbody.find_elements(By.TAG_NAME, "tr")

        if len(filas) == 0:
            print(f"No hay carreras en {fecha}")
            continue

        print(f"Hay carreras en {fecha}")

        # =====================================================
        # RECORRER CARRERAS
        # =====================================================

        for fila in filas:

            tds = fila.find_elements(By.TAG_NAME, "td")

            if len(tds) < 6:
                continue

            enlace = tds[0].find_element(By.TAG_NAME, "a")

            href = enlace.get_attribute("href")

            nombre = limpiar_nombre_carrera(
                enlace.text.strip()
            )

            fecha_formateada = (
                f"{fecha[0:4]}-{fecha[4:6]}-{fecha[6:8]}"
            )

            carrera = {
                "url": href,
                "nombre": nombre,
                "fecha": fecha_formateada,
                "hora": limpiar_hora(
                    obtener_valor_td(driver, tds[5])
                ),
                "distancia": obtener_valor_td(driver, tds[1]),
                "orden": obtener_valor_td(driver, tds[6]),
                "tipo": obtener_valor_td(driver, tds[2]),
                "categoria": obtener_valor_td(driver, tds[3]),
                "premio": obtener_valor_td(driver, tds[4]),
                "hipodromo": "Hipódromo de la Zarzuela",
                "pista": "Desconocido",
                "estado_pista": "Desconocido",
                "participantes": [],
                "resultados": []
            }

            print(f"\nEntrando en carrera: {href}")

            # =====================================================
            # ENTRAR CARRERA
            # =====================================================

            driver.get(href)

            try:

                tabla_carrera = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.ID, "datatable"))
                )

                thead = tabla_carrera.find_element(By.TAG_NAME, "thead")

                primer_th = thead.find_element(
                    By.TAG_NAME,
                    "th"
                ).text.strip().lower()

                es_resultado = "pos" in primer_th

                print(
                    f"Tipo tabla: "
                    f"{'RESULTADOS' if es_resultado else 'PARTICIPANTES'}"
                )

                # =====================================================
                # TIPO PISTA
                # =====================================================

                if es_resultado:

                    carrera["pista"] = (
                        obtener_tipo_pista_resultados(
                            driver
                        )
                    )

                else:

                    carrera["pista"] = (
                        obtener_tipo_pista_participantes(
                            driver
                        )
                    )

                tbody_carrera = tabla_carrera.find_element(
                    By.TAG_NAME,
                    "tbody"
                )

                filas_carrera = tbody_carrera.find_elements(
                    By.TAG_NAME,
                    "tr"
                )

                participantes = []
                resultados = []

                # =====================================================
                # FILAS
                # =====================================================

                for fila_carrera in filas_carrera:

                    tds_carrera = fila_carrera.find_elements(
                        By.TAG_NAME,
                        "td"
                    )

                    if len(tds_carrera) < 8:
                        continue

                    # =================================================
                    # RESULTADOS
                    # =================================================

                    if es_resultado:

                        info = parsear_caballo(
                            tds_carrera[1].text.strip()
                        )

                        resultado = {
                            "posicion": int(
                                tds_carrera[0].text.strip()
                            ),
                            "caballo": info["caballo"],
                            "nacionalidad": info["nacionalidad"],

                            "peso": limpiar_peso(
                                tds_carrera[2].text.strip()
                            ),

                            "edad": limpiar_edad(
                                tds_carrera[3].text.strip()
                            ),

                            "distancia": tds_carrera[4].text.strip(),

                            "mantilla": tds_carrera[5].text.strip(),

                            "dividendo": tds_carrera[6].text.strip(),

                            "propietario": tds_carrera[7].text.strip(),

                            "entrenador": tds_carrera[8].text.strip(),

                            "jinete": tds_carrera[9].text.strip()
                        }

                        resultados.append(resultado)

                        # =============================================
                        # CREAR PARTICIPANTE DESDE RESULTADO
                        # =============================================

                        participantes.append({

                            "numero": tds_carrera[5].text.strip(),

                            "caballo": info["caballo"],

                            "nacionalidad": info["nacionalidad"],

                            "sexo": "",

                            "edad": limpiar_edad(
                                tds_carrera[3].text.strip()
                            ),

                            "peso": limpiar_peso(
                                tds_carrera[2].text.strip()
                            ),

                            "jinete": tds_carrera[9].text.strip(),

                            "propietario": tds_carrera[7].text.strip(),

                            "entrenador": tds_carrera[8].text.strip(),

                            "cajon": "",

                            "retirado": False
                        })

                    # =================================================
                    # PARTICIPANTES
                    # =================================================

                    else:

                        info = parsear_caballo(
                            tds_carrera[1].text.strip()
                        )

                        participante = {

                            "numero": int(
                                tds_carrera[0].text.strip()
                            ),

                            "caballo": info["caballo"],

                            "nacionalidad": info["nacionalidad"],

                            "sexo": "",

                            # tds_carrera[2] = columna basura

                            "edad": limpiar_edad(
                                tds_carrera[3].text.strip()
                            ),

                            "peso": limpiar_peso(
                                tds_carrera[4].text.strip()
                            ),

                            "jinete": tds_carrera[5].text.strip(),

                            "propietario": tds_carrera[6].text.strip(),

                            "entrenador": tds_carrera[7].text.strip(),

                            "cajon": tds_carrera[8].text.strip(),

                            "retirado": False
                        }

                        participantes.append(participante)

                carrera["participantes"] = participantes
                carrera["resultados"] = resultados

            except Exception as e:

                print("Error obteniendo carrera:", e)

            carreras_fecha.append(carrera)

            # =====================================================
            # VOLVER
            # =====================================================

            driver.back()

            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located(
                    (By.ID, "datatable-jornada")
                )
            )

        datos_fechas.extend(carreras_fecha)

    except Exception as e:

        print(f"Error jornada {fecha}: {e}")

# =========================================================
# MOSTRAR
# =========================================================

for carrera in datos_fechas:

    print("\n===================================================")

    print(f"Carrera: {carrera['nombre']}")
    print(f"Fecha: {carrera['fecha']}")
    print(f"Hora: {carrera['hora']}")
    print(f"Distancia: {carrera['distancia']}")

    print("\nParticipantes:")

    for participante in carrera["participantes"]:
        print(participante)

    print("\nResultados:")

    for resultado in carrera["resultados"]:
        print(resultado)

driver.quit()

# =========================================================
# GUARDAR JSON
# =========================================================

with open(
    "../json/datos_carreras_zarzuela.json",
    "w",
    encoding="utf-8"
) as archivo:

    json.dump(
        datos_fechas,
        archivo,
        ensure_ascii=False,
        indent=4
    )