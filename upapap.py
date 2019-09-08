#!/usr/bin/env python
# encoding: utf-8 (as per PEP 263)

import abc

import requests
from bs4 import BeautifulSoup

__all__ = ["URLS", "Callback", "Markdown", "parse_lolol", "feed_handler"]

URLS = [
    'https://www.fim.uni-passau.de/studium/modulkataloge/',
    'https://www.fim.uni-passau.de/index.php?id=17010',
    'https://www.fim.uni-passau.de/ueber-die-fakultaet/ausschuesse/pruefungsausschuss/',
    'https://www.fim.uni-passau.de/studium/pruefungsordnungen/',
]


class Callback(object):
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def handle_page_title(self, url, pagetitle):
        pass

    @abc.abstractmethod
    def handle_section_title(self, heading):
        pass

    @abc.abstractmethod
    def handle_entry(self, href, text):
        pass

    @abc.abstractmethod
    def handle_end(self):
        pass


class Markdown(Callback):
    def __init__(self):
        self.response = ""
        self.last_heading = ""

    def handle_page_title(self, url, pagetitle):
        if self.response:
            self.response += '\n'
        self.response += '# %s\n' % pagetitle
        self.response += '%s\n' % url

    def handle_section_title(self, heading):
        if self.last_heading != heading:
            self.response += '\n## %s\n' % heading
        self.last_heading = heading

    def handle_entry(self, href, text):
        if href:
            self.response += '* %s  \n  %s\n' % (text, href)
        else:
            self.response += '* %s\n' % (text)

    def handle_end(self):
        pass


def parse_lolol(url, soup, handler):
    """Parse list of lists of links. Requires full page soup as input."""

    pagetitle = soup.find('header', {'class': 'h1'}).find('h1').get_text().strip()
    handler.handle_page_title(url, pagetitle)

    content = soup.find('main')

    for l in content.find_all('ul'):
        heading = l.find_previous(['h1', 'h2', 'h3', 'h4', 'h5', 'h6']).get_text().strip()
        handler.handle_section_title(heading)
        elems = l.find_all('li')
        for i in elems:
            text = i.get_text().strip()
            a = i.find('a')
            if not a:
                handler.handle_entry(None, text)
            else:
                href = a.attrs['href']
                if not href.startswith('http://') and not href.startswith('https://'):
                    if not href.startswith('/'):
                        href = '/' + href
                    href = 'https://www.fim.uni-passau.de' + href
                handler.handle_entry(href, text)

    handler.handle_end()


def feed_handler(handler):
    for url in URLS:
        req = requests.get(url)
        soup = BeautifulSoup(req.content, 'lxml')
        parse_lolol(url, soup, handler)


def main():
        handler = Markdown()
    feed_handler(handler)
    print(handler.response)


if __name__ == '__main__':
    main()
