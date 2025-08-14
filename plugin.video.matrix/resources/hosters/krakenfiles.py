#-*- coding: utf-8 -*-

from resources.lib.handler.requestHandler import cRequestHandler
from resources.hosters.hoster import iHoster
from resources.lib.comaddon import VSlog
from resources.lib.parser import cParser
from six.moves import urllib_parse

class cHoster(iHoster):

    def __init__(self):
        iHoster.__init__(self, 'krakenfiles', 'Krakenfiles')

    def _getMediaLinkForGuest(self, autoPlay = False):
        oRequest = cRequestHandler(self._url)
        oRequest.enableCache(False)
        sHtmlContent = oRequest.request()

        api_call = ''

        oParser = cParser()
        sPattern = 'source src="([^"]+)'
        aResult = oParser.parse(sHtmlContent, sPattern)
        if aResult[0] is True:
            api_call = aResult[1][0]
            if api_call.startswith('//'):
                api_call = 'https:' + api_call

        if api_call:
            return True, urllib_parse.quote(api_call, '/:?=&')

        return False, False