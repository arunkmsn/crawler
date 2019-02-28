import requests
from concurrent.futures import ThreadPoolExecutor, as_completed
from urllib.parse import urlparse, urljoin, parse_qsl, unquote_plus
from queue import Queue
from bs4 import BeautifulSoup as bs
from collections import defaultdict

class Url(object):
    '''A url object that can be compared with other url orbjects
    without regard to the vagaries of encoding, escaping, and ordering
    of parameters in query strings.'''

    def __init__(self, url):
        parts = urlparse(url)
        _query = frozenset(parse_qsl(parts.query))
        _path = unquote_plus(parts.path)
        if _path == '/':
            _path = ''
        parts = parts._replace(query=_query, path=_path)
        self.parts = parts

    def __eq__(self, other):
        return self.parts == other.parts

    def __hash__(self):
        return hash(self.parts)

    def __repr__(self):
        return str(self.parts)


def extract_urls(q):
    images = defaultdict(list)
    child_links = []
    for x in q:
        url, response = x
        domain = urlparse(url).netloc
        sp = bs(response.content, 'html.parser')

        # extract child links
        for x in sp.find_all('a'):
            link = x.get('href')
            # get full path
            if not urlparse(link).netloc:
                    link = urljoin(url, link)

            if link and (link not in child_links):
                if urlparse(link).netloc == domain:
                    child_links.append(link)

        # extract image urls
        for x in sp.find_all('img'):
            link = x.get('src')
            # get full path
            if not urlparse(link).netloc:
                    link = urljoin(url, link)

            if link and (link not in images[url]):
                images[url].append(link)

    return images, child_links

def fetch_pages(q, urls):
    # We can use a with statement to ensure threads are cleaned up promptly
    with ThreadPoolExecutor(max_workers=8) as executor:
        # Start the load operations and mark each future with its URL
        future_to_url = {executor.submit(requests.get, url): url for url in urls}
        for future in as_completed(future_to_url):
            url = future_to_url[future]
            try:
                data = future.result()
            except Exception as exc:
                print('%r generated an exception: %s' % (url, exc))
            else:
                print('%r page is %d bytes' % (url, len(data.content)))
                q.append((url, data,))

if __name__ == '__main__':
    # Test cases
    q = []
    urls = [
        'http://www.foxnews.com/',
        'http://www.cnn.com/',
        'http://europe.wsj.com/',
        'https://www.bbc.co.uk/',
        'http://sdlfasdf.com/'
        ]
    fetch_pages(q, urls)
    images, children = extract_urls(q)
    print(children)
