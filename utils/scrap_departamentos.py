import csv
import json
import copy
from datetime import datetime
from urllib.parse import urlparse, parse_qs

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import pyautogui
import time
import requests


from utils.util_funcs import get_href_selenium, scrape_extensao, scrape_objetivos, scrape_programa, scrape_avaliacao, is_in_bad_links


buffer_info_disciplinas = []
counter_jsons = 1
counter_disciplinas_json = 0


buffer_grades_curriculares = []
counter2 = 1
counter_grades_json = 0



buffer_requisitos = []
counter3 = 1
counter_requisitos_json = 0



buffer_infos_especificas = []
counter4 = 1
counter_infos_json = 0



def scrape_infos_disciplina(driver, lnk_disciplina, codigo_departamento, codigo_disciplina, nome_disciplina, ativacao_disciplina, desativacao_disciplina):
    driver.get(lnk_disciplina)
    print(f"Scrape_infos_disciplina: At link: {lnk_disciplina}\n")
    time.sleep(1)

    table_contents = driver.find_element(By.XPATH, "(//div[@id='layout_conteudo']/table)[1]")

    table_infos = table_contents.find_element(By.XPATH, ".//tbody/tr[4]/td/form/table[1]")
    tables = table_infos.find_elements(By.XPATH, ".//tbody/tr[1]/td/table")

    table_extensao = []
    try:
        #print("Essa disciplina TEM conteudo de extensao")
        table_extensao = table_contents.find_element(By.XPATH, ".//tbody/tr[4]/td/form/table[2]")
    except:
        table_extensao = []

    global buffer_info_disciplinas
    global counter_disciplinas_json
    global counter_jsons

    objetivos_disciplina = ""
    nome_docentes = [] 
    codigo_docentes = []
    programa_disciplina = ""
    programa_resumido_disciplina = ""
    metodo_avaliacao = "" 
    criterio_avaliacao = "" 
    recuperacao_avaliacao = ""
    bibliografia_disciplina = ""

    grupo_social_alvo_extensao = "" 
    objetivos_atividade_extensao = ""
    descricao_atividade_extensao = "" 
    avaliacao_atividade_extensao = ""


    nome_disciplina_ingles = driver.find_element(By.XPATH, "//div[@id='layout_conteudo']/table[1]/tbody/tr[4]/td/form/table[1]/tbody/tr[1]/td/table[3]/tbody/tr[6]/td/font/span")
    nome_disciplina_ingles = nome_disciplina_ingles.text

    #unidade_disciplina, departamento_disciplina, nome_disciplina, nome_disciplina_ingles = scrape_cabecalho(tables[2])
    #creditos_aula_disciplina, creditos_trabalho_disciplina, carga_horaria_disciplina, tipo_disciplina = scrape_creditos(tables[3].text)
    
    if table_extensao:
         grupo_social_alvo_extensao, objetivos_atividade_extensao, descricao_atividade_extensao, avaliacao_atividade_extensao = scrape_extensao(table_extensao.text)

    for i in range(4, len(tables)):
        if tables[i].text.startswith("Objetivos") and objetivos_disciplina == "":
            objetivos_disciplina = scrape_objetivos(tables[i].text)

        if tables[i].text.startswith("Docent") and nome_docentes == []:
            #print("DOCENTES\n")
            table = tables[i].find_element(By.TAG_NAME, "table")
            rows_docentes = table.find_elements(By.TAG_NAME, "tr")
            #rows_docentes = rows_docentes[1:]

            for row in rows_docentes:
                text_to_scrape = row.text

                aux = text_to_scrape.split()
                aux_id = aux[0]
                aux_docente = ' '.join(aux[2:])

                #print(f"    Docente: {aux_id} - {aux_docente}")
                nome_docentes.append(aux_docente)
                codigo_docentes.append(aux_id)
            #print("\n")

        if tables[i].text.startswith("Programa") and programa_disciplina == "":
            programa_disciplina, programa_resumido_disciplina = scrape_programa(tables[i].text)


        if tables[i].text.startswith("Método") and metodo_avaliacao == "":
            metodo_avaliacao, criterio_avaliacao, recuperacao_avaliacao = scrape_avaliacao(tables[i].text)


        if tables[i].text.startswith("  Bibliografia") and bibliografia_disciplina == "" and i+1 < len(tables):
            bibliografia_disciplina = tables[i+1].text



    infos_disciplina= {
        "codigo_disciplina": codigo_disciplina,
        "objetivos_disciplina": objetivos_disciplina,
        "programa_disciplina": programa_disciplina,
        "programa_resumido_disciplina": programa_resumido_disciplina,
        "metodo_avaliacao": metodo_avaliacao,
        "criterio_avaliacao": criterio_avaliacao,
        "recuperacao_avaliacao": recuperacao_avaliacao,
        "bibliografia_disciplina": bibliografia_disciplina,
        "grupo_social_alvo_extensao": grupo_social_alvo_extensao,
        "objetivos_atividade_extensao": objetivos_atividade_extensao,
        "descricao_atividade_extensao": descricao_atividade_extensao,
        "avaliacao_atividade_extensao": avaliacao_atividade_extensao
    }

    buffer_info_disciplinas.append(infos_disciplina)
    counter_disciplinas_json += 1

    if counter_disciplinas_json == 500:
        print("-------------DUMPING-DISCIPLINAS---------------")
        name_json = "outputs\\texto_disciplinas\\texto_disciplinas_" + str(counter_jsons) + ".json"

        with open(name_json, "w", encoding="utf-8") as file:
            json.dump(buffer_info_disciplinas, file, indent=4, ensure_ascii=False)
        
        buffer_info_disciplinas = []
        counter_jsons = counter_jsons + 1
        counter_disciplinas_json = 0
    


    with open("outputs\\docentes\\docentes.csv", "a", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        for i in range(len(nome_docentes)):
            writer.writerow([codigo_docentes[i], nome_docentes[i]])


    with open("outputs\\docentes_disciplina\\docentes_disciplina.csv", "a", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        for i in range(len(nome_docentes)):
            writer.writerow([codigo_docentes[i], codigo_disciplina])


    if desativacao_disciplina == "":
        desativacao_disciplina = "None"
    with open("outputs\\disciplinas\\disciplinas.csv", "a", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow([codigo_disciplina, nome_disciplina, nome_disciplina_ingles, ativacao_disciplina, desativacao_disciplina, codigo_departamento])


    print("INFORMAÇÕES DE DISCIPLINA")
    print(f"        DEPT: {codigo_departamento}")
    print(f"        CODI: {codigo_disciplina}")
    print(f"        NOME: {nome_disciplina}\n")
    print("***********************************************\n")
    #print(f"        NAME: {nome_disciplina_ingles}")    
    #print(f"        ATIV: {ativacao_disciplina}")  
    #print(f"        DETV: {desativacao_disciplina}")  
    
    #print(f"        OBJT: {objetivos_disciplina}")
    #print(f"        PROG: {programa_disciplina}")
    #print(f"        PRES: {programa_resumido_disciplina}")

    #print(f"        METO: {metodo_avaliacao}")
    #print(f"        CRIT: {criterio_avaliacao}")
    #print(f"        RECU: {recuperacao_avaliacao}")

    #print(f"        BIBI: {bibliografia_disciplina}\n\n")


def scrape_pagina_disciplinas(driver, has_pag, link_pag, codigo_departamento, is_landing_page):
    #print(f"scape_pagina_disciplinas: At link: {link_pag}")
    #if has_pag:
    if not is_landing_page:
        driver.get(link_pag)
    time.sleep(1)


    print(f"scape_pagina_disciplinas: At link: {link_pag}\n")
    table_disciplinas = []

    try:
        table_disciplinas = driver.find_element(By.XPATH, "//div[@id='layout_conteudo']/table[1]")
    except:
        print("PAGE HAS NULL CONTENT!!")
        return        
    
    if has_pag:
            table_disciplinas = driver.find_element(By.XPATH, "//div[@id='layout_conteudo']/table[2]")


    disciplinas = table_disciplinas.find_elements(By.TAG_NAME, "tr")
    disciplinas = disciplinas[1:]

    print(f"Encontradas {len(disciplinas)} disciplinas\n")
    # for disciplina in disciplinas:
    #    print(f"{disciplina.text}")

    count_disciplina = 1

    disciplinas_data = []
    for disciplina in disciplinas:
        tds_disciplina = disciplina.find_elements(By.TAG_NAME, "td")

        anchor_disciplina = tds_disciplina[1].find_element(By.TAG_NAME, "a")
        lnk_disciplina = anchor_disciplina.get_attribute("href")

        codigo_disciplina = tds_disciplina[0].text
        nome_disciplina = tds_disciplina[1].text
        ativacao_disciplina = tds_disciplina[2].text
        desativacao_disciplina = tds_disciplina[3].text

        #print(f"Sigla {tds_disciplina[0].text} .. {tds_disciplina[1].text} .. Ativ {tds_disciplina[2].text} .. Desativ {tds_disciplina[3].text}")
        #print(f"Redirect link: {lnk_disciplina}\n")

        aux = [codigo_disciplina, nome_disciplina, ativacao_disciplina, desativacao_disciplina, lnk_disciplina]
        disciplinas_data.append(aux)


    for data in disciplinas_data:
        dtime = datetime.now().strftime("%H:%M:%S")
        print(f"{dtime}: Disciplina {count_disciplina}/{len(disciplinas)}")
        count_disciplina += 1
        scrape_infos_disciplina(driver, data[4], codigo_departamento, data[0], data[1], data[2], data[3])



def scrape_depts(driver, page, lnk, codigo_unidade_CH_E):
    driver.get(lnk)
    print(f"Scrape_depts: At link: {lnk}")
    time.sleep(1)

    lnk_disciplinas_departamentos = get_href_selenium(driver, By.XPATH, "(//div[@id='layout_conteudo']/table)[3]/tbody/tr[3]")
    driver.get(lnk_disciplinas_departamentos)
    print(f"Scrape_depts: At link: {lnk_disciplinas_departamentos}")
    time.sleep(1)


    table_departamentos = []
    try:
        table_departamentos = driver.find_element(By.XPATH, "(//div[@id='layout_conteudo']/table)[3]")
    except NoSuchElementException:
        print(f"Unidade {codigo_unidade_CH_E} não tem departamentos cadastrados!\n")
        return  # Exit the function early


    rows_departamentos = table_departamentos.find_elements(By.TAG_NAME, "tr")
    rows_departamentos = rows_departamentos[1:]

    departamento_data = []

    
    for departamento in rows_departamentos:
        tds_row = departamento.find_elements(By.TAG_NAME, "td")
        codigo_departamento = tds_row[0].text
        nome_departamento = tds_row[1].text

        with open("outputs\\departamentos\\departamentos.csv", "a", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow([codigo_departamento, nome_departamento, codigo_unidade_CH_E])

        anchor_to_lnk = departamento.find_element(By.TAG_NAME, "a")
        lnk_disciplina_curso = anchor_to_lnk.get_attribute("href")

        aux = [codigo_departamento, nome_departamento, lnk_disciplina_curso]

        departamento_data.append(aux)


    for departamento in departamento_data:
        print(f"Departamento: {departamento[1]}  Link: {departamento[2]}")

    for data in departamento_data:
        driver.get(data[2])
        print(f"Scrape_depts: Acessando lista disciplinas at link: {data[2]}")
        time.sleep(1)

        first_td = []
        try:
            first_td = driver.find_element(By.XPATH, "//div[@id='layout_conteudo']/table[1]/tbody/tr")
        except NoSuchElementException:
            print(f"Departamento {data[1]} não possui disciplinas associadas a ele")
            continue
        

        anchors_to_pagination_links = first_td.find_elements(By.TAG_NAME, "a")

        pagination_links = []
        has_pagination = False

        if anchors_to_pagination_links:
            #print(f"This page has {len(pagination_links)} pagination links!")
            anchors_to_pagination_links = anchors_to_pagination_links[1:]
            has_pagination = True
        
        for anchor in anchors_to_pagination_links:
            pagination_link = anchor.get_attribute("href")
            pagination_links.append(pagination_link)


        #print("\n*****Acessando landing disciplina*****\n")
        scrape_pagina_disciplinas(driver, has_pagination, data[2], data[0], True)#tem que pegar todas as disciplinas da pagina

        #time.sleep(5)
        for pag_link in pagination_links:
            #print("\n*****Acessando paginação disciplina*****\n")
            scrape_pagina_disciplinas(driver, has_pagination, pag_link, data[0], False)
            





def scrape_grade_curricular(driver, semestres_curso, codigo_curriculo, codigo_habilitacao, c_grade):
    table_grade_curricular = driver.find_element(By.XPATH, f"//div[@id='layout_conteudo']/table[1]/tbody/tr[4]/td/form/table/tbody/tr[1]/td/table[{c_grade}]/tbody/tr/td/table")
                                  
    rows_grade_curricular = table_grade_curricular.find_elements(By.XPATH, "./tbody/tr")

    global counter3
    global counter_requisitos_json
    global buffer_requisitos

    periodo = -1
    tipo_disciplina = "disciplinas_obrigatorias"
    
    array_grade_template = []
    for i in range(int(semestres_curso)):
        array_grade_template.append([])

    grade = {"disciplinas_obrigatorias": copy.deepcopy(array_grade_template),
             "disciplinas_eletivas": copy.deepcopy(array_grade_template),
             "disciplinas_livres": copy.deepcopy(array_grade_template)}
    

    for i in range(len(rows_grade_curricular)):
        if rows_grade_curricular[i].text.endswith("Requisito") or rows_grade_curricular[i].text.endswith("fraco"):
            forca_requisito = "forte"
            if rows_grade_curricular[i].text.endswith("fraco"):
                forca_requisito = "fraco"

            id_last_discipline_searched = rows_grade_curricular[i-1].text.split()[0]

            id_requisito = rows_grade_curricular[i].text.split()
            id_requisito = id_requisito[0]
        
            json_requisito = {
                "codigo_curriculo": codigo_curriculo,
                "codigo_habilitacao": codigo_habilitacao,
                "codigo_disciplina": id_last_discipline_searched,
                "codigo_requisito": id_requisito,
                "forca_requisito": forca_requisito
            }
            #print(f"Requisito de {id_last_discipline_searched}: {id_requisito} (Curriculo {codigo_curriculo})")


            buffer_requisitos.append(copy.deepcopy(json_requisito))
            counter_requisitos_json = counter_requisitos_json + 1
            #print(f"counter_requisitos_json: {counter_requisitos_json}")

            if counter_requisitos_json  == 5000:
                print("-------------DUMPING-REQUISITOS---------------")
                name_json = "outputs\\requisitos\\requisitos_disciplinas_" + str(counter3) + ".json"
                print(f"nm: {name_json}")

                with open(name_json, "w", encoding="utf-8") as file:
                    json.dump(buffer_requisitos, file, indent=4, ensure_ascii=False)

                buffer_requisitos = []
                counter_requisitos_json = 0
                counter3 = counter3 + 1

    id_last_discipline_searched = "None"
    cc = 0 
    for row in rows_grade_curricular:
        #print(f"row {cc}:|{row.text}|")
        #print(f"row {cc} |{repr(row.text.strip())}|")
        cc += 1

        if row.text == "" or row.text.startswith("Subtotal") or  row.text.startswith(" "):
            #print("----------------")
            continue
                    
        elif row.find_elements(By.TAG_NAME, "a"):
            #é uma disciplina
            colums = row.find_elements(By.TAG_NAME, "td")

            dictionary = {
                    "codigo_disciplina": colums[0].text,
                    "nome_disciplina": colums[1].text,
                    "cred_aula_disciplina": colums[2].text,
                    "cred_trabalho_disciplina": colums[3].text,
                    "carga_horaria_total": colums[4].text,
                    "carga_horaria_estagio": colums[5].text,
                    "carga_horaria_praticas": colums[6].text,
                    "carga_horaria_ATPA": colums[7].text,
                    "carga_horaria_extensionista": colums[8].text
                }
            

            if colums[5].text == "":
                dictionary["carga_horaria_estagio"] = "0"
            if colums[6].text == "":
                dictionary["carga_horaria_praticas"] = "0"
            if colums[7].text == "":
                dictionary["carga_horaria_ATPA"] = "0"
            if colums[8].text == "":
                dictionary["carga_horaria_extensionista"] = "0"


            id_last_discipline_searched = colums[0].text

            #print(f"Adicionando disciplina {dictionary["sigla_disciplina"]} {dictionary['nome_disciplina']} na grade {tipo_disciplina} no {periodo+1}")

            grade[tipo_disciplina][periodo].append(dictionary)

        elif row.text.startswith("Disciplinas Obrigatórias"):
            periodo = -1
            tipo_disciplina = "disciplinas_obrigatorias"

        elif row.text.startswith("Disciplinas Optativas Eletivas"):
            periodo = -1
            tipo_disciplina = "disciplinas_eletivas"
        
        elif row.text.startswith("Disciplinas Optativas Livres"):
            periodo = -1
            tipo_disciplina = "disciplinas_livres"

        elif ord("0") <= ord(row.text[0]) <= ord("9"):
            #É um período
            periodo = int(row.text[0])-1
            #print(f"Escrevendo em {tipo_disciplina} {periodo}")
            #print(f"{row.text[0]}     {row.text[1]}")
            if not row.text[1] == "º":
                periodo = int(row.text[0:2])-1

            #print(f"Escrevendo em {tipo_disciplina} {periodo}")
        else:
            print("Weird row found")

        #print("----------------")

    return grade




def scrape_url_info_curso(url):
    parsed_url = urlparse(url)
    query_params = parse_qs(parsed_url.query)

    # Extract values
    codcg = query_params.get("codcg", [None])[0]
    codcur = query_params.get("codcur", [None])[0]
    codhab = query_params.get("codhab", [None])[0]

    return codcg, codcur, codhab



def scrape_info_curso(driver, lnk, nome_habilitacao, periodo_habilitacao, codigo_unidade):
    driver.get(lnk)
    time.sleep(1)
    print(f"Scrape_info_curso: At link: {lnk}")

    if is_in_bad_links(lnk):
        print("THIS COURSE IS IN BAD_LINKS LIST! GO CHECK IT YOURSELF :)\n")
        return

    global counter2
    global counter4

    global counter_grades_json
    global counter_infos_json
    global counter_requisitos_json

    global buffer_grades_curriculares
    global buffer_infos_especificas
    global buffer_requisitos

    tables_interesse = driver.find_elements(By.XPATH, "//div[@id='layout_conteudo']/table[1]/tbody/tr[4]/td/form/table/tbody/tr[1]/td/table")

    print(f"FOUND {len(tables_interesse)} ELEMENTS!!")
    #time.sleep(3)
    c = 1
    c_duracao_curso = 0
    c_infos_especificas = 0
    c_grade = 0
    for tables in tables_interesse:
        if tables.text.startswith("Data de"):   
            c_duracao_curso = c
            print(f"C de duracao: {c_duracao_curso}")
        if tables.text.startswith("Informações Específicas"):  
            c_infos_especificas = c
            print(f"C de infos: {c_infos_especificas}")
        if tables.text.startswith("Disciplinas Obrigatórias"):  
            c_grade = c
            print(f"C de grade: {c_grade}")
        c += 1

    if not c_infos_especificas:
        print("BAD LINK FOUND!!\n")
        with open("badlinks.txt", "a", encoding="utf-8") as file:
            file.write(f" {lnk}")
        return

    table_duracao_ideal = driver.find_element(By.XPATH, f"//div[@id='layout_conteudo']/table[1]/tbody/tr[4]/td/form/table/tbody/tr[1]/td/table[{c_duracao_curso}]/tbody/tr[1]")
    table_duracao_minima = driver.find_element(By.XPATH, f"//div[@id='layout_conteudo']/table[1]/tbody/tr[4]/td/form/table/tbody/tr[1]/td/table[{c_duracao_curso}]/tbody/tr[2]")
    table_duracao_maxima = driver.find_element(By.XPATH, f"//div[@id='layout_conteudo']/table[1]/tbody/tr[4]/td/form/table/tbody/tr[1]/td/table[{c_duracao_curso}]/tbody/tr[3]")

    duracao_minima = table_duracao_minima.text #!
    duracao_minima = duracao_minima.split()
    duracao_minima = duracao_minima[1]

    duracao_maxima = table_duracao_maxima.text #!
    duracao_maxima = duracao_maxima.split()
    duracao_maxima = duracao_maxima[1]

    duracao_ideal = table_duracao_ideal.text
    duracao_ideal = duracao_ideal.split()
    duracao_ideal = duracao_ideal[len(duracao_ideal) - 2]
    

    row_carga_obrigatoria_total = driver.find_element(By.XPATH, "//table[@id='tabelaCargaHoraria']/tbody/tr[2]")
    text_carga_obrigatoria = row_carga_obrigatoria_total.text
    text_carga_obrigatoria = text_carga_obrigatoria.split()
    carga_horaria_obrigatoria_aula = text_carga_obrigatoria[1]#!
    carga_horaria_obrigatoria_trabalho = text_carga_obrigatoria[2]#!


    row_carga_opt_livre_total = driver.find_element(By.XPATH, "//table[@id='tabelaCargaHoraria']/tbody/tr[3]")
    text_carga_opt_livre = row_carga_opt_livre_total.text
    text_carga_opt_livre = text_carga_opt_livre.split()
    carga_horaria_opt_livre_aula = text_carga_opt_livre[2]#!
    carga_horaria_opt_livre_trabalho = text_carga_opt_livre[3]#!

    row_carga_opt_eletiva_total = driver.find_element(By.XPATH, "//table[@id='tabelaCargaHoraria']/tbody/tr[4]")
    text_carga_opt_eletiva = row_carga_opt_eletiva_total.text
    text_carga_opt_eletiva = text_carga_opt_eletiva.split()
    carga_horaria_opt_eletiva_aula = text_carga_opt_eletiva[2]#!
    carga_horaria_opt_eletiva_trabalho = text_carga_opt_eletiva[3]#!


    row_carga_extencao_total = driver.find_element(By.XPATH, "//table[@id='tabelaCargaHoraria']/tbody/tr[7]")
    carga_horaria_extensao = row_carga_extencao_total.text.split()
    carga_horaria_extensao = carga_horaria_extensao[8]#!
    
    table_infos_especificas = driver.find_element(By.XPATH, f"//div[@id='layout_conteudo']/table[1]/tbody/tr[4]/td/form/table/tbody/tr[1]/td/table[{c_infos_especificas}]")
    infos_especificas = table_infos_especificas.text#!


    #print(f"codigo_habilitacao: {codigo_habilitacao}")



    codigo_unidade, codigo_curriculo, codigo_habilitacao = scrape_url_info_curso(lnk)

    grade_curricular = scrape_grade_curricular(driver, duracao_ideal, codigo_curriculo, codigo_habilitacao, c_grade)

    #codigo_habilitacao #CH_E
    #codigo_curriculo 
    #grade_curricular #json stuff
    json_grade = {
        "link": lnk,
        "codigo_curriculo": codigo_curriculo,
        "codigo_habilitacao": codigo_habilitacao,
        "grade_curricular": grade_curricular
    }

    buffer_grades_curriculares.append(json_grade)
    counter_grades_json = counter_grades_json + 1
    #print(f"counter_grades_json: {counter_grades_json}")

    if counter_grades_json == 500:
        print("-------------DUMPING-GRADES---------------")
        name_json = "outputs\\grades\\grades_curriculares_" + str(counter2) + ".json"

        with open(name_json, "w", encoding="utf-8") as file:
            json.dump(buffer_grades_curriculares, file, indent=4, ensure_ascii=False)

        buffer_grades_curriculares = []
        counter_grades_json = 0
        counter2 = counter2 + 1


    json_infos = {
        "link": lnk,
        "codigo_curriculo": codigo_curriculo,
        "codigo_habilitacao": codigo_habilitacao,
        "informações_específicas": infos_especificas
    }

    buffer_infos_especificas.append(json_infos)
    counter_infos_json += 1
    #print(f"counter_infos_json: {counter_infos_json}")

    if counter_infos_json == 500:
        print("-------------DUMPING-INFOS---------------")
        name_json = "outputs\\infos\\informacoes_especificas_habilitacao_" + str(counter4) + ".json"

        with open(name_json, "w", encoding="utf-8") as file:
            json.dump(buffer_infos_especificas, file, indent=4, ensure_ascii=False)

        buffer_infos_especificas = []
        counter_infos_json = 0
        counter4 = counter4 + 1


    with open("outputs\\habilitacoes\\habilitacoes.csv", "a", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow([codigo_habilitacao, nome_habilitacao, periodo_habilitacao,
                        duracao_minima, duracao_maxima, duracao_ideal,
                        carga_horaria_obrigatoria_aula, carga_horaria_obrigatoria_trabalho,
                        carga_horaria_opt_eletiva_aula, carga_horaria_opt_eletiva_trabalho,
                        carga_horaria_opt_livre_aula, carga_horaria_opt_livre_trabalho,
                        carga_horaria_extensao, codigo_unidade])
        
    print(f"\n\nnome_habilitacao: {nome_habilitacao}")
    print(f"    periodo_habilitacao: {periodo_habilitacao}")

    print(f"    duracao_minima: {duracao_minima}")
    print(f"    duracao_maxima: {duracao_maxima}")
    print(f"    duracao_ideal: {duracao_ideal}")

    print(f"    carga_horaria_obrigatoria_aula: {carga_horaria_obrigatoria_aula}")
    print(f"    carga_horaria_obrigatoria_trabalho: {carga_horaria_obrigatoria_trabalho}")

    print(f"    carga_horaria_opt_eletiva_aula: {carga_horaria_opt_eletiva_aula}")
    print(f"    carga_horaria_opt_eletiva_trabalho: {carga_horaria_opt_eletiva_trabalho}")

    print(f"    carga_horaria_opt_livre_aula: {carga_horaria_opt_livre_aula}")
    print(f"    carga_horaria_opt_livre_trabalho: {carga_horaria_opt_livre_trabalho}")

    print(f"    carga_horaria_extensao: {carga_horaria_extensao}")
    print(f"    codigo_unidade: {codigo_unidade}\n\n")
    #print(f"    Infos especificas:\n{infos_especificas}\n")

    print(f"        COUNTER REQUISITOS: {counter_requisitos_json}")
    print(f"        COUNTER GRADES: {counter_grades_json}")
    print(f"        COUNTER INFOS: {counter_infos_json}\n\n")
        
    



def scrape_cursos(driver, page, lnk, codigo_unidade):
    driver.get(lnk)
    print(f"Scrape_cursos: At link: {lnk}")
    time.sleep(1)

    lnk_cursos_habilitacoes_unidade = get_href_selenium(driver, By.XPATH, "(//div[@id='layout_conteudo']/table)[3]/tbody/tr[1]")
    print(f"Scrape_cursos: At link: {lnk_cursos_habilitacoes_unidade}")
    driver.get(lnk_cursos_habilitacoes_unidade)
    time.sleep(1)

    table_cursos = []
    try:
        table_cursos = driver.find_element(By.XPATH, "//div[@id='layout_conteudo']/table[3]")
    except NoSuchElementException:
        print(f"Unidade {codigo_unidade} não tem cursos cadastrados!")
        return  # Exit the function early
    

    rows_cursos = table_cursos.find_elements(By.TAG_NAME, "tr")
    rows_cursos = rows_cursos[1:]

    curso_data = []

    for curso in rows_cursos:
        #print("------------------------------------------------")
        #print(curso.get_attribute("outerHTML"))
        #print("------------------------------------------------\n\n")
        tds_curso = curso.find_elements(By.TAG_NAME, "td")
        nome_habilitacao = tds_curso[0].text #!
        periodo_habilitacao = tds_curso[1].text #!

        anchor_to_lnk = curso.find_element(By.TAG_NAME, "a")
        lnk_curso = anchor_to_lnk.get_attribute("href")

        aux = [nome_habilitacao, periodo_habilitacao, lnk_curso]
        curso_data.append(aux)


    for curso in curso_data:
        scrape_info_curso(driver, curso[2], curso[0], curso[1], codigo_unidade)

        #driver.get(lnk_cursos_habilitacoes_unidade)
        #print(f"At link: {lnk_cursos_habilitacoes_unidade}")
        #time.sleep(1)
        


