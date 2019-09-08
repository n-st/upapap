#!/usr/bin/env python2
# encoding: utf-8 (as per PEP 263)

try:
    import sys
    import os
    import requests
    import requests_cache
    from bs4 import BeautifulSoup

    requests_cache.install_cache('/tmp/upapap-cache-%s' % sys.version_info[0], backend='sqlite', expire_after=900)

    def parse_lolol(url, soup, html=False):
        """Parse list of lists of links. Requires full page soup as input."""

        response = ''

        pagetitle = soup.find('header', {'class': 'h1'}).find('h1').get_text().strip()
        if html:
            response += '<a href="%s"><h1>%s</h1></a>\n' % (url, pagetitle)
        else:
            response += '# %s\n' % pagetitle
            response += '%s\n' % url
        response += '\n'

        content = soup.find('main')

        last_heading = ""
        close_ul = False
        for l in content.find_all('ul'):
            heading = l.find_previous(['h1', 'h2', 'h3', 'h4', 'h5', 'h6']).get_text().strip()
            elems = l.find_all('li')

            if heading != last_heading:
                if close_ul:
                    response += '</ul>\n'
                    close_ul = False
                if html:
                    response += '<h2>%s</h2>\n' % heading
                    if elems:
                        response += '<ul>\n'
                        close_ul = True
                else:
                    response += '## %s\n' % heading
                last_heading = heading

            for i in elems:
                text = i.get_text().strip()
                a = i.find('a')
                if not a:
                    if html:
                        response += '<li>%s</li>\n' % (text)
                    else:
                        response += '* %s  \n' % (text)
                else:
                    href = i.find('a').attrs['href']
                    if not href.startswith('http://') and not href.startswith('https://'):
                        if not href.startswith('/'):
                            href = '/' + href
                        href = 'https://www.fim.uni-passau.de' + href
                    if html:
                        response += '<li><a href="%s">%s</a></li>\n' % (href, text)
                    else:
                        response += '* %s  \n  %s\n' % (text, href)
            response += '\n'
        if close_ul:
            response += '</ul>\n'

        return response


    urls = [
        'https://www.fim.uni-passau.de/studium/modulkataloge/',
        'https://www.fim.uni-passau.de/index.php?id=17010',
        'https://www.fim.uni-passau.de/ueber-die-fakultaet/ausschuesse/pruefungsausschuss/',
        'https://www.fim.uni-passau.de/studium/pruefungsordnungen/',
    ]

    html = False
    if 'SCRIPT_NAME' in os.environ:
        script_name = os.environ['SCRIPT_NAME']
        html = script_name.endswith('.html')

    response = ''
    for url in urls:
        req = requests.get(url)
        soup = BeautifulSoup(req.content, 'lxml')
        response += parse_lolol(url, soup, html)

    if not response:
        raise Exception('Empty response from upstream server')

    if html:
        response = 'Content-Type: text/html; charset=utf-8\n\n' + response
    else:
        response = 'Content-Type: text/markdown; charset=utf-8\n\n' + response
    print(response.rstrip().encode('utf-8'))

except Exception as e:
    print('Status: 500 Internal Server Error')
    print('Content-Type: text/plain; charset=utf-8')
    print('')
    print('Error: %s' % str(e))