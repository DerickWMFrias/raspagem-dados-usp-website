import pyautogui
import time
import requests

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

from utils.util_funcs import start_selenium_drive, extract_options_from_select


no_print = False


def scrap_info_curso(driver):
    table_element = driver.find_element(By.CSS_SELECTOR, "div#step2 > table")
    table_text = table_element.text

    if not no_print:
        print("\n\n\nInformacões do Curso \n\n")
        print(table_text)

    return table_text

def scrap_projeto_pedagogico(driver):
    """
    O pdf contendo o projeto pedagógico de muitos cursos da usp se encontram não baixáveis no momento, portanto esta função
    ainda não pode ser implementada.
    """
    pass

def scrape_grade_curricular(driver):
    descricao_curso_html = driver.find_element(By.CLASS_NAME, "informacoesEspecificas")
    grade_curricular_html = driver.find_element(By.ID, "gradeCurricular")
    tabelas_grade_curricular = grade_curricular_html.find_elements(By.TAG_NAME, "table")

    descricao_curso = descricao_curso_html.text
    #print(grade_curricular_html.get_attribute("outerHTML"))
    #grade_curricular = grade_curricular_html.text

    texto_legenda = "Legenda: CH = Carga horária Total; CE = Carga horária de Estágio; CP = Carga horária de Práticas como Componentes Curriculares; ATPA = Atividades Teórico-Práticas de AprofundamentoLegenda: CH = Carga horária Total; CE = Carga horária de Estágio; CP = Carga horária de Práticas como Componentes Curriculares; ATPA = Atividades Teórico-Práticas de Aprofundamento"

    return descricao_curso, texto_legenda, tabelas_grade_curricular






driver, page = start_selenium_drive("https://uspdigital.usp.br/jupiterweb/jupCarreira.jsp?codmnu=8275")


select_unidade, options_select_unidade = extract_options_from_select(page, By.ID, "comboUnidade")
options_select_unidade = options_select_unidade[1:]

i = 1
for option in options_select_unidade:
    print(f"{i}: {option}")
    i = i+1


cursos = []
print('\n\n')

for unidade in options_select_unidade:
    print(f"Cursos da Unidade: {unidade}")

    select_unidade.select_by_visible_text(unidade)  # Select by visible text
    time.sleep(1)

    select_cursos, options_select_cursos = extract_options_from_select(page, By.ID, "comboCurso")
    options_select_cursos = options_select_cursos[1:]

    i = 1
    for curso in options_select_cursos:
        print(f"{i}: {curso}")
        i = i+1
        select_cursos.select_by_visible_text(curso)

        button_enviar = page.until(EC.element_to_be_clickable((By.ID, "enviar")))
        button_enviar.click()
        time.sleep(2)


        ul_navigation_tabs = driver.find_element(By.CSS_SELECTOR, "div#tabs > ul")
        li_tabs = ul_navigation_tabs.find_elements(By.TAG_NAME, "li")
        link_buscar = li_tabs[0].find_element(By.TAG_NAME, "a")


        link_info_curso = li_tabs[1].find_element(By.TAG_NAME, "a")
        link_projeto_pedagogico = li_tabs[2].find_element(By.TAG_NAME, "a")
        link_grade_curricular = li_tabs[3].find_element(By.TAG_NAME, "a")


        #-----------RASPA INFO CURSO----------------
        table_element = driver.find_element(By.CSS_SELECTOR, "div#step2 > table")
        table_text = table_element.text
        print("\n\n\nInformacões do Curso \n\n")
        print(table_text)

        texto_info_curso = scrap_info_curso(driver)

        #-----------RASPA PROJETO PEDAGOGICO----------------
        #print("Trying to download PDF")
        #time.sleep(1)
        #link_projeto_pedagogico.click()
        #print("Still impossible to download pdfs from Jupiterweb")
        #time.sleep(1)


        #-----------RASPA GRADE CURRICULAR----------------
        link_grade_curricular.click()
        time.sleep(1)
        descricao_curso, texto_legenda, tabelas_grade_curricular = scrape_grade_curricular(driver)

        print("\n\nDescricao do Curso\n")
        print(descricao_curso)
        print("\n\n\n")
        print(texto_legenda)
        for grade_curricular in tabelas_grade_curricular:
            print(grade_curricular.text)
        print("\n\n\n\n")
        time.sleep(1)

        #-----------RETORNA---------
        link_buscar.click() 
        time.sleep(1)


    cursos.append(options_select_unidade)


driver.quit()


