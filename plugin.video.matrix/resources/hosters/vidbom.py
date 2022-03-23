from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.lib.comaddon import VSlog, xbmcgui, isMatrix
from resources.hosters.hoster import iHoster
from resources.lib.packer import cPacker
import re,xbmcgui

class cHoster(iHoster):

    def __init__(self):
        self.__sDisplayName = 'vidbom'
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
        return 'vidbom'

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
        oRequest.addHeaderEntry('Referer',self.__sUrl)
        sHtmlContent = oRequest.request()
        if isMatrix():
           sHtmlContent = str(sHtmlContent.encode('latin-1'),'utf-8')
        #VSlog(sHtmlContent)
        oParser = cParser()
        
        api_call = False
        
        sPattern =  '(?:[>;]\s*)(ﾟωﾟ.+?\(\'_\'\);)'
        aResult = oParser.parse(sHtmlContent, sPattern)
         
        
        if aResult[0]:
            for i in aResult[1]:
                decoded = AADecoder(i).decode()

                r = re.search('file:"([^<]+)",', decoded, re.DOTALL | re.UNICODE)
                if r:
                    api_call = r.group(1)
                    break
        
        #VSlog(api_call)

        if (api_call):
            return True, api_call

        return False, False