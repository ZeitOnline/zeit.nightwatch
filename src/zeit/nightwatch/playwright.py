from urllib.parse import parse_qs, urljoin, urlparse

from playwright.sync_api._generated import Page


def sso_login(self, url, username, password):
    self.goto(url)
    query_params = parse_qs(urlparse(url).query)
    redirect_url_list = query_params.get("url")
    redirect_uri_list = query_params.get("redirect_uri")

    if self.locator("#kc-login").count() == 1:
        self.locator("#username").fill(username)
        self.locator("#password").fill(password)
        self.locator("#kc-login").click()
    else:
        self.locator("#login_email").fill(username)
        self.locator("#login_pass").fill(password)
        self.locator("input.submit-button.log").click()

    if redirect_url_list or redirect_uri_list:
        redirect_list = redirect_url_list or redirect_uri_list
        redirect = redirect_list.pop()
        target = urljoin(redirect, urlparse(redirect).path)
        self.wait_for_url(target + "**")
    else:
        self.wait_for_url("**/konto")


Page.sso_login = sso_login
