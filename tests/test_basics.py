import pytest


@pytest.fixture(scope='session')
def nightwatch_config():
    return dict(browser=dict(baseurl='https://httpbin.org'),
                selenium=dict(baseurl='https://httpbin.org'))


def test_get(http):
    r = http.get('/get')
    assert r.status_code == 200


def test_playwright_works(playwright):
    playwright.goto('http://www.zeit.de')
    playwright.context.add_cookies(
        [{'url': 'https://www.zeit.de', 'name': 'brownie', 'value': 'big'}])
    cookies = [c['name'] for c in playwright.context.cookies() if 'name' in c]
    assert 'brownie' in cookies


def test_playwright_cookie_is_not_stored_between_tests(playwright):
    playwright.goto('http://www.zeit.de')
    cookies = [c['name'] for c in playwright.context.cookies() if 'name' in c]
    assert 'brownie' not in cookies


def test_selenium_works(selenium):
    selenium.get('/forms/post')
    assert selenium.find_element_by_css_selector('form')
