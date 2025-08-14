#-*- coding: utf-8 -*-
# https://github.com/Kodi-vStream/venom-xbmc-addons

from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.hosters.hoster import iHoster
from resources.lib.comaddon import VSlog
from resources.lib import random_ua

UA = random_ua.get_pc_ua()

class cHoster(iHoster):

    def __init__(self):
        iHoster.__init__(self, 'vidbom', 'Vidbom')

    def _getMediaLinkForGuest(self, autoPlay = False):
        VSlog(self._url)
        api_call = ''
        oParser = cParser()
        sReferer = self._url 

        oRequest = cRequestHandler(self._url)
        oRequest.addHeaderEntry('user-agent', UA)
        oRequest.addHeaderEntry('Referer', sReferer)
        oRequest.addHeaderEntry('x-requested-with', 'XMLHttpRequest')
        oRequest.addHeaderEntry('accept', '*/*')
        oRequest.enableCache(False)
        sHtmlContent = oRequest.request()

        sPattern = 'sources: *\[{file:"([^"]+)"'
        aResult = oParser.parse(sHtmlContent, sPattern)
        if aResult[0]:
            api_call = aResult[1][0]

        if api_call:
            return True, api_call+ '|User-Agent=' + UA + '&Referer='+sReferer

        return False, False
