import uuid
from ui.fixtures import *


@pytest.fixture(scope='session')
def repo_root():
    return os.path.abspath(os.path.join(__file__, os.path.pardir))


@pytest.fixture(scope='session')
def base_temp_dir():
    if sys.platform.startswith('win'):
        base_dir = 'C:\\tests'
    else:
        base_dir = '/tmp/tests'
    if os.path.exists(base_dir):
        shutil.rmtree(base_dir)
    return base_dir


@pytest.fixture(scope='function')
def temp_dir(request):
    if sys.platform.startswith('win'):
        test_dir = os.path.join(request.config.base_temp_dir,
                                request._pyfuncitem.nodeid.replace('/', '_').replace('::', '_'))
    else:
        test_dir = os.path.join(request.config.base_temp_dir, request._pyfuncitem.nodeid)
    os.makedirs(test_dir)
    return test_dir


@pytest.fixture(scope='function')
def unique_name():
    unique_name = uuid.uuid1()
    return str(unique_name)


def pytest_addoption(parser):
    parser.addoption('--browser', default='chrome')
    parser.addoption('--url', default='https://target-sandbox.my.com/dashboard/')
    parser.addoption('--headless', action='store_true')
    parser.addoption('--selenoid', action='store_true')
    parser.addoption('--vnc', action='store_true')
    parser.addoption('--enable_video', action='store_true')


@pytest.fixture(scope='session')
def config(request):
    browser = request.config.getoption('--browser')
    url = request.config.getoption('--url')
    headless = request.config.getoption('--headless')
    if request.config.getoption('--selenoid'):
        if request.config.getoption('--vnc'):
            vnc = True
        else:
            vnc = False
        if request.config.getoption('--enable_video'):
            enable_video = True
        else:
            enable_video = False
        selenoid = 'http://127.0.0.1:4444/wd/hub'
    else:
        selenoid = None

        vnc = False
        enable_video = False

    return {
        'browser': browser,
        'url': url,
        'headless': headless,
        'selenoid': selenoid,
        'vnc': vnc,
        'enable_video': enable_video,
    }

