import time
import os
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.wait import WebDriverWait

# -------------------------------------------- Funciones ------------------------------------


# ------------------------- LOGGIN -----------------------------------------
def loggin():
    # driver.maximize_window()
    driver.get("https://usuarios.telecentro.net.ar/logIn.php")
    time.sleep(2)
    wait.until(EC.element_to_be_clickable(
        (By.XPATH, '//*[@id="usuario"]'))).send_keys(user)
    wait.until(EC.element_to_be_clickable(
        (By.XPATH, '//*[@id="password"]'))).send_keys(clave)
    wait.until(EC.element_to_be_clickable(
        (By.XPATH, '//*[@id="btn-login"]'))).click()
# --------------------------------------------------------------------------


# ------------------------- BANDEJAS -----------------------------------------
def Bandejas():
    time.sleep(1)
    driver.get("https://moica2.telecentro.net.ar/home.php")
    time.sleep(1)
    # -------------------- Bandeja General ----------------------------
    dropdwn = driver.find_element(
        By.XPATH, '//*[@id="SECTOR-SELECT"]')           # Sector
    # Busca la opcion Diseño de red/-Edificios FTTH
    dd = Select(dropdwn)
    dd.select_by_value("6324b5691d2eef081b091b6d")
    wait.until(EC.element_to_be_clickable(
        (By.XPATH, '//*[@id="BT-LIST-6324b5691d2eef081b091b6d"]'))).click()   # Selecciona la opcion Diseño de red/-Edificios FTTH
    time.sleep(1)
    wait.until(EC.element_to_be_clickable(
        (By.XPATH, '//*[@id="pager_TktsSector_left"]/table/tbody/tr/td[2]/div/span'))).click()  # Boton de descarga
    time.sleep(1)
    # --------------------------------------------------------------------------

    # -------------------- Bandeja Diseño Edificios Armado Reforma de Red ----------------------------
    wait.until(EC.element_to_be_clickable(
        (By.XPATH, '//*[@id="BT-LIST-6324b6491d2eef029e6173fc"]'))).click()   # Selecciona la Bandeja Diseño Edificios Armado Reforma de Red
    time.sleep(1)
    wait.until(EC.element_to_be_clickable(
        (By.XPATH, '//*[@id="pager_TktsSector_left"]/table/tbody/tr/td[2]/div/span'))).click()  # Boton de descarga
    time.sleep(1)
# --------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------------------------------------------------------------------


# -------------------------------------------- VARIABLES ------------------------------------
posicion = ["", ""]


DIRECTORIO_BASE = os.path.dirname(__file__)
DIRECTORIO_ANALIZAR = os.path.join(DIRECTORIO_BASE, 'Bandeja_Reformas')
DIRECTORIO_ANALIZADO = os.listdir(DIRECTORIO_ANALIZAR)

path = "/chromedriver.exe"
chromeOptions = Options()
chromeOptions.add_experimental_option(
    "prefs", {"download.default_directory": DIRECTORIO_ANALIZAR, })
Service = Service(executable_path=path)
driver = webdriver.Chrome(service=Service, chrome_options=chromeOptions)
wait = WebDriverWait(driver, 10)
# driver.maximize_window()
driver.minimize_window()

with open("Credenciales.txt", mode="r") as archivo:
    credenciales = archivo.readline().strip().split(",")
    user = credenciales[0].strip()
    clave = credenciales[1].strip()

# ------------------------------- CICLO PRINCIPAL -----------------


def principal():

    DIRECTORIO_BASE = os.path.dirname(__file__)
    DIRECTORIO_ANALIZAR = os.path.join(DIRECTORIO_BASE, 'Bandeja_Reformas')
    DIRECTORIO_ANALIZADO = os.listdir(DIRECTORIO_ANALIZAR)

    for x in range(len(DIRECTORIO_ANALIZADO)):
        if ("export" in DIRECTORIO_ANALIZADO[x]):
            path = os.path.join(DIRECTORIO_ANALIZAR, DIRECTORIO_ANALIZADO[x])
            os.remove(path)
        if ("Bandeja_de_Reformas" in DIRECTORIO_ANALIZADO[x]):
            path = os.path.join(DIRECTORIO_ANALIZAR, DIRECTORIO_ANALIZADO[x])
            os.remove(path)

    loggin()

    Bandejas()

    DIRECTORIO_ANALIZADO = os.listdir(DIRECTORIO_ANALIZAR)
    y = 0
    for x in range(len(DIRECTORIO_ANALIZADO)):
        if ("export" in DIRECTORIO_ANALIZADO[x]):
            posicion[y] = x
            y = +1

    path = os.path.join(DIRECTORIO_ANALIZAR, DIRECTORIO_ANALIZADO[posicion[0]])
    df1 = pd.read_csv(path)
    os.remove(path)

    path = os.path.join(DIRECTORIO_ANALIZAR, DIRECTORIO_ANALIZADO[posicion[1]])
    df2 = pd.read_csv(path)
    os.remove(path)

    dftotal = pd.concat([df1, df2], axis=0)

    bandeja = dftotal[["Ticket", "Nodos", "Nodos Cmts",
                       "Asunto", "Problema", "Prioridad", "Data zona"]]

    path = os.path.join(DIRECTORIO_ANALIZAR, "Bandeja_de_Reformas.csv")
    bandeja.to_csv(path, index=False)

    driver.quit()


# ---------------------------------------------------------------------------------------------------------------------------------


principal()

# ---------------------------------------------------------------------------------------------
# ------------------------------------
"""






"""
