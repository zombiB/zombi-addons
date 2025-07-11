#-*- coding: utf-8 -*-
#Vstream https://github.com/Kodi-vStream/venom-xbmc-addons
#http://uqload.com/embed-xxx.html
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.hosters.hoster import iHoster
from resources.lib.comaddon import VSlog
from resources.lib.packer import cPacker
import xbmcgui
UA = 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:68.0) Gecko/20100101 Firefox/68.0'

class cHoster(iHoster):

    def __init__(self):
        iHoster.__init__(self, 'vidoba', 'vidoba')

    def _getMediaLinkForGuest(self):
        VSlog(self._url)
        api_call = ''
        oParser = cParser()
      #  xbmcgui.Dialog().ok("","hi")

        oRequest = cRequestHandler(self._url)
        sHtmlContent = oRequest.request()
        sPattern ='(eval\(function\(p,a,c,k,e(?:.|\s)+?\))<\/script>'
      #  aResult = re.findall(sPattern, sHtmlContent, re.DOTALL)
        aResult = oParser.parse(sHtmlContent, sPattern)
        if aResult:
            data = aResult[1][0]
            sHtmlContent = cPacker().unpack(data)
    # (.+?) .+? ([^<]+)

        sPattern = 'file:"(.+?)"'

        aResult = oParser.parse(sHtmlContent, sPattern)
        api_call = False

        if (aResult[0] == True):
      #      xbmcgui.Dialog().ok("aResult",  aResult[1][0])
            api_call = aResult[1][0]
            VSlog(api_call)

            if (api_call):
                return True, api_call + '|User-Agent=' + UA
        return False, False
