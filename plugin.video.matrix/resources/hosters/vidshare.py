#-*- coding: utf-8 -*-

from resources.lib.handler.requestHandler import cRequestHandler
from resources.hosters.hoster import iHoster
from resources.lib.parser import cParser
from resources.lib.packer import cPacker
from resources.lib.comaddon import VSlog
from resources.lib import random_ua

UA = random_ua.get_pc_ua()

class cHoster(iHoster):

    def __init__(self):
        iHoster.__init__(self, 'vidshare', 'Vidshare')

    def _getMediaLinkForGuest(self, autoPlay = False):
        VSlog(self._url)

        oParser = cParser()
        sReferer = self._url 

        oRequest = cRequestHandler(self._url)
        oRequest.addHeaderEntry('user-agent', UA)
        oRequest.addHeaderEntry('Referer', sReferer)
        oRequest.addHeaderEntry('x-requested-with', 'XMLHttpRequest')
        oRequest.addHeaderEntry('accept', '*/*')
        oRequest.enableCache(False)
        sHtmlContent = oRequest.request()
       
        sPattern = '(eval\(function\(p,a,c,k,e(?:.|\s)+?\))<\/script>'
        aResult = oParser.parse(sHtmlContent,sPattern)
        if (aResult[0] == True):
            sHtmlContent = cPacker().unpack(aResult[1][0])
            sPattern = 'file:"(.+?)",label:".+?"}'
            aResult = oParser.parse(sHtmlContent,sPattern)
            if (aResult[0] == True):
                api_call = aResult[1][0] 

        sPattern = 'file:"(.+?)"}'
        aResult = oParser.parse(sHtmlContent, sPattern)
        if (aResult[0] == True):
            api_call = aResult[1][0] +'|User-Agent=' + UA + '&Referer=' + sReferer
                
        if (api_call):
            return True, api_call
					
        return False, False