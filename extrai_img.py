import fitz  # PyMuPDF
import os

# Abre o arquivo PDF
pdf_path  = r'links_pdf\artefato2.pdf'
doc = fitz.open(pdf_path)

# Cria uma pasta para salvar as imagens
os.makedirs("imagens_extraidas", exist_ok=True)

# Itera pelas páginas do PDF
for page_num in range(len(doc)):
    page = doc[page_num]
    imagens = page.get_images(full=True)

    print(f"Página {page_num + 1} tem {len(imagens)} imagem(ns).")

    for img_index, img in enumerate(imagens, start=1):
        xref = img[0]
        base_image = doc.extract_image(xref)
        image_bytes = base_image["image"]
        image_ext = base_image["ext"]

        # Salva a imagem extraída
        image_filename = f"imagens_extraidas/pag{page_num + 1}_img{img_index}.{image_ext}"
        with open(image_filename, "wb") as img_file:
            img_file.write(image_bytes)
        print(f"Imagem salva em: {image_filename}")
