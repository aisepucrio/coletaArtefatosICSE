import csv
import json

def unir_csvs_e_gerar_json_formatado(csv_links_path, csv_artifacts_path, csv_saida, json_formatado_saida):
    # Lê o CSV com informações de artefatos
    with open(csv_artifacts_path, newline='', encoding='utf-8') as f_artifacts:
        reader_artifacts = csv.DictReader(f_artifacts)
        dados_artifacts = {linha["Title"].strip(): linha for linha in reader_artifacts}

    # Lê o CSV com os links
    with open(csv_links_path, newline='', encoding='utf-8') as f_links:
        reader_links = csv.DictReader(f_links)
        dados_links = list(reader_links)

    # Colunas extras dos artifacts (menos Title)
    colunas_extras = [col for col in next(iter(dados_artifacts.values())).keys() if col != "Title"]

    # Cabeçalho completo para o CSV unificado
    cabecalho_csv = reader_links.fieldnames + colunas_extras

    dados_para_json = []

    # Escreve o CSV unificado
    with open(csv_saida, mode='w', newline='', encoding='utf-8') as f_out_csv:
        writer = csv.DictWriter(f_out_csv, fieldnames=cabecalho_csv)
        writer.writeheader()

        for linha_link in dados_links:
            titulo = linha_link["Title"].strip()
            extras = dados_artifacts.get(titulo, {})
            
            # Adiciona os campos extras ao CSV
            for col in colunas_extras:
                linha_link[col] = extras.get(col, "")
            
            writer.writerow(linha_link)

            # Gera o JSON com todos os campos desejados
            links_antes = [l.strip() for l in linha_link.get("Links_antes_REFERENCES", "").split(';') if l.strip()]
            links_depois = [l.strip() for l in linha_link.get("Links_depois_REFERENCES", "").split(';') if l.strip()]

            dados_para_json.append({
                "Title": titulo,
                "Links_antes_REFERENCES": links_antes,
                "Links_depois_REFERENCES": links_depois,
                "DOI": linha_link.get("DOI", ""),
                "Artifact Available": linha_link.get("Artifact Available", ""),
                "Artifact Reusable": linha_link.get("Artifact Reusable", ""),
                "Artifact Functional": linha_link.get("Artifact Functional", "")
            })

    # Salva o JSON formatado
    with open(json_formatado_saida, 'w', encoding='utf-8') as f_json:
        json.dump(dados_para_json, f_json, indent=2, ensure_ascii=False)

    print(f'\n✅ CSV unificado salvo em: {csv_saida}')
    print(f'✅ JSON formatado salvo em: {json_formatado_saida}')


# Executa a função com os arquivos fornecidos
unir_csvs_e_gerar_json_formatado(
    csv_links_path='links_artigos_divididos.csv',
    csv_artifacts_path='icse_articles\2024acm_articles.csv',
    csv_saida='icse2024_links_no_artigo.csv',
    json_formatado_saida='icse2024_links_no_artigo.json'
)
