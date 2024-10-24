import docker
from django.contrib.auth import get_user
from docker import errors
from django.core.exceptions import ObjectDoesNotExist
import yaml
from containers.models import Container
import os
from dns.service.s_ovh import adddns


# variable global
#client = docker.from_env()
from dotenv import load_dotenv
load_dotenv()

host = os.getenv('DOCKER_HOSTS')
TLS_veriy=os.getenv('DOCKER_TLS_VERIFY')
client = docker.DockerClient(base_url=host, tls=None)


class DockerService:
    """
    Class pour la logique metier lieer a la manipulation de Docker
    """
    def __init__(self, name=None, image=None, command=None, environment=None, ports=None, volumes=None, network=None):

        self.name = name
        self.image = image
        self.command = command
        self.environment = environment
        self.ports = ports
        self.volumes = volumes
        self.network = network

    def traefikRoute(self, name):
        labels = {
            "traefik.enable": "true",
            f"traefik.http.routers.{name}.rule": f"Host(`{name}.dockeronline.ovh`)",
            f"traefik.http.routers.{name}.entrypoints": "web",
            f"traefik.http.services.{name}.loadbalancer.server.port": "8084",

            # Middleware pour redirection de port
            f"traefik.http.middlewares.{name}-redirect-to-port.redirectscheme.scheme": "http",
            f"traefik.http.middlewares.{name}-redirect-to-port.redirectscheme.port": "8084",
            f"traefik.http.routers.{name}.middlewares": f"{name}-redirect-to-port@docker"
        }
        return labels




    def dockerStatus(self):

        try:
            container = client.containers.get(self.name)
            return container.status
        except errors.NotFound:
            return 'Container not found'
        except errors.APIError as e:
            print(f"Error getting container status: {e}")
            return 'Error'

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

    def removeDockerBDD(self,name):
        try:
            container = Container.objects.get(name=name)
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
                network=self.network,
                labels=self.traefikRoute(self.name)
            )
            self.addDockerBDD(request)
            dns=adddns(self.name)
            return container
        except errors.APIError as e:
            print(f"Error creating container: {e}")
            return None

    def docker_run(self,name):
        container= client.containers.get(name)
        if container:
            try:
                container.start()
                return container
            except errors.APIError as e:
                print(f"Error starting container: {e}")
                return None
        return None

    def docker_stop(self,name):
        container = client.containers.get(name)
        if container:
            try:
                container.stop()
                return container
            except errors.APIError as e:
                print(f"Error stopping container: {e}")
                return None

    def docker_remove(self, name):
        try:
            container = client.containers.get(name)
            if container:
                container.remove()
                self.removeDockerBDD(name)
                return container
        except errors.NotFound:
            print(f"Container '{name}' not found.")
        except errors.APIError as e:
            print(f"Error removing container: {e}")
        except Exception as e:
            print(f"Unexpected error: {e}")
        return None

    def docker_list(self):
        return client.containers.list(all=True)


    def docker_list_user(self, request):
        userLogin = get_user(request)
        user_containers = []
        for container in client.containers.list(all=True):
            if container.name.startswith(f'{userLogin}'):
                user_containers.append({
                    "id": container.id,
                    "name": container.name,
                    "status": container.status,
                    "image": container.image.tags[0] if container.image.tags else "No tag"
                })
        return user_containers

    def list_images(self):
        return client.images.list()

    def run_dockerfile(self,request, dockerfile,name):
        try:
            if dockerfile is None:
                raise ValueError("Dockerfile is None")

            image, _ = client.images.build(fileobj=dockerfile.file, rm=True, tag="my_image:latest")
            self.name=name
            print(f"Image built with tag: {image.tags[0] if image.tags else 'No tag'}")
            container = client.containers.run(image=image.tags[0], name=self.name, detach=True, labels=self.traefikRoute(self.name))
            self.addDockerBDD(request)
            print(f"Container {image} added to database")
            dns=adddns(self.name)
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
                container = client.containers.run(image=image, name=name,labels=self.traefikRoute(self.name), detach=True, **options)
                print(f"Container {service_name} created with ID: {container.id}")
                self.addDockerBDD(request)
                dns=adddns(self.name)
                print(f"Container {service_name} added to database")
            return "Containers created successfully"
        except (errors.DockerException, errors.APIError, yaml.YAMLError, ValueError) as e:
            return f"Error creating containers: {str(e)}"

    def get_logs(self,name):
        container = client.containers.get(name)
        if container:
            try:
                logs = container.logs()
                return logs.decode('utf-8')
            except errors.APIError as e:
                print(f"Error getting logs: {e}")
                return None
        return None

    def get_Docker_error(self, name):
        try:
            container = client.containers.get(name)
            if container:
                error_info = client.api.inspect_container(name)
                state = error_info['State']
                exit_code = state['ExitCode']
                error_message = state.get('Error', '')

                return {
                    'state': state,
                    'exit_code': exit_code,
                    'error_message': error_message
                }
        except docker.errors.NotFound:
            print(f"Container '{name}' not found.")
        except docker.errors.APIError as e:
            print(f"API Error getting logs for '{name}': {e}")
        except Exception as e:
            print(f"Unexpected error: {e}")

        return None

