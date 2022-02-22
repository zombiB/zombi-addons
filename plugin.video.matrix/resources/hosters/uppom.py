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
        self.__sDisplayName = 'uppom'
        self.__sFileName = self.__sDisplayName
        self.__sHD = ''

    def getDisplayName(self):
        return  self.__sDisplayName

    def setDisplayName(self, sDisplayName):
        self.__sDisplayName = sDisplayName + ' [COLOR skyblue]' + self.__sDisplayName + '[/COLOR]'

    def setFileName(self, sFileName):
        self.__sFileName = sFileName

    def getFileName(self):
        return self.__sFileName

    def getPluginIdentifier(self):
        return 'uppom'

    def setHD(self, sHD):
        self.__sHD = ''

    def getHD(self):
        return self.__sHD

    def isDownloadable(self):
        return True
        
    def getPattern(self):
        return ''

    def setUrl(self, sUrl):
        self.__sUrl = str(sUrl)
        if 'embed' in sUrl:
            self.__sUrl = self.__sUrl.replace("embed-","")

    def checkUrl(self, sUrl):
        return True

    def __getUrl(self, media_id):
        return

    def getMediaLink(self):
        return self.__getMediaLinkForGuest()

    def __getMediaLinkForGuest(self):
        sUrl = self.__sUrl
        VSlog(sUrl)
        d = re.findall('https://(.*?)/(.*?)',sUrl)
        for aEntry1 in d:
            sHost= aEntry1[0]
            VSlog(sHost)

        oRequest = cRequestHandler(self.__sUrl)
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

    
  # ([^<]+) .+?
        headers = {'Host': sHost,
                	'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36',
                	'Accept': '*/*',
                	'Accept-Language': 'fr,fr-FR;q=0.8,en-US;q=0.5,en;q=0.3',
                	'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
                	'X-Requested-With': 'XMLHttpRequest',
                	'cookie': cook,
                	'Referer': Quote(sUrl),
                	'origin': 'https://'+sHost+'/',
                	'Connection': 'keep-alive'}
        data = {'op':'download2','id':sId,'rand':'','referer':Quote(sUrl)}
        s = requests.Session()
        r = s.post(sUrl, headers = headers,data = data)
        sHtmlContent = r.content.decode('utf8',errors='ignore')
        sPattern = '<span id="direct_link" style=.+?<a href="(.+?)</a>'
        aResult = oParser.parse(sHtmlContent, sPattern)
        if (aResult[0] == True):
        	api_call = aResult[1][0] + '|User-Agent=' + UA +'&verifypeer=false'+ '&Referer=https://m.seeeed.xyz' 

        if (api_call):
            return True, api_call

        return False, False