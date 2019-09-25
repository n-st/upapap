#!/usr/bin/env python
# encoding: utf-8 (as per PEP 263)

try:
    import sys
    import os
    import requests
    import requests_cache
    from upapap import *

    requests_cache.install_cache('/tmp/upapap-cache-%s' % sys.version_info[0], backend='sqlite', expire_after=900)

    html = False
    if 'SCRIPT_NAME' in os.environ:
        script_name = os.environ['SCRIPT_NAME']
        html = script_name.endswith('.html')

    if html:
        handler = HTML()
    else:
        handler = Markdown()
    feed_handler(handler)
    response = handler.response

    if not response:
        raise Exception('Empty response from upstream server')

    if html:
        response = 'Content-Type: text/html; charset=utf-8\n\n' + response
    else:
        response = 'Content-Type: text/markdown; charset=utf-8\n\n' + response
    response = response.rstrip()
    if not isinstance(response, str):
        response = response.encode('utf-8')
    print(response)

except Exception as e:
    print('Status: 500 Internal Server Error')
    print('Content-Type: text/plain; charset=utf-8')
    print('')
    print('Error: %s' % str(e))
