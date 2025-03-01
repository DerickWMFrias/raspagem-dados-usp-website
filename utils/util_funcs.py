import time
import csv
import json

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from fake_useragent import UserAgent



def start_selenium_drive(weburl):
    """
    
    """
    # Initialize WebDriver

    ua = UserAgent(browsers=['chrome'])
    user_agent = ua.random
    chrome_options = Options()

    chrome_options.add_argument("--incognito")  # Enables Incognito Mode
    chrome_options.add_argument(f'user-agent={user_agent}')  # Set the random User-Agent from fake_useragent
    #chrome_options.add_argument("--disable-gpu")  # Avoid GPU acceleration for headless mode
    chrome_options.add_argument("--no-sandbox")  # Bypass OS security model
    #chrome_options.add_argument("--disable-dev-shm-usage")  # Use disk for shared memory
    chrome_options.add_argument("--disable-extensions")  # Disable extensions
    chrome_options.add_argument("--disable-plugins")  # Disable unnecessary plugins
    chrome_options.add_argument("--lang=pt-BR")
    chrome_options.add_argument("accept-lang=pt-BR")
    chrome_options.add_argument("--log-level=OFF")
    #chrome_options.add_experimental_option("excludeSwitches", ['enable-logging'])

    chrome_options.add_argument("--start-maximized")  # Open in full screen
    #chrome_options.add_argument("--headless") # Run headless to reduce resource usage
    driver = webdriver.Chrome(options=chrome_options)

    # Open the webpage
    driver.get(weburl) 

    # Wait for the <select> element to be present
    page = WebDriverWait(driver, 10)  # Wait up to 10 seconds
    return driver, page
    


def extract_options_from_select(page, by_what, filter_str):
    """
    Scrape a

    Returns: a reference to the <select> element,
    an array with each option from the selector 
    """
    cursos_unidade = page.until(EC.presence_of_element_located((by_what, filter_str))) #Normally By.ID
    selector = Select(cursos_unidade)
    time.sleep(1)

    # Extract all options
    options = [option.text for option in selector.options]
    return selector, options


def get_href_selenium(driver, by_what, filter_str):
    element = driver.find_element(by_what, filter_str)
    anchor = element.find_element(By.TAG_NAME, "a")
    lnk = anchor.get_attribute("href")

    return lnk


def scrape_cabecalho(text_to_scrape):
    cabecalho_disciplina = text_to_scrape
    cabecalho_disciplina = cabecalho_disciplina.split('\n')

    unidade_disciplina = cabecalho_disciplina[0]
    departamento_disciplina = cabecalho_disciplina[1]
    nome_disciplina = cabecalho_disciplina[2]
    nome_disciplina_ingles = cabecalho_disciplina[3]

    return unidade_disciplina, departamento_disciplina, nome_disciplina, nome_disciplina_ingles



def scrape_creditos(text_to_scrape):
    creditos_disciplina = text_to_scrape.split('\n')

    creditos_aula_disciplina = creditos_disciplina[0][:]
    creditos_trabalho_disciplina = creditos_disciplina[1]
    carga_horaria_disciplina = creditos_disciplina[2]
    tipo_disciplina = creditos_disciplina[3]

    creditos_aula_disciplina = ' '.join(creditos_aula_disciplina.split()[2:])
    creditos_trabalho_disciplina = ' '.join(creditos_trabalho_disciplina.split()[2:])
    carga_horaria_disciplina = ' '.join(carga_horaria_disciplina.split()[3:])
    tipo_disciplina = ' '.join(tipo_disciplina.split()[1:])

    return creditos_aula_disciplina, creditos_trabalho_disciplina, carga_horaria_disciplina, tipo_disciplina
    

def scrape_objetivos(text_to_scrape):
    objetivos_disciplina = text_to_scrape.split()
    objetivos_disciplina = ' '.join(objetivos_disciplina[1:])

    return objetivos_disciplina

