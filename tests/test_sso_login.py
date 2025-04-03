import os

import pytest


@pytest.fixture(scope="session")
def nightwatch_config():
    return {
        "browser": {
            "new_sso_url": "https://login.zeit.de/realms/zeit-online-public/protocol/openid-connect/auth?client_id=member&response_type=code&scope=openid&nonce=6JoG2RI4t3q7fAz8&state=n4Ny98ojp2KYWn81",
            "sso_url": "https://meine.zeit.de/anmelden",
            "user_agent": "Mozilla/ZONFrontendMonitoring",
        },
        "normal_username": os.environ.get("NORMAL_USERNAME"),
        "normal_password": os.environ.get("NORMAL_PASSWORD"),
    }


@pytest.fixture(scope="session")
def browser_context_args(playwright, nightwatch_config):
    return {
        "user_agent": nightwatch_config["browser"]["user_agent"],
    }


def test_playwright_sso_login_konto(nightwatch_config, page):
    page.sso_login(
        nightwatch_config["browser"]["sso_url"],
        nightwatch_config["normal_username"],
        nightwatch_config["normal_password"],
    )
    assert page.locator("#main").get_by_text("Mein Konto")


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


def test_playwright_new_sso_login_redirect_article(nightwatch_config, page):
    article = (
        "https://www.zeit.de/2020/54/hackerangriff-us-regierung-russland-solarwinds-cyberkrieg"
    )
    page.sso_login(
        f"{nightwatch_config['browser']['new_sso_url']}&redirect_uri={article}",
        nightwatch_config["normal_username"],
        nightwatch_config["normal_password"],
    )
    assert page.locator("h1").get_by_text("Offenes Geheimnis")
