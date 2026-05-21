from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import json
import re

# =========================================================
# CONFIG
# =========================================================

URL = "https://www.hipodromoa.com/temporada/grandes_premios/_IqQzNPbID9if9RF9lTMfY7AMnt-i5dKO"

# =========================================================
# LIMPIEZA
# =========================================================

def limpiar_jinete(nombre):

    nombre = re.sub(r"\s*\([^)]*\)", "", nombre)

    return nombre.strip()


def limpiar_nombre_carrera(texto):

    texto = re.sub(r'^\d+\s+', '', texto)
    texto = re.sub(r'\s*\(\d{1,2}:\d{2}\)\s*$', '', texto)

    return texto.strip()


def limpiar_distancia(valor):

    numeros = re.findall(r"\d+", str(valor))

    return int(numeros[0]) if numeros else 0


def limpiar_hora(hora):

    hora = hora.replace("h", "").replace(".", ":").strip()

    if len(hora) == 5:
        hora += ":00"

    return hora


def limpiar_peso(valor):

    valor = valor.replace(",", ".").strip()

    try:
        return float(valor)
    except:
        return None


def limpiar_edad(valor):

    try:
        return int(re.findall(r"\d+", str(valor))[0])
    except:
        return None

# =========================================================
# TABLAS
# =========================================================

def extraer_tabla_objetos(tabla, claves):

    datos = []

    tbody = tabla.find_element(By.TAG_NAME, "tbody")
    filas = tbody.find_elements(By.TAG_NAME, "tr")

    for fila in filas:

        tds = fila.find_elements(By.TAG_NAME, "td")

        if not tds:
            continue

        valores = [td.text.strip() for td in tds]

        if len(valores) < len(claves):
            valores.extend([""] * (len(claves) - len(valores)))

        datos.append(dict(zip(claves, valores)))

    return datos

# =========================================================
# CABALLOS
# =========================================================

def parsear_ncaballo(texto):

    patron = r"^\s*(\d+)\s+([^(]+?)\s+\(([^)]*)\)"

    match = re.search(patron, texto)

    if match:

        contenido = match.group(3).strip()

        nacionalidad = contenido if contenido.isalpha() else "ESP"

        return {
            "numero": int(match.group(1)),
            "caballo": match.group(2).strip(),
            "nacionalidad": nacionalidad
        }

    patron_simple = r"^\s*(\d+)\s+(.*)$"

    match_simple = re.search(patron_simple, texto)

    if match_simple:

        return {
            "numero": int(match_simple.group(1)),
            "caballo": match_simple.group(2).strip(),
            "nacionalidad": "ESP"
        }

    return {
        "numero": None,
        "caballo": texto,
        "nacionalidad": "ESP"
    }


def parsear_pcaballo(texto):

    patron = r"^\s*(\d+)\s+([^(]+?)\s+\(([^)]*)\)"

    match = re.search(patron, texto)

    if match:

        return {
            "posicion": int(match.group(1)),
            "caballo": match.group(2).strip()
        }

    patron_simple = r"^\s*(\d+)\s+(.*)$"

    match_simple = re.search(patron_simple, texto)

    if match_simple:

        return {
            "posicion": int(match_simple.group(1)),
            "caballo": match_simple.group(2).strip()
        }

    return {
        "posicion": None,
        "caballo": texto
    }

# =========================================================
# DRIVER
# =========================================================

driver = webdriver.Chrome()

driver.get(URL)

wait = WebDriverWait(driver, 10)

elemento = wait.until(
    EC.presence_of_element_located((By.CLASS_NAME, "blog-main"))
)

jornadas = elemento.find_elements(By.CLASS_NAME, "JornadaHolder")

# =========================================================
# LINKS
# =========================================================

links = []

for jornada in jornadas:

    carreras = jornada.find_element(By.CLASS_NAME, "carreras")
    carrera = carreras.find_elements(By.CLASS_NAME, "carrera")

    for enlace in carrera:

        link = enlace.find_element(By.TAG_NAME, "p").find_element(By.TAG_NAME, "a")

        links.append({
            "url": link.get_attribute("href"),
            "nombre": limpiar_nombre_carrera(
                link.get_attribute("textContent").strip()
            )
        })

# =========================================================
# SCRAPING
# =========================================================

carreras_final = []

