import os
import csv
import json
from concurrent.futures import ThreadPoolExecutor
import sys

# vou ler o diretorio de criteria 4
IAC_FILES = {
    "Pulumi": ["Pulumi.yaml", "Pulumi.yml"],
    "Terraform": ["cdktf.json"],
    "AWS CDK": ["cdk.json"]
}  
ALLOWED_EXTENSIONS = [".py", ".go", ".js", ".ts", ".rb", ".java", ".tf"] 
# 1° Iac Files With Neighbors
# OUTPUT_CSV = "iac_files_with_neighbors.csv"    

def process_directory(parent_dir, subdir_name):
    """Processa um diretório pai e identifica os arquivos IaC e vizinhos."""
    subdir_path = os.path.join(parent_dir, subdir_name)
    iac_data = {
        "id": subdir_name,
        "iac_type": None,
        "iac_paths": [],
        "related_files": []
    }

    print(f"[DEBUG] Processando diretório: {subdir_path}")

    # Percorre arquivos no diretório pai
    for dirpath, _, filenames in os.walk(subdir_path):
        # Verifica se há arquivos IaC no diretório atual
        for iac_type, file_names in IAC_FILES.items():
            found_iac_files = [f for f in filenames if f in file_names]
            if found_iac_files:
                # Adiciona o tipo e os caminhos dos arquivos IaC encontrados
                iac_data["iac_type"] = iac_type
                iac_data["iac_paths"].extend(
                    [os.path.join(dirpath, f) for f in found_iac_files]
                )

                # Adiciona arquivos vizinhos relevantes
                neighbor_files = [
                    os.path.join(dirpath, f)
                    for f in filenames
                    if os.path.splitext(f)[1] in ALLOWED_EXTENSIONS
                ]
                iac_data["related_files"].extend(neighbor_files)

    print(f"[DEBUG] Resultados para ID '{subdir_name}': {iac_data}")
    return iac_data

def find_iac_files_with_neighbors_parallel(root_dir, MAX_THREADS = 8):
    """Procura arquivos IaC e seus vizinhos usando paralelização."""
    iac_results = []  # Lista para armazenar os resultados
    parent_dirs = [d for d in os.listdir(root_dir) if os.path.isdir(os.path.join(root_dir, d))]

    print(f"[DEBUG] Diretórios identificados: {parent_dirs}")

    with ThreadPoolExecutor(max_workers=MAX_THREADS) as executor:
        tasks = [executor.submit(process_directory, root_dir, subdir) for subdir in parent_dirs]

        # Coleta os resultados das threads
        for future in tasks:
            iac_results.append(future.result())

    print(f"[DEBUG] Total de diretórios processados: {len(iac_results)}")
    return iac_results

def save_to_csv(data, output_file):
    """Salva os resultados em um arquivo CSV."""
    print(f"[DEBUG] Salvando resultados no arquivo: {output_file}")
    with open(output_file, mode="w", newline="", encoding="utf-8") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=["id", "iac_type", "iac_paths", "related_files"])
        writer.writeheader()
        for entry in data:
            writer.writerow({
                "id": entry["id"],
                "iac_type": entry["iac_type"] if entry["iac_type"] else "None",
                "iac_paths": json.dumps(entry["iac_paths"]),  # Encapsula os caminhos em JSON
                "related_files": json.dumps(entry["related_files"])  # Encapsula os vizinhos em JSON
            })
    print(f"[DEBUG] Resultados salvos com sucesso em {output_file}")

if __name__ == "__main__":
    if not "--input" in sys.argv or not "--output" in sys.argv:
        print("Usage: python3 1-related-files-generator.py --input path --output path -t number_threads")
    
    root_dir = os.path.expanduser(sys.argv[sys.argv.index("--input") + 1])
    output = os.path.expanduser(sys.argv[sys.argv.index("--output") + 1])

    if "-t" in sys.argv:
        n_threads = sys.argv[sys.argv.index("-t") + 1]
        iac_data = find_iac_files_with_neighbors_parallel(root_dir, n_threads)
    else:
        iac_data = find_iac_files_with_neighbors_parallel(root_dir)
    
    save_to_csv(iac_data, output)
