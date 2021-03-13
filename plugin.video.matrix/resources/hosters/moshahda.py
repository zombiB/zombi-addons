#-*- coding: utf-8 -*-

from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.lib.comaddon import dialog
from resources.hosters.hoster import iHoster
from resources.lib.packer import cPacker
import re,xbmcgui

class cHoster(iHoster):

    def __init__(self):
        self.__sDisplayName = 'moshahda'
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
        return 'moshahda'

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
        if not "embed" in sUrl:
			self.__sUrl = sUrl.replace("moshahda.online/","moshahda.online/embed-")

    def checkUrl(self, sUrl):
        return True

    def getUrl(self):
        return self.__sUrl

    def getMediaLink(self):
        return self.__getMediaLinkForGuest()

    def __getMediaLinkForGuest(self):
		print self.__sUrl
		UA = 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36'
        
		oRequest = cRequestHandler(self.__sUrl)
		sHtmlContent = oRequest.request()
        
		oParser = cParser()
		
		sPattern = "<script type='text/javascript'>(.+?)</script>"
		aResult = oParser.parse(sHtmlContent, sPattern)
		sHtmlContent2 = cPacker().unpack(aResult[1][0])

        
            # (.+?) .+?
		sPattern = 'file:"(.+?)",label:"(.+?)"'
		aResult = oParser.parse(sHtmlContent2, sPattern)
        
		api_call = False

		if (aResult[0] == True):
            
            #initialisation des tableaux
			url=[]
			qua=[]
            
            #Replissage des tableaux
			for i in aResult[1]:
				url.append(str(i[0]).replace("moshahda.online","moshahda.online/hls").replace("v.mp4","index-v1-a1.m3u8"))
				qua.append(str(i[1]))

			api_call = dialog().VSselectqual(qua, url)
 
			if (api_call):
				return True, api_call + '|User-Agent=' + UA + '&Referer=' + self.__sUrl
            
		return False, False
        
