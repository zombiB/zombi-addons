#-*- coding: utf-8 -*-

from resources.hosters.hoster import iHoster
from resources.lib.parser import cParser
from resources.lib.comaddon import VSlog
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib import random_ua
from urllib.parse import urlparse

UA = random_ua.get_pc_ua()

class cHoster(iHoster):

   def __init__(self):
        iHoster.__init__(self, 'uploady', 'Uploady')

   def setUrl(self, sUrl):
      parsed_url = urlparse(sUrl)
      domain = parsed_url.netloc
      file_id = parsed_url.path.strip("/")
      self._url = f'https://{domain}/embed-{file_id}.html'

   def _getMediaLinkForGuest(self, autoPlay = False):
         VSlog(self._url)
         oParser = cParser() 
         oRequest = cRequestHandler(self._url)
         oRequest.addHeaderEntry('User-Agent', UA)
         oRequest.enableCache(False)
         sHtmlContent = oRequest.request()
        
         sPattern = 'src: ["\']([^"\']+)'
         aResult = oParser.parse(sHtmlContent, sPattern)

         if aResult[0] is True:
               api_call = aResult[1][0]
         
         if api_call:
             return True, f'{api_call}|verifypeer=false&User-Agent={UA}'

         return False, False