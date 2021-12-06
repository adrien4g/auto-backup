import docker, os

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
                    volumes.append(current_volume['Source'])

            self.containers.append({
                'name':container_name,
                'volumes':volumes,
                'project_name': project_name
            })

        return self.containers
    
    def create_tar(self, container, root_path):
        name, volumes, project_name = container.values()
        if volumes <= 0:
            return ('Error', f'Container {name} não tem volumes montados.')

        if root_path != project_name:
            project_name = project_name.replace(root_path, '')
        else:
            project_name = project_name.split('/')[-1]

        
d = DockerAnalytics()
containers = d.get_data()
root = [i['project_name'] for i in containers if i['project_name'] != 'other']
root = os.path.commonpath(root)
for current_container in containers:
    d.create_tar(current_container, root)