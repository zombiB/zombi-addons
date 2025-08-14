#-*- coding: utf-8 -*-

from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.hosters.hoster import iHoster
from resources.lib.util import urlHostName
from resources.lib.packer import cPacker
from resources.lib.comaddon import dialog, VSlog
from resources.lib import random_ua

UA = random_ua.get_phone_ua()

class cHoster(iHoster):

    def __init__(self):
        iHoster.__init__(self, 'vidspeeds', 'Vidspeeds')

    def _getMediaLinkForGuest(self, autoPlay = False):
        VSlog(self._url)
        sReferer = f'https://{urlHostName(self._url)}/'
        
        oRequest = cRequestHandler(self._url)
        oRequest.addHeaderEntry('User-Agent', UA)
        oRequest.addHeaderEntry('Accept-Language', 'en-US,en;q=0.9')
        oRequest.enableCache(False)
        sHtmlContent = oRequest.request()
        
        oParser = cParser()
        sPattern = '(eval\(function\(p,a,c,k,e(?:.|\s)+?\))<\/script>'
        aResult = oParser.parse(sHtmlContent, sPattern)
        if aResult[0]:
            data = aResult[1][0]
            sHtmlContent = cPacker().unpack(data)

        sPattern = 'file:"(.+?)"'
        aResult = oParser.parse(sHtmlContent, sPattern)
        
        api_call = False

        if (aResult[0] == True):
            api_call = aResult[1][0]

            if (api_call):
                return True, f'{api_call}|User-Agent={UA}&Referer={sReferer}&verifypeer=false&Accept-Language=en-US,en;q=0.9'
            
        return False, False
        
