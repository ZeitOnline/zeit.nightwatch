import logging
import pytest


def pytest_addoption(parser):
    parser.addoption(
        '--nightwatch-environment', default='staging',
        help=nightwatch_environment.__doc__)
    parser.addoption(
        '--selenium-visible', action='store_true', default=False,
        help='Show selenium browser when running tests')
    parser.addoption(
        '--prometheus', action='store_true', default=False,
        help='Send metrics to prometheus')


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


@pytest.hookimpl(tryfirst=True)  # run before pytest-prometheus to configure it
def pytest_configure(config):
    logging.getLogger().setLevel(logging.INFO)
    config.inicfg['log_format'] = (
        '%(asctime)s %(levelname)-5.5s [%(name)s][%(threadName)s] %(message)s')

    config.addinivalue_line(
        'markers', 'selenium: Selenium test (helper for test selection)')

    configure_prometheus(config)


def configure_prometheus(config):
    if not config.getoption('--prometheus'):
        config.option.prometheus_pushgateway_url = None  # disables reporting
        return

    # Set sensible defaults
    if not config.option.prometheus_pushgateway_url:
        config.option.prometheus_pushgateway_url = (
            'https://prometheus-pushgw.ops.zeit.de')
    if not config.option.prometheus_metric_prefix:
        config.option.prometheus_metric_prefix = 'nightwatch_'
    if not config.option.prometheus_job_name:
        config.option.prometheus_job_name = 'unknown'

    if config.option.prometheus_extra_label is None:
        config.option.prometheus_extra_label = []
    config.option.prometheus_extra_label.append(
        'environment=%s' % config.getoption('--nightwatch-environment'))


def pytest_collection_modifyitems(items):
    """Allow selecting selenium test with `pytest -m selenium` or
    `-m 'not selenium'`. (The fixture must be provided by the client project.)
    """
    for item in items:
        if 'selenium' in item.fixturenames:
            item.add_marker(pytest.mark.selenium)
