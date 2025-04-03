#!/bin/bash

log_file="run_acid.log"
source_dir="criterias/criteria4"
flag_arg="REPLICATION"
target_dir="ACID/dataset/$flag_arg"
output_dir="csv/acid-output"
script_to_run="ACID/main.py"  # Padrão

function usage() {
  echo "Usage: $0 [-c]"
  echo "Options:"
  echo "  -c    Use 'main-concurrent.py' instead of 'main.py'"
  exit 1
}

echo "Starting run-acid.sh" | tee -a "$log_file"

while getopts "c" opt; do
  case "$opt" in
    c) 
      script_to_run="ACID/main-concurrent.py"
      echo "[INFO] Using concurrent script: $script_to_run" | tee -a "$log_file"
      ;;
    *) 
      usage 
      ;;
  esac
done

echo "[INFO] Creating directories..." | tee -a "$log_file"
mkdir -p "ACID/dataset" | tee -a "$log_file"
mkdir -p "$target_dir"  | tee -a "$log_file"
mkdir -p "$output_dir"  | tee -a "$log_file"

echo "[INFO] Creating symbolic links from $source_dir to $target_dir..." | tee -a "$log_file"
for dir in "$source_dir"/*; do
  if [[ -d "$dir" ]]; then
    dir_abs_path=$(realpath "$dir")
    dir_name=$(basename "$dir")
    
    ln -s "$dir_abs_path" "$target_dir/$dir_name" 2>>"$log_file"
    
    echo "[INFO] Link created: $target_dir/$dir_name -> $dir_abs_path" | tee -a "$log_file"
  fi
done

echo "[INFO] Generating eligible repositories CSV at $target_dir/eligible_repos.csv..." | tee -a "$log_file"
ls "$target_dir" > "$target_dir/eligible_repos.csv" 2>>"$log_file"
if [[ $? -eq 0 ]]; then
  echo "[SUCCESS] CSV generated successfully." | tee -a "$log_file"
else
  echo "[ERROR] Failed to generate CSV." | tee -a "$log_file"
  exit 1
fi

echo "[INFO] Running $script_to_run..." | tee -a "$log_file"
python3 "$script_to_run" --flag-arg $flag_arg --csv-replication csv/criterias-output/csv3_iac_criterias_output.csv --csv-default criterias/criteria4 --output "$output_dir" 2>>"$log_file"
if [[ $? -eq 0 ]]; then
  echo "[SUCCESS] $script_to_run executed successfully." | tee -a "$log_file"
else
  echo "[ERROR] $script_to_run failed." | tee -a "$log_file"
  exit 1
fi

echo "[INFO] Script completed. Logs saved to $log_file." | tee -a "$log_file"
