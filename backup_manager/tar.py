import subprocess, os, sys, shutil
from utils import get_main_paths
from configparser import ConfigParser
config = ConfigParser()
config.read('config.ini')

class CreateTar:
    def __init__(self):
        self.paths = []
        if config['Default']['backup_dir'] == '':
            path = '/home/ntm/backup'
            if os.path.isdir(path):
                self.backup_dir = path
            else:
                sys.exit(f'{path} not found.')
            self.backup_dir = '/home/ntm/backup/'
        else:
            if os.path.isdir(config['Default']['backup_dir']):
                self.backup_dir = config['Default']['backup_dir']
            else:
                sys.exit('Invalid backup dir, please configure in config.ini')

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
            command_paths += f'-C {container} '
            for path in tar_paths[container]:
                command_paths += f'{path} '
        command = f'tar -cjf /tmp/{filename}.tar.xz {command_paths} > /dev/null'
        subprocess.run(command, shell=True)

    def send_to_backup_folder(self, filename):
        shutil.move(f'/tmp/{filename}.tar.xz', f'{self.backup_dir}{filename}.tar.xz')
