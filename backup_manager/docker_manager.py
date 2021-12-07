import docker, os
from tar import Tar

class DockerAnalytics():
    def __init__(self):
        self.docker_client = docker.APIClient(base_url='unix://var/run/docker.sock')
        self.docker_compose_key = 'com.docker.compose.project.working_dir'

        self.containers = []

    def get_data(self, ignored_containers = []):
        container_list = self.docker_client.containers()
        for current_container in container_list:
            container_name = current_container['Names'][0].replace('/','')
            # Ignore containers
            if container_name in ignored_containers: continue
            try:
                project_name = current_container['Labels'][self.docker_compose_key]
            except:
                project_name = 'other'
            volumes = []
            if len(current_container['Mounts']) > 0:
                for current_volume in current_container['Mounts']:
                    if os.path.isdir(current_volume['Source']) or os.path.isfile(current_volume['Source']):
                        volumes.append(current_volume['Source'])

            self.containers.append({
                'name':container_name,
                'volumes':volumes,
                'project_name': project_name
            })

        return self.containers
        
