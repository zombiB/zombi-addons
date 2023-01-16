#-*- coding: utf-8 -*-
#Vstream https://github.com/Kodi-vStream/venom-xbmc-addons
#https://sama-share.com/embed-shsaa6s49l55-750x455.html
from resources.lib.handler.requestHandler import cRequestHandler
from resources.hosters.hoster import iHoster
from resources.lib.parser import cParser
from resources.lib.comaddon import dialog
from resources.lib.comaddon import VSlog
import re,xbmc
import requests
UA = 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Mobile Safari/537.36'



class cHoster(iHoster):

    def __init__(self):
        iHoster.__init__(self, 'uppom', 'uppom')

    def setUrl(self, sUrl):
        self._url = str(sUrl).replace(".html","")
        if 'embed' in sUrl:
            self._url = self._url.replace("embed-","")

    def _getMediaLinkForGuest(self):
        	VSlog(self._url)
        	sUrl = self._url
        	VSlog(sUrl)
        	d = re.findall('https://(.*?)/([^<]+)',sUrl)
        	for aEntry1 in d:
        	    sHost= aEntry1[0]
        	    sID= aEntry1[1]
        	    if '/' in sID:
        	       sID = sID.split('/')[0]
        	    sLink= 'https://'+aEntry1[0]+'/'+aEntry1[1]
        	    VSlog(sHost)
        	    VSlog(sID)
        	    VSlog(sLink)

        	api_call = ''

        	oRequest = cRequestHandler(self._url)
        	sHtmlContent = oRequest.request()
        	VSlog(sHtmlContent)
        	_id = sID
        	VSlog(_id)
        	Sgn=requests.Session()
        	UA = 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:68.0) Gecko/20100101 Firefox/68.0'
        	hdr = {'Host': sHost,
        	'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:84.0) Gecko/20100101 Firefox/84.0',
        	'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        	'Accept-Language': 'fr,fr-FR;q=0.8,en-US;q=0.5,en;q=0.3',
        	'Accept-Encoding': 'gzip, deflate',
        	'Content-Type': 'application/x-www-form-urlencoded',
        	'Content-Length': '111',
        	'Origin': 'https://'+sHost,
        	'Connection': 'keep-alive',
        	'Referer': self._url,
        	'Upgrade-Insecure-Requests': '1'}
        	prm={
                "op": "download2",
                "id": _id,
                "rand": "",
                "referer": self._url,
                "method_free": "+",
                "method_premium": ""}
        	_r = Sgn.post(sLink,headers=hdr,data=prm,allow_redirects=False).headers
        	api_call = _r['Location'].replace(" ","").replace("[","%5B").replace("]","%5D").replace("+","%20")
                	
        	if api_call:
        	   return True, api_call+ '|User-Agent=' + UA +'&verifypeer=false'+ '&Referer=' + 'https://'+sHost

        	return False, False