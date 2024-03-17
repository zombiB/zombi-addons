#-*- coding: utf-8 -*-

from resources.hosters.hoster import iHoster
from resources.lib.parser import cParser
from resources.lib.comaddon import VSlog
from resources.lib.util import Unquote
from resources.lib.packer import cPacker
import re
import requests

UA = 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Mobile Safari/537.36'

class cHoster(iHoster):

    def __init__(self):
        iHoster.__init__(self, 'cimacafe', 'CimaCafe')

    def _getMediaLinkForGuest(self, autoPlay = False):
         VSlog(self._url)
         oParser = cParser() 

         headers = {'User-Agent': UA,
                   'Referer': self._url
                   }
         s = requests.session()
         sHtmlContent = s.get(self._url, headers=headers).text
        
         sPattern = 'file: ["\']([^"\']+)'
         aResult = oParser.parse(sHtmlContent, sPattern)

         if aResult[0] is True:
            api_call = aResult[1][0]
         
         if api_call:
             return True, api_call + '|User-Agent=' + UA + '&Referer=' + self._url

         return False, False