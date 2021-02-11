import logging
import pytest


def pytest_addoption(parser):
    parser.addoption(
        '--nightwatch-environment', default='staging',
        help=nightwatch_environment.__doc__)


@pytest.fixture(scope='session')
def nightwatch_environment(request):  # convenience spelling
    """Run tests against this environment (staging, production, etc.)"""
    return request.config.getoption('--nightwatch-environment')


@pytest.fixture(scope='session')
def zeitde(nightwatch_environment):
    if nightwatch_environment == 'production':
        return lambda x: 'https://%s.zeit.de' % x
    else:
        return lambda x: 'https://%s.%s.zeit.de' % (x, nightwatch_environment)


def pytest_configure(config):
    logging.getLogger().setLevel(logging.INFO)
    config.inicfg['log_format'] = (
        '%(asctime)s %(levelname)-5.5s [%(name)s][%(threadName)s] %(message)s')
