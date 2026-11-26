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


def test_logs_no_credentials(http, caplog):
    # httpbin echoes cookies, headers and basic-auth paths in some responses,
    # which are logged as well, so this only uses endpoints that do not.
    http.get("https://user:url-secret@httpbin.org/status/200")
    http.get("/cookies/set?session=cookie-secret", allow_redirects=False)
    http.get("/status/200")
    assert "url-secret" not in caplog.text
    # httpbin only sets cookies from the query string, which we don't redact.
    headers = [x for x in caplog.text.splitlines() if "/cookies/set?" not in x]
    assert "cookie-secret" not in "\n".join(headers)
    assert "> GET https://user:<redacted>@httpbin.org/status/200" in caplog.text
    assert "< GET https://user:<redacted>@httpbin.org/status/200" in caplog.text
    assert "> Authorization: <redacted>" in caplog.text
    assert "< set-cookie: session=<redacted>; " in caplog.text
    assert "> Cookie: session=<redacted>" in caplog.text
