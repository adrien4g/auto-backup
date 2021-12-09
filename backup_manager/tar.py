import subprocess, pathlib, os, shutil
from hurry.filesize import size
from utils import get_root_paths, write_log
from configparser import ConfigParser

config = ConfigParser()
config.read('../config.ini')

class Tar:
    def __init__(self):
        self.paths = {}
        self.backup_dir = config['Default']['backup_dir']

    def create_tar(self, container):
        name, volumes, _ = container.values()

        if len(volumes) <= 0:
            return ('Error', f'O container {name} não tem volumes montados')

        root_paths = get_root_paths(volumes)

        for current_volume in volumes:
            for current_root_path in root_paths:
                if current_volume.startswith(current_root_path):
                    current_volume = current_volume.replace(current_root_path, '')
                    if not current_root_path in self.paths:
                        self.paths[current_root_path] = []
                    self.paths[current_root_path].append(current_volume)
                    break

        path_commands = ''
        for current_root_path in self.paths:
            folder_to_change = f'-C {current_root_path} '
            paths = ''
            for current_path in self.paths[current_root_path]:
                paths = f'{current_path} '
            path_commands += f'{folder_to_change} {paths} '
        
        command = f'tar -cjf /tmp/{name}.tar.xz {path_commands} >> /dev/null'
        try:
            subprocess.run(command, shell=True, capture_output=True, text=True)
        except:
            return (f'Error', 'Não foi possível gerar o arquivo {name}.tar.xz')

        if os.path.isfile(f'/tmp/{name}.tar.xz'):
            filesize = size(pathlib.Path(f'/tmp/{name}.tar.xz').stat().st_size)
            return ('Ok', f'O arquivo {name}.tar.xz foi gerado - tamanho {filesize}')
        else:
            return ('Error', f'O arquivo {name}.tar.xz foi gerado na pasta /tmp, mas não foi encontrado')

    def send_to_backup_folder(self, container):
        name, _, project_name = container.values()
        backup_folder = f'{self.backup_dir}/volumes/{project_name}'
        pathlib.Path(backup_folder).mkdir(parents=True, exist_ok=True)
        try:
            shutil.move(f'/tmp/{name}.tar.xz', f'{backup_folder}/{name}.tar.xz')
            return ('Ok', f'O arquivo {name}.tar.xz foi enviado para pasta de backup')
        except:
            return ('Error', f'O arquivo {name}.tar.xz NÃO foi enviado para pasta de backup')