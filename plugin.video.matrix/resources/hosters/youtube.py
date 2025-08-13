# -*- coding: utf-8 -*-
import re, requests
import xbmcaddon
from resources.hosters.hoster import iHoster
from resources.lib.comaddon import VSlog, dialog, addon

UA = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
'Chrome/98.0.4758.141 YaBrowser/22.3.3.852 Yowser/2.5 Safari/537.36'

class cHoster(iHoster):

    def __init__(self):
        iHoster.__init__(self, 'youtube', 'Youtube')

    def _getMediaLinkForGuest(self, autoPlay = False):

        sMode = addon().getSetting('youtube')

        api_call = ''

        if (sMode == '1'):
            video_id = self.__getIdFromUrl(self._url)
            headers = {
                'authority': 'downloader.freemake.com',
                'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="98", "Yandex";v="22"',
                'dnt': '1',
                'x-cf-country': 'RU',
                'sec-ch-ua-mobile': '?0',
                'x-user-platform': 'Win32',
                'accept': 'application/json, text/javascript, */*; q=0.01',
                'x-user-browser': 'YaBrowser',
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                            'Chrome/98.0.4758.141 YaBrowser/22.3.3.852 Yowser/2.5 Safari/537.36',
                'x-analytics-header': 'UA-18256617-1',
                'x-request-attempt': '1',
                'x-user-id': '94119398-e27a-3e13-be17-bbe7fbc25874',
                'sec-ch-ua-platform': '"Windows"',
                'origin': 'https://www.freemake.com',
                'sec-fetch-site': 'same-site',
                'sec-fetch-mode': 'cors',
                'sec-fetch-dest': 'empty',
                'referer': 'https://www.freemake.com/ru/free_video_downloader/',
                'accept-language': 'ru,en;q=0.9,uk;q=0.8',
            }

            sHtmlContent = requests.get(f'https://downloader.freemake.com/api/videoinfo/{video_id}', headers=headers).json()

            qualities = sHtmlContent.get('qualities', [])
            sLink = []
            sQual = []
            for quality in qualities:
                url = quality.get('url')
                qual = quality.get('qualityInfo').get('qualityLabel')

                sLink.append(str(url))
                sQual.append(str(qual))
            api_call = dialog().VSselectqual(sQual, sLink)
            if 'freemake.com' in api_call:
                return True, api_call 
            else:
                return True, f'https://redirector-cf.freemake.com/download/{api_call}'  
      
        try:
            if (sMode == '0'):
                xbmcaddon.Addon('plugin.video.youtube')
        except:
            VSlog('Plugin YouTube not installed')
            return False, False

        if 'plugin'  in self._url:
            api_call = self._url
        else:
            videoID = self.__getIdFromUrl(self._url)
            api_call = 'plugin://plugin.video.youtube/play/?video_id=' + videoID

        if api_call:
            return True, api_call
        else:
            return False, False

    def __getIdFromUrl(self, sUrl):
        if 'plugin' not in sUrl:
            isYouTubeUrl = re.compile( r'^(?:(?:https?:)?\/\/)?(?:(?:(?:www|m(?:usic)?)\.)?youtu(?:\.be|be\.com)\/(?:shorts\/|live\/|v\/|e(?:mbed)?\/|watch(?:\/|\?(?:\S+=\S+&)*v=)|oembed\?url=https?%3A\/\/(?:www|m(?:usic)?)\.youtube\.com\/watch\?(?:\S+=\S+&)*v%3D|attribution_link\?(?:\S+=\S+&)*u=(?:\/|%2F)watch(?:\?|%3F)v(?:=|%3D))?|www\.youtube-nocookie\.com\/embed\/)(([\w-]{11}))[\?&#]?\S*$' )
            match = isYouTubeUrl.match(sUrl)
            return match.group(2) if match else None
        else:
            return sUrl
