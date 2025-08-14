#-*- coding: utf-8 -*-

from resources.hosters.hoster import iHoster
from resources.lib.packer import cPacker
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.comaddon import VSlog
from resources.lib.parser import cParser
from resources.lib.util import urlHostName
from resources.lib import random_ua

UA = random_ua.get_phone_ua()

class cHoster(iHoster):

    def __init__(self):
        iHoster.__init__(self, 'upstream', 'Upstream')

    def isDownloadable(self):
        return False
			
    def setUrl(self, sUrl):
        self._url = str(sUrl)
        if not 'embed-' in self._url:
            self._url = self._url.replace('d/','embed-') + '.html'

    def _getMediaLinkForGuest(self, autoPlay = False):
        VSlog(self._url)
        api_call = ''
        if '|Referer=' in self._url:
            sReferer = self._url.split('|Referer=')[1]
            self._url = self._url.split('|Referer=')[0]
        else:
            sReferer = f'https://{urlHostName(self._url)}/'
            
        oParser = cParser()
        oRequestHandler = cRequestHandler(self._url)
        oRequestHandler.addHeaderEntry('User-Agent', UA)
        oRequestHandler.addHeaderEntry('Accept-Language', 'en-US,en;q=0.9')
        oRequestHandler.enableCache(False)
        sHtmlContent = oRequestHandler.request()

        sPattern = '(eval\(function\(p,a,c,k,e(?:.|\s)+?)</script>'
        aResult = oParser.parse(sHtmlContent, sPattern)
        if aResult[0]:
            for aEntry in aResult[1]:
                sHtmlContent = cPacker().unpack(aEntry)

        sPattern = r'sources: *\[{file:["\']([^"\']+)'
        aResult = oParser.parse(sHtmlContent, sPattern)
        if aResult[0]:
            api_call = aResult[1][0]

        if api_call:
            if 'http' not in api_call:
                api_call = self._url.rsplit('/', 1)[0] + api_call

            return True, f'{api_call}|User-Agent={UA}&Referer={sReferer}&Accept-Language=en-US,en;q=0.9'

        return False, False
