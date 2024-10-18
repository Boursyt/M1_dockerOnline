import docker
from django.contrib.auth import get_user
from docker import errors
from django.core.exceptions import ObjectDoesNotExist
import yaml
from urllib3 import request
from containers.models import Container

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


    def dockerStatus(self):
        try:
            container = client.containers.get(self.name)
            return container.status
        except errors.NotFound:
            return 'Container not found'
        except errors.APIError as e:
            print(f"Error getting container status: {e}")
            return 'Error'

    #on ajoute le container a la base de données (definie dans m_container)
    def addDockerBDD(self,request):
        try:
            specs = f'{self.image},{self.ports},{self.command},{self.environment},{self.network},{self.volumes}'
            getStatus = self.dockerStatus()
            container = Container.objects.create(
                user=get_user(request),
                name=self.name,
                spec=specs,
                status=getStatus
            )
            container.save()
        except Exception as e:
            print(f"Error adding container to database: {e}")

    def removeDockerBDD(self):
        try:
            # Trouver le conteneur en fonction du nom (ou un autre critère, selon tes besoins)
            container = Container.objects.get(name=self.name)

            # Ici, on peut aussi gérer la logique Docker si tu veux arrêter ou supprimer le conteneur Docker côté Docker Engine
            self.docker_stop()

            # Supprimer l'objet de la base de données
            container.delete()

            print(f"Le conteneur '{self.name}' a été supprimé de la base de données.")
        except ObjectDoesNotExist:
            print(f"Le conteneur '{self.name}' n'existe pas dans la base de données.")
        except Exception as e:
            print(f"Une erreur s'est produite lors de la suppression du conteneur : {e}")


    def download_image(self, url):
        try:
            self.image = client.images.pull(url)
        except errors.APIError as e:
            print(f"Error pulling image: {e}")
            self.image = None
        return self.image

    def docker_create(self,request):
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
            self.addDockerBDD(request)
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
                self.removeDockerBDD()
                return container
            except errors.APIError as e:
                print(f"Error removing container: {e}")
                return None

    def docker_list(self):
        return client.containers.list(all=True)

    def list_images(self):
        return client.images.list()

    def run_dockerfile(self,request, dockerfile,name):
        try:
            if dockerfile is None:
                raise ValueError("Dockerfile is None")
            # Build the image from the Dockerfile

            image, _ = client.images.build(fileobj=dockerfile.file, rm=True, tag="my_image:latest")
            self.name=name
            self.addDockerBDD(request)
            print(f"Container {image} added to database")
            print(f"Image built with tag: {image.tags[0] if image.tags else 'No tag'}")
            # Run a container using the built image
            container = client.containers.run(image=image.tags[0], name=self.name, detach=True)

            print(f"Container started with ID: {container.id}")
            return container
        except (errors.BuildError, errors.APIError) as e:
            print(f"Error building or running container: {e}")
            return None

    def run_compose(self,request, compose_data, name):
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
                options = {key: value for key, value in service_data.items() if key != 'image'}
                self.name=name
                container = client.containers.run(image=image, name=name, detach=True, **options)
                print(f"Container {service_name} created with ID: {container.id}")
                self.addDockerBDD(request)
                print(f"Container {service_name} added to database")
            return "Containers created successfully"
        except (errors.DockerException, errors.APIError, yaml.YAMLError, ValueError) as e:
            return f"Error creating containers: {str(e)}"

    def get_logs(self):
        container = client.containers.get(self.name)
        if container:
            try:
                logs = container.logs()
                return logs.decode('utf-8')
            except errors.APIError as e:
                print(f"Error getting logs: {e}")
                return None
        return None
    def __str__(self):
        return 'DockerService(name={}, image={}, command={}, environment={}, ports={}, volumes={}, network={})'.format(
            self.name, self.image, self.command, self.environment, self.ports, self.volumes, self.network)

    def __repr__(self):
        return self.__str__()