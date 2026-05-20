from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import json
import re

#AEMET 20069

# ==============================================
# LIMPIAR NOMBRE CARRERA
# ==============================================
def limpiar_jockey(nombre):

    # Eliminar todo lo que esté entre paréntesis
    nombre = re.sub(r"\s*\([^)]*\)", "", nombre)

    return nombre.strip()

def limpiar_nombre_carrera(texto):

    # Quitar número inicial
    texto = re.sub(r'^\d+\s+', '', texto)

    # Quitar hora final (11:05)
    texto = re.sub(r'\s*\(\d{1,2}:\d{2}\)\s*$', '', texto)

    return texto.strip()

def extraer_tabla_objetos(tabla, claves):
    datos = []

    tbody = tabla.find_element(By.TAG_NAME, "tbody")
    filas = tbody.find_elements(By.TAG_NAME, "tr")

    for fila in filas:
        tds = fila.find_elements(By.TAG_NAME, "td")

        if not tds:
            continue

        valores = [td.text.strip() for td in tds]

        # Evitar errores si faltan columnas
        if len(valores) < len(claves):
            valores.extend([""] * (len(claves) - len(valores)))

        objeto = dict(zip(claves, valores))

        datos.append(objeto)

    return datos


def parsear_ncaballo(texto):

    patron = r"^\s*(\d+)\s+([^(]+?)\s+\(([^)]*)\)"

    match = re.search(patron, texto)

    if match:

        contenido_parentesis = match.group(3).strip()

        # Si el contenido del primer paréntesis es texto -> nacionalidad
        if contenido_parentesis.isalpha():
            nacionalidad = contenido_parentesis
        else:
            nacionalidad = "ESP"

        return {
            "numero": int(match.group(1)),
            "caballo": match.group(2).strip(),
            "nacionalidad": nacionalidad
        }

    # Fallback por si no hay paréntesis
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

    # Fallback
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



#url = "https://www.hipodromoa.com/temporada/grandes_premios/_IqQzNPbID9if9RF9lTMfY7AMnt-i5dKO"

url = "https://www.hipodromoa.com/temporadas_anteriores/_IqQzNPbID9hmdCrEM50YFelRT0DKLYB1"

driver = webdriver.Chrome()
driver.get(url)

wait = WebDriverWait(driver, 10)

elemento = wait.until(
    EC.presence_of_element_located((By.CLASS_NAME, "blog-main"))
)

jornadas = elemento.find_elements(By.CLASS_NAME, "JornadaHolder")

# Guardar links
links = []

for jornada in jornadas:
    carreras = jornada.find_element(By.CLASS_NAME, "carreras")
    carrera = carreras.find_elements(By.CLASS_NAME, "carrera")

    for enlace in carrera:

        link = enlace.find_element(By.TAG_NAME, "p").find_element(By.TAG_NAME, "a")

        href = link.get_attribute("href")

        nombre_raw = link.get_attribute("textContent").strip()
        nombre = limpiar_nombre_carrera(nombre_raw)

        links.append({
            "url": href,
            "nombre": nombre
        })

# Recorrer links
tablas_datos = []

