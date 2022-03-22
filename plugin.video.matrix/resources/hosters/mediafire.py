#-*- coding: utf-8 -*-

from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.lib.comaddon import VSlog, xbmcgui
from resources.hosters.hoster import iHoster
from resources.lib.packer import cPacker
from resources.lib.comaddon import dialog
from resources.lib.comaddon import VSlog
import re,xbmcgui

UA = 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:53.0) Gecko/20100101 Firefox/53.0'

class cHoster(iHoster):

    def __init__(self):
        iHoster.__init__(self, 'mediafire', 'mediafire')

    def _getMediaLinkForGuest(self):
        VSlog(self._url)
    
        oRequest = cRequestHandler(self._url)
        sHtmlContent = oRequest.request()
            #(.+?)([^<]+)
        oParser = cParser()
        sPattern =  'aria-label="Download file".+?href="(.+?)"'
        aResult = oParser.parse(sHtmlContent, sPattern)
        if (aResult[0]):
            api_call = aResult[1][0]
        if api_call:
            return True, api_call + '|User-Agent=' + UA
                     
            
        return False, False