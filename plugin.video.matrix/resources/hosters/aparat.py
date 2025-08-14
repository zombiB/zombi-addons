# -*- coding: utf-8 -*-
# https://github.com/Kodi-vStream/venom-xbmc-addons

from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.hosters.hoster import iHoster
from resources.lib.comaddon import dialog, VSlog
from resources.lib import random_ua

UA = random_ua.get_ua()

class cHoster(iHoster):

    def __init__(self):
        iHoster.__init__(self, 'aparat', 'Aparat')

    def _getMediaLinkForGuest(self, autoPlay = False):
        VSlog(self._url)
        VideoType = 2  # mp4
        VideoType = 1  # m3u8

        list_q = []
        list_url = []

        if VideoType == 1:
            oRequestHandler = cRequestHandler(self._url)
            oRequestHandler.enableCache(False)
            sHtmlContent = oRequestHandler.request()

            oParser = cParser()
            sPattern = '"src":"([^"]+)'
            aResult = oParser.parse(sHtmlContent, sPattern)
            if aResult[0]:
                url2 = aResult[1][0]
                oRequestHandler = cRequestHandler(url2)
                sHtmlContent2 = oRequestHandler.request()

                sPattern = 'RESOLUTION=(\d+x\d{0,4})\s*(https?://[^\s]+)'
                aResult = oParser.parse(sHtmlContent2, sPattern)
                for aEntry in aResult[1]:
                    list_q.append(aEntry[0])
                    list_url.append(aEntry[1])  

            if list_url:
                api_call = dialog().VSselectqual(list_q, list_url)
                if api_call:
                    return True, api_call + '|User-Agent=' + UA + '&Referer=' + self._url

        if VideoType == 2:
            oRequestHandler = cRequestHandler(self._url)
            oRequestHandler.enableCache(False)
            sHtmlContent = oRequestHandler.request()

            oParser = cParser()
            sPattern = 'file_code=(\w+)&hash=([^&]+)'
            aResult = oParser.parse(sHtmlContent, sPattern)

            if aResult[0]:
                resultId = aResult[1][0][0]
                resultHash = aResult[1][0][1]
                url = 'https://wolfstream.tv/dl?op=download_orig&id=' + resultId + \
                    '&mode=0&hash=' + resultHash
                data = 'op=download_orig&id=' + resultId + '&mode=n&hash=' + resultHash
                oRequestHandler = cRequestHandler(url)
                oRequestHandler.setRequestType(1)
                oRequestHandler.addHeaderEntry('Referer', url)
                oRequestHandler.addParametersLine(data)
                sHtmlContent = oRequestHandler.request()

                sPattern = 'href="([^"]+.mp4)'
                aResult = oParser.parse(sHtmlContent, sPattern)
                if aResult[0]:
                    api_call = aResult[1][0]
                    if api_call:
                        return True, api_call

        return False, False
