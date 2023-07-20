#-*- coding: utf-8 -*-
#############################################################
# Yonn1981 https://github.com/Yonn1981/Repo
#############################################################

from resources.lib.handler.requestHandler import cRequestHandler
from resources.hosters.hoster import iHoster
from resources.lib.parser import cParser
from resources.lib.packer import cPacker
from resources.lib.comaddon import dialog
from resources.lib.comaddon import VSlog
import re,xbmc
import requests
UA = 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Mobile Safari/537.36'



class cHoster(iHoster):

    def __init__(self):
        iHoster.__init__(self, 'vidhls', 'vidHLS')

    def setUrl(self, sUrl):
        self._url = str(sUrl).replace(".html","")


    def _getMediaLinkForGuest(self):
        sUrl = self._url

        oRequest = cRequestHandler(self._url)
        sHtmlContent = oRequest.request()

        sdata = sUrl.split('data=')[1]

        Sgn=requests.Session()

        hdr = {'Sec-Fetch-Mode': 'navigate',
        	'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        	'Accept-Language': 'en-US,en;q=0.9,ar;q=0.8',
        	'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Mobile Safari/537.36 Edg/114.0.1823.82',
        	'Upgrade-Insecure-Requests': '1',
        	'Referer': 'https://movtime3.store/'}
        prm={
                "data": sdata}
        _r = Sgn.post(sUrl,headers=hdr,data=prm)
        sHtmlContent = _r.content.decode('utf8',errors='ignore').replace('\\','')
        oParser = cParser() 

        sPattern = '"videoServer":"([^"]+)'
        aResult = oParser.parse(sHtmlContent, sPattern)
        
        if aResult[0]:
            VidServ = aResult[1][0]
            if "1" in VidServ :
                sHost = 'https://yaviidcdn.com'
            if "2" in VidServ :
                sHost = 'https://cvidme.com'
            if "3" in VidServ :
                sHost = 'https://muviz-se2.com'
            if "4" in VidServ :
                sHost = 'https://muviz-se1.com'
            if "5" in VidServ :
                sHost = 'https://yavidcdn.com'
            if "6" in VidServ :
                sHost = 'https://storemecdn.com'
            if "7" in VidServ :
                sHost = 'https://storemycdn.com'
            if "8" in VidServ :
                sHost = 'https://cvidme.com'
            if "9" in VidServ :
                sHost = 'https://saudflix.com'
            if "10" in VidServ :
                sH1ost = 'https://cdvidme.com'
            if "11" in VidServ :
                sHost = 'https://aotcdn.com'
            if "12" in VidServ :
                sHost = 'https://cdnvidme.com'

        sPattern = '"videoUrl":"([^"]+)'
        aResult = oParser.parse(sHtmlContent, sPattern)
        
        if aResult[0]:
            Url2 = aResult[1][0]
            Url2 = sHost+Url2
            api_call = Url2.replace('hls','down')

        if api_call:
            return True, api_call

        return False, False