import os
import re

from .conftest import infra_dir_path, root_dir


class TestDockerfileCompose:

    def test_infra_structure(self):
        assert 'infra' in os.listdir(root_dir), (
            f'Проверьте, что по пути {root_dir} есть папка `infra`'
        )
        assert os.path.isdir(infra_dir_path), (
            f'Проверьте, что {infra_dir_path} - это папка, а не файл'
        )

    def test_docker_compose_file(self):
        try:
            with open(f'{os.path.join(infra_dir_path, "docker-compose.yaml")}', 'r') as f:
                docker_compose = f.read()
        except FileNotFoundError:
            assert False, f'Проверьте, что добавили файл `docker-compose.yaml` в директорию {infra_dir_path} '

        assert re.search(r'image:\s+postgres:', docker_compose), (
            'Проверьте, что добавили образ postgres:latest в файл docker-compose.yaml'
        )