for carrera_info in links:

    href = carrera_info["url"]

    driver.get(href)

    fecha = href.split("/reunion/")[1].split("/")[0]

    try:

        wait.until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, "table.table.table-striped")
            )
        )

        # =====================================================
        # DATOS CARRERA
        # =====================================================

        datos_carrera = {}

        try:

            info = driver.find_element(
                By.CSS_SELECTOR,
                "div.informacion.col-sm-10"
            )

            strongs = info.find_elements(By.TAG_NAME, "strong")

            for strong in strongs:

                clave = strong.text.replace(":", "").strip()

                if clave == "Dotación":
                    continue

                valor = driver.execute_script("""
                    let node = arguments[0].nextSibling;
                    let text = '';

                    while(node){

                        if(node.tagName === 'STRONG'){
                            break;
                        }

                        if(node.nodeType === Node.TEXT_NODE){
                            text += node.textContent;
                        }

                        else if(node.tagName === 'BR'){
                            break;
                        }

                        node = node.nextSibling;
                    }

                    return text.trim();
                """, strong)

                datos_carrera[clave] = valor

            top_resultado = driver.find_element(By.CLASS_NAME, "topResultado")

            hora = top_resultado.find_element(
                By.XPATH,
                ".//div[contains(@style,'float:right')]"
            ).text.strip()

            datos_carrera["Hora"] = limpiar_hora(hora)

        except Exception as e:
            print("Error carrera:", e)

        # =====================================================
        # PARTICIPANTES
        # =====================================================

        participantes = []

        try:

            a_participantes = wait.until(
                EC.element_to_be_clickable(
                    (By.XPATH, "//li[.//a[contains(., 'Participantes')]]//a")
                )
            )

            driver.execute_script("arguments[0].click();", a_participantes)

            WebDriverWait(driver, 2).until(
                lambda d: d.find_element(
                    By.CSS_SELECTOR,
                    "table.table.table-striped"
                ).get_attribute("innerHTML") != ""
            )

            claves = [
                "Ncaballo",
                "sexo",
                "edad",
                "cajon",
                "peso",
                "jinete",
                "entrenador",
                "propietario"
            ]

            tabla = driver.find_element(
                By.CSS_SELECTOR,
                "table.table.table-striped"
            )

            datos = extraer_tabla_objetos(tabla, claves)

            retirados = False

            for fila in datos:

                info_caballo = parsear_ncaballo(fila["Ncaballo"])

                if info_caballo["caballo"].strip() == "Retirados":
                    retirados = True
                    continue

                participantes.append({
                    "numero": info_caballo["numero"],
                    "caballo": info_caballo["caballo"],
                    "nacionalidad": info_caballo["nacionalidad"],
                    "sexo": fila["sexo"],
                    "edad": limpiar_edad(fila["edad"]),
                    "cajon": fila["cajon"],
                    "peso": limpiar_peso(fila["peso"]),
                    "jinete": limpiar_jinete(fila["jinete"]),
                    "entrenador": fila["entrenador"],
                    "propietario": fila["propietario"],
                    "retirado": retirados
                })

        except Exception as e:
            print("Error participantes:", e)

        # =====================================================
        # RESULTADOS
        # =====================================================

        resultados = []

        try:

            tabla_antes = driver.find_element(
                By.CSS_SELECTOR,
                "table.table.table-striped"
            ).get_attribute("innerHTML")

            a_resultados = wait.until(
                EC.element_to_be_clickable(
                    (By.XPATH, "//li[.//a[contains(., 'Llegadas')]]//a")
                )
            )

            driver.execute_script("arguments[0].click();", a_resultados)

            WebDriverWait(driver, 2).until(
                lambda d: d.find_element(
                    By.CSS_SELECTOR,
                    "table.table.table-striped"
                ).get_attribute("innerHTML") != tabla_antes
            )

            tabla = driver.find_element(
                By.CSS_SELECTOR,
                "table.table.table-striped"
            )

            filas = tabla.find_element(
                By.TAG_NAME,
                "tbody"
            ).find_elements(By.TAG_NAME, "tr")

            for fila in filas:

                tds = fila.find_elements(By.TAG_NAME, "td")

                if not tds:
                    continue

                info = parsear_pcaballo(tds[0].text.strip())

                resultados.append({
                    "posicion": info["posicion"],
                    "caballo": info["caballo"],
                    "distancia": tds[8].text.strip()
                })

        except:
            print("Sin resultados")

        carreras_final.append({
            "url": href,
            "nombre": carrera_info["nombre"],
            "fecha": fecha,
            "hora": datos_carrera.get("Hora", "00:00:00"),
            "distancia": limpiar_distancia(
                datos_carrera.get("Distancia", "")
            ),
            "tipo": datos_carrera.get("Tipo", ""),
            "categoria": datos_carrera.get("Categoría", ""),
            "hipodromo": "Hipódromo de San Sebastián",
            "pista": datos_carrera.get("Pista", "Desconocido"),
            "estado_pista": datos_carrera.get("Estado", "Desconocido"),
            "participantes": participantes,
            "resultados": resultados
        })

    except Exception as e:
        print(f"Error en {href}: {e}")

driver.quit()

# =========================================================
# GUARDAR JSON
# =========================================================

with open(
    "../json/datos_carreras_sansebastian.json",
    "w",
    encoding="utf-8"
) as archivo:

    json.dump(
        carreras_final,
        archivo,
        ensure_ascii=False,
        indent=4
    )