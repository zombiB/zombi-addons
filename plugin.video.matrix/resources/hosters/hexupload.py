#-*- coding: utf-8 -*-
# Yonn1981 https://github.com/Yonn1981/Repo

from resources.lib.handler.requestHandler import cRequestHandler
from resources.hosters.hoster import iHoster
from resources.lib.comaddon import VSlog
import re
import requests
import base64

UA = 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Mobile Safari/537.36'

class cHoster(iHoster):

    def __init__(self):
        iHoster.__init__(self, 'hexupload', 'Hexupload')

    def _getMediaLinkForGuest(self, autoPlay = False):
         VSlog(self._url)
         api_call = ''

         if 'embed' in self._url:
            oRequestHandler = cRequestHandler(self._url)
            oRequestHandler.addHeaderEntry('User-Agent', UA)
            oRequestHandler.addHeaderEntry('Referer', self._url)
            oRequestHandler.addHeaderEntry('origin', self._url.rsplit('/', 1)[0])
            sHtmlContent = oRequestHandler.request()

            aResult = re.search(r'b4aa\.buy\("([^"]+)', sHtmlContent)
            if aResult:
               api_call = base64.b64decode(aResult.group(1)).decode('utf8',errors='ignore')
               VSlog(api_call)
               api_call = api_call
                
         else:
               d = re.findall('https://(.*?)/([^<]+)',self._url)
               for aEntry in d:
                  sHost= aEntry[0]
                  sID= aEntry[1]
                  if '/' in sID:
                     sID = sID.split('/')[0]
               sLink= 'https://'+sHost+'/'+sID     

               Sgn=requests.Session()
               headers = {
                  'Origin': 'http://{0}'.format(sHost),
                  'Referer': sLink,
                  'User-Agent': UA
                  }
               payload = {
                  'op': 'download2',
                  'id': sID,
                  'rand': '',
                  'referer': sLink,
                  'method_free': 'Free Download'
                  }
               _r = Sgn.post(sLink,headers=headers,data=payload)
               sHtmlContent = _r.content.decode('utf8',errors='ignore')

               url = re.search(r"ldl.ld\('([^']+)", sHtmlContent)
               if url:
                  api_call = base64.b64decode(url.group(1)).decode('utf8',errors='ignore')
                  api_call = api_call.replace(' ', '%20')
         
         if api_call:
             return True, api_call

         return False, False