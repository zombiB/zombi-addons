#-*- coding: utf-8 -*-

from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.lib.comaddon import dialog, xbmcgui
from resources.hosters.hoster import iHoster
from resources.lib.comaddon import VSlog
import re
import requests
UA = 'Mozilla/5.0 (Linux; Android 8.0; Pixel 2 Build/OPD3.170816.012) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.93 Mobile Safari/537.36'

class cHoster(iHoster):

    def __init__(self):
        self.__sDisplayName = 'hibridvod'
        self.__sFileName = self.__sDisplayName
        self.__sHD = ''

    def getDisplayName(self):
        return  self.__sDisplayName

    def setDisplayName(self, sDisplayName):
        self.__sDisplayName = sDisplayName + ' [COLOR skyblue]'+self.__sDisplayName+'[/COLOR] [COLOR khaki]'+self.__sHD+'[/COLOR]'

    def setFileName(self, sFileName):
        self.__sFileName = sFileName

    def getFileName(self):
        return self.__sFileName

    def getPluginIdentifier(self):
        return 'hibridvod'

    def setHD(self, sHD):
        self.__sHD = ''

    def getHD(self):
        return self.__sHD

    def isDownloadable(self):
        return True

    def isJDownloaderable(self):
        return True

    def getPattern(self):
        return '';
        
    def __getIdFromUrl(self, sUrl):
        return ''

    def setUrl(self, sUrl):
        self.__sUrl = str(sUrl)

    def checkUrl(self, sUrl):
        return True

    def getUrl(self):
        return self.__sUrl

    def getMediaLink(self):
        return self.__getMediaLinkForGuest()

    def __getMediaLinkForGuest(self):

        api_call = ''
        VSlog(self.__sUrl)

        oRequest = cRequestHandler(self.__sUrl)
        sHtmlContent = oRequest.request()
    
  # ([^<]+) .+?
        headers = {'User-Agent': UA,
                	'Accept': '*/*',
                	'referer': 'https://rotana.net/',
                	'origin': 'https://rotana.net',
                	'x-correlation-id': 'undefined',
                	'x-embed-version': 'VOD Embed v1.0'}
        s = requests.Session()
        r = s.get(self.__sUrl, headers = headers)
        sHtmlContent = r.content.decode('utf8')
        VSlog(sHtmlContent)
        oParser = cParser()

        list_q = []
        list_url = []
        sPattern = ',"embed_url":"(.+?)",'
        aResult = oParser.parse(sHtmlContent, sPattern)
        if (aResult[0] == True):
        	url2 = aResult[1][0]
        	r = s.get(url2, headers = headers)
        	sHtmlContent2 = r.content.decode('utf8')
        	VSlog(sHtmlContent2)
        	sPattern = ',RESOLUTION=(.+?),LANGUAGE="eng"(.+?)#EXT'
        	aResult = oParser.parse(sHtmlContent2, sPattern)
        	for aEntry in aResult[1]:
        	    list_q.append(aEntry[0]) 
        	    list_url.append(url2.replace("playlist.m3u8",aEntry[1])) 

        	if list_url:
        	   api_call = dialog().VSselectqual(list_q,list_url)
        if (api_call):
        	return True, api_call 

        return False, False
        
