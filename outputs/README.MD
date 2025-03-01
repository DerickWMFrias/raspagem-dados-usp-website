# Outputs

## Descrição de outputs por diretório

### Departamentos
  Dados raspados: codigo_departamento, nome_departamento, codigo_unidade_CH_E
  Tipo de arquivo: .csv
  Link base: https://uspdigital.usp.br/jupiterweb/jupDepartamentoLista?codcg=86&tipo=D
  Vindo do script: utils/scrap_departamentos
  Vindo da função: scrape_info_curso

### Disciplinas
  Dados raspados: codigo_disciplina, nome_disciplina, nome_disciplina_ingles, ativacao_disciplina, desativacao_disciplina, codigo_departamento
  Tipo de arquivo: .csv
  Link base: https://uspdigital.usp.br/jupiterweb/obterDisciplina?sgldis=ACH3867&verdis=1
  Vindo do script: utils/scrap_departamentos
  Vindo da função: scrape_infos_disciplinas

### Docentes
  Dados raspados: codigo_docente, nome_docente
  Tipo de arquivo: .csv
  Link base: https://uspdigital.usp.br/jupiterweb/obterDisciplina?sgldis=ACH3867&verdis=1
  Vindo do script: utils/scrap_departamentos
  Vindo da função: scrape_infos_disciplinas

### Docentes_disciplina
  Dados raspados: codigo_docente, codigo_disciplina
  Tipo de arquivo: .csv
  Link base: https://uspdigital.usp.br/jupiterweb/obterDisciplina?sgldis=ACH3867&verdis=1
  Vindo do script: utils/scrap_departamentos
  Vindo da função: scrape_infos_disciplinas

### Grades
  Dados raspados: link, codigo_curriculo, codigo_habilitacao, grade_curricular
  Tipo de arquivo: .json
  Link base: https://uspdigital.usp.br/jupiterweb/listarGradeCurricular?codcg=86&codcur=86551&codhab=200&tipo=N
  Vindo do script: utils/scrap_departamentos
  Vindo da função: scrape_info_curso

### Habilitações
  Dados raspados: codigo_habilitacao, nome_habilitacao, periodo_habilitacao, duracao_minima, duracao_maxima, duracao_ideal,carga_horaria_obrigatoria_aula, carga_horaria_obrigatoria_trabalho, carga_horaria_opt_eletiva_aula, carga_horaria_opt_eletiva_trabalho, carga_horaria_opt_livre_aula, carga_horaria_opt_livre_trabalho, carga_horaria_extensao, codigo_unidade
  Tipo de arquivo: .json
  Link base: https://uspdigital.usp.br/jupiterweb/listarGradeCurricular?codcg=86&codcur=86551&codhab=200&tipo=N
  Vindo do script: utils/scrap_departamentos
  Vindo da função: scrape_info_curso

### Infos
  Dados raspados: link, codigo_curriculo, codigo_habilitacao, infos_especificas
  Tipo de arquivo: .json
  Link base: https://uspdigital.usp.br/jupiterweb/listarGradeCurricular?codcg=86&codcur=86551&codhab=200&tipo=N
  Vindo do script: utils/scrap_departamentos
  Vindo da função: scrape_info_curso

### Requisitos
  Dados raspados: codigo_curriculo, codigo_habilitacao, id_last_discipline_searched, id_requisito, forca_requisito
  Tipo de arquivo: .json
  Link base: https://uspdigital.usp.br/jupiterweb/listarGradeCurricular?codcg=86&codcur=86551&codhab=200&tipo=N
  Vindo do script: utils/scrap_departamentos
  Vindo da função: scrape_grade_curricular

### Texto_disciplinas
  Dados raspados: codigo_disciplina, objetivos_disciplina, programa_disciplina, programa_resumido_disciplina, metodo_avaliacao, criterio_avaliacao, recuperacao_avaliacao,bibliografia_disciplina, grupo_social_alvo_extensao, objetivos_atividade_extensao, descricao_atividade_extensao, avaliacao_atividade_extensao
  Tipo de arquivo: .json
  Link base: https://uspdigital.usp.br/jupiterweb/obterDisciplina?sgldis=ACH3867&verdis=1
  Vindo do script: utils/scrap_departamentos
  Vindo da função: scrape_infos_disciplinas

### Unidades
  Dados raspados: Codigo Unidade; Nome Unidade
  Tipo de arquivo: .csv
  Link base: https://uspdigital.usp.br/jupiterweb/jupColegiadoLista?tipo=D
  Vindo do script: scrap_disciplinas.py
  Vindo da função: global scope