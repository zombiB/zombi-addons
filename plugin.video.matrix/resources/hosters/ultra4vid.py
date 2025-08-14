#-*- coding: utf-8 -*-

from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.hosters.hoster import iHoster
from resources.lib.comaddon import VSlog
from resources.lib.util import urlHostName
from resources.lib import random_ua

UA = random_ua.get_phone_ua()

class cHoster(iHoster):

    def __init__(self):
        iHoster.__init__(self, 'ultra4vid', 'Ultra4Vid')

    def _getMediaLinkForGuest(self, autoPlay = False):
        api_call = False
        VSlog(self._url)

        sRefer = f'https://{urlHostName(self._url)}/'

        oParser = cParser()
        oRequest = cRequestHandler(self._url)
        oRequest.addHeaderEntry('User-Agent', UA)
        oRequest.addHeaderEntry('Referer', sRefer)
        oRequest.enableCache(False)
        sHtmlContent = oRequest.request()


        sPattern = 'data-link="([^"]+)'
        aResult = oParser.parse(sHtmlContent, sPattern)
        if aResult[0]:  
            api_call = aResult[1][0]

        if api_call:
            return True, f'{api_call}|User-Agent={UA}&Referer=https://{sRefer}/'

        return False, False

