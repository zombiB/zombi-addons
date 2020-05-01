from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.lib.gui.gui import cGui
from resources.lib.comaddon import dialog
from resources.hosters.hoster import iHoster
from resources.lib.packer import cPacker
import urllib2,urllib,re,xbmcgui,xbmc
UA = 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:68.0) Gecko/20100101 Firefox/68.0'

class cHoster(iHoster):

    def __init__(self):
        self.__sDisplayName = '[COLOR gold]CimaClub[/COLOR]'
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
        return 'govid'

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
        if 'play'  in sUrl:
            self.__sUrl = self.__sUrl.replace("play","down")
        else:
            self.__sUrl = sUrl

    def checkUrl(self, sUrl):
        return True

    def getUrl(self):
        return self.__sUrl

    def getMediaLink(self):
        return self.__getMediaLinkForGuest()

    def __getMediaLinkForGuest(self):

        oRequest = cRequestHandler(self.__sUrl)
        sHtmlContent = oRequest.request()

            # (.+?) .+? ([^<]+)
        oParser = cParser()
        sPattern = '<small  >(.+?)</small> <a target="_blank"  download=".+?" onclick="updateData.+?"  href="(.+?)" > <small  >.+?</small> '
        aResult = oParser.parse(sHtmlContent, sPattern)

        api_call = False

        if (aResult[0] == True):
            
            #initialisation des tableaux
            url=[]
            qua=[]
            
            #Replissage des tableaux
            for i in aResult[1]:
                url.append(str(i[1])) 
                qua.append(str(i[0]))

            api_call = dialog().VSselectqual(qua, url)

        if (api_call):
            return True, api_call + '|User-Agent=' + UA 

        return False, False