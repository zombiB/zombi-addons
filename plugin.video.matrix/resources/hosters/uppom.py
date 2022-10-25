#-*- coding: utf-8 -*-
#Vstream https://github.com/Kodi-vStream/venom-xbmc-addons
#https://sama-share.com/embed-shsaa6s49l55-750x455.html
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.hosters.hoster import iHoster
from resources.lib.packer import cPacker
from resources.lib.comaddon import VSlog
from resources.lib.util import cUtil, Quote
import re
import requests
UA = 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Mobile Safari/537.36'

class cHoster(iHoster):

    def __init__(self):
        iHoster.__init__(self, 'uppom', 'uppom')

    def setUrl(self, sUrl):
        self._url = str(sUrl)
        if 'embed' in sUrl:
            self._url = self._url.replace("embed-","")
				
    def _getMediaLinkForGuest(self):
        sUrl = self._url
        VSlog(sUrl)
        d = re.findall('https://(.*?)/(.*?)',sUrl)
        for aEntry1 in d:
            sHost= aEntry1[0]
            VSlog(sHost)

        oRequest = cRequestHandler(self._url)
        sHtmlContent = oRequest.request()
        cook = oRequest.GetCookies()
        VSlog(cook)
        oParser = cParser()
    
        sId = ''

        sPattern = 'name="id" value="(.+?)">'
        aResult = oParser.parse(sHtmlContent, sPattern)
    
        if (aResult[0]):
        	sId = aResult[1][0]
        	VSlog(sId)
        pdata = 'op=download2&id='+sId+'&rand= '+'&referer='+Quote(sUrl)
        UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:65.0) Gecko/20100101 Firefox/65.0"
        oRequest = cRequestHandler(sUrl)
        oRequest.setRequestType(1)
        oRequest.addHeaderEntry('user-Agent', UA)
        oRequest.addHeaderEntry('cookie', cook)
        oRequest.addHeaderEntry('referer', Quote(sUrl))
        oRequest.addHeaderEntry('origin', 'https://'+sHost)
        oRequest.addParametersLine(pdata)
        sHtmlContent = oRequest.request() 

    
  # ([^<]+) .+?
        VSlog(sHtmlContent)
        sPattern = '<span id="direct_link" style=.+?<a href="(.+?)</a>'
        aResult = oParser.parse(sHtmlContent, sPattern)
        if aResult[0] is True:
        	api_call = aResult[1][0] + '|User-Agent=' + UA +'&verifypeer=false'+ '&Referer=https://m.seeeed.xyz' 

        if api_call:
            return True, api_call

        return False, False