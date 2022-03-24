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
        iHoster.__init__(self, 'moshahda', 'moshahda')

    def setUrl(self, sUrl):
        self._url = str(sUrl)
        if not "embed" in self._url:
               self._url = self._url.replace("https://moshahda.net/","https://moshahda.net/embed-")

    def _getMediaLinkForGuest(self):
        VSlog(self._url)
        sReferer = ""
        url = self._url.split('|Referer=')[0]
        sReferer = self._url.split('|Referer=')[1]
        
        oRequest = cRequestHandler(url)
        oRequest.addHeaderEntry('user-agent',UA)
        oRequest.addHeaderEntry('Referer',sReferer)
        sHtmlContent = oRequest.request()
        VSlog(self._url)
        
        oParser = cParser()
        
        sPattern = '(eval\(function\(p,a,c,k,e(?:.|\s)+?\))<\/script>'
        aResult = oParser.parse(sHtmlContent, sPattern)
        if aResult[0] is True:
            sHtmlContent = cPacker().unpack(aResult[1][0])
        
            # (.+?) .+?
        sPattern = 'file: "(.+?)"}'
        aResult = oParser.parse(sHtmlContent, sPattern)
        
        api_call = False

        if aResult[0] is True:
            oRequest = cRequestHandler(aResult[1][0])
            data = oRequest.request()
            VSlog(data)
        	
            sPattern =  ',RESOLUTION=(.+?),.+?https(.+?&i=([0-9]+).([0-9]+))'
            aResult = oParser.parse(data, sPattern)
            if aResult[0] is True:
               url=[]
               qua=[]
               for i in aResult[1]:
                  url.append('https'+str(i[1]))
                  qua.append(str(i[0]).split('x')[1]+"p")
               api_call = dialog().VSselectqual(qua, url)
 
            if api_call:
                return True, api_call + '|User-Agent=' + UA + '&Referer=' + sReferer
            
        return False, False
   