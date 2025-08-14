#-*- coding: utf-8 -*-

from resources.hosters.hoster import iHoster
from resources.lib.comaddon import VSlog
from six.moves import urllib_parse
import re
import requests

UA = 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Mobile Safari/537.36'

class cHoster(iHoster):

    def __init__(self):
        iHoster.__init__(self, 'hexupload', 'Hexupload')

    def _getMediaLinkForGuest(self, autoPlay = False):
         VSlog(self._url)
         api_call = ''
         headers = {
            'User-Agent': UA
         }

         if 'embed' in self._url:
               d = re.findall('https://(.*?)/embed-([^<]+).html', self._url)
               for aEntry in d:
                  sHost = aEntry[0]
                  file_id = aEntry[1]
                
         else:
               d = re.findall('https://(.*?)/([^<]+)', self._url)
               for aEntry in d:
                  sHost = aEntry[0]
                  file_id = aEntry[1]
                  if '/' in file_id:
                     file_id = file_id.split('/')[0]

         payload = {
                  "op": "download3",
                  "id": f"{file_id}",
                  "ajax": "1",
                  "method_free": "1"
                  }
         headers['content-type'] = "application/x-www-form-urlencoded"
         headers['Accept'] = "application/json"
         sContent = requests.post(f'https://{sHost}/download', data=payload, headers=headers).json()
         api_call = sContent['result']['url']
         
         if api_call:
             return True, urllib_parse.quote(api_call, ':/?=&')

         return False, False