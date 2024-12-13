from selenium.webdriver.common.by import By
import pytest


@pytest.fixture(scope="session")
def nightwatch_config():
    return dict(
        browser=dict(baseurl="https://httpbin.org"),
        selenium=dict(baseurl="https://httpbin.org"),
    )


@pytest.fixture(scope="session")
def base_url(nightwatch_config):
    return nightwatch_config.get("selenium", {}).get("baseurl")


def test_get(http):
    r = http.get("/get")
    assert r.status_code == 200


def test_selenium_works(selenium):
    selenium.get("/forms/post")
    assert selenium.find_element(By.CSS_SELECTOR, "form")


def test_playwright_works(page):
    page.goto("/forms/post")
    assert page.locator("form").count() == 1
