# -*- coding: utf-8 -*-
# vStream https://github.com/Kodi-vStream/venom-xbmc-addons

import re
from resources.hosters.hoster import iHoster
from resources.lib.parser import cParser
from resources.lib.comaddon import  VSlog
from resources.lib.handler.requestHandler import cRequestHandler

UA = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0'

class cHoster(iHoster):

    def __init__(self):
        iHoster.__init__(self, 'megaup', 'Megaup')

    def _getMediaLinkForGuest(self, autoPlay = False):
        VSlog(self._url)
        oRequestHandler = cRequestHandler(self._url)
        oRequestHandler.addHeaderEntry('User-Agent', UA)
        sHtmlContent = oRequestHandler.request()
        cookies = oRequestHandler.GetCookies() + ";"

        oParser = cParser()
        sPattern = 'btn-default"\s*href="([^"]+)'
        aResult = oParser.parse(sHtmlContent, sPattern)
        if aResult[0] :
            data = aResult[1][0]
        
            oRequestHandler = cRequestHandler(data)
            oRequestHandler.addHeaderEntry('User-Agent', UA)
            sHtmlContent = oRequestHandler.request()
             
            la = re.search("replace','(.*?)'",sHtmlContent).group(1)

            oRequestHandler = cRequestHandler(la)
            oRequestHandler.disableRedirect()
            oRequestHandler.addHeaderEntry('User-Agent', UA)
            oRequestHandler.addHeaderEntry("Referer", "https://download.megaup.net/")
            oRequestHandler.addHeaderEntry("Cookie", cookies)
            sHtmlContent = oRequestHandler.request()
            api_call = oRequestHandler.getResponseHeader()['Location']

        if api_call:
            return True, api_call + "|User-Agent=" + UA

        return False, False