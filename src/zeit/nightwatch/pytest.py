import logging

import pytest

import zeit.nightwatch.jsonreport
import zeit.nightwatch.playwright  # NOQA activate sso_login monkeypatch
import zeit.nightwatch.prometheus


def pytest_addoption(parser):
    parser.addoption(
        "--nightwatch-environment",
        default="staging",
        help=nightwatch_environment.__doc__,
    )
    zeit.nightwatch.jsonreport.addoption(parser)
    zeit.nightwatch.prometheus.addoption(parser)


@pytest.fixture(scope="session")
def nightwatch_environment(request):  # convenience spelling
    """Run tests against this environment (staging, production, etc.)"""
    return request.config.getoption("--nightwatch-environment")


@pytest.fixture()
def http(nightwatch_config):
    """Testbrowser using `requests` & `mechanicalsoup` libraries"""
    config = nightwatch_config.get("browser", {})
    return zeit.nightwatch.Browser(**config)


@pytest.fixture(scope="session")
def zeitde(nightwatch_environment):
    if nightwatch_environment == "production":
        return lambda x: "https://%s.zeit.de" % x
    else:
        return lambda x: "https://%s.%s.zeit.de" % (x, nightwatch_environment)


def pytest_configure(config):
    logging.getLogger().setLevel(logging.INFO)
    config.inicfg["log_format"] = (
        "%(asctime)s %(levelname)-5.5s [%(name)s][%(threadName)s] %(message)s"
    )

    config.addinivalue_line(
        "markers", "playwright: Playwright test (helper for test selection)"
    )

    # Is there seriously no proper API?
    config._inicache["junit_logging"] = "all"
    config._inicache["junit_log_passing_tests"] = False

    zeit.nightwatch.jsonreport.configure(config)
    zeit.nightwatch.prometheus.configure(config)


def pytest_unconfigure(config):
    zeit.nightwatch.jsonreport.unconfigure(config)
    zeit.nightwatch.prometheus.unconfigure(config)


def pytest_collection_modifyitems(items):
    """Allow selecting playwright test with `pytest -m playwright` or
    `-m 'not playwright'`.
    """
    for item in items:
        if "page" in getattr(item, "fixturenames", []):
            item.add_marker(pytest.mark.playwright)
