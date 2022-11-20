import os
import subprocess
import time

import requests

import settings

repo_root = os.path.abspath(os.path.join(__file__, os.pardir))


def wait_ready(host, port):
    started = False
    st = time.time()
    while time.time() - st <= 5:
        try:
            requests.get(f'http://{host}:{port}')
            started = True
            break
        except ConnectionError:
            pass

    if not started:
        raise RuntimeError('App did not started in 5s!')


def pytest_configure(config):
    if not hasattr(config, 'workerinput'):
        ######### application configuration #########
        app_stderr = open(os.path.join(repo_root, 'application', 'logfile.log'), 'w')
        app_stdout = open(os.path.join(repo_root, 'application', 'logfile.log'), 'w')

        app_path = os.path.join(repo_root, 'application', 'main.py')
        mock_proc = subprocess.Popen(['python', app_path], stdout=app_stdout, stderr=app_stderr)
        config.app_proc = mock_proc
        wait_ready(settings.APP_HOST, settings.APP_PORT)

        ######### mock configuration #########

        from mock import flask_mock
        flask_mock.run_mock()
        wait_ready(settings.MOCK_HOST, settings.MOCK_PORT)


def pytest_unconfigure(config):
    config.app_proc.terminate()

    requests.get(f'http://{settings.MOCK_HOST}:{settings.MOCK_PORT}/shutdown')
