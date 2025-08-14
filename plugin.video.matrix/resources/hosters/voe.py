# coding: utf-8

from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.hosters.hoster import iHoster
from resources.lib.comaddon import VSlog
from resources.lib import random_ua
from resources.lib import helpers
from resources.lib.util import urlHostName
import re
from six.moves import urllib_parse
import base64

UA = random_ua.get_random_ua()

class cHoster(iHoster):

    def __init__(self):
        iHoster.__init__(self, 'voe', 'Voe')

    def _getMediaLinkForGuest(self, autoPlay = False):
        VSlog(self._url)
        
        oParser = cParser()
        oRequest = cRequestHandler(self._url)
        oRequest.enableCache(False)
        sHtmlContent = oRequest.request()

        if 'const currentUrl' in sHtmlContent:
            sPattern = "window\.location\.href\s*=\s*'([^']+)"
            aResult = oParser.parse(sHtmlContent, sPattern)
            if aResult[0]:
                self._url = aResult[1][0]
                oRequest = cRequestHandler(self._url)
                sHtmlContent = oRequest.request()

        r = re.search(r'json">\["([^"]+)"]</script>\s*<script\s*src="([^"]+)', sHtmlContent)
        if r:
            oRequest = cRequestHandler(urllib_parse.urljoin(f'https://{urlHostName(self._url)}/', r.group(2)))
            html2 = oRequest.request()
            repl = re.search(r"(\[(?:'\W{2}'[,\]]){1,9})", html2)
            if repl:
                s = self.voe_decode(r.group(1), repl.group(1))
                sources = [(s.get(x).split("?")[0].split(".")[-1], s.get(x)) for x in ['file', 'source', 'direct_access_url'] if x in s.keys()]
                if len(sources) > 1:
                    sources.sort(key=lambda x: int(re.sub(r"\D", "", x[0])))
                stream_url = helpers.pick_source(sources)
            return True, stream_url + '|Referer=' + self._url + '&Origin=' + self._url.rsplit('/', 2)[0]


        oParser = cParser()
        sPattern = '["\']hls["\']:\s*["\']([^"\']+)["\']'
        aResult = oParser.parse(sHtmlContent, sPattern)
        aResult1 = base64.b64decode(aResult[1][0])
        if aResult[0]:
            api_call = aResult1.decode("utf-8")

        if api_call:
            return True, api_call

        return False, False

    @staticmethod
    def voe_decode(ct, luts):
        import json
        lut = [''.join([('\\' + x) if x in '.*+?^${}()|[]\\' else x for x in i]) for i in luts[2:-2].split("','")]
        txt = ''
        for i in ct:
            x = ord(i)
            if 64 < x < 91:
                x = (x - 52) % 26 + 65
            elif 96 < x < 123:
                x = (x - 84) % 26 + 97
            txt += chr(x)
        for i in lut:
            txt = re.sub(i, '_', txt)
        txt = "".join(txt.split("_"))
        ct = helpers.b64decode(txt)
        txt = ''.join([chr(ord(i) - 3) for i in ct])
        txt = helpers.b64decode(txt[::-1])
        return json.loads(txt)