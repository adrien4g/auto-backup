import subprocess, os, sys, shutil, pathlib
from utils import get_main_paths, write_log
from configparser import ConfigParser

config = ConfigParser()
config.read('../config.ini')

class CreateTar:
    def __init__(self):
        self.paths = []
        if os.path.isdir(config['Default']['backup_dir']):
            self.backup_dir = config['Default']['backup_dir']
            if self.backup_dir[-1] != '/': self.backup_dir += '/'
        else:
            sys.exit('Configure a pasta no arquivo config.ini')
    def insert_path(self, path):
        if not path in self.paths:
            self.paths.append(path)
            return path
        return 'Path already exists.'

    def create_tar(self, filename):
        main_paths = get_main_paths(self.paths)
        tar_paths = {}
        # Organize paths
        for path in self.paths:
            # Return the main path from full path
            main_path = [x for x in main_paths if x in path]
            path = path.replace(main_path[0], '')
            if path[0] == '/': path = path[1:]

            # Verify if tar_paths has 'main_path[0]' key
            if not main_path[0] in tar_paths:
                tar_paths[main_path[0]] = []

            # Add new path
            tar_paths[main_path[0]].append(path)
            # Get only main paths 
            tar_paths_copy = tar_paths.copy()
            for tar_path1 in tar_paths[main_path[0]]:
                for tar_path2 in tar_paths[main_path[0]]:
                    if tar_path1 != tar_path2 and tar_path1 in tar_path2:
                        tar_paths_copy[main_path[0]].remove(tar_path2)
            tar_paths = tar_paths_copy.copy()

        # Create tar file
        command_paths = ''
        for container in tar_paths:
            folder_to_change = f'-C {container} '
            paths = ''
            if not os.path.isdir(container):
                continue
            for path in tar_paths[container]:
                if os.path.isdir(container + '/' + path) or os.path.isfile(container + '/' + path):
                    paths += f'{path} '
            command_paths += folder_to_change + paths
        if paths == '':
            write_log(f'Volumes não encontrados do container {filename}.')
            return
        command = f'tar -cjf /tmp/{filename}.tar.xz {command_paths} >> /dev/null'
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        if os.path.isfile(f'/tmp/{filename}.tar.xz'):
            write_log(f'{filename}.tar.xz criado.')

    def send_to_backup_folder(self, filename, project_folder = ''):
        backup_folder = f'{self.backup_dir}/volumes/{project_folder}'
        pathlib.Path(backup_folder).mkdir(parents=True, exist_ok=True)
        try:
            shutil.move(f'/tmp/{filename}.tar.xz', f'{backup_folder}/{filename}.tar.xz')
            write_log(f'{filename}.tar.xz enviado para a pasta de backup')
        except:
            write_log(f'{filename}.tar.xz não enviado para a pasta de backup')