# -*- coding: utf-8 -*-
# vStream https://github.com/Kodi-vStream/venom-xbmc-addons
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.lib.comaddon import dialog
from resources.hosters.hoster import iHoster
from resources.lib.comaddon import xbmcgui
from resources.lib.comaddon import VSlog


class cHoster(iHoster):

    def __init__(self):
        iHoster.__init__(self, 'vk', 'Vk')

    def _getMediaLinkForGuest(self):
        VSlog(self._url)
        url = []
        qua = []

        oRequest = cRequestHandler(self._url)
        sHtmlContent = oRequest.request()
    # (.+?) # ([^<]+) .+? 
        sPattern = 'quality="(.+?)" frameRate.+?<BaseURL>(.+?)<\/BaseURL>'

        oParser = cParser()
        aResult = oParser.parse(sHtmlContent, sPattern)
        if aResult[0] is True:
            url=[]
            qua=[]
            for i in aResult[1]:
                url.append(str(i[1]))
                qua.append(str(i[0]))
            api_call = dialog().VSselectqual(qua, url)

            if api_call:
                return True, api_call

        return False, False
