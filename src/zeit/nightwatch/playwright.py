from playwright.sync_api._generated import Page


def sso_login(self, url, username, password):
    self.goto(url)
    if self.locator("#kc-login").count() == 1:
        self.locator("#username").fill(username)
        self.locator("#password").fill(password)
        self.locator("#kc-login").click()
    else:
        self.locator("#login_email").fill(username)
        self.locator("#login_pass").fill(password)
        self.locator("input.submit-button.log").click()


Page.sso_login = sso_login