for carrera_info in links:

    href = carrera_info["url"]
    nombre = carrera_info["nombre"]

    driver.get(href)

    fecha = href.split("/reunion/")[1].split("/")[0]

    datos_participantes = {'Ncaballo':'','sexo':'','edad':'','cajon':'','jockey':'','Entrenador':'','Propietario':'',}
    datos_resultados = {'Pcaballo':'','sexo':'','edad':'','numero':'','peso':'','jockey':'','Entrenador':'','Propietario':'','Distancia':'',}

    try:
        wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "table.table.table-striped"))
        )

        # ==============================================
        # CARRERA
        # ==============================================
        try:
            info = driver.find_element(By.CSS_SELECTOR, "div.informacion.col-sm-10")
            strongs = info.find_elements(By.TAG_NAME, "strong")
            datos_carrera = {}

            for strong in strongs:
                clave = strong.text.replace(":", "").strip()
                # Saltar Dotación
                if clave == "Dotación":
                    continue

                valor = driver.execute_script("""
                    let node = arguments[0].nextSibling;
                    let text = '';
                    let clave = arguments[1];
                    while(node){
                        // parar al siguiente campo
                        if(node.tagName === 'STRONG'){
                            break;
                        }
                        if(node.nodeType === Node.TEXT_NODE){
                            text += node.textContent;
                        }
                        else if(node.tagName === 'BR' && clave !== 'Condiciones'){
                            break;
                        }
                        node = node.nextSibling;
                    }
                    return text.trim();
                """, strong, clave)

                datos_carrera[clave] = valor

                # ==========================================
                # OBTENER HORA
                # ==========================================

                top_resultado = driver.find_element(By.CLASS_NAME, "topResultado")

                hora = top_resultado.find_element(
                    By.XPATH,
                    ".//div[contains(@style,'float:right')]"
                ).text.strip()

                datos_carrera["Hora"] = hora

        except Exception as e:
            print("Error en carreras:", e)

        # ==============================================
        # PARTICIPANTES
        # ==============================================
        try:
            a_participantes = wait.until(
                EC.element_to_be_clickable(
                    (By.XPATH, "//li[.//a[contains(., 'Participantes')]]//a")
                )
            )

            driver.execute_script("arguments[0].click();", a_participantes)

            # Esperar a que cargue contenido (HTML)
            WebDriverWait(driver, 1).until(
                lambda d: d.find_element(
                    By.CSS_SELECTOR, "table.table.table-striped"
                ).get_attribute("innerHTML") != ""
            )

            claves_participantes = [
                'Ncaballo',
                'sexo',
                'edad',
                'cajon',
                'peso',
                'jockey',
                'Entrenador',
                'Propietario'
            ]
            tabla = driver.find_element(By.CSS_SELECTOR, "table.table.table-striped")
            datos_participantes = extraer_tabla_objetos(tabla,claves_participantes)

            # ==========================================
            # NORMALIZAR NCABALLO
            # ==========================================
            participantes_limpios = []

            for fila in datos_participantes:

                info_caballo = parsear_ncaballo(fila["Ncaballo"])

                if info_caballo["caballo"].strip() == "Retirados":
                    break

                fila["jockey"] = limpiar_jockey(fila["jockey"])

                fila["numero"] = info_caballo["numero"]
                fila["caballo"] = info_caballo["caballo"]
                fila["nacionalidad"] = info_caballo["nacionalidad"]

                del fila["Ncaballo"]

                participantes_limpios.append(fila)

            datos_participantes = participantes_limpios

        except Exception as e:
            print("Error en participantes:", e)

        # ==============================================
        # RESULTADOS
        # ==============================================
        try:

            tabla_antes = driver.find_element(
                By.CSS_SELECTOR, "table.table.table-striped"
            ).get_attribute("innerHTML")

            a_resultados = wait.until(
                EC.element_to_be_clickable(
                    (By.XPATH, "//li[.//a[contains(., 'Llegadas')]]//a")
                )
            )

            driver.execute_script("arguments[0].click();", a_resultados)

            WebDriverWait(driver, 1).until(
                lambda d: d.find_element(
                    By.CSS_SELECTOR, "table.table.table-striped"
                ).get_attribute("innerHTML") != tabla_antes
            )

            tabla = driver.find_element(By.CSS_SELECTOR, "table.table.table-striped")

            tbody = tabla.find_element(By.TAG_NAME, "tbody")
            filas = tbody.find_elements(By.TAG_NAME, "tr")

            datos_resultados = []

            for fila in filas:

                tds = fila.find_elements(By.TAG_NAME, "td")

                if not tds:
                    continue

                info_resultado = parsear_pcaballo(tds[0].text.strip())

                resultado = {
                    "posicion": info_resultado["posicion"],
                    "caballo": info_resultado["caballo"],
                    "Distancia": tds[8].text.strip()
                }

                datos_resultados.append(resultado)

        except Exception as e:
            print("Sin resultados")

        tablas_datos.append({
            "url": href,
            "nombre": nombre,
            "fecha" : fecha,
            "datos_carrera": datos_carrera,
            "tabla_participantes": datos_participantes,
            "tabla_resultados": datos_resultados
        })

    except Exception as e:
        print(f"Error en {href}: {e}")

# Mostrar resultados
for tabla in tablas_datos:
    print(f"\nURL: {tabla['url']}")

    print("\nFECHA:")
    print(tabla["fecha"])

    # ==========================================
    # DATOS CARRERA
    # ==========================================
    print("\nDATOS CARRERA:")

    for clave, valor in tabla["datos_carrera"].items():
        print(f"{clave}: {valor}")

    # ==========================================
    # PARTICIPANTES
    # ==========================================
    print("\nPARTICIPANTES:")

    for fila in tabla["tabla_participantes"]:
        print(fila)

    # ==========================================
    # RESULTADOS
    # ==========================================
    print("\nRESULTADOS:")

    for fila in tabla["tabla_resultados"]:
        print(fila)

    print("========================================================================================================================================================================")

driver.quit()

with open("../json/datos_carreras_sansebastian.json", "w", encoding="utf-8") as archivo:
    json.dump(tablas_datos, archivo, ensure_ascii=False, indent=4)