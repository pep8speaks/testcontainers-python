import blindspin
import crayons
from docker.models.containers import Container

from testcontainers.core.docker_client import DockerClient
from testcontainers.core.exceptions import ContainerStartException
from testcontainers.core.utils import is_windows


class DockerContainer(object):
    def __init__(self, image):
        self.env = {}
        self.ports = {}
        self._docker = DockerClient()
        self.image = image
        self._container = None
        self._command = None
        self._name = None

    def add_env(self, key, value):
        self.env[key] = value
        return self

    def bind_ports(self, container, host=None):
        self.ports[container] = host
        return self

    def _configure(self):
        pass

    def start(self):
        self._configure()
        print("")
        print("{} {}".format(crayons.yellow("Pulling image"), crayons.red(self.image)))
        with blindspin.spinner():
            self._container = self.get_docker_client().run(self.image,
                                                           command=self._command,
                                                           detach=True,
                                                           environment=self.env,
                                                           ports=self.ports,
                                                           publish_all_ports=True,
                                                           name=self._name)
                                                           publish_all_ports=True)
        print("")
        print("Container started: ", crayons.yellow(self._container.short_id, bold=True))
        return self

    def stop(self):
        self.get_wrapped_contaner().remove(force=True)

    def __enter__(self):
        return self.start()

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.stop()

    def get_container_host_ip(self) -> str:
        if is_windows():
            return "localhost"
        else:
            return "0.0.0.0"

    def get_exposed_port(self, port) -> str:
        return self.get_docker_client().port(self._container.id, port)

    def with_command(self, command):
        self._command = command
        return self

    def with_name(self, name):
        self._name = name
        return self

    def get_wrapped_contaner(self) -> Container:
        return self._container

    def get_docker_client(self) -> DockerClient:
        return self._docker

    def exec(self, command):
        if not self._container:
            raise ContainerStartException("Container should be started before")
        return self.get_wrapped_contaner().exec_run(command)
