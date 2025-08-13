#-*- coding: utf-8 -*-

from resources.hosters.hoster import iHoster
from resources.lib.comaddon import VSlog
from resources.lib import helpers
from resources.lib.parser import cParser
from resources.lib.handler.requestHandler import cRequestHandler
from six.moves import urllib_parse

UA = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36 Edg/135.0.0.0'

class cHoster(iHoster):

    def __init__(self):
        iHoster.__init__(self, 'filepv', 'FilePV')

    def _getMediaLinkForGuest(self, autoPlay = False):
        VSlog(self._url)
        api_call = ''

        oParser = cParser() 
        headers = {
            'referer': self._url,
            'User-Agent': UA
                }

        oRequest = cRequestHandler(self._url)
        for key, value in headers.items():
            oRequest.addHeaderEntry(key, value)
        oRequest.enableCache(False)
        sHtmlContent = oRequest.request()

        data = helpers.get_hidden(sHtmlContent)
        data.update({"method_free": "Free Download"})
        data.update({"referer": ""})

        oRequestHandler = cRequestHandler(self._url)
        for key, value in headers.items():
            oRequestHandler.addHeaderEntry(key, value)
        for key, value in data.items():
            oRequestHandler.addParameters(key, value)
        oRequestHandler.setRequestType(1)
        sHtmlContent = oRequestHandler.request()

        data = helpers.get_hidden(sHtmlContent)
        oRequestHandler = cRequestHandler(self._url)
        for key, value in headers.items():
            oRequestHandler.addHeaderEntry(key, value)
        for key, value in data.items():
            oRequestHandler.addParameters(key, value)
        oRequestHandler.setRequestType(1)
        sHtmlContent = oRequestHandler.request()

        sPattern = r'<a class="stretched-link" href="([^"]+)"'
        aResult = oParser.parse(sHtmlContent, sPattern)
        if aResult[0]:
            api_call = urllib_parse.quote(aResult[1][0], '/:?=&') + helpers.append_headers(headers)

        if api_call:
            return True, api_call

        return False, False

