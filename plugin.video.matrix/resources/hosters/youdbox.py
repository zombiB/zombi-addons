from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.hosters.hoster import iHoster
import re,xbmc
import requests


class cHoster(iHoster):

    def __init__(self):
        self.__sDisplayName = 'youdbox'
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
        return 'youdbox'

    def isDownloadable(self):
        return True

    def isJDownloaderable(self):
        return True

    def getPattern(self):
        return ''
        
    def __getIdFromUrl(self, sUrl):
        sPattern = "https://youdbox.com/([^<]+)/"
        oParser = cParser()
        aResult = oParser.parse(sUrl, sPattern)
        if (aResult[0] == True):
            return aResult[1][0]
        return ''

    def setUrl(self, sUrl):
        self.__sUrl = str(sUrl)
        if 'embed' in sUrl:
            self.__sUrl = self.__sUrl.replace("embed-","")
        if 'embed' not in sUrl:
        	sId = self.__getIdFromUrl(self.__sUrl)
        	self.__sUrl = 'https://youdbox.com/'+sId+'.html'

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
        _id = self.__sUrl.split('/')[-1].replace(".html","")
        Sgn=requests.Session()
        UA = 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:68.0) Gecko/20100101 Firefox/68.0'
        hdr = {'Host': 'youdbox.com',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:84.0) Gecko/20100101 Firefox/84.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'fr,fr-FR;q=0.8,en-US;q=0.5,en;q=0.3',
        'Accept-Encoding': 'gzip, deflate',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Content-Length': '111',
        'Origin': 'https://youdbox.com',
        'Connection': 'keep-alive',
        'Referer': self.__sUrl,
        'Upgrade-Insecure-Requests': '1'}
        prm={
        	"op": "download2",
        	"id": _id,
        	"rand": "",
        	"referer": self.__sUrl,
        	"method_free": "",
        	"method_premium": "",
        	"adblock_detected": "1"}
        _r = Sgn.post(self.__sUrl,headers=hdr,data=prm)
        sHtmlContent = _r.content.decode('utf8')
        oParser = cParser() 
        sPattern = '<a href="([^<]+)"><button class="lastbtn"><span>Free Download</span></button></a>'
        aResult = oParser.parse(sHtmlContent,sPattern)
        if (aResult[0] == True):
        	api_call = aResult[1][0] 
        if (api_call):
        	return True, api_call 
        return False, False