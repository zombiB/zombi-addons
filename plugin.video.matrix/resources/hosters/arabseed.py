#-*- coding: utf-8 -*-

from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.lib.comaddon import dialog, xbmcgui
from resources.hosters.hoster import iHoster
import re
import requests
UA = 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Mobile Safari/537.36'

class cHoster(iHoster):

    def __init__(self):
        self.__sDisplayName = 'arabseed'
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
        return 'arabseed'

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

		oRequest = cRequestHandler(self.__sUrl)
		sHtmlContent = oRequest.request()
		oParser = cParser()
		sUrl = self.__sUrl
    
    #Recuperation infos
		sId = ''

		sPattern = 'name="id" value="(.+?)">'
		aResult = oParser.parse(sHtmlContent, sPattern)
    
		if (aResult[0]):
			sId = aResult[1][0]

    
  # ([^<]+) .+?
		headers = {'Host': 'm.arabseed.me',
					'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36',
					'Accept': '*/*',
					'Accept-Language': 'fr,fr-FR;q=0.8,en-US;q=0.5,en;q=0.3',
					'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
					'X-Requested-With': 'XMLHttpRequest',
					'Referer': sUrl,
					'origin': 'https://m.arabseed.me',
					'Connection': 'keep-alive'}
		data = {'op':'download2','id':sId,'rand':'','referer':'','method_free':'','method_premium':''}
		s = requests.Session()
		r = s.post(sUrl, headers = headers,data = data)
		sHtmlContent += r.content
		sPattern = '<span id="direct_link" style.+?<a href="([^<]+)">'
		aResult = oParser.parse(sHtmlContent, sPattern)
		if (aResult[0] == True):
			api_call = aResult[1][0]

		if (api_call):
			return True, api_call + '|User-Agent=' + UA +'&verifypeer=false'

		return False, False
        
