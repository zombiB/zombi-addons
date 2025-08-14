# -*- coding: utf-8 -*-
# vStream https://github.com/Kodi-vStream/venom-xbmc-addons

import json
import requests

from resources.lib.parser import cParser
from resources.hosters.hoster import iHoster
from resources.lib.comaddon import dialog
from resources.lib.util import cUtil
from resources.lib.comaddon import VSlog
from resources.lib import random_ua

UA = random_ua.get_pc_ua()

class cHoster(iHoster):
    def __init__(self):
        iHoster.__init__(self, 'ok_ru', 'Ok.ru')

    def getHostAndIdFromUrl(self, sUrl):
        sPattern = 'https*:\/\/.*?((?:(?:ok)|(?:odnoklassniki))\.ru)\/.+?\/([0-9]+)'
        oParser = cParser()
        aResult = oParser.parse(sUrl, sPattern)
        if aResult[0]:
            return aResult[1][0]
        return ''

    def _getMediaLinkForGuest(self, autoPlay = False):
        VSlog(self._url)
        v = self.getHostAndIdFromUrl(self._url)
        sId = v[1]
        sHost = v[0]
        web_url = 'http://' + sHost + '/videoembed/' + sId

        hdrs = {'User-Agent': UA,
                   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'}

        St=requests.Session()
        sHtmlContent = St.get(web_url, headers = hdrs).content.decode('utf-8')
        oParser = cParser()

        sHtmlContent = oParser.abParse(sHtmlContent, 'data-options=', '" data-player-container', 14)
        sHtmlContent = cUtil().removeHtmlTags(sHtmlContent)
        sHtmlContent = cUtil().unescape(sHtmlContent)

        page = json.loads(sHtmlContent)
        page = json.loads(page['flashvars']['metadata'])

        resolutions = {
            "ultra": "2160",
            "quad": "1440",
            "full": "1080",
            "hd": "720",
            "sd": "480",
            "low": "360",
            "lowest": "240",
            "mobile": "144"
        }

        if page:
            sPattern = "'hlsMasterPlaylistUrl': '(.+?)',"
            aResult = oParser.parse(page, sPattern)
            if (aResult[0] == True):
                api_call = aResult[1][0]
            url = []
            qua = []

            for x in reversed(page['videos']):
                resolution_name = x['name']
                resolution_value = resolutions.get(resolution_name.lower(), "Unknown")
                url.append(x['url'])
                qua.append(f"{resolution_value}p" if resolution_value != "Unknown" else resolution_name)

            if (url):
                api_call = dialog().VSselectqual(qua, url)

        if api_call:
            api_call = api_call + '|Referer=' + self._url
            return True, api_call

        return False, False
