#-*- coding: utf-8 -*-

from resources.hosters.hoster import iHoster
from resources.lib.comaddon import VSlog, dialog
from resources.lib.hunter import hunter
import re
import requests


UA = 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:39.0) Gecko/20100101 Firefox/39.0'

class cHoster(iHoster):

    def __init__(self):
        iHoster.__init__(self, 'multiembed', 'MultiEmbed')

    def _getMediaLinkForGuest(self, autoPlay = False):
        VSlog(self._url)
        referer = self._url.split('?Referer=')[1]
        self._url = self._url.split('?Referer=')[0]

        headers = {'User-Agent': UA,
                   'Referer': referer
                   }
        s = requests.session()

        req = s.get(self._url, headers=headers)
        matches = re.search(r'escape\(r\)\)}\((.*?)\)', req.text)
        processed_values = []
        
        if not matches:
            dialog().VSerror(f'Open: {self._url} directly and solve the captcha before re-trying. ')
            return

        for val in matches.group(1).split(','):
            val = val.strip()
            if val.isdigit() or (val[0] == '-' and val[1:].isdigit()):
                processed_values.append(int(val))
            elif val[0] == '"' and val[-1] == '"':
                processed_values.append(val[1:-1])

        unpacked = hunter(*processed_values)
        hls_url = re.search(r'file:"([^"]*)"', unpacked).group(1)       

        if hls_url:
            return True, hls_url + '|User-Agent=' + UA + '&Referer=' + referer

        return False, False