from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime
import json
import re

#AEMET 28079

BASE_URL = "https://www.hipodromodelazarzuela.es/carreras/jornada/"

# =========================================================
# GENERAR FECHAS
# =========================================================

def fechas_mes_actual():
    año = datetime.now().strftime("%Y")
    mes = datetime.now().strftime("%m")

    fechas = []

    for d in range(1, 32):
        dia = str(d).zfill(2)
        fecha = año + mes + dia
        fechas.append(fecha)

    return fechas


# =========================================================
# OBTENER TEXTO REAL DE LOS TD
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
# SEPARAR CABALLO Y NACIONALIDAD
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
        "nacionalidad": None
    }

# =========================================================
# LIMPIAR NOMBRE CARRERA
# =========================================================

def limpiar_nombre_carrera(texto):

    # Cortar al primer paréntesis
    return texto.split("(")[0].strip()

# =========================================================
# DRIVER
# =========================================================

driver = webdriver.Chrome()

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
            print(f"❌ No hay carreras en {fecha}")
            continue

        print(f"✅ Hay carreras en {fecha}")

        # =========================================================
        # RECORRER CARRERAS
        # =========================================================

        for fila in filas:

            tds = fila.find_elements(By.TAG_NAME, "td")

            if len(tds) < 6:
                continue

            enlace = tds[0].find_element(By.TAG_NAME, "a")

            href = enlace.get_attribute("href")

            nombre_raw = enlace.text.strip()
            nombre = limpiar_nombre_carrera(nombre_raw)
            fecha_formateada = f"{fecha[0:4]}-{fecha[4:6]}-{fecha[6:8]}"

            carrera = {
                "url": href,
                "nombre": nombre,
                "distancia": obtener_valor_td(driver, tds[1]),
                "tipo": obtener_valor_td(driver, tds[2]),
                "categoria": obtener_valor_td(driver, tds[3]),
                "premio": obtener_valor_td(driver, tds[4]),
                "fecha": fecha_formateada,
                "hora": obtener_valor_td(driver, tds[5]),
                "participantes": [],
                "resultados": []
            }

            print(f"\nEntrando en carrera: {href}")

            # =========================================================
            # ENTRAR EN LA CARRERA
            # =========================================================

            driver.get(href)

            try:

                tabla_carrera = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.ID, "datatable"))
                )

                # =========================================================
                # COMPROBAR TIPO TABLA
                # =========================================================

                thead = tabla_carrera.find_element(By.TAG_NAME, "thead")
                primer_th = thead.find_element(By.TAG_NAME, "th").text.strip().lower()
                es_resultado = "pos" in primer_th
                print(f"Tipo tabla: {'RESULTADOS' if es_resultado else 'PARTICIPANTES'}")
                tbody_carrera = tabla_carrera.find_element(By.TAG_NAME, "tbody")
                filas_carrera = tbody_carrera.find_elements(By.TAG_NAME, "tr")
                participantes = []
                resultados = []

                # =========================================================
                # RECORRER FILAS
                # =========================================================

                for fila_carrera in filas_carrera:

                    tds_carrera = fila_carrera.find_elements(By.TAG_NAME, "td")

                    if len(tds_carrera) < 8:
                        continue

                    # =========================================================
                    # RESULTADOS
                    # =========================================================

                    if es_resultado:
                        info_caballo = parsear_caballo(tds_carrera[1].text.strip())

                        resultado = {
                            "posicion": tds_carrera[0].text.strip(),
                            "caballo": info_caballo["caballo"],
                            "nacionalidad": info_caballo["nacionalidad"],
                            "peso": tds_carrera[2].text.strip(),
                            "edad": tds_carrera[3].text.strip(),
                            "distancia": tds_carrera[4].text.strip(),
                            "mantilla": tds_carrera[5].text.strip(),
                            "dividendo": tds_carrera[6].text.strip(),
                            "propietario": tds_carrera[7].text.strip(),
                            "entrenador": tds_carrera[8].text.strip(),
                            "jinete": tds_carrera[9].text.strip()
                        }

                        resultados.append(resultado)

                    # =========================================================
                    # PARTICIPANTES
                    # =========================================================

                    else:
                        info_caballo = parsear_caballo(tds_carrera[1].text.strip())

                        if info_caballo["nacionalidad"] is None:
                            info_caballo["nacionalidad"] = "ESP"

                        participante = {
                            "numero": tds_carrera[0].text.strip(),
                            "caballo": info_caballo["caballo"],
                            "nacionalidad": info_caballo["nacionalidad"],
                            "edad": tds_carrera[2].text.strip(),
                            "peso": tds_carrera[3].text.strip(),
                            "jockey": tds_carrera[4].text.strip(),
                            "propietario": tds_carrera[5].text.strip(),
                            "entrenador": tds_carrera[6].text.strip(),
                            "cajón": tds_carrera[7].text.strip()
                        }

                        participantes.append(participante)

                # =========================================================
                # GUARDAR DATOS
                # =========================================================

                if es_resultado:
                    carrera["resultados"] = resultados

                else:
                    carrera["participantes"] = participantes

            except Exception as e:
                print("⚠️ Error obteniendo datos de carrera:", e)

            carreras_fecha.append(carrera)

            # =========================================================
            # VOLVER A LA JORNADA
            # =========================================================

            driver.back()

            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.ID, "datatable-jornada"))
            )

        # =========================================================
        # GUARDAR FECHA
        # =========================================================

        fecha_formateada = f"{fecha[0:4]}/{fecha[4:6]}/{fecha[6:8]}"

        datos_fechas.append({
            "fecha": fecha_formateada,
            "carreras": carreras_fecha
        })

    except Exception as e:
        print(f"⚠️ Error en jornada {fecha}: {e}")

# =========================================================
# MOSTRAR RESULTADOS
# =========================================================

for fecha in datos_fechas:

    print("\n===================================================")
    print(f"FECHA: {fecha['fecha']}")

    for carrera in fecha["carreras"]:

        print("\n------------------- CARRERA -------------------")

        print(f"URL: {carrera['url']}")
        print(f"Distancia: {carrera['distancia']}")
        print(f"Tipo: {carrera['tipo']}")
        print(f"Categoria: {carrera['categoria']}")
        print(f"Premio: {carrera['premio']}")
        print(f"Hora: {carrera['hora']}")

        # =========================================================
        # PARTICIPANTES
        # =========================================================

        if len(carrera["participantes"]) > 0:

            print("\nParticipantes:")

            for participante in carrera["participantes"]:
                print(participante)

        # =========================================================
        # RESULTADOS
        # =========================================================

        if len(carrera["resultados"]) > 0:

            print("\nResultados:")

            for resultado in carrera["resultados"]:
                print(resultado)

driver.quit()

with open("../json/datos_carreras_zarzuela.json", "w", encoding="utf-8") as archivo:
    json.dump(datos_fechas, archivo, ensure_ascii=False, indent=4)