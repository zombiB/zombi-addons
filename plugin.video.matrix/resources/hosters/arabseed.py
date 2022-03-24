#-*- coding: utf-8 -*-

from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.lib.comaddon import dialog
from resources.hosters.hoster import iHoster
from resources.lib.comaddon import VSlog

UA = 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Mobile Safari/537.36'

class cHoster(iHoster):

    def __init__(self):
        iHoster.__init__(self, 'arabseed', 'arabseed')

    def isDownloadable(self):
        return True

    def setUrl(self, sUrl):
        self._url = str(sUrl)
        if 'embed' in sUrl:
            self._url = self._url.replace("embed-","")

    def _getMediaLinkForGuest(self):
        VSlog(self._url)
        sUrl = self._url

        oRequest = cRequestHandler(self._url)
        sHtmlContent = oRequest.request()
        oParser = cParser()
    
        sId = ''

        sPattern = 'name="id" value="(.+?)">'
        aResult = oParser.parse(sHtmlContent, sPattern)
    
        if (aResult[0]):
        	sId = aResult[1][0]
        import requests

    
  # ([^<]+) .+?
        headers = {'Host': 'm.seeeed.xyz',
                	'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36',
                	'Accept': '*/*',
                	'Accept-Language': 'fr,fr-FR;q=0.8,en-US;q=0.5,en;q=0.3',
                	'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
                	'X-Requested-With': 'XMLHttpRequest',
                	'Referer': sUrl,
                	'origin': 'https://m.seeeed.xyz',
                	'Connection': 'keep-alive'}
        data = {'op':'download2','id':sId,'rand':'','referer':'','method_free':'','method_premium':''}
        s = requests.Session()
        r = s.post(sUrl, headers = headers,data = data)
        sHtmlContent = r.content
        sPattern = '<span id="direct_link" style.+?<a href="([^<]+)">'
        aResult = oParser.parse(sHtmlContent, sPattern)
        if aResult[0] is True:
        	api_call = aResult[1][0] + '|User-Agent=' + UA +'&verifypeer=false'+ '&Referer=https://m.seeeed.xyz' 

        if api_call:
            return True, api_call

        return False, False
        
