import pandas as pd
import matplotlib.pyplot as plt
from tabulate import tabulate
import sys
from matplotlib import font_manager as fm
import os

if len(sys.argv) < 2:
    print("Por favor, forneça o caminho do arquivo CSV como argumento.")
    sys.exit(1)

# input: iac_output_frequency
dados = pd.read_csv(f"{sys.argv[1]}.csv")

dados['type'] = dados['type'].replace({'': None, 'empty': None})

dados[['start_date', 'end_date']] = dados['time_period'].str.split(' - ', expand=True)
dados['start_date'] = pd.to_datetime(dados['start_date'], format='%Y-%m-%d')
dados['end_date'] = pd.to_datetime(dados['end_date'], format='%Y-%m-%d')
dados['repos'] = dados['repos'].apply(lambda x: f'{x:,}' if pd.notna(x) else '')
dados['total_commits'] = dados['total_commits'].apply(lambda x: f'{x:,}' if pd.notna(x) else '')
dados['iac_files'] = dados['iac_files'].apply(lambda x: f'{x:,}' if pd.notna(x) else '')
dados['iac_commits'] = dados['iac_commits'].apply(lambda x: f'{x:,}' if pd.notna(x) else '')

# Criando a tabela com a segunda parte do time period em uma nova linha
tabela = pd.DataFrame({
    'Attribute': ['Repo. Type', 'Tot. Repos', 'Tot. Commits', 'Tot. IaC Scripts', 'Tot. IaC-related Commits', 'Time Period', ''],
    'TOTAL': [dados['type'][0] if pd.notna(dados['type'][0]) else '', dados['repos'][0], dados['total_commits'][0], dados['iac_files'][0], dados['iac_commits'][0],
              f"{dados['start_date'][0].strftime('%m/%Y')} -", dados['end_date'][0].strftime('%m/%Y')],
    'PULUMI': [dados['type'][2], dados['repos'][2], dados['total_commits'][2], dados['iac_files'][2], dados['iac_commits'][2],
               f"{dados['start_date'][2].strftime('%m/%Y')} -", dados['end_date'][2].strftime('%m/%Y')],
    'TERRAFORM': [dados['type'][1], dados['repos'][1], dados['total_commits'][1], dados['iac_files'][1], dados['iac_commits'][1],
           f"{dados['start_date'][1].strftime('%m/%Y')} -", dados['end_date'][1].strftime('%m/%Y')],
    'AWS CDK': [dados['type'][3], dados['repos'][3], dados['total_commits'][3], dados['iac_files'][3], dados['iac_commits'][3],
                f"{dados['start_date'][3].strftime('%m/%Y')} -", dados['end_date'][3].strftime('%m/%Y')]
})

print(tabulate(tabela, headers='keys', tablefmt='grid', showindex=False))

fig, ax = plt.subplots(figsize=(9, len(tabela) *  0.25))
ax.axis('off')

# Definindo cores alternadas para as células

cell_colors = [["#f0f0f0" if i % 2 == 0 else "white" for _ in range(len(tabela.columns))] for i in range(len(tabela))]

table = ax.table(
    cellText=tabela.values, 
    colLabels=tabela.columns, 
    cellLoc='left',
    colLoc='left', 
    loc='center',
    cellColours=cell_colors
)

# Ajustando a largura das colunas
table.auto_set_column_width(col=list(range(4)))
table.auto_set_font_size(False)
table.set_fontsize(50)

path_to_times = "/usr/share/fonts/truetype/msttcorefonts/times.ttf"
times_new_roman = fm.FontProperties(fname=path_to_times)
times_bold = fm.FontProperties(fname=path_to_times, weight='bold')

# Definindo a formatação das células
for (i, cell) in table.get_celld().items():
    # Ajustando a formatação
    if i[0] == 0:  # Para a linha de cabeçalho
        cell.set_text_props(ha='left', va='center', fontproperties=times_bold)
    else:
        cell.set_text_props(ha='left', va='top', fontproperties=times_new_roman)
    cell.set_aa(0.1)

# Remover as bordas das células
for key, cell in table.get_celld().items():
    cell.set_edgecolor('none')
    cell.visible_edges = "horizontal"

# Adicionando linhas pretas no topo da primeira linha e na parte inferior da última linha
for j in range(len(tabela.columns)):
    # Topo da primeira linha: apenas borda superior
    table[(0, j)].set_edgecolor('black')
    table[(0, j)].set_linewidth(1)
    # table[(0, j)].visible_edges = "T"
    # table[(1, j)].set_edgecolor('black')
    # table[(1, j)].visible_edges = "T"
    # table[(1, j)].set_linewidth(1)
    
    # Inferior da última linha: apenas borda inferior
    table[(len(tabela), j)].set_edgecolor('black')
    table[(len(tabela), j)].visible_edges = "B"
    table[(len(tabela), j)].set_linewidth(1)

plt.show()
