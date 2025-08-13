# -*- coding: utf-8 -*-
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.comaddon import VSlog, addon
from resources.lib.util import QuotePlus
from resources.lib import random_ua

UA = random_ua.get_phone_ua()

def get_links(sType, imdb_id, sTitle, sSeason, sEpisode):
    addons = addon()

    sMagnetUrls = []

    if sType == 'movie':
        sUrl = f'https://yrkde.link/movie/{imdb_id}'

    else:
        sUrl = f'https://yrkde.link/show/{imdb_id}'
        
    oRequest = cRequestHandler(sUrl)
    oRequest.addHeaderEntry('User-Agent', UA)
    oRequest.addHeaderEntry('Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8')
    oRequest.addHeaderEntry('Accept-Language', 'en-US,en;q=0.5')
    oRequest.addHeaderEntry('Connection', 'keep-alive')
    oRequest.addHeaderEntry('Upgrade-Insecure-Requests', '1')
    data = oRequest.request(jsonDecode=True)       

    if 'episodes' in data:
        episodes_data = data.get('episodes')

        for episode in episodes_data:
            for torrent in episode['torrents'].values():
                sMagnetUrls.append((torrent['title'],torrent['url'],str(torrent.get('filesize', 'Unknown')),torrent['quality']))
                
        else:
            VSlog(f"No torrents found")

    else:
        for language, language_data in data["torrents"].items():
            for resolution, torrent_details in language_data.items():      
            
                sMagnetUrls.append((torrent_details['title'],torrent_details['url'],str(torrent_details.get('filesize', 'Unknown')),resolution))
           
    return sMagnetUrls

