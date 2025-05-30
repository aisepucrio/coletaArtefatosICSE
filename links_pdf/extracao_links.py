import fitz 
import re

def extrair_links_pdf(caminho_pdf):
    documento = fitz.open(caminho_pdf)

    texto = ''
    for pagina in documento:
        texto += pagina.get_text()

    padrao = r'(https?://(?:www\.)?(?:figshare\.com|github\.com|zenodo\.org)[^\s\)\]\}"]+)'

    links = re.findall(padrao, texto)

    documento.close()

    return links


caminho_pdf = r'links_pdf\artefato2.pdf'

links = extrair_links_pdf(caminho_pdf)

if links:
    print('\nLinks encontrados:')
    for link in links:
        print(link)
    print("\n")
else:
    print('Nenhum link encontrado.')
