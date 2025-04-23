# Replication Package for "A Defect Taxonomy for Infrastructure as Code Scripts: A Replication Study"

## Purpose

This article presents the replication package associated with our paper:

TO-DO

<!-- > Junayed Mahmud, Nadeeshan De Silva, Safwat Ali Khan, Seyed Hooman Mostafavi, SM Hasan Mansur, Oscar Chaparro, Andrian Marcus, and Kevin Moran, “_**On Using GUI Interaction Data to Improve Text Retrieval-based Bug Localization**_,” in Proceedings of the 46th IEEE/ACM International Conference on Software Engineering (ICSE 2024) -->

<!-- Nosso trabalho replica o trabalho: [...] -->
Link to the full paper: TO-DO

## Dataset & Reproducibility

This repository contains the full source code and detailed instructions needed to reproduce the results presented in our paper.

The dataset used in our experiments is available here, and a permanent archive of code is hosted on Zenodo: <zenodo-link>.

## Directory Structure (Source Code)

```bash
├── ACID
│   ├── classifier.py --> text
│   ├── constants.py --> text
│   ├── diff_parser.py --> text
│   ├── excavator.py --> text
│   ├── main-concurrent.py --> text
│   └── main.py --> text
├── apply-criterias.sh --> text
├── clone-repos.sh --> text
├── README.md --> text
├── replication
│   ├── 1-related-files-generator.py --> text
│   ├── 2-commits-count.py --> text
│   ├── 3-time-period.py --> text
│   ├── 4-analyze.py --> text
│   ├── criteria-frequency.py --> text
│   └── criterias.py --> text
├── repos_list.txt --> text
├── requirements.txt --> text
└── run-acid.sh --> text
```

## Replication Tool

### Setup

- The `spacy` library needs to be used in **version 3.8.3**, which currently (April 2025) is only **compatible with Python 3.10 or 3.11**.
- Utilize either the Linux or macOS operating systems to execute the tool.

### If you are using virtual environment (venv)

**1.** Check the Python version in the environment:
   ```bash
   $ ./<your-venv-name>/bin/python --version
   ```

**2.** If it is not Python 3.10 or 3.11, install using `pyenv`:
   ```bash
   # Install pyenv
   curl https://pyenv.run | bash

   # Add to your shell (~/.bashrc, ~/.zshrc, ...)
   export PATH="$HOME/.pyenv/bin:$PATH"
   eval "$(pyenv init --path)"
   eval "$(pyenv init -)"
   ```
**3.** Install the compatible Python version and recreate the venv:
   ```bash
   pyenv install 3.11.7
   pyenv local 3.11.7

   python -m venv <your-venv-name>
   source <your-venv-name>/bin/activate
   pip install -r requirements.txt
   ```

### If you are NOT using virtual environment (venv)

**1.** Check the Python version:
   ```bash
   python --version
   ```

**2.** If it is not Python 3.10 or 3.11, use `pyenv` to install the compatible Python version:
   ```bash
   pyenv install 3.11.7
   pyenv global 3.11.7
   ```

**3.** Install the dependencies:
```bash
pip install -r requirements.txt
```

> **Note:** If you encounter any issues installing the packages, the following command may be helpful:

```bash
pip install -r requirements.txt --break-system-packages
```

**4.** After installing all the packages, run the following command:
```bash
python3 -m spacy download en_core_web_sm
```

### Script Execution Guide

**1.** Populate the `repos_list.txt` file with the links of all repositories intended for cloning.

**2.** Subsequently, the cloning script can be executed:

```bash
./clone-repos.sh
```

```bash
"Usage: ./clone-repos.sh [-d directory] [-f repos_file] [-s start_line] [-t threads] [-c credential]

Options:
    -d  Destination directory for cloning the repositories (default: dataset)
    -f  File containing the list of repositories (one per line) (default: repos_list.txt)
    -s  Starting line to resume the cloning process (default: 2)
    -t  Number of concurrent clones (default: 10)
    -c  Credential type: ssh or token"
```

Upon completion of the execution, the repositories will be cloned to the specified destination. Additionally, a CSV file will be generated within the `csv` directory, indicating the success or failure status of each repository's cloning process.

> **Note:** Depending on the number of threads chosen, you may encounter a "Too Many Open Files" error. To resolve this, you can redefine the limit for concurrently open files using the following command:

```bash
# The default is 1024; a higher number such as 4096 can be selected.
ulimit -n 4096
```

**3.** Apply selection criteria and generate the necessary CSV files for analysis with the following command:

```bash
./apply-criterias.sh
```

```bash
"Usage: ./apply-criterias.sh [-d directory]
Options:
    -d  Destination directory where the repositories were cloned (default: dataset)"
```

**4.** Execute the defect categorization tool, which is available in two versions: concurrent and serial.

```bash
./run-acid.sh
```

```bash
"Usage: ./run-acid [-c]
Options:
    -c  This option will utilize 'main-concurrent.py' instead of 'main.py'."
```

### Toy Example

> **Note**: All scripts generate logs, and in the event of a failure, the reason can be investigated.

**1.** Add a repository to clone list:
```bash
echo "https://github.com/mitodl/ol-infrastructure" >> repos_list.txt
```

**2.** Clone repository:
```bash
./clone-repos.sh
```

> **Note**: As this repository is public, authentication is not required. For private repositories, it is necessary to provide the type of authentication desired:
```bash
# SSH
./clone-repos.sh -c ssh
# Token
./clone-repos.sh -c token
```

**3.** Apply repository selection criterias:
```bash
./apply-criterias.sh
```

**4.** Execute the tool:
```bash
# Serial version
./run-acid 
# Concurrent version (RECOMMENDED)
./run-acid -c
```

**5.** Finally, all the results will be located within the `csv` directory. These include the execution results, defect categorization of the repositories and a summary of the repositories characteristics (e.g., the number of Pulumi, AWS CDK, Terraform, or EDN languages).

## References

TO-DO
- PIPR
- Go8