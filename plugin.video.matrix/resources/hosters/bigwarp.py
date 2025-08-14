#-*- coding: utf-8 -*-

from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.util import urlHostName
from resources.lib.parser import cParser
from resources.hosters.hoster import iHoster
from resources.lib.packer import cPacker
from resources.lib.comaddon import VSlog
from resources.lib import random_ua

UA = random_ua.get_pc_ua()

class cHoster(iHoster):

    def __init__(self):
        iHoster.__init__(self, 'bigwarp', 'BigWarp')
			
    def isDownloadable(self):
        return True

    def _getMediaLinkForGuest(self, autoPlay = False):
        VSlog(self._url)
        api_call = ''
        sReferer = f'https://{urlHostName(self._url)}/'

        oParser = cParser()
        oRequestHandler = cRequestHandler(self._url)
        oRequestHandler.addHeaderEntry('User-Agent', UA)
        oRequestHandler.addHeaderEntry('Referer', sReferer)
        oRequestHandler.enableCache(False)
        sHtmlContent = oRequestHandler.request()

        sPattern = '(eval\(function\(p,a,c,k,e(?:.|\s)+?)</script>'
        aResult = oParser.parse(sHtmlContent, sPattern)
        if aResult[0]:
            for aEntry in aResult[1]:
                sHtmlContent = cPacker().unpack(aEntry)

        sPattern = r'sources: *\[{file:["\']([^"\']+)["\']'
        aResult = oParser.parse(sHtmlContent, sPattern)
        if aResult[0]:
            api_call = aResult[1][0]

        if api_call:
            if 'http' not in api_call:
                api_call = self._url.rsplit('/', 1)[0] + api_call

            return True, api_call + '|Referer=' + sReferer
        
        return False, False