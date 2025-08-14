# -*- coding: utf-8 -*-

from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.hosters.hoster import iHoster
from resources.lib.comaddon import dialog, VSlog
from resources.lib.packer import cPacker
from resources.lib import random_ua

UA = random_ua.get_phone_ua()

class cHoster(iHoster):

    def __init__(self):
        iHoster.__init__(self, 'clipwatching', 'ClipWatching')

    def isDownloadable(self):
        return False

    def _getMediaLinkForGuest(self, autoPlay = False, api_call=None):
        VSlog(self._url)
        sReferer = f'https://{self._url.split("/")[2]}'
        oParser = cParser()
        oRequest = cRequestHandler(self._url)
        oRequest.enableCache(False)
        sHtmlContent = oRequest.request()

        sHtmlContent1 = oParser.abParse(sHtmlContent, 'var holaplayer', 'vvplay')
        sHtmlContent1 = sHtmlContent1.replace(',', '').replace('master.m3u8', 'index-v1-a1.m3u8')
        sPattern = '"(http[^"]+(?:.m3u8|.mp4))"'
        aResult = oParser.parse(sHtmlContent1, sPattern)

        if aResult[0]:
            url = []
            qua = []
            n = 1

            for i in aResult[1]:
                url.append(str(i))
                qua.append('Lien ' + str(n))
                n += 1

            api_call = dialog().VSselectqual(qua, url)

        sPattern = '(eval\(function\(p,a,c,k,e(?:.|\s)+?\))<\/script>'
        aResult = oParser.parse(sHtmlContent, sPattern)
        if aResult[0]:
            data = aResult[1][0]
            sHtmlContent = cPacker().unpack(data)

        sPattern = 'file:"(.+?)"'
        aResult = oParser.parse(sHtmlContent, sPattern)
        if aResult[0]:
            api_call = aResult[1][0] 

        if api_call:
            return True, api_call  + '|User-Agent=' + UA + '&Referer=' + sReferer

        return False, False
