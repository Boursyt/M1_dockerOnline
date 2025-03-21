import docker
from django.contrib.auth import get_user
from docker import errors
from django.core.exceptions import ObjectDoesNotExist
import yaml
from containers.models import Container
import os
from dns.service.s_ovh import adddns, rmdns
from io import BytesIO
from dotenv import load_dotenv

# Charger les variables d'environnement depuis .env
load_dotenv()

# Charger les paramètres Docker depuis les variables d'environnement
host = os.getenv('DOCKER_HOSTS')
tls_verify = os.getenv('DOCKER_TLS_VERIFY') == 'True'
cert_path = os.getenv('DOCKER_CERT_PATH')

# Configuration du TLS
tls_config = docker.tls.TLSConfig(
    client_cert=(f"{cert_path}/client-cert.pem", f"{cert_path}/client-key.pem"),
    ca_cert=f"{cert_path}/ca.pem",
    verify=tls_verify
)

# Initialiser le client Docker avec TLS
client = docker.DockerClient(base_url=host, tls=tls_config)


class DockerService:
    """
    Class pour la logique metier lieer a la manipulation de Docker.
    """
    def __init__(self, name=None, image=None, command=None, environment=None, ports=None, volumes=None, network=None):

        self.name = name
        self.image = image
        self.command = command
        self.environment = environment
        self.ports = ports
        self.volumes = volumes
        self.network = network
        if os.path.exists("./counter.txt"):
            with open("./counter.txt", "r") as file:
                self.count = int(file.read())
        else:
            self.count = 8000
            with open("./counter.txt", "w") as file:
                file.write(str(self.count))

    def traefikRoute(self, name):
        """
        Fonction pour definir les labels pour Traefik.
        :param name: nom de type username-container
        :return: labels
        """
        labels = {
            "traefik.enable": "true",
            f"traefik.http.routers.{name}.rule": f"Host(`{name}.dockeronline.ovh`)",
            f"traefik.http.routers.{name}.entrypoints": "web",
            f"traefik.http.services.{name}.loadbalancer.server.port": "80",
            f"traefik.docker.network": "traefik-net"
        }
        return labels

    def counter(self):
        """
        Fonction pour incrementer le compteur de port. Ecrait dans un fichier
        :return: le compteur
        """
        self.count += 1
        with open("counter.txt", "w") as file: # "w" donc ecrasement de la valeur
            file.write(str(self.count))
        return self.count

    def dockerStatus(self):
        """
        Fonction pour obtenir le status d'un conteneur.
        :return: errors, status
        """
        try:
            container = client.containers.get(self.name)
            return container.status
        except errors.NotFound:
            return 'Container not found'
        except errors.APIError as e:
            print(f"Error getting container status: {e}")
            return 'Error'

    def addDockerBDD(self,request):
        """
        Fonction pour ajouter un conteneur a la base de donnees.
        :param request:
        :return: errors
        """
        try:
            specs = f'{self.image},{self.ports},{self.command},{self.environment},{self.network },{self.volumes}'
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
        """
        Fonction pour supprimer un conteneur de la base de donnees.
        :param name:
        :return:
        """
        try:
            container = Container.objects.get(name=name)
            container.delete()
            print(f"Le conteneur '{self.name}' a été supprimé de la base de données.")
        except ObjectDoesNotExist:
            print(f"Le conteneur '{self.name}' n'existe pas dans la base de données.")
        except Exception as e:
            print(f"Une erreur s'est produite lors de la suppression du conteneur : {e}")


    def download_image(self, url):
        """
        Fonction pour telecharger une image Docker. Image du docker hub uniquement. Via le nom de l'image.
        :param url:
        :return:
        """
        try:
            self.image = client.images.pull(url)
        except errors.APIError as e:
            print(f"Error pulling image: {e}")
            self.image = None
        return self.image

    def docker_create(self,request):
        """
        Fonction pour creer un conteneur Docker. Utilise les attributs de la classe. Les utilisent pour creer un conteneur.
        :param request:
        :return: message de reussite ou d'echec avec les informations du conteneur
        """
        self.image = self.download_image(self.image)

        try:
            container = client.containers.create(
                name=self.name,
                image=self.image,
                command=self.command,
                ports=self.ports,
                volumes=self.volumes,
                network='traefik-net',
                labels=self.traefikRoute(self.name)
            )
            self.addDockerBDD(request)
            dns=adddns(self.name)
            return container
        except errors.APIError as e:
            print(f"Error creating container: {e}")
            return None

    def docker_run(self,name):
        """
        Fonction pour demarrer un conteneur Docker. Via le nom du conteneur.
        :param name:
        :return: message de reussite ou d'echec ou errors
        """
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
        """
        Fonction pour arreter un conteneur Docker. Via le nom du conteneur.
        :param name:
        :return: message de reussite ou d'echec ou errors
        """
        container = client.containers.get(name)
        if container:
            try:
                container.stop()
                return container
            except errors.APIError as e:
                print(f"Error stopping container: {e}")
                return None

    def docker_remove(self, name):
        """
        Fonction pour supprimer un conteneur Docker. Via le nom du conteneur.
        :param name:
        :return: message de reussite ou d'echec ou errors
        """
        try:
            container = client.containers.get(name)
            if container:
                container.remove()
                self.removeDockerBDD(name)
                rmdns(name)
                return container
        except errors.NotFound:
            print(f"Container '{name}' not found.")
        except errors.APIError as e:
            print(f"Error removing container: {e}")
        except Exception as e:
            print(f"Unexpected error: {e}")
        return None

    def docker_list(self):
        """
        Fonction pour lister les conteneurs Docker. Tous les conteneurs.
        :return: liste des conteneurs
        """
        containers = []
        for container in client.containers.list(all=True):
            containers.append({
                "id": container.id,
                "name": container.name,
                "status": container.status,
                "image": container.image.tags[0] if container.image.tags else "No tag"
            })
        return containers

    def docker_list_user(self, request):
        """
        Fonction pour lister les conteneurs Docker. Seulement les conteneurs de l'utilisateur connecte.
        :param request:
        :return: liste des conteneurs
        """
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
        """
        Fonction pour lister les images Docker.
        :return: liste des images
        """

        return client.images.list()


    def getPortExposed(self, dockerfile):
        """
        Fonction pour obtenir le port expose dans un Dockerfile.
        :param dockerfile: le fichier dockerfile
        :return: parts[1] : le port expose
        """
        dockerfile_content = dockerfile.read().decode("utf-8")
        dockerfile.seek(0)
        for line in dockerfile_content.splitlines():
            if line.startswith("EXPOSE"):
                parts = line.split()
                if len(parts) > 1:
                    return parts[1]  # Renvoie le port exposé
        raise ValueError("No EXPOSE directive found in Dockerfile")

    def run_dockerfile(self, request, dockerfile, name):
        """
        Fonction pour creer un conteneur Docker a partir d'un Dockerfile.
        :param request: la requete http
        :param dockerfile: le fichier dockerfile
        :param name: nom a donner au conteneur
        :return: message de reussite ou d'echec ou errors
        """
        try:
            if dockerfile is None:
                raise ValueError("Dockerfile is None")

            expose = self.getPortExposed(dockerfile)
            redirect_port = self.counter()
            port = {str(expose): redirect_port}
            image, _ = client.images.build(fileobj=BytesIO(dockerfile.read()), rm=True, tag="my_image:latest")
            self.name = name
            print(f"Image built with tag: {image.tags[0] if image.tags else 'No tag'}")
            container = client.containers.run(
                image=image.tags[0],
                name=self.name,
                detach=True,
                ports=port,
                network='traefik-net',
                labels=self.traefikRoute(self.name)
            )

            self.addDockerBDD(request)
            print(f"Container {image} added to database")

            dns = adddns(self.name)
            print(f"Container started with ID: {container.id}")
            return container

        except (errors.BuildError, errors.APIError) as e:
            print(f"Error building or running container: {e}")
            return None

    def getPortCompose(self, ports):
        """
        Fonction pour obtenir les ports d'un conteneur a partir d'un fichier docker-compose.yml.
        :param ports:
        :return:  liste des ports du conteneur
        """
        if not ports:
            pass
        container_ports = [int(port.split(':')[1]) for port in ports]
        return container_ports  # Retourne une liste des ports de conteneur


    def run_compose(self,request, compose_data, name):
        """
        Fonction pour creer un conteneur Docker a partir d'un fichier docker-compose.yml.
        :param request: requete http
        :param compose_data: le fichier docker-compose.yml
        :param name: le nom a donner au conteneur
        :return: message de reussite ou d'echec ou errors
        """

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

                options = {key: value for key, value in service_data.items() if key not in ['image','ports','restart','depends_on']}
                container_name = f"{name}-{service_name}"
                self.name=container_name

                ports = service_data.get('ports', [])
                container_ports = self.getPortCompose(ports)
                port_mappings = {}
                for container_port in container_ports:
                    redirect_port = self.counter()  # Port redirigé sur l'hôte
                    port_mappings[str(container_port)] = redirect_port

                container = client.containers.run(
                    image=image,
                    name=container_name,
                    labels=self.traefikRoute(self.name),
                    ports=port_mappings,
                    detach=True,
                    network='traefik-net',
                    **options)

                print(f"Container {service_name} created with ID: {container.id}")
                self.addDockerBDD(request)
                dns=adddns(self.name)
                print(f"Container {service_name} added to database")
            return "Containers created successfully"

        except (errors.DockerException, errors.APIError, yaml.YAMLError, ValueError) as e:
            return f"Error creating containers: {str(e)}"

    def get_logs(self,name):
        """
        Fonction pour obtenir les logs d'un conteneur Docker.
        :param name: nom du conteneur
        :return: les messages d'ereurs, les logs
        """
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
        """
        Fonction pour obtenir les erreurs d'un conteneur Docker.
        :param name: nom du conteneur
        :return: les messages d'erreurs, les erreurs du conteneur
        """
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

