import fitz
import re
import csv
import json

def ler_titulos_csv(caminho_csv):
    titulos = []
    with open(caminho_csv, newline='', encoding='utf-8') as f:
        reader = csv.reader(f)
        for linha in reader:
            if linha:  # evita linhas vazias
                titulos.append(linha[0].strip())
    return titulos

def extrair_links_artigos_em_bloco(texto, titulos):
    artigos = []
    titulos_com_indices = []

    # Localiza a posição de cada título no texto
    for titulo in titulos:
        match = re.search(re.escape(titulo), texto)
        if match:
            titulos_com_indices.append((match.start(), titulo))

    titulos_com_indices.sort()

    for i, (inicio, titulo) in enumerate(titulos_com_indices):
        fim = titulos_com_indices[i+1][0] if i+1 < len(titulos_com_indices) else len(texto)
        bloco = texto[inicio:fim]

        # Divide por REFERENCES
        ponto_referencia = re.search(r'\bREFERENCES\b', bloco, re.IGNORECASE)
        if ponto_referencia:
            texto_antes = bloco[:ponto_referencia.start()]
            texto_depois = bloco[ponto_referencia.start():]
        else:
            texto_antes = bloco
            texto_depois = ''

        padrao = r'(https?://(?:www\.)?(?:figshare\.com|github\.com|zenodo\.org)[^\s\)\]\}"]+)'
        links_antes = re.findall(padrao, texto_antes)
        links_depois = re.findall(padrao, texto_depois)

        artigos.append({
            "Titulo": titulo,
            "Links_antes_REFERENCES": links_antes,
            "Links_depois_REFERENCES": links_depois
        })

    return artigos

# --------- EXECUÇÃO ---------

caminho_pdf = r'links_pdfzao/icse_2024.pdf'
caminho_csv_titulos = r'2024acm_articles.csv'

# 1. Lê os títulos do CSV
titulos_artigos = ler_titulos_csv(caminho_csv_titulos)

# 2. Extrai o texto do PDF
documento = fitz.open(caminho_pdf)
texto_completo = ''
for i, pagina in enumerate(documento):
    print(f'Lendo página {i + 1}/{len(documento)}...')
    texto_completo += pagina.get_text()
documento.close()

# 3. Extrai os links de cada artigo
dados_artigos = extrair_links_artigos_em_bloco(texto_completo, titulos_artigos)

# 4. Salva os dados em CSV
with open('links_artigos_divididos.csv', mode='w', newline='', encoding='utf-8') as arquivo_csv:
    writer = csv.DictWriter(arquivo_csv, fieldnames=["Titulo", "Links_antes_REFERENCES", "Links_depois_REFERENCES"])
    writer.writeheader()
    for artigo in dados_artigos:
        writer.writerow({
            "Title": artigo["Titulo"],
            "Links_antes_REFERENCES": ';'.join(artigo["Links_antes_REFERENCES"]),
            "Links_depois_REFERENCES": ';'.join(artigo["Links_depois_REFERENCES"])
        })

# 5. Salva os dados em JSON
with open('links_artigos_divididos.json', 'w', encoding='utf-8') as f:
    json.dump(dados_artigos, f, indent=2, ensure_ascii=False)
