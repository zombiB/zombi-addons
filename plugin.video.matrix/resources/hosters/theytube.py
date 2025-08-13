#-*- coding: utf-8 -*-

from resources.hosters.hoster import iHoster
from resources.lib.comaddon import VSlog
from resources.lib import helpers
from resources.lib.util import urlHostName
from resources.lib.packer import cPacker
from six.moves import urllib_parse
import re
import requests

UA = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36 Edg/128.0.0.0'

class cHoster(iHoster):

    def __init__(self):
        iHoster.__init__(self, 'theytube', 'TheyTube')

    def _getMediaLinkForGuest(self, autoPlay = False):
        VSlog(self._url)
        api_call = ''
        Requests = requests.Session()

        headers = {
            'referer': self._url,
            'User-Agent': UA
                }

        sHtmlContent = Requests.get(self._url, headers=headers).text
        data = helpers.get_hidden(sHtmlContent)
        data.update({"file_code": self._url.split('/')[-1]})

        sHtmlContent = Requests.post(f'https://{urlHostName(self._url)}/dl', data, headers=headers)
        sHtmlContent = sHtmlContent.content.decode('utf8',errors='ignore')

        aResult = re.search(r'(\s*eval\s*\(\s*function\(p,a,c,k,e(?:.|\s)+?)<\/script>', sHtmlContent)
        if aResult:
            sHtmlContent = cPacker().unpack(aResult.group(1))

        aResult = re.search(r'''sources:\s*\[{file:\s*["'](?P<url>[^"']+)''', sHtmlContent, re.DOTALL)
        if aResult:
            api_call = urllib_parse.quote(aResult.group(1), '/:?=&') + helpers.append_headers(headers)

        if api_call:
            return True, api_call

        return False, False