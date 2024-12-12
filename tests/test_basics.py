import pytest


@pytest.fixture(scope="session")
def nightwatch_config():
    return dict(
        browser=dict(baseurl="https://httpbin.org"),
        playwright=dict(baseurl="https://httpbin.org"),
    )


def test_get(http):
    r = http.get("/get")
    assert r.status_code == 200


def test_playwright_works(page):
    page.goto("/forms/post")
    assert page.locator("form").count() == 1
