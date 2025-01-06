import pandas as pd
import re
from threading import Thread

def filtrar_linhas_csv(primeiro_csv, segundo_csv, parametro_iac_type, output_csv):
    # Lendo os CSVs
    df1 = pd.read_csv(primeiro_csv)
    df2 = pd.read_csv(segundo_csv)
    linhas_filtradas = []

    # Itera sobre cada linha do primeiro CSV
    for _, row in df1.iterrows():
        path = row['REPO']  
        match = re.search(r'PIPR-replication/(\d+)', path)  # Extrai o ID após PIPR-replication
        
        if match:
            repo_id = int(match.group(1))  # Converte o ID para inteiro
            filtro = df2[(df2['id'] == repo_id) & (df2['iac_type'] == parametro_iac_type)]
            if not filtro.empty:
                linhas_filtradas.append(row)  # Adiciona a linha do primeiro CSV
    
    novo_df = pd.DataFrame(linhas_filtradas)
    novo_df.to_csv(output_csv, index=False)
    print(f"Novo CSV gerado com sucesso: {output_csv}")

# Caminhos de exemplo (substitua pelos reais)
primeiro_csv = '/home/aluno/ACID-dataset/ARTIFACT/OUTPUT/REPLICATION_ONLY_CATEG_OUTPUT_FINAL.csv'
segundo_csv = '/home/aluno/ACID-dataset/ARTIFACT/IaC_Defect_Categ_Revamp/replication/iac_time_period.csv'
output_csv = '/home/aluno/ACID-dataset/ARTIFACT/IaC_Defect_Categ_Revamp/replication/filter-acid-output/'
parametro_iac_type = ['Terraform', 'Pulumi', 'AWS CDK']
threads = []

for parametro in parametro_iac_type:
    output_local = output_csv + (parametro.upper()).replace(" ", "_") + '_REPLICATION_ONLY_CATEG_OUTPUT_FINAL.csv'
    threads.append(Thread(target= filtrar_linhas_csv, args=(primeiro_csv, segundo_csv, parametro, output_local)))
    
for thread in threads:
    thread.start()
for thread in threads:
    thread.join()