.. image:: https://github.com/ZeitOnline/zeit.nightwatch/workflows/Run%20tests/badge.svg
   :alt: Test status badge


===============
zeit.nightwatch
===============

pytest helpers for http smoke tests


Making HTTP requests
====================

``zeit.nightwatch.Browser`` wraps a `requests <https://pypi.org/project/requests/>`_ ``Session`` to provide some convenience features:

- Instantiate with a base url, and then only use paths:
  ``http = Browser('https://example.com'); http.get('/foo')``
  will request https://example.com/foo
- A convenience ``http`` fixture is provided, which can be configured via the ``nightwatch_config`` fixture.
- Use call instead of get, because it's just that *little bit* shorter.
  (``http('/foo')`` instead of ``http.get('/foo')``)
- Fill and submit forms, powered by `mechanicalsoup <https://pypi.org/project/MechanicalSoup/>`_.
  (We've customized this a bit, so that responses are only parsed with beautifulsoup if a feature like forms or links is actually used.)
- Logs request and response headers, so pytest prints these on test failures, to help debugging.
- Use ``sso_login(username, password)`` to log into https://meine.zeit.de.
- See source code for specific API details.


Example usage::

    @pytest.fixture(scope='session')
    def nightwatch_config():
        return dict(browser=dict(
            baseurl='https://example.com',
            sso_url='https://meine.zeit.de/anmelden',
        ))

    def test_my_site(http):
        r = http.get('/something')
        assert r.status_code == 200

    def test_login(http):
        http('/login')
        http.select_form()
        http.form['username'] = 'joe@example.com'
        http.form['password'] = 'secret'
        r = http.submit()
        assert '/home' in r.url

    def test_meinezeit_redirects_to_konto_after_login(http):
        r = http.sso_login('joe@example.com', 'secret')
        assert r.url == 'https://www.zeit.de/konto'


Examining HTML responses
========================

nightwatch adds two helper methods to the ``requests.Response`` object:

* ``xpath()``: parses the response with ``lxml.html`` and then calls ``xpath()`` on that document
* ``css()``: converts the selector to xpath using `cssselect <https://pypi.org/project/cssselect/>`_ and then calls ``xpath()``


Example usage::

    def test_error_page_contains_home_link(http):
        r = http('/nonexistent')
        assert r.status_code == 404
        assert r.css('a.home')


Controlling a browser with playwright
=====================================

nightwatch pulls in the ``pytest-playwright`` plugin, so you can use their fixtures.

Unfortunately, the playwright API is too unfriendly to allow nightwatch to set the base url automatically,
so you'll need to do that yourself, for example by overriding the ``base_url`` fixture::

    @pytest.fixture(scope="session")
    def base_url():
        return 'https://example.com'

    def test_playwright_works(page):
        page.goto('/something')


Running against different environments
======================================

To help with running the same tests against e.g. a staging and production environment, nightwatch declares a pytest commandline option ``--nightwatch-environment``.

A pattern we found helpful is using a fixture to provide environment-specific settings, like this::

    CONFIG_STAGING = {
        'base_url': 'https://staging.example.com',
        'username': 'staging_user',
        'password': 'secret',
    }

    CONFIG_PRODUCTION = {
        'base_url': 'https://www.example.com',
        'username': 'production_user',
        'password': 'secret2',
    }

    @pytest.fixture(scope='session')
    def nightwatch_config(nightwatch_environment):
        config = globals()['CONFIG_%s' % nightwatch_environment.upper()]
        return dict(environment=nightwatch_environment, browser=config)

    def test_some_integration_that_has_no_staging(http, nightwatch_config):
        if nightwatch_config['environment'] != 'production':
            pytest.skip('The xyz integration has no staging')
        r = http('/trigger-xyz')
        assert r.json()['message'] == 'OK'


Sending test results to prometheus
==================================

Like the medieval night watch people who made the rounds checking that doors were locked,
our use case for this library is continuous black box high-level tests that check that main functional areas of our systems are working.

For this purpose, we want to integrate the test results with our monitoring system, which is based on `Prometheus <https://prometheus.io>`_.
We've taken inspiration from the `pytest-prometheus <https://pypi.org/project/pytest-prometheus/>`_ plugin, and tweaked it a little to use a stable metric name, so we can write a generic alerting rule.

This uses the configured `Pushgateway <https://prometheus.io/docs/practices/pushing/>`_ to record metrics like this::

    nightwatch_check{test="test_error_page_contains_home_link",environment="staging",project="website",job="website-staging"}=1  # pass=1, fail=0

The ``environment`` label is populated from ``--nightwatch-environment``, see above,
and the ``project`` label is populated from an environment variable ``NIGHTWATCH_NAMESPACE`` if present
(this can be set e.g. via `k8s Downward API <https://kubernetes.io/docs/concepts/workloads/pods/downward-api/#available-fields>`_).
(Note that we use a separate ``project`` label, since the ``namespace`` label is occupied by the pushgateway itself and thus does not help.)

This functionality is disabled by default, nightwatch declares a pytest commandline option ``--prometheus`` which has to be present to enable pushing the metrics.
There also are commandline options to override the pushgateway url etc., please see the source code for those details.


Sending test results to elasticsearch
=====================================

We're running our tests as kubernetes pods, and their stdout/stderr output is captured and sent to elasticsearch.
However the normal pytest output is meant for humans, but is not machine-readable.
Thus we've implemented a JSON lines test report format that can be enabled with ``--json-report=filename`` or ``--json-report=-`` to directly send to stdout.

Here's an output example, formatted for readability (in reality, each test produces a single JSON line, since that's what our k8s log processor expects)::

    {
      "time": "2023-12-08T10:37:40.630617+00:00",
      "test_stage": "call",
      "test_class": "smoketest.test_api",
      "test_name": "test_example",
      "test_outcome": "passed",
      "system_log": "11:37:40 INFO  [zeit.nightwatch.requests][MainThread] > POST http://example.com/something\n..."
    }
