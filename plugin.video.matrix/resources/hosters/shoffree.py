#-*- coding: utf-8 -*- 

from resources.lib.handler.requestHandler import cRequestHandler
from resources.hosters.hoster import iHoster
from resources.lib.parser import cParser
from resources.lib.packer import cPacker
from resources.lib.comaddon import dialog, VSlog
from resources.lib import random_ua

UA = random_ua.get_pc_ua()

class cHoster(iHoster):

    def __init__(self):
        iHoster.__init__(self, 'shoffree', 'Shoffree/EgyBest', 'gold')

    def isDownloadable(self):
        return False

    def setUrl(self, url):
        self._url = str(url)

    def _getMediaLinkForGuest(self, autoPlay = False):
        VSlog(self._url)
        sReferer = ""
        url = self._url
        if '|Referer=' in self._url:
            url = self._url.split('|Referer=')[0]
            sReferer = self._url.split('|Referer=')[1]
        sHost = self._url.rsplit("/")[2]
        
        oRequest = cRequestHandler(url)
        oRequest.addHeaderEntry('user-agent',UA)
        oRequest.addHeaderEntry('Referer',sReferer.encode('utf-8'))
        oRequest.addHeaderEntry('Host',sHost.encode('utf-8'))
        oRequest.enableCache(False)
        sHtmlContent = oRequest.request()

        oParser = cParser()
        api_call = False        
        sPattern = '(eval\(function\(p,a,c,k,e(?:.|\s)+?\))<\/script>'
        aResult = oParser.parse(sHtmlContent, sPattern)
        if aResult[0]:
            sHtmlContent = cPacker().unpack(aResult[1][0])
            sPattern = 'file:"(.+?)"'
            aResult = oParser.parse(sHtmlContent, sPattern) 
            if aResult[0]:
                api_call = aResult[1][0]
 
                if api_call:
                    return True, api_call + '|User-Agent=' + UA + '&Referer=' + sReferer
        url=[]
        qua=[]
        sPattern = 'file:\s*"([^"]+)",\s*label:\s*"([^"]+)'
        aResult = oParser.parse(sHtmlContent,sPattern)
        if aResult[0] is True:
            for aEntry in aResult[1]:

                url.append(aEntry[0])
                qua.append(aEntry[1]) 
            if url:
                api_call = dialog().VSselectqual(qua,url)

        if api_call:
            return True, api_call.replace(' ','%20') + '|User-Agent=' + UA + '&Referer=https://' + sHost + '/'

        sPattern = '<source src="(.+?)" type='
        aResult = oParser.parse(sHtmlContent, sPattern)
        
        api_call = False

        if aResult[0]:
            api_call = aResult[1][0]
 
            if api_call:
                return True, api_call + '|User-Agent=' + UA + '&Referer=' + sReferer


        sPattern = 'sources:.+?file:.+?"(.+?)",'
        aResult = oParser.parse(sHtmlContent, sPattern)
        
        api_call = False

        if aResult[0]:
            
            api_call = aResult[1][0]
 
            if api_call:
                return True, api_call  + '|User-Agent=' + UA + '&Referer=' + sReferer

        return False, False
