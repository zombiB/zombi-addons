#-*- coding: utf-8 -*-
#Vstream https://github.com/Kodi-vStream/venom-xbmc-addons
#http://cloudvid.co/embed-xxxx.html
#https://clipwatching.com/embed-xxx.html
from resources.lib.handler.requestHandler import cRequestHandler
from resources.hosters.hoster import iHoster
from resources.lib.parser import cParser
from resources.lib.packer import cPacker
from resources.lib.comaddon import dialog
from resources.lib.comaddon import VSlog
import re,xbmc
import requests
UA = 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:68.0) Gecko/20100101 Firefox/68.0'

class cHoster(iHoster):

    def __init__(self):
        iHoster.__init__(self, 'mpupload', 'mp4upload')
			
    def setUrl(self, sUrl):
        self._url = str(sUrl).replace(".html","")
        if 'embed' in sUrl:
            self._url = self._url.replace("embed-","")

    def _getMediaLinkForGuest(self):
        	VSlog(self._url)

        	api_call = ''

        	oRequest = cRequestHandler(self._url)
        	sHtmlContent = oRequest.request()
        	_id = self._url.split('/')[-1].replace(".html","")
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
        	'Referer': self._url,
        	'Upgrade-Insecure-Requests': '1'}
        	prm={
                "op": "download2",
                "id": _id,
                "rand": "",
                "referer": self._url,
                "method_free": "+",
                "method_premium": ""}
        	_r = Sgn.post(self._url,headers=hdr,data=prm,allow_redirects=False).headers
        	api_call = _r['Location'].replace(" ","").replace("[","%5B").replace("]","%5D").replace("+","%20")
                	
        	if api_call:
        	   return True, api_call+ '|User-Agent=' + UA +'&verifypeer=false'+ '&Referer=' + 'https://www.mp4upload.com'

        	return False, False