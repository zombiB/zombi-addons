#-*- coding: utf-8 -*-
#Vstream https://github.com/Kodi-vStream/venom-xbmc-addons
import re

from resources.lib.handler.requestHandler import cRequestHandler
from resources.hosters.hoster import iHoster
from resources.lib.comaddon import dialog, VSlog
from resources.lib.util import urlEncode, Quote
UA = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:68.0) Gecko/20100101 Firefox/68.0'

class cHoster(iHoster):

    def __init__(self):
        iHoster.__init__(self, 'lien_direct', 'Lien direct')

    def setUrl(self, url):
        self._url = str(url).replace('+', '%20') # un lien direct n'est pas forcement urlEncoded

    def _getMediaLinkForGuest(self):
        api_call = self._url
        VSlog(self._url)

        api_call = self._url.replace("rrsrr","cimanow")
        if 'ddsdd' in api_call:
            api_call = self._url.replace("ddsdd","upbam")    
            UA = 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.109 Safari/537.36'
            api_call = api_call + '|User-Agent=' + UA + '&Referer=' + self._url
 	   
        if 'ffsff' in api_call:
            api_call = self._url.replace("ffsff","moshahda")
            sReferer = self._url.split('|Referer=')[1]      
            UA = 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.109 Safari/537.36'
            api_call = api_call + '|User-Agent=' + UA + '&Referer=' + sReferer
        if 'wasabisys' in api_call:
            UA = 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.109 Safari/537.36'
            api_call = api_call + '|User-Agent=' + UA + '&Referer=https://www.toonsland.site'
 
        if 'aflaam' in api_call:
            UA = 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.109 Safari/537.36'
            api_call = api_call + '|User-Agent=' + UA  + '&Referer=https://aflaam.com/'
				
        if 'fushaar' in api_call:
            api_call = api_call + '|AUTH=TLS&verifypeer=false'  + '&Referer=https://fushaar.com/'
       
        if 'akwam' in api_call or '.akw.' in api_call:
            api_call = api_call + '|AUTH=TLS&verifypeer=false'  + '&Referer=https://to.akwam.im/'
        if 'panet' in api_call:
            api_call = api_call + '|AUTH=TLS&verifypeer=false' 
        if 'scorarab' in api_call:
            UA = 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Mobile Safari/537.36'
            api_call = api_call + '|&User-Agent=' + UA + '&Referer=' + 'https://live.scorarab.com/'
        if 'beintube' in api_call:
            UA = 'Mozilla/5.0 (iPad; CPU OS 13_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) CriOS/87.0.4280.77 Mobile/15E148 Safari/604.1'
            api_call = api_call + '|AUTH=TLS&verifypeer=false&Referer=' + 'https://beinmatch.site'
        if 'cimanow' in api_call:
            UA = 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.109 Safari/537.36'
            api_call = api_call + '|AUTH=TLS&verifypeer=false' + '&User-Agent=' + UA + '&Referer=' + 'https://en.cimanow.cc'
       
        if '?src=' in api_call:
            api_call = api_call.split('?src=')[1]
       
        if '+' in api_call:
            api_call = api_call.replace("[","%5B").replace("]","%5D").replace("+","%20")
        	
        if 'bittube.video/videos/' in api_call:
            api_call = api_call + '-1080.mp4' 
            api_call = api_call.replace("/videos/embed/","/download/videos/")
	   
        if 'goal4live.com' in api_call:
            UA = 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.109 Safari/537.36'
            api_call = api_call + '|User-Agent=' + UA 



        if 'fushaar' in api_call:
            UA = 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.109 Safari/537.36'
            api_call = api_call + '|User-Agent=' + UA  + '&Referer=' + self._url
        if 'egybest' in api_call:
            from resources.lib.parser import cParser
            import requests
            oParser = cParser()
            sHtmlContent=requests.get(api_call).content
        	
            sPattern =  ',RESOLUTION=(.+?),.+?(http.+?.m3u8)'
            aResult = oParser.parse(sHtmlContent, sPattern)
            if (aResult[0] == True):
               url=[]
               qua=[]
               for i in aResult[1]:
                  url.append(str(i[1]))
                  qua.append(str(i[0]).split('x')[1]+"p")
               api_call = dialog().VSselectqual(qua, url)

        #Special pour toonanime.
        if 'toonanime' in api_call:
            oRequest = cRequestHandler(api_call)
            oRequest.addHeaderEntry('Referer', 'https://lb.toonanime.xyz/')
            sHtmlContent = oRequest.request()

            aResult = re.findall(',RESOLUTION=(.+?)\n(.+?).m3u8',sHtmlContent)
            #initialisation des tableaux
            url=[]
            qua=[]
            api_call = ''
            #Remplissage des tableaux
            for i in aResult:
                url.append(str(i[1]) + '.m3u8')
                qua.append(str(i[0]))

            headers = {
                "User-Agent":Quote("Mozilla/5.0 (Linux; Android 6.0.1; SM-G930V Build/MMB29M) " + \
                    "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.89 Mobile Safari/537.36"),
                "Referer":"https://lb.toonanime.xyz/"
            }

            #Affichage du tableau
            api_call = "http://127.0.0.1:2424?u=https://lb.toonanime.xyz" + dialog().VSselectqual(qua, url) + \
                "@" + urlEncode(headers)

        if api_call:
            return True, api_call

        return False, False
