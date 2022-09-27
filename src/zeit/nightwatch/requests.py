from mechanicalsoup.stateful_browser import _BrowserState
import bs4
import cssselect
import logging
import lxml.html
import mechanicalsoup
import re
import requests


log = logging.getLogger(__name__)


# requests offers no easy way to customize the response class (response_hook
# and copy everything over to a new instance, anyone?), but since we only want
# two simple helper methods, monkey patching them should be quite alright.
def css(self, selector):
    xpath = cssselect.HTMLTranslator().css_to_xpath(selector)
    return self.xpath(xpath)


def xpath(self, selector):
    if not hasattr(self, 'parsed'):
        self.parsed = lxml.html.document_fromstring(self.text)
    return self.parsed.xpath(selector)


requests.models.Response.css = css
requests.models.Response.xpath = xpath


class Browser(mechanicalsoup.StatefulBrowser):
    """Wraps a requests.Session to add some helpful features.

    - instantiate with a base url, and then only use paths:
      `http = Browser('https://example.com'); http.get('/foo')`
      will request https://example.com/foo
    - can use call instead of get, because it's just that little bit shorter
      (`http('/foo')` instead of `http.get('/foo')`)
    - fill and submit forms, powered by mechanicalsoup
      (note that we override the "state" mechanics so beautifulsoup parsing
       is only performed when it's actually needed)
    """

    def __init__(self, baseurl=None, sso_url=None, *args, **kw):
        self.baseurl = baseurl
        self.sso_url = sso_url
        kw.setdefault('session', HeaderPrintingSession())
        super().__init__(*args, **kw)

    @property
    def headers(self):
        return self.session.headers

    def get(self, *args, **kw):
        return self.request('get', *args, **kw)

    def __call__(self, *args, **kw):
        return self.get(*args, **kw)

    def open(self, url, *args, **kw):
        return self.request('get', url, *args, **kw)

    def head(self, *args, **kw):
        kw.setdefault('allow_redirects', False)
        return self.request('head', *args, **kw)

    def patch(self, *args, **kw):
        return self.request('patch', *args, **kw)

    def put(self, *args, **kw):
        return self.request('put', *args, **kw)

    def post(self, *args, **kw):
        return self.request('post', *args, **kw)

    def delete(self, *args, **kw):
        return self.request('delete', *args, **kw)

    def request(self, method, url, *args, **kw):
        if url.startswith('/') and self.baseurl:
            url = self.baseurl + url
        r = self.session.request(method, url, *args, **kw)
        # Taken from StatefulBrowser.open()
        self._StatefulBrowser__state = LazySoupBrowserState(
            r, self.soup_config, url=r.url, request=r.request)
        return r

    def submit(self, form=None, url=None, submit=None, **kw):
        # This combines StatefulBrowser.submit_selected() and Browser.submit()
        # and bases it all on self.request()
        if form is None:
            form = self.form
            url = self._StatefulBrowser__state.url
            self.form.choose_submit(submit)
        if isinstance(form, mechanicalsoup.Form):
            form = form.form
        return self.request(**self.get_request_kwargs(form, url, **kw))

    submit_selected = NotImplemented  # Use our customized submit() instead

    def links(self, url_regex=None, link_text=None, exact_text=False,
              *args, **kw):
        """Enhanced to support contains instead of equals for link_text."""
        links = self.page.find_all('a', href=True, *args, **kw)
        if url_regex is not None:
            return [a for a in links if re.search(url_regex, a['href'])]
        if link_text is not None:
            if exact_text:
                return [a for a in links if a.text == link_text]
            else:
                return [a for a in links if link_text in a.text]
        return []

    def sso_login(self, username, password, url=None):
        """Performs login on meine.zeit.de. Opens either the configured sso_url,
        or the given one (useful if e.g. it contains a return `?url` parameter)
        and fills in and submits the form.
        """
        if url is None:
            url = self.sso_url
        if url is None:
            raise ValueError('No url given and no sso_url configured')
        self.get(url)
        self.select_form()
        self.form['email'] = username
        self.form['pass'] = password
        return self.submit(headers={"referer": url})


class LazySoupBrowserState(_BrowserState):
    """Only parse with beautifulsoup if a client wants to use features that
    need it (form filling, link selection)."""

    def __init__(self, response, soup_config, **kw):
        self.soup_config = soup_config
        self.response = response
        self._page = None
        super().__init__(**kw)

    @property
    def page(self):
        if self._page is None:
            # Taken from mechanicalsoup.Browser.add_soup()
            self._page = bs4.BeautifulSoup(
                self.response.content, **self.soup_config)
        return self._page

    @page.setter
    def page(self, value):
        pass


class HeaderPrintingSession(requests.Session):
    """Prints request+response headers, to help understanding test failures."""

    def request(self, method, url, *args, **kw):
        log.info('> %s %s', method.upper(), url)
        response = super().request(method, url, *args, **kw)
        request = response.request
        lines = ['< %s %s' % (request.method, request.url)]
        lines.extend(['> %s: %s' % x for x in request.headers.items()])
        lines.append('---')
        resp = {'Status': response.status_code}
        resp.update(response.headers)
        lines.extend(['< %s: %s' % x for x in resp.items()])
        log.info('\n'.join(lines))
        return response
