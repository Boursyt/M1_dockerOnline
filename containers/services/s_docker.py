import docker
from docker import errors
import yaml

# variable global
#client = docker.from_env()
client = docker.DockerClient(base_url='tcp://192.168.1.39:2375', tls=False)
class DockerService:
    def __init__(self, name=None, image=None, command=None, environment=None, ports=None, volumes=None, network=None):
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
        container= client.containers.get(self.name)
        if container:
            try:
                container.start()
                return container
            except errors.APIError as e:
                print(f"Error starting container: {e}")
                return None
        return None

    def docker_stop(self):
        container = client.containers.get(self.name)
        if container:
            try:
                container.stop()
                return container
            except errors.APIError as e:
                print(f"Error stopping container: {e}")
                return None
    def docker_remove(self):
        container = client.containers.get(self.name)
        if container:
            try:
                container.remove()
                return container
            except errors.APIError as e:
                print(f"Error removing container: {e}")
                return None

    def docker_list(self):
        return client.containers.list(all=True)

    def list_images(self):
        return client.images.list()

    def run_dockerfile(self, dockerfile):
        image, logs = client.images.build(fileobj=dockerfile, tag='my_image')
        for log in logs:
            print(log)
        return image

    def run_compose(self, compose_data):
        try:
            if compose_data is None:
                raise ValueError("Compose data is None, possibly due to an invalid YAML file.")


            services = compose_data.get('services', {})

            if not services:
                raise ValueError("No services found in compose data")

            for service_name, service_data in services.items():
                image = service_data.get('image')

                if not image:
                    raise errors.DockerException(f"Missing mandatory 'image' key in service: {service_name}")

                # Préparer les options pour la création du conteneur
                options = {key: value for key, value in service_data.items() if key != 'image'}

                # Créer et démarrer le conteneur
                container = client.containers.run(image=image, name=service_name, **options)
                print(f"Container {service_name} created with ID: {container.id}")

            return "Containers created successfully"

        except (errors.DockerException, errors.APIError, yaml.YAMLError, ValueError) as e:
            return f"Error creating containers: {str(e)}"


    def __str__(self):
        return 'DockerService(name={}, image={}, command={}, environment={}, ports={}, volumes={}, network={})'.format(
            self.name, self.image, self.command, self.environment, self.ports, self.volumes, self.network)

    def __repr__(self):
        return self.__str__()