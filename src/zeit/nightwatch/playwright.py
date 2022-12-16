from playwright.sync_api._generated import Page


def sso_login(self, url, username, password):
    self.goto(url)
    self.locator('#login_email').fill(username)
    self.locator('#login_pass').fill(password)
    self.locator('input.submit-button.log').click()


Page.sso_login = sso_login
