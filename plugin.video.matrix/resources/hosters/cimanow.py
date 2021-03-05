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
        self.__sDisplayName = 'cimanow'
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
        return 'cimanow'

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
		oRequest.addHeaderEntry('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:70.0) Gecko/20100101 Firefox/70.0')
		oRequest.addHeaderEntry('Referer', 'https://cimanow.tv/')
		sHtmlContent = oRequest.request()
		oParser = cParser()
		print "sHtmlContente"
    
    #/uploads/2021/02/19/_Cima-Now.CoM_ I.Care.a.Lot.2021.HD/[Cima-Now.CoM] I.Care.a.Lot.2021.HD-360p.mp4
		sId = ''

		sPattern = '<source src="(.+?)" type="video/mp4" size="(.+?)">'
		aResult = oParser.parse(sHtmlContent, sPattern)
        
		api_call = False

		if (aResult[0] == True):
            
            #initialisation des tableaux
			url=[]
			qua=[]
            
            #Replissage des tableaux
			for i in aResult[1]:
				url.append("https://watch9.cimanow.net"+str(i[0]).replace("[","%5B").replace("]","%5D").replace("+","%20").replace(" ","%20"))
				qua.append(str(i[1])+'p')

			api_call = dialog().VSselectqual(qua, url)

			if (api_call):
				return True, api_call + '|AUTH=TLS&verifypeer=false' + '&User-Agent=' + UA + '&Referer=' + self.__sUrl+'&Host=watch8.cimanow.net'

		return False, False
        

