# -*- coding: utf-8 -*-
# vStream https://github.com/Kodi-vStream/venom-xbmc-addons
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.lib.comaddon import dialog
from resources.hosters.hoster import iHoster
from resources.lib.comaddon import xbmcgui
from resources.lib.comaddon import VSlog
UA = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:72.0) Gecko/20100101 Firefox/72.0'


class cHoster(iHoster):

    def __init__(self):
        iHoster.__init__(self, 'vk', 'Vk')

    def _getMediaLinkForGuest(self):
        VSlog(self._url)
        url = []
        qua = []

        oRequest = cRequestHandler(self._url)
        oRequest.addHeaderEntry('Host', 'vk.com')
        oRequest.addHeaderEntry('Referer', self._url)
        oRequest.addHeaderEntry('User-Agent', 'Mozilla/5.0 (iPad; CPU OS 13_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) CriOS/87.0.4280.77 Mobile/15E148 Safari/604.1')
        sHtmlContent = oRequest.request()
        sHtmlContent = sHtmlContent.replace('\\', '')
    # (.+?) # ([^<]+) .+? 
        sPattern = ',"hls_ondemand":"(.+?)",'

        oParser = cParser()
        aResult = oParser.parse(sHtmlContent, sPattern)
        if aResult[0]:
            api_call = aResult[1][0]+ '|User-Agent=' + UA + '&Referer=' + self._url 
            VSlog(api_call)

            if api_call:
                return True, api_call
    # (.+?) # ([^<]+) .+? 
        sPattern = ',"hls":"(.+?)",'

        oParser = cParser()
        aResult = oParser.parse(sHtmlContent, sPattern)
        if aResult[0]:
            api_call = aResult[1][0]+ '|User-Agent=' + UA + '&Referer=' + self._url 
            VSlog(api_call)

            if api_call:
                return True, api_call
    # (.+?) # ([^<]+) .+? 
        sPattern = 'quality="(.+?)" frameRate.+?<BaseURL>(.+?)<\/BaseURL>'

        oParser = cParser()
        aResult = oParser.parse(sHtmlContent, sPattern)
        if aResult[0]:
            url=[]
            qua=[]
            for i in aResult[1]:
                url.append(str(i[1]))
                qua.append(str(i[0]))
            api_call = dialog().VSselectqual(qua, url)

            if api_call:
                return True, api_call

        return False, False