def scrape_docentes(table_docentes):
    table = table_docentes.find_element(By.TAG_NAME, "table")
    rows_docentes = table.find_elements(By.TAG_NAME, "tr")
    rows_docentes = rows_docentes[1:]

    #print("----------------------")
    #print(table.get_attribute("outerHTML"))
    #print("----------------------")
    nome_docentes = []
    id_docentes = []
    #print(f"SIZE: {len(rows_docentes)}")

    for row in rows_docentes:
        text_to_scrape = row.text

        aux = text_to_scrape.split()
        print(f"rowtext: {row}")
        aux_id = aux[0]
        aux_docente = ' '.join(aux[1:])

        nome_docentes.append(aux_docente)
        id_docentes.append(aux_id)

    return nome_docentes, id_docentes


def scrape_programa(text_to_scrape):
    programa_disciplina = text_to_scrape
    index = programa_disciplina.find("      Programa")

    programa = ""
    programa_resumido = ""

    if index != -1:  # Check if the substring is found
        programa_resumido = programa_disciplina[:index]
        programa_resumido = programa_resumido.split()
        programa_resumido = ' '.join(programa_resumido[2:-1])

        programa = programa_disciplina[index:]
        programa = programa.split()
        programa = ' '.join(programa[1:-1])
        #print(programa_resumido)
        #print(programa)
    else:
        print("Error scrapping! write at a file that this link failed. At scrap_pagdisp")
        #write at a file that this link failed

    return programa, programa_resumido


def scrape_avaliacao(text_to_scrape):
    avaliacao_disciplina = text_to_scrape.split('\n')

    metodo_avaliacao = ""
    criterio_avaliacao = ""
    recuperacao_avaliacao = ""

    jj = 0
    while jj < len(avaliacao_disciplina):
        paragrafo = avaliacao_disciplina[jj]

        if paragrafo == "Método":
            jj = jj+1
            while avaliacao_disciplina[jj] != "Critério" and jj < len(avaliacao_disciplina):
                metodo_avaliacao += avaliacao_disciplina[jj]
                metodo_avaliacao += "\n"
                jj = jj+1
                if jj == len(avaliacao_disciplina)-1:
                    print("Não encontrou critério!!")
                    #Raise exception and continue

        elif paragrafo == "Critério":
            jj = jj+1
            while avaliacao_disciplina[jj] != "Norma de Recuperação" and jj < len(avaliacao_disciplina):
                criterio_avaliacao += avaliacao_disciplina[jj]
                criterio_avaliacao += "\n"
                jj = jj+1
                if jj == len(avaliacao_disciplina)-1:
                    print("Não encontrou norma de recuperação!!")
                    #Raise exception and continue

        elif paragrafo == "Norma de Recuperação":
            jj = jj+1
            while jj < len(avaliacao_disciplina):
                recuperacao_avaliacao += avaliacao_disciplina[jj]
                recuperacao_avaliacao += "\n"
                jj = jj+1
        else:
            jj = jj+1

    #print(f"Metodo: \n {metodo_avaliacao}")
    #print(f"Criterio: \n {criterio_avaliacao}")
    #print(f"Rec: \n {recuperacao_avaliacao}")

    return metodo_avaliacao, criterio_avaliacao, recuperacao_avaliacao
    


