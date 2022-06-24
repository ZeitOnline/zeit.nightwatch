from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
import selenium.webdriver


class Convenience:

    default_options = [
        'disable-gpu',
    ]

    def __init__(
            self, baseurl, timeout=30, sso_url=None, headless=True,
            window='1200x800', user_agent='Mozilla/ZONFrontendMonitoring',
            *args, **kw):
        self.baseurl = baseurl
        self.sso_url = sso_url
        self.timeout = timeout
        opts = Options()
        for x in self.default_options:
            opts.add_argument(x)
        if headless:
            opts.add_argument('headless')
        opts.add_argument('user-agent=[%s]' % user_agent)
        opts.add_argument('window-size=%s' % window)

        kw['options'] = opts
        super().__init__(*args, **kw)

    def get(self, url):
        if url.startswith('/'):
            url = self.baseurl + url
        super().get(url)

    def wait(self, condition, timeout=None):
        if timeout is None:
            timeout = self.timeout
        try:
            return WebDriverWait(self, timeout).until(condition)
        except TimeoutException as e:
            raise AssertionError() from e

    def sso_login(self, username, password, url=None):
        if url is None:
            url = self.sso_url
        if url is None:
            raise ValueError('No url given and no sso_url configured')
        self.get(url)
        self.find_element(By.ID, 'login_email').send_keys(username)
        self.find_element(By.ID, 'login_pass').send_keys(password)
        self.find_element(By.CSS_SELECTOR, 'input.submit-button.log').click()


class WebDriverChrome(Convenience, selenium.webdriver.Chrome):
    pass


try:
    import seleniumwire.webdriver

    class ProxiedWebDriverChrome(Convenience, seleniumwire.webdriver.Chrome):
        pass
except ImportError:  # soft dependency
    class ProxiedWebDriverChrome:
        def __init__(self, *args, **kw):
            raise RuntimeError(
                'Could not import `seleniumwire`, maybe run '
                '`pip install selenium-wire`?')
