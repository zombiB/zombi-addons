# -*- coding: utf-8 -*-
# vStream https://github.com/Kodi-vStream/venom-xbmc-addons
#
try:  # Python 2
    import urllib2
    from urllib2 import URLError as UrlError

except ImportError:  # Python 3
    import urllib.request as urllib2
    from urllib.error import URLError as UrlError

import re

from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.lib.comaddon import VSlog, xbmcgui
from resources.hosters.hoster import iHoster
from resources.lib.comaddon import VSlog
import xbmc


class cHoster(iHoster):

    def __init__(self):
        iHoster.__init__(self, 'samaup', 'samaup')

    def setUrl(self, sUrl):
        self._url = str(sUrl)
        if '.cc' in sUrl:
            self._url = self._url.replace(".cc",".org")
        if 'embed' in sUrl:
            self._url = self._url.replace("embed-","")
        self._url = self._url.split('-')[0]

    def _getMediaLinkForGuest(self):
        	VSlog(self._url)

        	api_call = ''

        	oRequest = cRequestHandler(self._url)
        	sHtmlContent = oRequest.request()
        	_id = self._url.split('/')[-1].replace(".html","")
        	Sgn=requests.Session()
        	UA = 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:68.0) Gecko/20100101 Firefox/68.0'
        	hdr = {'Host': 'sama-share.com',
        	'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:84.0) Gecko/20100101 Firefox/84.0',
        	'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        	'Accept-Language': 'fr,fr-FR;q=0.8,en-US;q=0.5,en;q=0.3',
        	'Accept-Encoding': 'gzip, deflate',
        	'Content-Type': 'application/x-www-form-urlencoded',
        	'Content-Length': '161',
        	'Origin': 'https://sama-share.com/',
        	'Connection': 'keep-alive',
        	'Referer': self._url,
        	'Upgrade-Insecure-Requests': '1'}
        	prm={
                "op": "download1",
                "id": _id,
                "rand": "",
                "referer": "",
                "method_free": "téléchargement libre"}
        	_r = Sgn.post(self._url,headers=hdr,data=prm,allow_redirects=False).headers
        	api_call = _r['Location'].replace(" ","").replace("[","%5B").replace("]","%5D").replace("+","%20")
                	
        	if api_call:
        	   return True, api_call+ '|User-Agent=' + UA +'&verifypeer=false'+ '&Referer=' + 'https://sama-share.com/'

        	return False, False