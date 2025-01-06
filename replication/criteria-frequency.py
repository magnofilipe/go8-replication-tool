import os
import csv
from concurrent.futures import ThreadPoolExecutor


def classify_technology(paths):
    """
    Classify the technology based on file names in the paths.
    Priority: Pulumi > Terraform > AWS CDK
    """
    for path in paths:
        if path.endswith("Pulumi.yaml") or path.endswith("Pulumi.yml"):
            return "Pulumi"
        elif path.endswith("cdktf.json"):
            return "Terraform"
        elif path.endswith("cdk.json"):
            return "AWS CDK"
    return None


def process_criteria(criteria_dir, ids_and_paths, output_dir):
    """
    Process a single criteria directory to classify technologies.
    """
    technology_counts = {"Pulumi": 0, "Terraform": 0, "AWS CDK": 0, "NOTFOUND": 0}
    results = []

    # Iterate over the subdirectories in the criteria directory
    for repo_id in os.listdir(criteria_dir):
        repo_path = os.path.join(criteria_dir, repo_id)

        # Only process if it's a directory
        if os.path.isdir(repo_path):
            # Find matching paths for this ID in the CSV
            matching_entry = next((paths for id_csv, paths in ids_and_paths if id_csv == repo_id), None)

            if matching_entry:
                tech_classification = classify_technology(matching_entry)
                if tech_classification:
                    technology_counts[tech_classification] += 1
                else:
                    tech_classification = "NOTFOUND"
                    technology_counts["NOTFOUND"] += 1
                results.append([repo_id, tech_classification])
            else:
                # Handle case where no matching entry is found
                results.append([repo_id, "NOTFOUND"])
                technology_counts["NOTFOUND"] += 1

    # Write results to a CSV
    output_csv = os.path.join(output_dir, f"{os.path.basename(criteria_dir.rstrip('/'))}_output.csv")
    os.makedirs(output_dir, exist_ok=True)
    with open(output_csv, "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["ID", "Technology"])
        writer.writerows(results)

    # Print counts
    string = f"Counts for {criteria_dir}:\n"
    for tech, count in technology_counts.items():
        string += f"{tech}: {count}\n"
    print(string)
    
    return output_csv



def read_csv(csv_file):
    """
    Reads the input CSV and extracts repository IDs and their respective paths.
    """
    ids_and_paths = []
    with open(csv_file, newline='') as file:
        reader = csv.reader(file)
        for row in reader:
            repo_id = row[0]
            # Convert the 14th column string to a list of paths
            paths = eval(row[13])  # Assumes paths are in the format ['path1', 'path2']
            ids_and_paths.append((repo_id, paths))
    return ids_and_paths


def process_directories_in_parallel(csv_file, criteria_dirs, output_dir):
    """
    Process all criteria directories in parallel.
    """
    ids_and_paths = read_csv(csv_file)

    with ThreadPoolExecutor() as executor:
        futures = [
            executor.submit(process_criteria, criteria_dir, ids_and_paths, output_dir)
            for criteria_dir in criteria_dirs
        ]
        for future in futures:
            print(f"Output CSV generated: {future.result()}")


# Main execution
if __name__ == "__main__":
    
    csv_file = "/home/aluno/Documentos/metadata-pipr/output.csv"  # Path to the input CSV
    criteria_dirs = [
        "/home/aluno/filtered-repositories/criteria1/",
        "/home/aluno/filtered-repositories/criteria2/",
        "/home/aluno/filtered-repositories/criteria3/",
        "/home/aluno/filtered-repositories/criteria4/",
    ]
    output_dir = "output-filtered-repositories"

    process_directories_in_parallel(csv_file, criteria_dirs, output_dir)
