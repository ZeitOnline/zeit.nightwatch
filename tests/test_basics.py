import pytest


@pytest.fixture(scope="session")
def base_url(nightwatch_config):
    return nightwatch_config.get("browser", {}).get("baseurl")


def test_get(http):
    r = http.get("/get")
    assert r.status_code == 200


def test_playwright_works(page):
    page.goto("/forms/post")
    assert page.locator("form").count() == 1
