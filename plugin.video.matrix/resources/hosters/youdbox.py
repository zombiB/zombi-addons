#-*- coding: utf-8 -*-
#
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.hosters.hoster import iHoster
from resources.lib.comaddon import VSlog
import requests


class cHoster(iHoster):

    def __init__(self):
        iHoster.__init__(self, 'youdbox', 'youdbox')
        
    def __getIdFromUrl(self, sUrl):
        sPattern = "https://youdbox.org/(.+?)/"
        oParser = cParser()
        aResult = oParser.parse(sUrl, sPattern)
        if aResult[0]:
            return aResult[1][0]
        return ''

    def setUrl(self, sUrl):
        self._url = str(sUrl)
        if 'embed' in sUrl:
            self._url = self._url.replace("embed-","")

    def _getMediaLinkForGuest(self):

        api_call = ''
        VSlog(self._url)

        oRequest = cRequestHandler(self._url)
        sHtmlContent = oRequest.request()
        oParser = cParser() 
        

        sPattern = '<source src="([^<]+)" type="video/mp4"'
        aResult = oParser.parse(sHtmlContent, sPattern)
        if aResult[0]:
            api_call = aResult[1][0] 
				
        _id = self._url.split('/')[-1].replace(".html","")
        Sgn=requests.Session()
        UA = 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:68.0) Gecko/20100101 Firefox/68.0'
        hdr = {'Host': 'yodbox.com',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:84.0) Gecko/20100101 Firefox/84.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'fr,fr-FR;q=0.8,en-US;q=0.5,en;q=0.3',
        'Accept-Encoding': 'gzip, deflate',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Content-Length': '111',
        'Origin': 'https://yodbox.com',
        'Connection': 'keep-alive',
        'Referer': self._url,
        'Upgrade-Insecure-Requests': '1'}
        prm={
        	"op": "download2",
        	"id": _id,
        	"rand": "",
        	"referer": self._url,
        	"method_free": "",
        	"method_premium": "",
        	"adblock_detected": "1"}
        _r = Sgn.post(self._url,headers=hdr,data=prm)
        sHtmlContent = _r.content.decode('utf8',errors='ignore')
        oParser = cParser() 
        sPattern = '<a href="([^<]+)"><button class="lastbtn"><span>Free Download</span></button>'
        aResult = oParser.parse(sHtmlContent,sPattern)
        if aResult[0]:
        	api_call = aResult[1][0] 
        if api_call:
        	return True, api_call 
        return False, False