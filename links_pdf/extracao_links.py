import fitz 
import re
import csv
import os
import json

def extrair_links_pdf(caminho_pdf):
    documento = fitz.open(caminho_pdf)

    texto = ''
    for pagina in documento:
        texto += pagina.get_text()

    ponto_referencia = re.search(r'\bREFERENCES\b', texto)
    
    if ponto_referencia:
        inicio_references = ponto_referencia.start()
        texto_antes = texto[:inicio_references]
        texto_depois = texto[inicio_references:]
    else:
        texto_antes = texto
        texto_depois = ''

    padrao = r'(https?://(?:www\.)?(?:figshare\.com|github\.com|zenodo\.org)[^\s\)\]\}"]+)'

    links_artigo = re.findall(padrao, texto_antes)
    links_referencias = re.findall(padrao, texto_depois)

    documento.close()

    return links_artigo, links_referencias

caminho_pdf = r'links_pdf\artefato2.pdf'
nome_pdf = os.path.basename(caminho_pdf)

links_antes, links_depois = extrair_links_pdf(caminho_pdf)

if links_antes or links_depois:
    print('\nLinks encontrados no artigo')
    for link in links_antes:
        print(link)

    print('\nLinks encontrados nas referências')
    for link in links_depois:
        print(link)

    print("\n")
else:
    print('Nenhum link encontrado.')

with open('links_extraidos.csv', mode='w', newline='', encoding='utf-8') as arquivo_csv:
    writer = csv.DictWriter(arquivo_csv, fieldnames=["PDF", "Links_antes_REFERENCES", "Links_depois_REFERENCES"])
    writer.writeheader()

    writer.writerow({
        "PDF": nome_pdf,
        "Links_antes_REFERENCES": ';'.join(links_antes),
        "Links_depois_REFERENCES": ';'.join(links_depois)
    })

dados = [{
    "PDF": nome_pdf,
    "Links_antes_REFERENCES": links_antes,
    "Links_depois_REFERENCES": links_depois
}]

with open('links_extraidos.json', 'w', encoding='utf-8') as f:
    json.dump(dados, f, indent=2, ensure_ascii=False)