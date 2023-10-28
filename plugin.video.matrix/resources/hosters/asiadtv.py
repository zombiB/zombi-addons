#-*- coding: utf-8 -*- 
import re

from resources.lib.handler.requestHandler import cRequestHandler
from resources.hosters.hoster import iHoster
from resources.lib.parser import cParser
from resources.lib.packer import cPacker
from resources.lib.comaddon import dialog, VSlog
UA = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36'

class cHoster(iHoster):

    def __init__(self):
        iHoster.__init__(self, 'asiadtv', 'AsiaDramaTV', 'gold')

    def isDownloadable(self):
        return False

    def setUrl(self, url):
        self._url = str(url)

    def _getMediaLinkForGuest(self):
        VSlog(self._url)
        sReferer = ""
        url = self._url.split('|Referer=')[0]
        sReferer = self._url.split('|Referer=')[1]
        
        oRequest = cRequestHandler(url)
        oRequest.addHeaderEntry('user-agent',UA)
        oRequest.addHeaderEntry('Referer',sReferer)
        oRequest.addHeaderEntry('x-requested-with','XMLHttpRequest')
        oRequest.addHeaderEntry('accept','*/*')
        
        sHtmlContent = oRequest.request()
        #VSlog(sHtmlContent)
        
        oParser = cParser()
        
        sPattern = '(eval\(function\(p,a,c,k,e(?:.|\s)+?\))<\/script>'
        aResult = oParser.parse(sHtmlContent, sPattern)
        if aResult[0]:
            sHtmlContent = cPacker().unpack(aResult[1][0])
        

        oParser = cParser()

        sStart = 'manifest.mpd'
        sEnd = 'image'
        sHtmlContent0 = oParser.abParse(sHtmlContent, sStart, sEnd)

        sPattern = 'file:"(.+?)",label:"([^"]+)'
        aResult = oParser.parse(sHtmlContent0, sPattern)
        VSlog(aResult)
        url=[]
        qua=[]
        if aResult[0]:
            for aEntry in aResult[1]:

                url.append(aEntry[0])

                qua.append(aEntry[1])

                api_call = dialog().VSselectqual(qua, url)
                
            if api_call:
                sReferer  = 'https://asiatvplayer.com/'

                return True, api_call  + '|AUTH=TLS&verifypeer=false' + '&Referer=' + sReferer 
        sPattern = '<source src="(.+?)" type='
        aResult = oParser.parse(sHtmlContent, sPattern)
        
        if aResult[0]:
            for aEntry in aResult[1]:
                url.append(aEntry[0])
                qua.append('Auto')


            api_call = dialog().VSselectqual(qua, url)
                
            if api_call:
                sReferer  = 'https://asiatvplayer.com/'
                VSlog(api_call)

                return True, api_call  + '|AUTH=TLS&verifypeer=false' + '&Referer=' + sReferer 
        return False, False