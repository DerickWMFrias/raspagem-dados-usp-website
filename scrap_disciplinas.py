import time
import requests
import csv

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import pyautogui


from utils.util_funcs import start_selenium_drive, cria_csvs
from utils.scrap_departamentos import scrape_depts, scrape_cursos


mode = "depts"

# Initialize WebDriver
driver, page = start_selenium_drive("https://uspdigital.usp.br/jupiterweb/jupColegiadoLista?tipo=D")
time.sleep(2)

cria_csvs()

lista_links_unidades = []

tabela_institutos_usp = driver.find_element(By.XPATH, "(//div[@id='layout_conteudo']/table)[2]")

rows_institutos_usp = tabela_institutos_usp.find_elements(By.TAG_NAME, "tr")
rows_institutos_usp = rows_institutos_usp[1:]






for row in rows_institutos_usp:
    tds_row = row.find_elements(By.TAG_NAME, "td")
    #print(f"{tds_row[0].text }: {tds_row[1].text}")

    anchor_to_lnk = row.find_element(By.TAG_NAME, "a")
    lnk = anchor_to_lnk.get_attribute("href")

    #print(f"Redirect link: {lnk}\n")

    ll = [tds_row[0].text, tds_row[1].text, lnk]
    lista_links_unidades.append(ll)



tabela_entidades_externas = driver.find_element(By.XPATH, "(//div[@id='layout_conteudo']/table)[4]")
rows_entidades_externas = tabela_entidades_externas.find_elements(By.TAG_NAME, "tr")
rows_entidades_externas = rows_entidades_externas[1:]

for row in rows_entidades_externas:
    tds_row = row.find_elements(By.TAG_NAME, "td")
    #print(f"{tds_row[0].text }: {tds_row[1].text}")

    anchor_to_lnk = row.find_element(By.TAG_NAME, "a")
    lnk = anchor_to_lnk.get_attribute("href")

    #print(f"Redirect link: {lnk}\n")
    #time.sleep(1)

    aux = [tds_row[0].text, tds_row[1].text, lnk]
    lista_links_unidades.append(aux)





print("IMPRIMINDO UNIDADES NO CSV\n\n")
#Escreve csv com as informações das unidades
for row in lista_links_unidades:
    codigo_unidade = row[0]
    nome_unidade = row[1]

    
    with open("outputs\\unidades\\unidades.csv", "a", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow([codigo_unidade, nome_unidade])

#Trim_index serve para contar algumas unidades no comeco da raspagem, para facilitar a reexecução do script a partir de um ponto futuro
trim_index = 0
lista_links_unidades = lista_links_unidades[trim_index:]

for lk_unidade in lista_links_unidades:
    codigo_unidade = lk_unidade[0]
    link_unidade = lk_unidade[2]

    if mode == "depts":
        print("INDO RASPAR DEPARTAMENTOS\n")
        time.sleep(1)
        scrape_depts(driver, page, link_unidade, codigo_unidade)
    elif mode == "cursos":
        print("INDO RASPAR CURSOS\n")
        time.sleep(1)
        scrape_cursos(driver, page, link_unidade, codigo_unidade)
    
    


print("Program ENDED :)")
time.sleep(10)





