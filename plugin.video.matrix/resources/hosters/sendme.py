#-*- coding: utf-8 -*-

from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.hosters.hoster import iHoster
from resources.lib.comaddon import VSlog
from resources.lib.util import urlHostName
from resources.lib import random_ua

UA = random_ua.get_pc_ua()

class cHoster(iHoster):

    def __init__(self):
        iHoster.__init__(self, 'sendme', 'Send.Me')

    def isDownloadable(self):
        return True

    def _getMediaLinkForGuest(self, autoPlay = False):
        VSlog(self._url)
        api_call = False
        if '|Referer=' in self._url:
            sReferer = self._url.split('|Referer=')[1]
            self._url = self._url.split('|Referer=')[0]
        else:
            sReferer = f'https://{urlHostName(self._url)}/'

        oParser = cParser()
        oRequest = cRequestHandler(self._url)
        oRequest.addHeaderEntry('Accept-Language', 'en-US,en;q=0.9')
        oRequest.addHeaderEntry('User-Agent', UA)
        oRequest.addHeaderEntry('Host', urlHostName(self._url))
        oRequest.enableCache(False)
        sHtmlContent = oRequest.request()

        sPattern = '<source src="([^"]+)'
        aResult = oParser.parse(sHtmlContent, sPattern)
        if aResult[0]:
            api_call = aResult[1][0]

        sPattern = 'video_source = "([^"]+)'
        aResult = oParser.parse(sHtmlContent, sPattern)
        if aResult[0]:
            api_call = aResult[1][0]

        if api_call:
            return True, f'{api_call}|User-Agent={UA}&Referer={sReferer}'

        return False, False
        
