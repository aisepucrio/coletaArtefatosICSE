import fitz  
import os
import shutil
from PIL import Image
import numpy as np
from io import BytesIO

def imagens_sao_semelhantes(img1_path, img2_bytes, threshold=20):
    img1 = Image.open(img1_path).convert('RGB')
    img2 = Image.open(BytesIO(img2_bytes)).convert('RGB')

    img1 = img1.resize((100, 100))
    img2 = img2.resize((100, 100))

    arr1 = np.array(img1).astype('float')
    arr2 = np.array(img2).astype('float')

    diff = np.mean(np.abs(arr1 - arr2))
    return diff < threshold


pasta_principal = r'extrair_imagens\ICSE-Research2025-6Z5izsaAA5CxoRqJH3Bidb' 
pasta_destino = r'extrair_imagens\pdfs_com_selo'  
pasta_icones = r'extrair_imagens\img'  

icones = [
    os.path.join(pasta_icones, 'verde.jpeg'),
    os.path.join(pasta_icones, 'vermelho.jpeg'),
    os.path.join(pasta_icones, 'rosa.jpeg')
]


os.makedirs(pasta_destino, exist_ok=True)


for root, dirs, files in os.walk(pasta_principal):
    for file in files:
        if file.lower().endswith('.pdf'):
            pdf_path = os.path.join(root, file)
            doc = fitz.open(pdf_path)

            encontrou_selo = False

            print(f'\n -- Analisando PDF: {file}')

            page = doc[0]
            imagens = page.get_images(full=True)

            if imagens:
                print(f' - Página 1: {len(imagens)} imagem(ns) encontrada(s)')
            else:
                print(f' - Página 1: nenhuma imagem encontrada')

            for img in imagens:
                xref = img[0]
                base_image = doc.extract_image(xref)
                image_bytes = base_image["image"]

                for icone_path in icones:
                    if imagens_sao_semelhantes(icone_path, image_bytes):
                        encontrou_selo = True
                        break

                if encontrou_selo:
                    break

            if encontrou_selo:
                shutil.copy(pdf_path, pasta_destino)
                print(f'PDF copiado para {pasta_destino}')
            else:
                print('Nenhum selo encontrado nesse PDF .')
