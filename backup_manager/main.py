import docker
from tar import CreateTar
from utils import write_log

class DockerAnalytics:
    def __init__(self):
        self.docker_client = docker.APIClient(base_url='unix://var/run/docker.sock')
        self.paths = {}
        #self.docker_compose_key = 'com.docker.compose.project.working_dir'

    def get_volumes(self):
        container_list = self.docker_client.containers()
        for current_container in container_list:
            try:
                if len(current_container['Mounts']) > 0:
                    container_name = current_container['Names'][0].replace('/','')
                    # Ignore onedrive container
                    if container_name == 'onedrive':
                        continue
                    self.paths[container_name] = []
                    for mounts in current_container['Mounts']:
                        self.paths[container_name].append(mounts['Source'])
            except Exception as e:
                write_log(e)
                continue

        return self.paths

    def create_tar(self):
        for container in self.paths:
            tar = CreateTar()
            for path in self.paths[container]:
                tar.insert_path(path)
            tar.create_tar(container)
            tar.send_to_backup_folder(container)

d = DockerAnalytics()
d.get_volumes()
d.create_tar()
