import os
import sys
import subprocess
from concurrent.futures import ThreadPoolExecutor

# Extensões de arquivos IAC
iac_extensions = [".tf", "Pulumi.yaml", "Pulumi.yml", "cdk.json", "cdktf.json"]

# Funções para os filtros
def is_not_fork(repo_path):
    config_file = os.path.join(repo_path, ".git", "config")
    if not os.path.exists(config_file):
        return False
    with open(config_file, "r") as f:
        return "fork = true" not in f.read()
    

def iac_percentage(repo_path):
    total_files = 0
    iac_files = 0
    iac_directories = set()  # Diretórios que possuem arquivos IaC

    for root, _, files in os.walk(repo_path):
        has_iac_file = any(file.endswith(ext) for file in files for ext in iac_extensions)
        if has_iac_file:
            iac_directories.add(root)
        total_files += len(files)

    # Contar todos os arquivos dos diretórios que possuem arquivos IaC
    for iac_dir in iac_directories:
        iac_files += sum(len(files) for _, _, files in os.walk(iac_dir))
    print(iac_files)
    print(total_files)
    return (iac_files / total_files) * 100 if total_files > 0 else 0

def commits_per_month(repo_path):
    result = subprocess.run(
        ["git", "log", "--date=format:%Y-%m", "--pretty=format:%ad"],
        cwd=repo_path,
        stdout=subprocess.PIPE,
        text=True
    )
    dates = result.stdout.splitlines()
    unique_months = set(dates)
    return len(dates) / len(unique_months) if unique_months else 0

def num_contributors(repo_path):
    result = subprocess.run(
        ["git", "log", "--pretty=format:%ae"],
        cwd=repo_path,
        stdout=subprocess.PIPE,
        text=True
    )
    all_emails = set(result.stdout.splitlines())
    filtered_emails = {email for email in all_emails if not email.endswith("@github.com")}
    return [len(filtered_emails), filtered_emails]

def analyze_and_copy(repo, filters, input_dir, output_dir):
    repo_path = os.path.join(input_dir, repo)
    try:
        print(f"Analyzing repository: {repo}")
        if not os.path.isdir(os.path.join(repo_path, ".git")):
            print(f"Not a Git repository: {repo}")
            return

        if (
            (not filters['--fork'] or  is_not_fork(repo_path)) and
            (not filters['--iac-percentage'] or iac_percentage(repo_path) >= 11) and
            (not filters['--commits-per-month'] or commits_per_month(repo_path) >= 2) and
            (not filters['--num-contributors'] or num_contributors(repo_path)[0] >= 10)
        ):
            target_path = os.path.join(output_dir, repo)
            if not os.path.exists(target_path):
                os.symlink(repo_path, target_path)
                print(f"Created symbolic link to repository: {target_path}")
            else:
                print(f"Link already exists for {repo}")
        else:
            print(f"Repository {repo} did not meet the criteria.")
    except Exception as e:
        print(f"Error analyzing repository {repo}: {e}")

if __name__ == "__main__":
    if not '--input' in sys.argv or not '--output' in sys.argv:
        print("Usage: python3 criterias.py --input path --output path --fork --iac-percentage --commits-permonth --num-contributors")
        sys.exit(1)

    input_dir = os.path.expanduser(sys.argv[sys.argv.index('--input') + 1])
    output_dir = os.path.expanduser(sys.argv[sys.argv.index('--output') + 1])
    os.makedirs(output_dir, exist_ok=True)
    
    filters = {
        '--fork': '--fork' in sys.argv,
        '--iac-percentage': '--iac-percentage' in sys.argv,
        '--commits-per-month': '--commits-per-month' in sys.argv,
        '--num-contributors': '--num-contributors' in sys.argv
    }   
    
    repos = os.listdir(input_dir)
    
    with ThreadPoolExecutor() as executor:
        executor.map(lambda repo: analyze_and_copy(repo, filters, input_dir, output_dir), repos)

    print("Finished processing all repositories.")

