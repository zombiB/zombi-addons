# -*- coding: utf-8 -*-
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.comaddon import VSlog, addon
from resources.lib.util import QuotePlus
from resources.lib import random_ua

UA = random_ua.get_phone_ua()

sStop = 0

def get_links(sType, imdb_id, sTitle, sSeason, sEpisode):
    addons = addon()

    sMagnetUrls = []
      
    if sType == 'movie':
        search_url = [f"{sTitle.replace(' ','%20').lower()}&cat=207,202,201"]

    elif sType == 'tv':
        search_url = [f"{sTitle.replace(' ','%20').lower()}&cat=208,205"]

    for aEntry in search_url:
        sUrl = f'https://apibay.org/q.php?q={aEntry}'
        oRequest = cRequestHandler(sUrl)
        oRequest.addHeaderEntry('User-Agent', UA)
        oRequest.addHeaderEntry('Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8')
        oRequest.addHeaderEntry('Accept-Language', 'en-US,en;q=0.5')
        oRequest.addHeaderEntry('Connection', 'keep-alive')
        oRequest.addHeaderEntry('Upgrade-Insecure-Requests', '1')
        data = oRequest.request(jsonDecode=True)       
  
        for aResults in data:
            
            if sStop == 1:
                break

            sName = aResults['name']
            sSize = (float(aResults['size'])/(1024*1024*1024))
            sPeer = aResults['leechers']
            sSeed = aResults['seeders']
            
            sLink = f"magnet:?xt=urn:btih:{aResults['info_hash']}&dn={QuotePlus(sName)}"

            sRes = {    '4k': '2160p',
                        '2160': '2160p',
                        '1080': '1080p',
                        '720': '720p',
                        '480': '480p',
                        '360': '360p'}
                      
            sQual = next((sRes[key] for key in sRes if key in sName), 'HD')

            max_size = int(addons.getSetting('scrapers_size_limit'))
            
            if (sSize) < max_size:
                sMagnetUrls.append((sName, sLink, str(f'{sSize :.2f} GB'), sQual))

    return sMagnetUrls

