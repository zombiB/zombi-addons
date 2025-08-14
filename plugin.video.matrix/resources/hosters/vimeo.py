#-*- coding: utf-8 -*-

import re, json
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.hosters.hoster import iHoster
from resources.lib.comaddon import dialog, VSlog
from resources.lib.util import urlHostName
from resources.lib import random_ua

UA = random_ua.get_pc_ua()

class cHoster(iHoster):

    def __init__(self):
        iHoster.__init__(self, 'vimeo', 'Vimeo')

    def _getMediaLinkForGuest(self, autoPlay = False):
        VSlog(self._url)
        api_call = False
        sReferer = self._url
        if '|Referer=' in self._url:
            sReferer = self._url.split('|Referer=')[1]
            self._url = self._url.split('|Referer=')[0]

        oParser = cParser()
        oRequest = cRequestHandler(self._url)
        oRequest.addHeaderEntry('Host', urlHostName(self._url))
        oRequest.addHeaderEntry('Referer', sReferer)
        oRequest.addHeaderEntry('User-Agent', UA)
        oRequest.enableCache(False)
        sHtmlContent = oRequest.request()

        pattern = re.compile('window.playerConfig\\s*=\\s*({.+?})\\s*</script>', re.DOTALL)
        match = pattern.search(sHtmlContent)
        if match:
            try:
                sHtmlContent = json.loads(match.group(1))
            except:
                VSlog('failed to parse json')

        sPattern = '"config":"(.+?)",'
        aResult = oParser.parse(sHtmlContent, sPattern)
        if (aResult[0]):
            web_url = aResult[1][0]

            oRequest = cRequestHandler(web_url)
            oRequest.addHeaderEntry('Referer', f'https://{urlHostName(self._url)}/')
            oRequest.addHeaderEntry('User-Agent', UA)
            sHtmlContent = oRequest.request(jsonDecode=True)

        for cdn in sHtmlContent['request']['files']['hls']['cdns'].values():
            url=[]
            qua=[]
            url.append(str(cdn["url"]))
            qua.append(str(cdn["origin"]))

        api_call = dialog().VSselectqual(qua, url)

        if api_call:
            return True, api_call

        return False, False
