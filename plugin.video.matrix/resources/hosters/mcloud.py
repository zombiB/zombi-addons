#-*- coding: utf-8 -*-
#Vstream https://github.com/Kodi-vStream/venom-xbmc-addons
#############################################################
# Yonn1981 https://github.com/Yonn1981/Repo
#############################################################

import re

from resources.lib.handler.requestHandler import cRequestHandler
from resources.hosters.hoster import iHoster
from resources.lib.comaddon import dialog, VSlog
from resources.lib.parser import cParser
from resources.lib.util import urlEncode, Quote
UA = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:68.0) Gecko/20100101 Firefox/68.0'

class cHoster(iHoster):

    def __init__(self):
        iHoster.__init__(self, 'mcloud', 'mCloud/VizCLoud')

    def setUrl(self, url):
        self._url = str(url).replace('+', '%2B').split('#')[0]
        self._url0 = str(url)
    def _getMediaLinkForGuest(self):
        api_call = self._url
        oRequest = cRequestHandler(SubTitle)
        sHtmlContent = oRequest.request().replace('\\','')
        oParser = cParser()

        sPattern = '"file":"([^"]+)".+?"label":"(.+?)"'
        aResult = oParser.parse(sHtmlContent, sPattern)

        if aResult[0]:
            url = []
            qua = []
            for i in aResult[1]:
                    url.append(str(i[0]))
                    qua.append(str(i[1]))

        oParser = cParser()

        api_call = self._url

        if api_call:
           return True, api_call

        return False, False