#-*- coding: utf-8 -*-

from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.lib.comaddon import dialog
from resources.hosters.hoster import iHoster
from resources.lib.packer import cPacker
from resources.lib.comaddon import VSlog
import re,xbmcgui
UA = 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:68.0) Gecko/20100101 Firefox/68.0'

class cHoster(iHoster):

    def __init__(self):
        iHoster.__init__(self, 'fastplay', 'fastplay')

    def isDownloadable(self):
        return True
			
    def setUrl(self, sUrl):
        self._url = str(sUrl)
        if not "http" in sUrl:
        	self._url = 'https://'+self._url

    def _getMediaLinkForGuest(self):
        VSlog(self._url)
        
        oRequest = cRequestHandler(self._url)
        sHtmlContent = oRequest.request()
        oParser = cParser()
        
            # (.+?) .+?
        sPattern = 'file:"(.+?)",label:"(.+?)"'
        aResult = oParser.parse(sHtmlContent, sPattern)
        
        api_call = False

        if aResult[0] :
            
            #initialisation des tableaux
            url=[]
            qua=[]
            
            #Replissage des tableaux
            for i in aResult[1]:
                url.append(str(i[0]))
                qua.append(str(i[1]))

            api_call = dialog().VSselectqual(qua, url)

            if api_call:
                return True, api_call + '|User-Agent=' + UA + '&Referer=' + self._url

        return False, False
        
