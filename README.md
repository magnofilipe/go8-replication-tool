# go8-replication-tool

# Instalação do Requirements

## Importante!
A biblioteca `spacy` precisa ser utilizada na **versão `3.8.3`**, que atualmente **só é compatível com Python 3.10 ou 3.11**.

### Linux ou macOS

#### Se estiver usando **virtual environment (venv)**

1. Verifique a versão do Python no ambiente:
   ```bash
   $ ./<nome-do-seu-venv>/bin/python --version
   ```

2. Se não for 3.10 ou 3.11, instale com `pyenv`:

   ```bash
   # Instale o pyenv
   curl https://pyenv.run | bash

   # Adicione ao shell (~/.bashrc, ~/.zshrc etc.)
   export PATH="$HOME/.pyenv/bin:$PATH"
   eval "$(pyenv init --path)"
   eval "$(pyenv init -)"
   ```

3. Instale o Python compatível e recrie o venv:
   ```bash
   pyenv install 3.11.7
   pyenv local 3.11.7

   python -m venv <nome-do-seu-venv>
   source <nome-do-seu-venv>/bin/activate
   pip install -r requirements.txt
   ```

#### Se **não estiver usando venv**

1. Verifique a versão:
   ```bash
   python --version
   ```

2. Caso seja uma versão superior, use o `pyenv` para instalar o Python compatível:
   ```bash
   pyenv install 3.11.7
   pyenv global 3.11.7
   ```

3. Instale as dependências:
   ```bash
   pip install -r requirements.txt
   ```

**Observação:** Caso tenha algum problema instalando os packages,
o seguinte comando pode auxiliar: 
```bash
pip install -r requirements.txt --break-system-packages
```

Após instalar todos packages, ainda é necessário rodar o seguinte comando:

```bash
python3 -m spacy download en_core_web_sm
```

# Exemplo de execução:

- OBS1: Todos os scripts geram Logs, caso algum deles falhe, é possível verificar o motivo!

1. Adicionaremos um repositório na lista p/ clonagem:
```bash
echo "https://github.com/mitodl/ol-infrastructure" >> repos_list.txt
```

2. Clone o repositório:
```bash
./clone-repos.sh
```
- OBS2: Esse repositório é público por isso não precisa autenticação, em repositórios privados é necessário
passar o tipo de autenticação que deseja fazer:
```bash
# Autenticação por meio de SSH
./clone-repos.sh -c ssh
# Autenticação por meio de Token
./clone-repos.sh -c token
```

3. Aplique os critérios de seleção de repositório (O repositório do exemplo se encaixa dentro dos critérios):
```bash
./apply-criterias.sh
```

4. Após isso, execute a ferramenta por meio do seguinte comando:
```bash
# O comando a seguir roda a versão serial da ferramenta
./run-acid 
# E adicionando a flag -c, roda a versão concorrente (RECOMENDADO)
./run-acid -c
```

5. Por fim, dentro do diretório 'csv' estará todos resultados. Eles incluem o resultado da execução
e categorização de defeitos dos repositórios (no diretório csv/acid-ouput) e um resumo de quais são
as características dos repositórios (ex: quantidade de linguagens Pulumi, AWS CDK, Terraform ou EDN).

# Os comentário a seguir estão apenas detalhando o que cada comando bash faz:
# I. Clonagem Dos Repositórios
1. Preencha o arquivo `repos_list.txt` com o link de todos os repositórios para fazer o clone!

2. Após isso poderá rodar o script de clonagem:
```bash
./clone-repos.sh

"Uso: ./clone-repos.sh [-d directory] [-f repos_file] [-s start_line] [-t threads] [-c credential]
  Opções:
    -d  Diretório de destino para clonar os repositórios (padrão: dataset)
    -f  Arquivo contendo a lista de repositórios (um por linha) (padrão: repos_list.txt)
    -s  Linha inicial para continuar o processo de clonagem (padrão: 2)
    -t  Número de clones simultâneos (padrão: 10)
    -c  Tipo de credencial: ssh ou token"
```

**Observação:** Dependendo da escolha do número de threads, a máquina pode apresentar o erro **Too Many Files Open**, para resolver isso você pode redefinir o limite de arquivos que podem ser aberto ao mesmo tempo com o seguinte comando: 
``` bash
# O padrão é 1024, você pode escolher um número mais alto que 4096
ulimit -n 4096
```

Após finalizar a execução, os repositórios estarão clonados no destino indicado,
além de gerar um csv indicando quais repositórios tiveram sucesso ou falha dentro
do diretório `csv`.

# II. Aplicar Os Critérios De Seleção

Rode o seguinte comando para aplicar os critérios de seleção dos repositórios
e gerar os csvs necessários para análise.
```bash 
./apply-criterias.sh
"Uso: ./apply-criterias.sh [-d directory] 
  Opções:
    -d  Diretório de destino para clonar os repositórios (padrão: dataset)"
```

# III. Rodar A Ferramenta De Categorização De Defeitos 

Rode a ferramenta de categorização de defeitos, ela tem duas versões
uma concorrente e outra serial.
```bash
./run-acid.sh
"Uso: ./run-acid [-c]
  Opções:
    -c  Utilize 'main-concurrent.py' ao invés de 'main.py'"
```
