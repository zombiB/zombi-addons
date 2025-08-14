# -*- coding: utf-8 -*-

import random
import time

from resources.hosters.hoster import iHoster
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.comaddon import VSlog
from resources.lib import random_ua

UA = random_ua.get_pc_ua()

class cHoster(iHoster):

    def __init__(self):
        iHoster.__init__(self, 'dood', 'Dood')

    def setUrl(self, url):
        self._url = f'https://i.doodcdn.io/e/{url.rsplit("/",1)[1]}'

    def _getMediaLinkForGuest(self, autoPlay = False):
        VSlog(self._url)
        api_call = False
       
        sHost = getHost(self._url)

        oRequestHandler = cRequestHandler(self._url)
        oRequestHandler.addHeaderEntry('User-Agent', UA)
        oRequestHandler.enableCache(False)
        sHtmlContent = oRequestHandler.request()

        if '/pass_md5/' not in sHtmlContent:
            return None
        md5 = sHtmlContent.split("'/pass_md5/")[1].split("',")[0]

        token = md5.split("/")[-1]
        randomString = getRandomString()
        expiry = int(time.time() * 1000)

        oRequestHandler = cRequestHandler(f"{sHost}pass_md5/{md5}")
        oRequestHandler.addHeaderEntry('User-Agent', UA)
        oRequestHandler.addHeaderEntry('Referer', self._url)
        oRequestHandler.enableCache(False)
        videoUrlStart = oRequestHandler.request()

        api_call = f"{videoUrlStart}{randomString}?token={token}&expiry={expiry}"

        if api_call:
            return True, api_call.replace('~','%7E') + '|Referer=' + self._url + '&verifypeer=false'

        return False, False

def getRandomString(length=10):
    allowedChars = list('ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789')
    return ''.join(random.choice(allowedChars) for _ in range(length))

def getHost(self):
    parts = self.rsplit("/", 2)
    host = parts[0] 
    return f'{host}/'