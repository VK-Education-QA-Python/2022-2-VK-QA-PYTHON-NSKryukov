import os
import signal
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
        app_stderr = open(os.path.join(repo_root, 'app_err.log'), 'w')
        app_stdout = open(os.path.join(repo_root, 'app_out.log'), 'w')

        app_path = os.path.join(repo_root, 'application', 'main.py')
        app_proc = subprocess.Popen(['python', app_path], stdout=app_stdout, stderr=app_stderr)
        config.app_proc = app_proc
        config.app_stderr = app_stderr
        config.app_stdout = app_stdout
        wait_ready(settings.APP_HOST, settings.APP_PORT)

        ######### mock configuration #########
        mock_stderr = open(os.path.join(repo_root, 'mock_err.log'), 'w')
        mock_stdout = open(os.path.join(repo_root, 'mock_log.log'), 'w')
        mock_path = os.path.join(repo_root, 'mock', 'flask_mock.py')
        mock_process = subprocess.Popen(['python', mock_path], stdout=mock_stdout, stderr=mock_stderr)
        config.mock_process = mock_process
        config.mock_stdout = mock_stdout
        config.mock_stderr = mock_stderr
        wait_ready(settings.MOCK_HOST, settings.MOCK_PORT)


def pytest_unconfigure(config):
    os.kill(config.app_proc.pid, signal.CTRL_C_EVENT)
    os.kill(config.mock_process.pid, signal.CTRL_C_EVENT)

    config.app_stderr.close()
    config.app_stdout.close()
    config.mock_stdout.close()
    config.mock_stderr.close()
