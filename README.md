# Auto backup 

Documentação baseada no uso do debian 11 (bullseye)

## Pré requisitos
* docker
* python
* pip
  * docker


## Instalação
#### 1 - Docker
* Atualizar repositórios
    ```
    sudo apt-get update
    ```
* Instalar pré-requisitos
    ```
    sudo apt-get install \
        ca-certificates \
        curl \
        gnupg \
        lsb-release
    ```

* Adicionar chave GPG
    ```
     curl -fsSL https://download.docker.com/linux/debian/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg

    ```

* Adicionar repositório
    ```
    echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/debian \
  $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
    ```

* Atualizar repositório e instalar o docker
    ```
    sudo apt-get update && sudo apt-get install docker-ce docker-ce-cli containerd.io
    ```

* Criar grupo `docker`
    ```
    sudo groupadd docker
    ```

* Adicionar usuário ao grupo `docker`
    ```
    sudo usermod -aG docker $USER
    ```

* Instalar docker compose
    ```
     sudo curl -L "https://github.com/docker/compose/releases/download/1.29.2/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
    ```

* Dar permissão de execução
    ```
    sudo chmod +x /usr/local/bin/docker-compose
    ```
#### 2 - Docker module
* Entre na pasta do projeto python
    ```
    cd backup_manager
    ```
* Crie e entre em um ambiente virtual
    ```
    python3 -m venv .env && source .env/bin/activate
    ```
* Instale os modulos do python
    ```
    pip3 install -r requirements.txt
    ```
Agora seu ambiente está pronto para prosseguir! :D
## Configuração
#### 1 - Configurando o docker
* Criando um volume
    ```
    docker volume create onedrive_conf
    ```
* Criando os arquivos de configuração dentro do volume
    * Pegando diretório do volume
    ```
    docker inspect onedrive_conf
    ```
    * Criando arquivos de configuração

        * Pegue o  conteudo do arquivo config_files/config e insira nesse arquivo
        ```
        sudo vim {path_do_volume}/config
        ```
        * Pegue o conteúdo do arquivo config_files/sync_list e insira nesse arquivo
        ```
        sudo vim {path_do_volume}/sync_list
        ```
#### 2 - Configurando o python
* É necessário informar ao python qual o diretório padrão de backup, edite o arquivo `config.ini` na linha `backup_dir`.
*
#### 

