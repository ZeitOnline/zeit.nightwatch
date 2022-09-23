import pytest
from selenium.webdriver.common.by import By


@pytest.fixture(scope='session')
def nightwatch_config():
    return dict(browser=dict(baseurl='https://httpbin.org'),
                selenium=dict(baseurl='https://httpbin.org'))


def test_get(http):
    r = http.get('/get')
    assert r.status_code == 200


def test_selenium_works(selenium):
    selenium.get('/forms/post')
    assert selenium.find_element(By.CSS_SELECTOR, 'form')
