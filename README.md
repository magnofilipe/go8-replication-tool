# go8-replication-tool

# Instalação do Requirements

`pip install -r requirements.txt`

`python3 -m spacy download en_core_web_sm`

# Após isso pode iniciar, fluxo de execução:

1. Clona os Repositórios: 
`./clone-repos.sh`

2. Aplica os Critérios: 
`./apply-criterias`

3. Roda a ferramenta ACID:
    - Versão Serial:      `./run-acid` 
    - Versão Concorrente: `./run-acid -c`
