from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.lib.comaddon import VSlog, xbmcgui
from resources.hosters.hoster import iHoster
from resources.lib.comaddon import VSlog
import re,xbmc
UA = 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:68.0) Gecko/20100101 Firefox/68.0'


class cHoster(iHoster):

    def __init__(self):
        self.__sDisplayName = 'letsupload'
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
        return 'letsupload'

    def isDownloadable(self):
        return True

    def isJDownloaderable(self):
        return True

    def getPattern(self):
        return ''
        
    def __getIdFromUrl(self, sUrl):
        return ''

    def setUrl(self, sUrl):
        self.__sUrl = str(sUrl)
        if 'embed' in sUrl:
            self.__sUrl = self.__sUrl.replace("embed-","")
        if 'mediaplayer' not in sUrl:
            self.__sUrl = self.__sUrl.replace("https://letsupload.io/","https://letsupload.co/plugins/mediaplayer/site/_embed.php?u=")

    def checkUrl(self, sUrl):
        return True

    def getUrl(self):
        return self.__sUrl

    def getMediaLink(self):
        
        return self.__getMediaLinkForGuest()

    def __getMediaLinkForGuest(self):
        VSlog(self.__sUrl)
 
        api_call = ''
        
        oParser = cParser()
        oRequest = cRequestHandler(self.__sUrl)
        sHtmlContent = oRequest.request()

        sPattern = 'file: "([^<]+)",type: "mp4"'
        aResult = oParser.parse(sHtmlContent, sPattern)
        if (aResult[0] == True):
            api_call = aResult[1][0]

        sPattern = 'value="(.+?)"/>'
        aResult = oParser.parse(sHtmlContent, sPattern)
        if (aResult[0] == True):
            api_call = aResult[1][0]


        if (api_call):
            return True, api_call +'|User-Agent=' + UA  + '&Referer=' + self.__sUrl
        

        return False, False 