import json

try:
    import urllib.parse as parse
except ImportError:
    import urllib as parse

try:
    import urllib.request as request
except ImportError:
    import urllib2 as request

from cliist.lib.config import Config

API_URL = 'https://api.todoist.com/API'

def api_call(method, **options):
    options['token'] = Config.get('api_token')
    query_string = parse.urlencode(options)
    url = "{apiurl}/{method}?{query}".format(apiurl=API_URL,
                                             method=method,
                                             query=query_string)
    try:
        req = request.urlopen(url)
        content = req.read().decode('utf-8')
        return json.loads(content)

    except Exception as ex:
        print(ex)

