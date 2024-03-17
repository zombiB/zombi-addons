#-*- coding: utf-8 -*-

from resources.hosters.hoster import iHoster
from resources.lib.packer import cPacker
from resources.lib.comaddon import VSlog
from resources.lib import helpers
import re
import requests

UA = 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:39.0) Gecko/20100101 Firefox/39.0'

class cHoster(iHoster):

    def __init__(self):
        iHoster.__init__(self, 'lulustream', 'Lulustream')

    def _getMediaLinkForGuest(self, autoPlay = False):
        VSlog(self._url)

        headers = {'User-Agent': UA,
                   'Origin': self._url.rsplit('/', 1)[0],
                   'Referer': self._url
                   }
        s = requests.session()
        sHtmlContent = s.get(self._url, headers=headers).text

        api_call = ''

        aResult = re.search(r'(\s*eval\s*\(\s*function\(p,a,c,k,e(?:.|\s)+?)<\/script>', sHtmlContent)
        if aResult:
            sHtmlContent = cPacker().unpack(aResult.group(1))
        
        aResult = re.search(r'sources:\s*\[{file:\s*["\']([^"\']+)', sHtmlContent)
        if aResult:
            api_call = aResult.group(1)

        if api_call:
            return True, api_call + helpers.append_headers(headers)

        return False, False