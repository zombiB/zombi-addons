#-*- coding: utf-8 -*-
# https://github.com/Kodi-vStream/venom-xbmc-addons
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.hosters.hoster import iHoster
from resources.lib.comaddon import dialog
from resources.lib.comaddon import VSlog
from resources.lib.util import Quote
import re

class cHoster(iHoster):

    def __init__(self):
        iHoster.__init__(self, 'sharecast', 'ShareCast')

    def _getMediaLinkForGuest(self):
        VSlog(self._url)
        api_call = False
        Referer = ""
        if '|Referer=' in self._url:
            url = self._url.split('|Referer=')[0]
            Referer = self._url.split('|Referer=')[1]
        else:
            url = self._url
            Referer =  "https://sharecast.ws/"

        oRequestHandler = cRequestHandler(url)
        oRequestHandler.addHeaderEntry('Referer', Referer)
        data3 = oRequestHandler.request()

        sPattern = "new Player\(.+?player\",\"([^\"]+)\",{'([^\']+)"
        aResult = re.findall(sPattern, data3)

        if aResult:
            site = 'https://' + aResult[0][1]
            url = (site + '/hls/' + aResult[0][0]  + '/live.m3u8')

            api_call = url

        if api_call:
            return True, api_call  + '|Referer=https://sharecast.ws/'

        return False, False
