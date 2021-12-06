import docker, os, pathlib, sys
from tar import CreateTar
from utils import write_log

class DockerAnalytics:
    def __init__(self):
        self.docker_client = docker.APIClient(base_url='unix://var/run/docker.sock')
        self.paths = {}
        self.project_path = ''
        self.project_paths = set()
        self.docker_compose_key = 'com.docker.compose.project.working_dir'

    def get_volumes(self):
        write_log('Obtendo volume dos containers')
        container_list = self.docker_client.containers()
        for current_container in container_list:
            container_name = current_container['Names'][0].replace('/','')
            # Ignore onedrive container
            if container_name == 'onedrive':
                continue
            try:
                path = current_container['Labels'][self.docker_compose_key]
                self.project_path = path
                self.project_paths.add(path)
            except:
                write_log(f'Error - Não foi encontrado o docker compose do container: {container_name}')
                self.project_path = 'others'
            try:
                if len(current_container['Mounts']) > 0:
                    self.paths[container_name] = []
                    volumes = []
                    for mounts in current_container['Mounts']:
                        volumes.append(mounts['Source'])
                    self.paths[container_name] = {
                        'project_folder': self.project_path,
                        'volumes': volumes
                    }
            except Exception as e:
                write_log(e)
                continue

        return self.paths

    def create_tar(self):
        if len(self.paths) <= 0:
            write_log('Error - Nenhum container foi encontrado.')
            sys.exit('Nenhum container foi encontrado.')
        root_folder = os.path.commonpath(self.project_paths)
        for container in self.paths:
            project_folder = self.paths[container]['project_folder']
            if project_folder != root_folder:
                project_folder = project_folder.replace(root_folder, '')
                if project_folder[0] == '/': project_folder = project_folder[1:]
            else:
                project_folder_list = project_folder.split('/')[1:]
                project_folder = project_folder_list[-1]
            tar = CreateTar()
            for path in self.paths[container]['volumes']:
                tar.insert_path(path)
            write_log('Iniciando processo de criação do arquivo tar.xz')
            tar.create_tar(container)
            tar.send_to_backup_folder(container, project_folder)

d = DockerAnalytics()
d.get_volumes()
d.create_tar()
print(f'Logs salvos em {pathlib.Path("../data.log").resolve()}')
write_log(True)