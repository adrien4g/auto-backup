import os, sys, pathlib
from utils import write_log
from tar import Tar
from docker_manager import *
from configparser import ConfigParser

class Backup:
    def __init__(self):
        self.containers = []
        self.root_path = ''

        self.config = ConfigParser()
        self.config.read('../config.ini')
        if not os.path.isdir(self.config['Default']['backup_dir']):
            sys.exit(f'Insira um diretório válido no arquivo: {pathlib.Path("../config.ini").resolve()}')

    def get_docker_data(self):
        docker = DockerAnalytics()
        self.containers = docker.get_data(ignored_containers=['onedrive'])
        self.root_path = [i['project_name'] for i in self.containers if i['project_name'] != 'other']
        self.root_path = os.path.commonpath(self.root_path)
    
    def create_tar(self):
        for current_container in self.containers:
            tar = Tar()
            name, volumes, project_name = current_container.values()
            
            if self.root_path != project_name:
                project_name = project_name.replace(self.root_path, '')
            else:
                project_name = project_name.split('/')[-1]
            current_container['project_name'] = project_name
            
            status, msg = tar.create_tar(current_container)
            write_log(f'{status} - {msg}')
            status, msg = tar.send_to_backup_folder(current_container)
            write_log(f'{status} - {msg}')
            
backup = Backup()
backup.get_docker_data()
backup.create_tar()