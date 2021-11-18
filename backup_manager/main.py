import docker
from tar import CreateTar

class DockerAnalytics:
    def __init__(self):
        self.docker_client = docker.APIClient(base_url='unix://var/run/docker.sock')
        self.paths = {}
        #self.docker_compose_key = 'com.docker.compose.project.working_dir'

    def get_volumes(self):
        container_list = self.docker_client.containers()
        for current_container in container_list:
            if len(current_container['Mounts']) > 0:
                container_name = current_container['Names'][0].replace('/','')
                self.paths[container_name] = []
                for mounts in current_container['Mounts']:
                    self.paths[container_name].append(mounts['Source'])
        return self.paths

    def create_tar(self):
        for container in self.paths:
            tar = CreateTar()
            for path in self.paths[container]:
                tar.insert_path(path)
            tar.create_tar(container)

d = DockerAnalytics()
d.get_volumes()
d.create_tar()
