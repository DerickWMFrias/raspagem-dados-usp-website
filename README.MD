# Scripts de raspagem JupiterWeb

  Este são scripts de raspagem web das páginas da aba pública do site Jupiterweb, site da Universidade de São Paulo. Os dados aqui raspados são referentes aos institutos, cursos, habilitações, departamentos e disciplinas da USP; Em suma, o que desejo ter raspado ao final deste projeto são os seguintes dados:
  - Dados de todos os institutos da USP 
  - Dados e grade horária de todos os cursos da USP 
  - Dados de todas as habilitações da USP
  - Dados de todos os departamentos da USP
  - Dados de todas as disciplinas da USP

  Minha finalidade com isso é montar algumas bases de dados estruturas com estas informações públicas da universidade, e quem sabe futuramente desenvolver algo a partir destes dados.

  Até agora, não executei os scripts por cima de todas páginas da parte pública do JupiterWeb, portanto alguns erros no percurso ainda podem ocorrer. Debugar este programa exige um tanto de empirismo, como é comum em raspagens web, então isto ainda vai levar um tempo.

## Links base e badlinks.txt

  Ao longo deste projeto você verá uma série de 'Links base'. O que quero dizer com isso é que estes links são a página web de referência do que está sendo dito em contexto - seja em algum texto, ou seja em algum trecho de código - e portanto estes links devem ser acessados para que você melhor compreenda o que está sendo descrito ou feito nestes textos e códigos. Ou seja, estes links são para que você tenha base, contexto, do que está acontecendo. Quando encontrar um link base, recomendo a você acessa-lo, vasculha-lo e também inspecionar a página, e isto te dará contexto suficiente para entender o que for necessário.

  O arquivo badlinks.txt contém alguns links de páginas que por algum acaso não contém nenhum dados raspável quado deveriam conter, ou que geram alguma excessão aos scripts de raspagem.
     
## Descrição dos scripts
  
  scrap_cursos_usp.py: Script que raspa quais são e quais as informações gerais dos cursos que cada instituto da USP oferece.
  (Link base:https://uspdigital.usp.br/jupiterweb/jupCarreira.jsp?codmnu=8275)
        
  scrap_disciplinas.py: Script que raspa quais são e as informações de todas as disciplinas da USP, e quais disciplinas são pertencentes a grade de cada curso.
  (Link base: https://uspdigital.usp.br/jupiterweb/jupColegiadoLista?tipo=D)

## Descrição dos dados

  Os dados estão descritos na README.md do subdiretório '/outputs'.

## Estrutura de diretórios
    
  outputs -> Diretório para qual se direcionam todos os arquivos gerados por este script de raspagem.
    
  utils -> Diretório para organizar as funções escritas para este programa.
