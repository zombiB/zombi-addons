from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.lib.comaddon import dialog
from resources.hosters.hoster import iHoster
from resources.lib.packer import cPacker
import urllib, urllib2, re
UA = 'Android'

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
        self.__sUrl = str(sUrl)
        if '/down/'  in sUrl:
            self.__sUrl = self.__sUrl.replace("/down/","/play/")

    def checkUrl(self, sUrl):
        return True

    def getUrl(self):
        return self.__sUrl

    def getMediaLink(self):
        return self.__getMediaLinkForGuest()

    def __getMediaLinkForGuest(self):

	
        oRequestHandler = cRequestHandler(self.__sUrl)
        oRequestHandler.addHeaderEntry('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:45.0) Gecko/20100101 Firefox/45.0')
        oRequestHandler.addHeaderEntry('Host', 'govid.co')
        oRequestHandler.addHeaderEntry('Referer', 'https://www.cimaclub.me/watch/%D9%85%D8%B4%D8%A7%D9%87%D8%AF%D8%A9-%D9%81%D9%8A%D9%84%D9%85-no-place-2020-%D9%85%D8%AA%D8%B1%D8%AC%D9%85')
        sHtmlContent = oRequestHandler.request()
        if 'Video is processing now' in sHtmlContent:
			dialog().VSinfo("Video is processing...")
        
        api_call = ''
        #type1/([^"]+)/
        oParser = cParser()

       # (.+?) .+? ([^<]+)
        sPattern =  "file:'(.+?)'," 
        aResult = oParser.parse(sHtmlContent,sPattern)
        if (aResult[0] == True):
            api_call = aResult[1][0]

            if (api_call):
                return True, api_call +'|User-Agent=' + UA + '&AUTH=TLS&verifypeer=false' + '&Referer=' + self.__sUrl

       # (.+?) .+? ([^<]+)
        sPattern =  '<small  >([^<]+)</small> <a target="_blank"  download=".+?" onclick="updateData.+?"  href="([^<]+)" > <small  >' 
        aResult = oParser.parse(sHtmlContent,sPattern)
        if (aResult[0] == True):
            #initialisation des tableaux
            url=[]
            qua=[]
            #Replissage des tableaux
            for i in aResult[1]:
                url.append(str(i[1]).replace("[","%5B").replace("]","%5D").replace("+","%20"))
                qua.append(str(i[0]))

            api_call = dialog().VSselectqual(qua, url)

            if (api_call):
                return True, api_call +'|User-Agent=' + UA + '&AUTH=TLS&verifypeer=false' + '&Referer=' + self.__sUrl

        return False, False