import pytest


@pytest.fixture(scope='session')
def nightwatch_config():
    return dict(browser=dict(baseurl='https://httpbin.org'))


def test_get(http):
    r = http.get('/get')
    assert r.status_code == 200