def scrape_extensao(text_to_scrape):
    texto_extensao = text_to_scrape.split('\n')

    grupo_social_alvo = "" 
    objetivos_atividade_extensao = ""
    descricao_atividade_extensao = "" 
    avaliacao_atividade_extensao = ""

    jj = 0
    while jj < len(texto_extensao):
        paragrafo = texto_extensao[jj]
        #print(f"Paragrafo: |{paragrafo}|\n")
        if paragrafo == "      Grupo social alvo da atividade":
            jj = jj+1
            while texto_extensao[jj] != "Objetivos da atividade" and jj < len(texto_extensao):
                grupo_social_alvo += texto_extensao[jj]
                grupo_social_alvo += "\n"
                jj = jj+1
                if jj == len(texto_extensao)-1:
                    print("Não encontrou objetivos da atividade!!")
                    #Raise exception and continue

        elif paragrafo == "Objetivos da atividade":
            jj = jj+1
            while texto_extensao[jj] != "Descrição da atividade" and jj < len(texto_extensao):
                objetivos_atividade_extensao += texto_extensao[jj]
                objetivos_atividade_extensao += "\n"
                jj = jj+1
                if jj == len(texto_extensao)-1:
                    print("Não encontrou descrição da atividade!!")
                    #Raise exception and continue

        elif paragrafo == "Descrição da atividade":
            jj = jj+1
            while texto_extensao[jj] != "Indicadores de avaliação da atividade" and jj < len(texto_extensao):
                descricao_atividade_extensao += texto_extensao[jj]
                descricao_atividade_extensao += "\n"
                jj = jj+1
                if jj == len(texto_extensao)-1:
                    print("Não encontrou indicadores de avaliação da atividade!!")
                    #Raise exception and continue

        elif paragrafo == "Indicadores de avaliação da atividade":
            jj = jj+1
            while jj < len(texto_extensao):
                avaliacao_atividade_extensao += texto_extensao[jj]
                avaliacao_atividade_extensao += "\n"
                jj = jj+1
        else:
            jj = jj+1


    return grupo_social_alvo, objetivos_atividade_extensao, descricao_atividade_extensao, avaliacao_atividade_extensao

"""
Grupo social alvo da atividade
Esta atividade deverá ser voltada para o público externo à Universidade, previamente delimitado pelo aluno e com aval do professor.
Objetivos da atividade
A atividade extensionista deverá ter caráter historiográfico, sob diversas formas, tais como: formação historiográfica de público- externo à universidade, formação continuada de professores da rede básica, atividades e organização de eventos culturais com temas históricos, atividades de preservação patrimonial, organização documental e direito à memória, podendo ser de caráter presencial ou remoto, de acordo com as definições institucionais e normas vigentes na Universidade.
Descrição da atividade
A disciplina também destinará 20 horas para o planejamento e desenvolvimento de práticas extensionistas, a serem computadas nas ACE constantes do Histórico Escolar do aluno. O desenvolvimento das atividades se fará sob tutoria de um docente e de monitorias pedagógicas, sendo avaliada conforme as regras vigentes para aprovação em disciplinas.
Indicadores de avaliação da atividade
Entrega de relatório final e sistematização da avaliação pelo grupo social envolvido e pelo aluno, conforme modelo padronizado pelo Departamento de História e indicadores previamente definidos pela Universidade (aproveitamento, presença e ampliação do conhecimento historiográfico e da história aplicada a demandas sócio- culturais).

"""


def cria_csvs():
    with open("outputs\\unidades\\unidades.csv", "w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["codigo_unidade", "nome_unidade"])


    with open("outputs\\departamentos\\departamentos.csv", "w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["codigo_departamento", "nome_departamento", "codigo_unidade_CH_E"])


    with open("outputs\\docentes\\docentes.csv", "w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["codigo_docente", "nome_docente"])


    with open("outputs\\disciplinas\\disciplinas.csv", "w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["codigo_disciplina", "nome_disciplina", "nome_disciplina_ingles", "ativacao_disciplina", "desativacao_disciplina", "codigo_departamento_CH_E"])

    
    with open("outputs\\habilitacoes\\habilitacoes.csv", "w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["codigo_habilitacao", "nome_habilitacao", "periodo_habilitacao",
                        "duracao_minima", "duracao_maxima", "duracao_ideal",
                        "carga_horaria_obrigatoria_aula", "carga_horaria_obrigatoria_trabalho",
                        "carga_horaria_opt_eletiva_aula", "carga_horaria_opt_eletiva_trabalho",
                        "carga_horaria_opt_livre_aula", "carga_horaria_opt_livre_trabalho",
                        "carga_horaria_extensao", "codigo_unidade"])
        
    with open("outputs\\docentes_disciplina\\docentes_disciplina.csv", "w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["codigo_docentes", "codigo_disciplina"])
