# Extrator de Links e Metadados de para coleta dos artefatos dos artigos do ICSE.

## Arquivos

### 1. `links_pdf/extracao_links.py`

Este script é responsável por extrair links de artigos científicos a partir de arquivos PDF. Ele identifica links tanto no corpo principal do artigo quanto nas referências (antes e depois da seção `REFERENCES`).

- **Funções principais:**
  - `extrair_links_pdf(caminho_pdf)`: Abre um PDF e extrai os links de artigos hospedados nas plataformas Figshare, GitHub e Zenodo.
  
- **Entrada:**
  - Um arquivo PDF (por exemplo, `artigo.pdf`).

- **Saídas:**
  - Um arquivo CSV (`links_extraidos.csv`) com os links encontrados no artigo.
  - Um arquivo JSON (`links_extraidos.json`) com a mesma informação.

### 2. `links_pdfzao/extracao_links.py`

Este script é semelhante ao anterior, mas é mais complexo.
Ao invés de extrair os arquivos de um artigo, ele recebe um pdf com vários artigos, um abaixo do outro e com base em um csv que contém os titulos dos arquivos, ele pega os links de cada artigo separadamente.

### 3. `scrapping_acm/scrapping_firefox.py`

Este script usa o Selenium para fazer scraping dos artigos da ACM, especificamente das edições da conferência ICSE (International Conference on Software Engineering). Ele busca informações como título, DOI e badges (indicando disponibilidade e funcionalidade dos artefatos).

- **Funções principais:**
  - `open_close_session(elemento, heading_id)`: Expande ou recolhe sessões no site.
  - `get_metadata(year)`: Extrai metadados como título, DOI e informações sobre artefatos.
  - `accept_cookies()`: Aceita o pop-up de cookies no site.
  - `load_sessions()`: Carrega todas as sessões de artigos na página.
  
- **Entrada:**
  - URL de uma conferência específica, como o ICSE 2024.

- **Saídas:**
  - Um arquivo CSV (`<ano>acm_articles.csv`) contendo as informações extraídas.

### 4. `scrapping_2025icse.py`

Este script usa a biblioteca BeautifulSoup para fazer scraping da página do ICSE 2025, extraindo títulos de artigos, autores e informações sobre artefatos disponíveis.

- **Funções principais:**
  - O script busca por uma tabela específica na página e extrai as informações dos artigos.

- **Saídas:**
  - Um arquivo CSV (`icse2025_artifacts.csv`) contendo os títulos dos artigos, autores e a informação sobre a disponibilidade de artefatos.

### 5. `une_csv.py`

Este script combina os dados extraídos dos scripts de scraping e de PDF em um único arquivo CSV. Ele também gera um arquivo JSON formatado com as informações unificadas.

- **Funções principais:**
  - `unir_csvs_e_gerar_json_formatado(csv_links_path, csv_artifacts_path, csv_saida, json_formatado_saida)`: Combina dois arquivos CSV (um com links e outro com artefatos) em um arquivo CSV unificado e gera um arquivo JSON.

- **Saídas:**
  - Um arquivo CSV unificado com informações combinadas.
  - Um arquivo JSON formatado com os dados extraídos.

## Requisitos

- Python 3.6+
- Bibliotecas Python:
  - `fitz` (PyMuPDF)
  - `re`
  - `csv`
  - `json`
  - `selenium`
  - `beautifulsoup4`
  - `requests`
