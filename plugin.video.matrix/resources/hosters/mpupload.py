#-*- coding: utf-8 -*-
#Vstream https://github.com/Kodi-vStream/venom-xbmc-addons
#http://cloudvid.co/embed-xxxx.html
#https://clipwatching.com/embed-xxx.html
from resources.lib.handler.requestHandler import cRequestHandler
from resources.hosters.hoster import iHoster
from resources.lib.parser import cParser
from resources.lib.packer import cPacker
from resources.lib.comaddon import dialog
import re,xbmc
import requests
UA = 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:68.0) Gecko/20100101 Firefox/68.0'

class cHoster(iHoster):

    def __init__(self):
        self.__sDisplayName = 'mp4upload'
        self.__sFileName = self.__sDisplayName
        self.__sHD = ''

    def getDisplayName(self):
        return  self.__sDisplayName

    def setDisplayName(self, sDisplayName):
        self.__sDisplayName = sDisplayName + ' [COLOR skyblue]' + self.__sDisplayName + '[/COLOR]'

    def setFileName(self, sFileName):
        self.__sFileName = sFileName

    def getFileName(self):
        return self.__sFileName

    def getPluginIdentifier(self):
        return 'mpupload'

    def setHD(self, sHD):
        self.__sHD = ''

    def getHD(self):
        return self.__sHD

    def isDownloadable(self):
        return False

    def isJDownloaderable(self):
        return False

    def getPattern(self):
        return ''

    def __getIdFromUrl(self, sUrl):
        return ''

    def setUrl(self, sUrl):
        self.__sUrl = str(sUrl).replace(".html","")
        if 'embed' in sUrl:
            self.__sUrl = self.__sUrl.replace("embed-","")
            
    def checkUrl(self, sUrl):
        return True

    def __getUrl(self, media_id):
        return

    def getMediaLink(self):
        return self.__getMediaLinkForGuest()

    def __getMediaLinkForGuest(self):

        	api_call = ''

        	oRequest = cRequestHandler(self.__sUrl)
        	sHtmlContent = oRequest.request()
        	_id = self.__sUrl.split('/')[-1].replace(".html","")
        	Sgn=requests.Session()
        	UA = 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:68.0) Gecko/20100101 Firefox/68.0'
        	hdr = {'Host': 'www.mp4upload.com',
        	'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:84.0) Gecko/20100101 Firefox/84.0',
        	'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        	'Accept-Language': 'fr,fr-FR;q=0.8,en-US;q=0.5,en;q=0.3',
        	'Accept-Encoding': 'gzip, deflate',
        	'Content-Type': 'application/x-www-form-urlencoded',
        	'Content-Length': '111',
        	'Origin': 'https://www.mp4upload.com',
        	'Connection': 'keep-alive',
        	'Referer': self.__sUrl,
        	'Upgrade-Insecure-Requests': '1'}
        	prm={
                "op": "download2",
                "id": _id,
                "rand": "",
                "referer": self.__sUrl,
                "method_free": "+",
                "method_premium": ""}
        	_r = Sgn.post(self.__sUrl,headers=hdr,data=prm,allow_redirects=False).headers
        	api_call = _r['Location'].replace(" ","").replace("[","%5B").replace("]","%5D").replace("+","%20")
                	
        	if (api_call):
        	   return True, api_call+ '|User-Agent=' + UA +'&verifypeer=false'+ '&Referer=' + 'https://www.mp4upload.com'

        	return False, False