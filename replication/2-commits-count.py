import os
import subprocess
import csv

def count_commits_for_files(repo_path, file_paths):
    """
    Conta o número de commits relacionados a uma lista de arquivos em um repositório Git de forma sequencial.
    """
    if not os.path.exists(os.path.join(repo_path, ".git")):
        print(f"[WARNING] Diretório '{repo_path}' não é um repositório Git. Ignorando.")
        return 0

    unique_commits = set()
    try:
        for file_path in file_paths:
            relative_path = os.path.relpath(file_path, repo_path)
            cmd = ["git", "-C", repo_path, "log", "--pretty=%H", "--", relative_path]
            print(f"[DEBUG] Executando comando: {' '.join(cmd)}")
            result = subprocess.run(cmd, capture_output=True, text=True, check=True)
            commits = result.stdout.strip().split("\n")
            print(f"[DEBUG] Commits encontrados para '{relative_path}': {commits}")
            unique_commits.update(commits)
    except subprocess.CalledProcessError as e:
        print(f"[ERROR] Erro ao executar git log no repositório '{repo_path}': {e}")
    
    print(f"[DEBUG] Total de commits únicos para os arquivos: {len(unique_commits)}")
    return len(unique_commits)

# Função principal para processar os diretórios e arquivos IaC
def process_repositories_and_commits(input_csv, output_csv):
    """
    Processa o CSV de entrada, contando commits relacionados aos arquivos IaC e salvando o resultado em um CSV de saída.
    """
    with open(input_csv, mode="r") as infile, open(output_csv, mode="w", newline="") as outfile:
        reader = csv.DictReader(infile)
        fieldnames = reader.fieldnames + ["commit_count", "total_commit_count"]
        writer = csv.DictWriter(outfile, fieldnames=fieldnames)
        writer.writeheader()
        
        for row in reader:
            repo_id = row["id"]
            iac_paths = eval(row["iac_paths"])  # Supondo que você tenha os paths no formato de lista na coluna
            related_files = eval(row["related_files"])  # Coluna com os arquivos relacionados
            repo_path = f"/home/aluno/filtered-repositories-iac-criteria/criteria4/{repo_id}"  # Substitua pelo caminho real do repositório

            # Contar commits para arquivos IaC
            commit_count = count_commits_for_files(repo_path, iac_paths + related_files)

            # Contar commits do repositório inteiro
            cmd = ["git", "-C", repo_path, "log", "--pretty=%H"]
            result = subprocess.run(cmd, capture_output=True, text=True, check=True)
            total_commits = len(result.stdout.strip().split("\n"))

            # Escrever resultado no CSV de saída
            row["commit_count"] = commit_count
            row["total_commit_count"] = total_commits
            writer.writerow(row)

# Exemplo de uso:
# 2° IaC_Commits_Summary
process_repositories_and_commits("iac_files_with_neighbors.csv", "iac_commits_summary.csv")
