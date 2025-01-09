import os
import subprocess
import csv
from datetime import datetime
import sys

def get_commit_time_period(repo_path, file_paths):
    """
    Obtém o commit mais antigo e o mais recente para uma lista de arquivos em um repositório Git.
    """
    if not os.path.exists(os.path.join(repo_path, ".git")):
        print(f"[WARNING] Diretório '{repo_path}' não é um repositório Git. Ignorando.")
        return None, None

    commit_dates = []
    try:
        for file_path in file_paths:
            relative_path = os.path.relpath(file_path, repo_path)
            cmd = ["git", "-C", repo_path, "log", "--pretty=%ci", "--", relative_path]
            print(f"[DEBUG] Executando comando: {' '.join(cmd)}")
            result = subprocess.run(cmd, capture_output=True, text=True, check=True)
            dates = result.stdout.strip().split("\n")
            commit_dates.extend(dates)
    except subprocess.CalledProcessError as e:
        print(f"[ERROR] Erro ao executar git log no repositório '{repo_path}': {e}")
        return None, None

    # Converte as datas para objetos datetime
    commit_dates = [datetime.strptime(date, "%Y-%m-%d %H:%M:%S %z") for date in commit_dates]

    if not commit_dates:
        return None, None

    return min(commit_dates), max(commit_dates)

def process_time_period(input_csv, output_csv, dataset_dir):
    """
    Processa o CSV de entrada para obter o período de tempo dos commits por tipo de arquivo IaC.
    """
    with open(input_csv, mode="r") as infile, open(output_csv, mode="w", newline="") as outfile:
        reader = csv.DictReader(infile)
        fieldnames = reader.fieldnames + ["oldest_commit", "newest_commit", "commit_time_period"]
        writer = csv.DictWriter(outfile, fieldnames=fieldnames)
        writer.writeheader()

        for row in reader:
            repo_id = row["id"]
            iac_type = row["iac_type"]
            iac_paths = eval(row["iac_paths"])  # Coluna com paths dos arquivos IaC
#           repo_path = f"/home/aluno/filtered-repositories-iac-criteria/criteria4/{repo_id}"
            repo_path = f"{dataset_dir}/{repo_id}"

            # Obtemos o período de tempo para os arquivos IaC
            oldest_commit, newest_commit = get_commit_time_period(repo_path, iac_paths)
            if oldest_commit and newest_commit:
                commit_time_period = (newest_commit - oldest_commit).days
            else:
                commit_time_period = None

            # Adiciona as informações ao CSV
            row["oldest_commit"] = oldest_commit.strftime("%Y-%m-%d %H:%M:%S %z") if oldest_commit else "N/A"
            row["newest_commit"] = newest_commit.strftime("%Y-%m-%d %H:%M:%S %z") if newest_commit else "N/A"
            row["commit_time_period"] = commit_time_period
            writer.writerow(row)


# 3° IaC Time Period
if __name__=="__main__":
    if not "--input" in sys.argv or not "--output" in sys.argv or not "--dataset-dir" in sys.argv:
        print("Usage: python3 3-time-period.py --input path --output path --dataset-dir path")
    
    input_path = os.path.expanduser(sys.argv[sys.argv.index("--input") + 1])
    output = os.path.expanduser(sys.argv[sys.argv.index("--output") + 1])
    dataset_dir = os.path.expanduser(sys.argv[sys.argv.index("--dataset-dir") + 1])
    process_time_period(input_path, output, dataset_dir)
