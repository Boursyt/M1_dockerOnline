import docker
from docker import errors

# variable global
#client = docker.from_env()
client = docker.DockerClient(base_url='tcp://192.168.1.39:2375', tls=False)
class DockerService:
    def __init__(self, name, image, command=None, environment=None, ports=None, volumes=None, network=None):
        self.name = name
        self.image = image
        self.command = command
        self.environment = environment
        self.ports = ports
        self.volumes = volumes
        self.network = network

    def download_image(self, url):
        try:
            self.image = client.images.pull(url)
        except errors.APIError as e:
            print(f"Error pulling image: {e}")
            self.image = None
        return self.image

    def docker_create(self):
        self.image = self.download_image(self.image)
        try:
            container = client.containers.create(
                name=self.name,
                image=self.image,
                command=self.command,
                environment=self.environment,
                ports=self.ports,
                volumes=self.volumes,
                network=self.network
            )
            return container
        except errors.APIError as e:
            print(f"Error creating container: {e}")
            return None

    def docker_run(self):
        pass

    def docker_stop(self):
        pass

    def __str__(self):
        return 'DockerService(name={}, image={}, command={}, environment={}, ports={}, volumes={}, network={})'.format(
            self.name, self.image, self.command, self.environment, self.ports, self.volumes, self.network)

    def __repr__(self):
        return self.__str__()