#-*- coding: utf-8 -*-

from resources.hosters.hoster import iHoster
from resources.lib.comaddon import VSlog, dialog
import base64
import json
import requests, re

UA = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36 Edg/122.0.0.0'

class cHoster(iHoster):

    def __init__(self):
        iHoster.__init__(self, 'shortlink', 'Short.ink')

    def __getHost(self, url):
        parts = url.split('//', 1)
        host = parts[1].split('/', 1)[0]
        return host

    def _getMediaLinkForGuest(self, autoPlay = False):
        VSlog(self._url)
        response = requests.get(self._url)
        sUrl = response.url
        host = self.__getHost(sUrl)
        sHost = f'https://{host}/'

        api_call = ''
        s = requests.session()
        headers = {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
            "Accept-Language": "en-US,en;q=0.9",
            "Connection": "keep-alive",
            "Host": host,
            "sec-ch-ua": '"Chromium";v="122", "Not(A:Brand";v="24", "Microsoft Edge";v="122"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": '"Windows"',
            "Sec-Fetch-Dest": "iframe",
            "Sec-Fetch-Mode": "navigate",
            "Sec-Fetch-Site": "cross-site",
            "Upgrade-Insecure-Requests": "1",
            "User-Agent": UA
            }

        response = s.get(sUrl, headers=headers).text

        piece_length_json = json.loads(
            re.search(
                r'({"pieceLength.+?})',
                response,
            ).group(1)
        )

        resolution_option = {}
        quality_prefix = {}
        piece_length = {}
        if "sd" in piece_length_json.keys():
            resolution_option.update({"1": "360p"})
            quality_prefix.update({"1": ""})
            piece_length.update({"1": f'{piece_length_json["sd"][0]}'})
        if "mHd" in piece_length_json.keys():
            resolution_option.update({"2": "480p"})
            quality_prefix.update({"2": ""})
            piece_length.update({"2": f'{piece_length_json["mHd"][0]}'})
        if "hd" in piece_length_json.keys():
            resolution_option.update({"3": "720p"})
            quality_prefix.update({"3": "www"})
            piece_length.update({"3": f'{piece_length_json["hd"][0]}'})
        if "fullHd" in piece_length_json.keys():
            resolution_option.update({"4": "1080p"})
            quality_prefix.update({"4": "whw"})
            piece_length.update({"4": f'{piece_length_json["fullHd"][0]}'})

        max_quality = "4"
        quality = max([i for i in resolution_option if i <= max_quality])

        atob_domain, atob_id = [
            json.loads(
                base64.b64decode(
                    re.search(
                        r'PLAYER\(atob\("(.*?)"',
                        response,
                    ).group(1)
                )
            )[i]
            for i in ["domain", "id"]
        ]

        api_call = f"https://{atob_domain}/{quality_prefix[quality]}{atob_id}"

        if api_call:
            dialog().VSinfo('سيأخذ تشغيل الفيديو بعض الوقت', 'جاري التحميل', 4)
            return True, api_call + '|User-Agent=' + UA + '&Referer=' + sHost
        
        return False, False
