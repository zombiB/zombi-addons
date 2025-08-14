# -*- coding: utf-8 -*-
# vStream https://github.com/Kodi-vStream/venom-xbmc-addons

from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.hosters.hoster import iHoster
from resources.lib.comaddon import dialog
from resources.lib.comaddon import VSlog

class cHoster(iHoster):

    def __init__(self):
        iHoster.__init__(self, 'videobin', 'VideoBIN')

    def _getMediaLinkForGuest(self, autoPlay = False):
        VSlog(self._url)
        oParser = cParser()
        oRequest = cRequestHandler(self._url)
        oRequest.enableCache(False)
        sHtmlContent = oRequest.request()

        sHtmlContent = oParser.abParse(sHtmlContent, 'var player', 'vvplay')
        sHtmlContent = sHtmlContent.replace(',', '').replace('master.m3u8', 'index-v1-a1.m3u8')
        sPattern = '"(http[^"]+(?:.m3u8|.mp4))"'
        aResult = oParser.parse(sHtmlContent, sPattern)

        if aResult[0]:
            api_call = ''
            url=[]
            qua=[]
            n = 1

            for i in aResult[1]:
                url.append(str(i))
                qua.append('Lien ' + str(n))
                n += 1
            api_call = dialog().VSselectqual(qua, url)

        if api_call:
            return True, api_call

        return False, False
