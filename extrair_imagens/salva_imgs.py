import fitz  
import os

pasta_pdf = r'links_pdf' 
pasta_saida = r'extrair_imagens\imagens_selos'

os.makedirs(pasta_saida, exist_ok=True)


def extrair_e_salvar_imagens_primeira_pagina(pdf_path, nome_base):
    doc = fitz.open(pdf_path)

    contador = 1
    
    page = doc[0]
    imagens = page.get_images(full=True)

    print(f'\n📄 {os.path.basename(pdf_path)} - Página 1 - {len(imagens)} imagens encontradas')

    for img in imagens:
        xref = img[0]
        base_image = doc.extract_image(xref)
        image_bytes = base_image["image"]
        image_ext = base_image["ext"]

        image_filename = f"{nome_base}_pag1_img{contador}.{image_ext}"
        image_path = os.path.join(pasta_saida, image_filename)

        with open(image_path, "wb") as f:
            f.write(image_bytes)

        print(f'- Imagem {contador} salva em: {image_path}')
        contador += 1



for file in os.listdir(pasta_pdf):
    if file.lower().endswith('.pdf'):
        pdf_path = os.path.join(pasta_pdf, file)
        nome_base = os.path.splitext(file)[0]  
        extrair_e_salvar_imagens_primeira_pagina(pdf_path, nome_base)