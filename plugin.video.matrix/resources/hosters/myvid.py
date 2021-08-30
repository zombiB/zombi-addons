from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.lib.comaddon import dialog, xbmcgui
from resources.hosters.hoster import iHoster
from resources.lib.packer import cPacker
from resources.lib.comaddon import VSlog
import re

class cHoster(iHoster):

    def __init__(self):
        self.__sDisplayName = 'myvid'
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
        return 'myvid'

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
        
        api_call = ''
        #type1
        oParser = cParser()
        sPattern = 'file: "(.+?)",'
        aResult = oParser.parse(sHtmlContent, sPattern)
        if (aResult[0] == True):
            api_call = aResult[1][0]
            
        #type2?   
        sPattern =  "<script type='text/javascript'>(.+?)</script>"
        aResult = oParser.parse(sHtmlContent, sPattern)
        if (aResult[0] == True):
            stri = cPacker().unpack(aResult[1][0])
            sPattern =  'file:"(.+?)",label:"(.+?)"'
            aResult = oParser.parse(stri, sPattern)
            if (aResult[0] == True):
                url=[]
                qua=[]
                
                for aEntry in aResult[1]:
                    url.append(aEntry[0])
                    qua.append(aEntry[1][:3] + '*' + aEntry[1][3:])

            api_call = dialog().VSselectqual(qua, url)

            if (api_call):
                return True, api_call

        return False, False