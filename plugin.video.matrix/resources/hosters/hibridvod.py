#-*- coding: utf-8 -*-

from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.lib.comaddon import dialog, xbmcgui
from resources.hosters.hoster import iHoster
from resources.lib.comaddon import VSlog
import re
import requests
UA = 'Mozilla/5.0 (Linux; Android 8.0; Pixel 2 Build/OPD3.170816.012) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.93 Mobile Safari/537.36'

class cHoster(iHoster):

    def __init__(self):
        iHoster.__init__(self, 'hibridvod', 'hibridvod')

    def _getMediaLinkForGuest(self):

        api_call = ''
        VSlog(self._url)

        oRequest = cRequestHandler(self._url)
        sHtmlContent = oRequest.request()
    
  # ([^<]+) .+?
        headers = {'User-Agent': UA,
                	'Accept': '*/*',
                	'referer': 'https://rotana.net/',
                	'origin': 'https://rotana.net',
                	'x-correlation-id': 'undefined',
                	'x-embed-version': 'VOD Embed v1.0'}
        s = requests.Session()
        r = s.get(self._url, headers = headers)
        sHtmlContent = r.content.decode('utf8')
        oParser = cParser()

        list_q = []
        list_url = []
        sPattern = ',"embed_url":"(.+?)",'
        aResult = oParser.parse(sHtmlContent, sPattern)
        if aResult[0] :
        	url2 = aResult[1][0]
        	r = s.get(url2, headers = headers)
        	sHtmlContent2 = r.content.decode('utf8')
        	sPattern = ',RESOLUTION=(.+?),LANGUAGE="eng"(.+?)#EXT'
        	aResult = oParser.parse(sHtmlContent2, sPattern)
        	for aEntry in aResult[1]:
        	    list_q.append(aEntry[0]) 
        	    list_url.append(url2.replace("playlist.m3u8",aEntry[1])) 

        	if list_url:
        	   api_call = dialog().VSselectqual(list_q,list_url)
        if api_call:
        	return True, api_call 

        return False, False
        
