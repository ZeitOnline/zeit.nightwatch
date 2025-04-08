import os

import pytest


@pytest.mark.skipif(
    os.environ.get("NORMAL_USERNAME") is None, reason="Just for local testing with vault token"
)
def test_playwright_sso_login_konto(nightwatch_config, page):
    page.sso_login(
        nightwatch_config["browser"]["sso_url"],
        nightwatch_config["normal_username"],
        nightwatch_config["normal_password"],
    )
    assert page.locator("#main").get_by_text("Mein Konto")


@pytest.mark.skipif(
    os.environ.get("NORMAL_USERNAME") is None, reason="Just for local testing with vault token"
)
def test_playwright_sso_login_redirect_article(nightwatch_config, page):
    article = (
        "https://www.zeit.de/2020/54/hackerangriff-us-regierung-russland-solarwinds-cyberkrieg"
    )
    page.sso_login(
        f"{nightwatch_config['browser']['sso_url']}?url={article}",
        nightwatch_config["normal_username"],
        nightwatch_config["normal_password"],
    )
    assert page.locator("h1").get_by_text("Offenes Geheimnis")
