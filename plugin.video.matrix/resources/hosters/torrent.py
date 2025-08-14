# -*- coding: utf-8 -*-

from resources.hosters.hoster import iHoster
from resources.lib.comaddon import VSlog, VSPath
from resources.lib.handler.requestHandler import cRequestHandler
import xbmcaddon

class cHoster(iHoster):

    def __init__(self):
        iHoster.__init__(self, 'torrent', 'Torrent')

    def _getMediaLinkForGuest(self, autoPlay = False):

        api_call = ''
        try:
            xbmcaddon.Addon('plugin.video.torrest')
        except:
            VSlog('Plugin Torrest Not Installed')
            return False

        if 'magnet' in self._url:
            oRequestHandler = cRequestHandler("https://newtrackon.com/api/all")
            tList = oRequestHandler.request()
            trackers = [line.strip() for line in tList.strip().split('\n') if line.strip()]
            trackers2 = [
                        "udp://tracker.coppersurfer.tk:6969/announce",
                        "udp://9.rarbg.to:2920/announce",
                        "udp://tracker.opentrackr.org:1337",
                        "udp://tracker.internetwarriors.net:1337/announce",
                        "udp://tracker.leechers-paradise.org:6969/announce",
                        "udp://tracker.coppersurfer.tk:6969/announce",
                        "udp://tracker.pirateparty.gr:6969/announce",
                        "udp://tracker.cyberia.is:6969/announce",
                        "udp://tracker.openbittorrent.com:6969/announce",
                        "udp://public.popcorn-tracker.org:6969/announce",
                        "udp://tracker.bittor.pw:1337/announce"
                        ]
            api_call = f'plugin://plugin.video.torrest/play_magnet?magnet={self._url}'+ "&tr=" + "&tr=".join(trackers) + "&tr=".join(trackers2)
        
        else:
            if 'ttmxtt' in self._url:
                videoID = self.__getIdFromUrl(self._url)
                api_call = f'plugin://plugin.video.torrest/play_url?url={videoID}'
            
            else:
                import requests

                local_file_path = VSPath('special://home/addons/plugin.video.matrix/resources/extra/v.torrent')
                headers = {
                    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
                    "Accept-Language": "en-US,en;q=0.9",
                    "Connection": "keep-alive",
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36 Edg/134.0.0.0"
                }
                response = requests.get(self._url, headers=headers)
                
                with open(local_file_path, "wb") as file:
                    for chunk in response.iter_content(chunk_size=8192):
                        file.write(chunk)
                api_call = f'plugin://plugin.video.torrest/play_path?path={local_file_path}'
            
        if api_call:
            return True, api_call
        
        return False, False

    def __getIdFromUrl(self, sUrl):
        id = sUrl.replace('ttmxtt','')
        return id
