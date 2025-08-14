#-*- coding: utf-8 -*-
#Vstream https://github.com/Kodi-vStream/venom-xbmc-addons

import re

from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.lib.packer import cPacker
from resources.hosters.hoster import iHoster
from resources.lib.comaddon import VSlog

class cHoster(iHoster):

    def __init__(self):
        iHoster.__init__(self, 'letwatch', 'LetWatch')

    def __getUrlFromJavascriptCode(self, sHtmlContent):

        aResult = re.search('(eval\(function.*?)\s*</script>', sHtmlContent, re.DOTALL)

        if (aResult.group(1)):
            sJavascript = aResult.group(1)

            sUnpacked = cPacker().unpack(sJavascript)

            return sUnpacked

        return False

    def _getMediaLinkForGuest(self, autoPlay = False):
        VSlog(self._url)
        api_call = False

        oRequest = cRequestHandler(self._url)
        sHtmlContent = oRequest.request()

        sUnpacked = self.__getUrlFromJavascriptCode(sHtmlContent)

        sPattern = 'sources:\[{file:"(.+?)"'

        oParser = cParser()
        aResult = oParser.parse(sUnpacked, sPattern)
        if aResult[0]:
            api_call = aResult[1][0]
            return True, api_call

        return False, False
