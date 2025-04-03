import os

import pytest


@pytest.fixture(scope="session")
def nightwatch_config():
    return {
        "browser": {
            "baseurl": "https://httpbin.org",
            "sso_url": "https://meine.zeit.de/anmelden",
            "user_agent": "Mozilla/ZONFrontendMonitoring",
        },
        "normal_username": os.environ.get("NORMAL_USERNAME"),
        "normal_password": os.environ.get("NORMAL_PASSWORD"),
    }


@pytest.fixture(scope="session")
def browser_context_args(playwright, nightwatch_config):
    return {
        "base_url": nightwatch_config["browser"]["baseurl"],
        "user_agent": nightwatch_config["browser"]["user_agent"],
    }
