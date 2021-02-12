import pytest
import zeit.nightwatch


@pytest.fixture
def http():
    return zeit.nightwatch.requests.Browser('https://httpbin.org')


def test_get(http):
    r = http.get('/get')
    assert r.status_code == 200
