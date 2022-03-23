#-*- coding: utf-8 -*-

from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.lib.comaddon import dialog
from resources.hosters.hoster import iHoster
from resources.lib.comaddon import VSlog
import re,xbmcgui

class cHoster(iHoster):

    def __init__(self):
        self.__sDisplayName = 'fajer'
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
        return 'fajer'

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
        VSlog(self.__sUrl)
        
        oRequest = cRequestHandler(self.__sUrl)
        sHtmlContent = oRequest.request()
        

        
        oParser = cParser()
        
            # (.+?) .+?
        sPattern = '#EXT-X-STREAM-INF:BANDWIDTH=(.+?),RESOLUTION=.+?/drive//hls/(.+?).m3u8'
        aResult = oParser.parse(sHtmlContent, sPattern)

        
        api_call = False

        if (aResult[0] == True):
            
            #initialisation des tableaux
        	url=[]
        	qua=[]

            #Replissage des tableaux
        	for i in aResult[1]:
        	    url.append("https://fajer.video/drive/hls/"+str(i[1])+".m3u8")
        	    qua.append(str(i[0]).replace("1500000","720p").replace("3000000","1080p").replace("500000","360p").replace("750000","480p"))

        	api_call = dialog().VSselectqual(qua, url)
 
        	if (api_call):
        	    return True, api_call
            
        return False, False
        
