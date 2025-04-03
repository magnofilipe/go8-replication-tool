import os
import subprocess
import csv
from datetime import datetime
import sys

csv.field_size_limit(sys.maxsize)

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

    # Converte as datas para objetos datetime, ignorando entradas inválidas
    valid_dates = []
    for date in commit_dates:
        try:
            valid_dates.append(datetime.strptime(date, "%Y-%m-%d %H:%M:%S %z"))
        except ValueError as e:
            print(f"[WARNING] Data inválida '{date}' encontrada em {repo_path}: {e}")
            continue

    if not valid_dates:  # Verifica se há datas válidas
        print(f"[WARNING] Nenhuma data válida encontrada para os arquivos em '{repo_path}'.")
        return None, None

    return min(valid_dates), max(valid_dates)


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
            repo_path = f"{dataset_dir}/{repo_id}"

            try:
                # Obtemos o período de tempo para os arquivos IaC
                oldest_commit, newest_commit = get_commit_time_period(repo_path, iac_paths)

                if oldest_commit and newest_commit:
                    # Garante que as datas sejam objetos datetime
                    if isinstance(oldest_commit, str):
                        oldest_commit = datetime.strptime(oldest_commit, "%Y-%m-%d %H:%M:%S %z")
                    if isinstance(newest_commit, str):
                        newest_commit = datetime.strptime(newest_commit, "%Y-%m-%d %H:%M:%S %z")

                    commit_time_period = (newest_commit - oldest_commit).days
                else:
                    commit_time_period = None

                # Adiciona as informações ao CSV
                row["oldest_commit"] = oldest_commit.strftime("%Y-%m-%d %H:%M:%S %z") if oldest_commit else "N/A"
                row["newest_commit"] = newest_commit.strftime("%Y-%m-%d %H:%M:%S %z") if newest_commit else "N/A"
                row["commit_time_period"] = commit_time_period

            except Exception as e:
                print(f"[ERROR] Erro ao processar o repositório '{repo_id}': {e}")
                row["oldest_commit"] = "N/A"
                row["newest_commit"] = "N/A"
                row["commit_time_period"] = "N/A"

            writer.writerow(row)


# 3° IaC Time Period
if __name__=="__main__":
    if not "--input" in sys.argv or not "--output" in sys.argv or not "--dataset-dir" in sys.argv:
        print("Usage: python3 3-time-period.py --input path --output path --dataset-dir path")
        sys.exit(1)
    
    input_path = os.path.abspath(sys.argv[sys.argv.index("--input") + 1])
    output = os.path.abspath(sys.argv[sys.argv.index("--output") + 1])
    dataset_dir = os.path.abspath(sys.argv[sys.argv.index("--dataset-dir") + 1])
    process_time_period(input_path, output, dataset_dir)
