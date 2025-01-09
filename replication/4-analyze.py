import csv
from datetime import datetime
import os
import sys

def analyze_csv(file_path, output_csv):
    results = {
        "TOTAL": {"repos": 0, "commits": 0, "iac_files": 0, "iac_commits": 0, "time_period": None},
        "Terraform": {"repos": 0, "commits": 0, "iac_files": 0, "iac_commits": 0, "time_period": None},
        "Pulumi": {"repos": 0, "commits": 0, "iac_files": 0, "iac_commits": 0, "time_period": None},
        "AWS CDK": {"repos": 0, "commits": 0, "iac_files": 0, "iac_commits": 0, "time_period": None},
    }

    time_periods = {"TOTAL": [], "Terraform": [], "Pulumi": [], "AWS CDK": []}

    with open(file_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            iac_paths = row["iac_paths"].strip("[]").split(", ")  # Transforma a string em uma lista
            related_files = row["related_files"].strip("[]").split(", ")

            iac_files_count = len(iac_paths) if iac_paths[0] else 0
            related_commits_count = len(related_files) if related_files[0] else 0

            total_commits = int(row["total_commit_count"])
            repo_name = row["iac_type"]
            first_commit_date = datetime.strptime(row["oldest_commit"], "%Y-%m-%d %H:%M:%S %z")
            last_commit_date = datetime.strptime(row["newest_commit"], "%Y-%m-%d %H:%M:%S %z")


            category = "TOTAL"
            if "terraform" in repo_name.lower():
                category = "Terraform"
            elif "pulumi" in repo_name.lower():
                category = "Pulumi"
            elif "cdk" in repo_name.lower():
                category = "AWS CDK"

            # Atualizar métricas
            results[category]["repos"] += 1
            results[category]["commits"] += total_commits
            results[category]["iac_files"] += iac_files_count
            results[category]["iac_commits"] += related_commits_count
            time_periods[category].append(first_commit_date)
            time_periods[category].append(last_commit_date)

            # Atualizar TOTAL
            results["TOTAL"]["repos"] += 1
            results["TOTAL"]["commits"] += total_commits
            results["TOTAL"]["iac_files"] += iac_files_count
            results["TOTAL"]["iac_commits"] += related_commits_count
            time_periods["TOTAL"].append(first_commit_date)
            time_periods["TOTAL"].append(last_commit_date)

    # Calcular o período de tempo para cada categoria
    for category, times in time_periods.items():
        if times:
            results[category]["time_period"] = f"{min(times).strftime('%Y-%m-%d')} - {max(times).strftime('%Y-%m-%d')}"

    # Escrever resultados no CSV
    with open(output_csv, mode='w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ["category", "type", "repos", "total_commits", "iac_files", "iac_commits", "time_period"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        for category, data in results.items():
            writer.writerow({
                "category": category,
                "type": "GIT" if category != "TOTAL" else "",
                "repos": data["repos"],
                "total_commits": data["commits"],
                "iac_files": data["iac_files"],
                "iac_commits": data["iac_commits"],
                "time_period": data["time_period"] if data["time_period"] else "N/A"
            })


if __name__=="__main__":
    if not "--input" in sys.argv or not "--output" in sys.argv or not "--dataset-dir" in sys.argv:
        print("Usage: python3 4-analyze.py --input path --output path")
    
    input_csv = os.path.expanduser(sys.argv[sys.argv.index("--input") + 1])
    output_csv = os.path.expanduser(sys.argv[sys.argv.index("--output") + 1])

    analyze_csv(input_csv, output_csv)

    print(f"Resultados armazenados em: {output_csv}")
