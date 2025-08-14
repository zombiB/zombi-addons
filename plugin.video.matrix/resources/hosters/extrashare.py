from resources.hosters.hoster import iHoster
from resources.lib.packer import cPacker
from resources.lib.comaddon import VSlog
from resources.lib import helpers, random_ua
from resources.lib.util import urlHostName
import re
import requests

UA = random_ua.get_phone_ua()

class cHoster(iHoster):

    def __init__(self):
        iHoster.__init__(self, 'extrashare', 'ExtraShare')
			
    def isDownloadable(self):
        return True

    def _getMediaLinkForGuest(self, autoPlay = False):
        VSlog(self._url)
        api_call = ''
        if '|Referer=' in self._url:
            sReferer = self._url.split('|Referer=')[1]
            self._url = self._url.split('|Referer=')[0]

        headers = {'User-Agent': UA,
                   'Referer': sReferer
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

        headers.update({"Referer": f'https://{urlHostName(self._url)}/'})
        if api_call:
            return True, api_call + helpers.append_headers(headers)

        return False, False
