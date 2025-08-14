# -*- coding: utf-8 -*-

import re, time, urllib.parse
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.comaddon import VSlog
from resources.lib.util import urlHostName
from resources.hosters.hoster import iHoster
from resources.lib import random_ua

UA = random_ua.get_pc_ua()

class cHoster(iHoster):

    def __init__(self):
        iHoster.__init__(self, 'terabox', 'TeraBox')
			
    def _getMediaLinkForGuest(self, autoPlay = False):
        VSlog(self._url)

        sHost = urlHostName(self._url)

        oRequest = cRequestHandler(self._url)
        oRequest.addHeaderEntry('User-Agent', UA)
        oRequest.enableCache(False)
        sHtmlContent = oRequest.request()

        start_delimiter = "function%20fn%28a%29%7Bwindow.jsToken%20%3D%20a%7D%3Bfn%28%22"
        end_delimiter = "%22%29"

        pattern = re.escape(start_delimiter) + r"(.+?)" + re.escape(end_delimiter)
        match = re.search(pattern, sHtmlContent)
        if match:
            js_token = match.group(1)
            app_id = '250528'
            url_short = self._url.split('surl=')[1].split("&")[0]

            api_link = f'https://www.{sHost}/api/shorturlinfo?app_id={app_id}&web=1&channel=dubox&clienttype=0&jsToken={js_token}&shorturl=1{url_short}&root=1&scene='

            headers = {
                    "host": f"www.{sHost}",
                    "accept": "application/json, text/plain, */*",
                    "x-requested-with": "XMLHttpRequest",
                    "user-agent": UA,
                    "referer": self._url,
            }

            import requests
            sHtmlContent = requests.get(api_link, headers=headers).json()

            req_playlist_url = f'https://www.{sHost}/share/extstreaming.m3u8'
            timestamp = int(time.time() * 1000)
    
            params = {
                'app_id': app_id,
                'channel': 'dubox',
                'clienttype': 0,
                'uk': sHtmlContent["uk"],
                'shareid': sHtmlContent["shareid"],
                'type': 'M3U8_AUTO_1080',
                'fid': sHtmlContent["list"][0]["fs_id"],
                'sign': sHtmlContent["sign"],
                'timestamp': timestamp,
            }
            
            req_playlist_url += '?' + urllib.parse.urlencode(params)

            api_call = req_playlist_url

        if api_call:
            return True, api_call

        return False, False