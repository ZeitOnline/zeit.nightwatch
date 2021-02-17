import logging
import pytest
import zeit.nightwatch.prometheus


def pytest_addoption(parser):
    parser.addoption(
        '--nightwatch-environment', default='staging',
        help=nightwatch_environment.__doc__)
    parser.addoption(
        '--selenium-visible', action='store_true', default=False,
        help='Show selenium browser when running tests')
    zeit.nightwatch.prometheus.addoption(parser)


@pytest.fixture(scope='session')
def nightwatch_environment(request):  # convenience spelling
    """Run tests against this environment (staging, production, etc.)"""
    return request.config.getoption('--nightwatch-environment')


@pytest.fixture
def http(nightwatch_config):
    """Testbrowser using `requests` & `mechanicalsoup` libraries"""
    config = nightwatch_config.get('browser', {})
    return zeit.nightwatch.Browser(**config)


@pytest.fixture(scope='session')
def selenium_session(request, nightwatch_config):
    """Setup for `selenium` based testbrowser (not intended for direct use)"""
    headless = not request.config.getoption('--selenium-visible')
    config = nightwatch_config.get('selenium', {})
    config.setdefault('headless', headless)
    browser = zeit.nightwatch.WebDriverChrome(**config)
    request.addfinalizer(browser.quit)
    return browser


@pytest.fixture
def selenium(selenium_session):
    """Testbrowser using `selenium` & Chrome webdriver"""
    yield selenium_session
    selenium_session.delete_all_cookies()


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

    config.addinivalue_line(
        'markers', 'selenium: Selenium test (helper for test selection)')

    zeit.nightwatch.prometheus.configure(config)


def pytest_unconfigure(config):
    zeit.nightwatch.prometheus.unconfigure(config)


def pytest_collection_modifyitems(items):
    """Allow selecting selenium test with `pytest -m selenium` or
    `-m 'not selenium'`. (The fixture must be provided by the client project.)
    """
    for item in items:
        if 'selenium' in getattr(item, 'fixturenames', []):
            item.add_marker(pytest.mark.selenium)
