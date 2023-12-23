#-*- coding: utf-8 -*-

from resources.hosters.hoster import iHoster
from resources.lib.comaddon import VSlog
import re
import requests
import base64

UA = 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:39.0) Gecko/20100101 Firefox/39.0'

class cHoster(iHoster):

    def __init__(self):
        iHoster.__init__(self, 'vidsrcstream', 'VidsrcStrem')

    def _getMediaLinkForGuest(self, autoPlay = False):
        VSlog(self._url)
        referer = self._url
        if '?Referer=' in self._url:
            referer = self._url.split('?Referer=')[1]
            self._url = self._url.split('?Referer=')[0]

        headers = {'User-Agent': UA,
                   'Referer': referer
                   }
        s = requests.session()

        req = s.get(self._url, headers=headers)

        hls_url = re.search(r'file:"([^"]*)"', req.text).group(1)
        hls_url = re.sub(r'\/\/\S+?=', '', hls_url).replace('#2', '')

        try:
            hls_url = base64.b64decode(hls_url).decode('utf-8') 
        except Exception: 
            return self._getMediaLinkForGuest(self._url + f'?Referer={referer}')

        set_pass = re.search(r'var pass_path = "(.*?)";', req.text).group(1)
        if set_pass.startswith("//"):
            set_pass = f"https:{set_pass}"           

        if hls_url:
            return True, hls_url + '|User-Agent=' + UA + '&Referer=' + referer

        return False, False