from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.lib.gui.gui import cGui
from resources.lib.util import cUtil
from resources.hosters.hoster import iHoster
from resources.lib.packer import cPacker
import xbmcgui, re

class cHoster(iHoster):

    def __init__(self):
        self.__sDisplayName = 'Bitvid'
        self.__sFileName = self.__sDisplayName

    def getDisplayName(self):
        return  self.__sDisplayName

    def setDisplayName(self, sDisplayName):
        self.__sDisplayName = sDisplayName + ' [COLOR skyblue]'+self.__sDisplayName+'[/COLOR]'

    def setFileName(self, sFileName):
        self.__sFileName = sFileName

    def getFileName(self):
        return self.__sFileName

    def getPluginIdentifier(self):
        return 'bitvid'

    def isDownloadable(self):
        return True

    def isJDownloaderable(self):
        return True

    def getPattern(self):
        return ''
        
    def __getIdFromUrl(self):

        return ''
        
    def __modifyUrl(self, sUrl):

        return sUrl

    def setUrl(self, sUrl):       
        self.__sUrl = sUrl

    def checkUrl(self, sUrl):
        return True
		
    def getUrl(self,url):
            return 

    def getMediaLink(self):
        return self.__getMediaLinkForGuest()

    def __getMediaLinkForGuest(self):
        print self.__sUrl
        
        oRequest = cRequestHandler(self.__sUrl)
        sHtmlContent = oRequest.request()
        
        oParser = cParser()
              
        sPattern = '<source src="(.+?)" type='
        aResult = oParser.parse(sHtmlContent, sPattern)
        
        
        api_call = ''
        
        if (aResult[0]):
            api_call = aResult[1][0]
            
        if (api_call):
            #Rajout d'un header ?
            api_call = api_call + '|User-Agent=Mozilla/5.0 (Windows NT 6.1; WOW64; rv:39.0) Gecko/20100101 Firefox/39.0'
            return True, api_call
        else:
            cGui().showInfo(self.__sDisplayName, 'file not found' , 5)
        
        return False, False
