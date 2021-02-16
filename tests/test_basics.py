import pytest


@pytest.fixture
def http(nightwatch):
    return nightwatch.requests.Browser('https://httpbin.org')


def test_get(http):
    r = http.get('/get')
    assert r.status_code == 200
