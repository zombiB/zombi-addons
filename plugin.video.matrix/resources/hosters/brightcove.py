# -*- coding: utf-8 -*-

from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.lib.comaddon import dialog, VSlog
from resources.hosters.hoster import iHoster

import re

class cHoster(iHoster):

    def __init__(self):
        iHoster.__init__(self, 'brightcove', 'brightcove')

    def isDownloadable(self):
        return True

    def _getMediaLinkForGuest(self):
        VSlog(self._url)
        
        oRequest = cRequestHandler(self._url)
        sHtmlContent = oRequest.request()
        
        oParser = cParser()
    #recup du lien mp4
        sPattern =  ',policyKey:"(.+?)"}},{name:"dock",' 
        aResult = oParser.parse(sHtmlContent,sPattern)
        if aResult[0] :
            mkey =  aResult[1][0]
    
 
        sPattern = 'data-account="(.+?)"'
        aResult = oParser.parse(sHtmlContent, sPattern)
        if aResult[0] :
           import requests
           s = requests.Session()  
           mcnt =  aResult[1][0]   
           mvid =  self._url.rsplit('index.html?videoId=', 1)[1]      
           headers = {'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Mobile Safari/537.36',
							'accept': 'application/json;pk='+mkey,
							'origin': 'https://players.brightcove.net',
							'Referer': 'https://players.brightcove.net/'}
           r = s.get('https://edge.api.brightcove.com/playback/v1/accounts/'+mcnt+'/videos/'+mvid, headers=headers)
           sHtmlContent = r.content.decode('utf8')
		   
        sPattern = '"src":"([^"]+\.mp4)","width":(.+?)},'
        aResult = oParser.parse(sHtmlContent, sPattern)
        
        api_call = False

        if aResult[0] :
            
            #initialisation des tableaux
            url=[]
            qua=[]
            
            #Replissage des tableaux
            for i in aResult[1]:
                url.append(str(i[0]))
                qua.append(str(i[1]))

            api_call = dialog().VSselectqual(qua, url)

            if api_call:
                return True, api_call

        return False, False
