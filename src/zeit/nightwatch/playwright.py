from urllib.parse import parse_qs, urljoin, urlparse

from playwright.sync_api._generated import Page


def sso_login(self, url, username, password):
    self.goto(url)
    redirect_url_list = parse_qs(urlparse(url).query).get("url")

    if self.locator("#kc-login").count() == 1:
        self.locator("#username").fill(username)
        self.locator("#password").fill(password)
        self.locator("#kc-login").click()
    else:
        self.locator("#login_email").fill(username)
        self.locator("#login_pass").fill(password)
        self.locator("input.submit-button.log").click()

    if redirect_url_list:
        redirect = redirect_url_list.pop()
        target = urljoin(redirect, urlparse(redirect).path)
        self.wait_for_url(target + "**")
    else:
        self.wait_for_url("**/konto")


Page.sso_login = sso_login
