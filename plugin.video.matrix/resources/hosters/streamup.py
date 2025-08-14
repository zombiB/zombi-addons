# coding: utf-8

from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.hosters.hoster import iHoster
from resources.lib.util import urlHostName

TimeOut = 60 
class cHoster(iHoster):

    def __init__(self):
        iHoster.__init__(self, 'streamup', 'StreamUP')

    def _getMediaLinkForGuest(self, autoPlay = False):
        oRequest = cRequestHandler(self._url)
        oRequest.setTimeout(TimeOut)
        oRequest.enableCache(False)
        sHtmlContent = oRequest.request()

        api_call = ''

        oParser = cParser()       
        sPattern = 'streaming_url:\s*["\']([^"\']+)'
        aResult = oParser.parse(sHtmlContent, sPattern)
        if aResult[0]:
            api_call = aResult[1][0]

        if api_call:
            return True, f'{api_call}|AUTH=TLS&verifypeer=false&Origin=https://{urlHostName(self._url)}&Referer=https://{urlHostName(self._url)}/'

        return False, False
