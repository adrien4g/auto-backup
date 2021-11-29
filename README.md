# Auto backup 

Documentação baseada no uso do debian 11 (bullseye)

## Sobre
Esse projeto tem como objetivo automatizar o backup dos volumes dos containers e os enviar para o onedrive.

## Pré requisitos
* docker
* python
* pip
  * docker

## Aviso
O container do onedrive não pode ser executado como root


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

* Instalar docker compose (Opcional)
    ```
     sudo curl -L "https://github.com/docker/compose/releases/download/1.29.2/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
    ```

* Dar permissão de execução (Opcional)
    ```
    sudo chmod +x /usr/local/bin/docker-compose
    ```
#### 2 - Baixando projeto
```
git clone https://github.com/adrien4g/auto-backup
```

#### 3 - Docker module
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
* Saia do ambiente virtual e volte para pasta do projeto
    ```
    deactivate && cd ..
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

        * Pegue o  conteudo do arquivo `config_files/config` e insira nesse arquivo
        ```
        sudo vim {path_do_volume}/config
        ```
        * Pegue o conteúdo do arquivo `config_files/sync_list` e insira nesse arquivo
        ```
        sudo vim {path_do_volume}/sync_list
        ```
## Executando projeto

#### 🟥 Antes de continuar verifique o espaço livre em sua conta do onedrive!
* Execute o arquivo `startonedrive.sh`, espere ser inicializado, copie a URL que ele mandar e cole no navegador, logue no seu One Drive, espere ser direcionado a uma tela branca e copie a URL, volte ao terminal e cole. Com isso você já está autenticado e a sincronização vai começar. Ao executar esse arquivo uma pasta chamada `backup` será criada em sua home, todos os arquivos dentro serão enviados ao onedrive e apagados dessa pasta.
* Execute o arquivo `makebackup.sh` como sudo para que o backup dos volumes dos containers seja feito. Um arquivo .tar.xz para cado projeto será gerado, enviado para a pasta configurada, e após enviado será apagado de sua máquina.
* Em caso de problemas com o container do onedrive, execute o arquivo `restartonedrive.sh`, ele apagará a instância atual e fará deploy de uma nova, não precisa se autenticar novamente.

## Dicas
#### Automatizando backup com cron
* No exemplo abaixo o backup será feito as 4h da manhã, meio dia e 20h da noite de todos os dias.
    ```
    0 4,12,20 * * * {path_do_arquivo}/makebackup
    ```
