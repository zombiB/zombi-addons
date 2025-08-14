#-*- coding: utf-8 -*-

from resources.hosters.hoster import iHoster
from resources.lib.comaddon import VSlog
import re
import requests

UA = 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:39.0) Gecko/20100101 Firefox/39.0'

class cHoster(iHoster):

    def __init__(self):
        iHoster.__init__(self, 'qiwi', 'Qiwi')

    def _getMediaLinkForGuest(self, autoPlay = False):
        VSlog(self._url)

        headers = {'User-Agent': UA,
                   'Origin': self._url.rsplit('/', 1)[0],
                   'Referer': self._url
                   }
        s = requests.session()

        api_call = ''

        file_id = self._url.split("/")[-1]
        try:
            sHtmlContent = s.get(self._url, headers=headers).text
        except Exception as e:
            VSlog('Error: ' + str(e))
        aResult = re.search(r'class="page_TextHeading__VsM7r">(.+?)</h1>', sHtmlContent)
        if aResult:
            ext = aResult.group(1).split('.')[-1]

            api_call = f"https://spyderrock.com/{file_id}.{ext}"

        if api_call:
            return True, api_call + '|User-Agent=' + UA + '&Referer=' + self._url

        return False, False
