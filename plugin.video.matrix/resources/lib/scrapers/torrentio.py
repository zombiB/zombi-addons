# -*- coding: utf-8 -*-
import re
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
        sUrl = f'https://torrentio.strem.fun/stream/movie/{imdb_id}.json'

    elif sType == 'tv':
        sUrl = f'https://torrentio.strem.fun/stream/movie/{imdb_id}%3A{sSeason}%3A{sEpisode}.json'
     
    if 1:
        oRequest = cRequestHandler(sUrl)
        oRequest.addHeaderEntry('User-Agent', UA)
        oRequest.addHeaderEntry('Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8')
        oRequest.addHeaderEntry('Accept-Language', 'en-US,en;q=0.5')
        oRequest.addHeaderEntry('Connection', 'keep-alive')
        oRequest.addHeaderEntry('Upgrade-Insecure-Requests', '1')
        data = oRequest.request(jsonDecode=True)

        for aEntry in data['streams']:            
            if sStop == 1:
                break
            
            sName = aEntry['title']
            sPattern = '💾(.+?)⚙️'

            aResult = re.compile(sPattern).findall(sName)
            sSize = 0
            if len(aResult) > 0:
                sSize = float(aResult[0].replace('GB','').replace('MB','').replace(",",'').strip())
                if 'MB' in str(aResult[0]):
                   sSize = sSize/1000
            
            sLinks = aEntry['infoHash']
            sLink = f'magnet:?xt=urn:btih:{sLinks}&dn={QuotePlus(sTitle)}'

            sRes = {    '4k': '2160p',
                        '2160': '2160p',
                        '1080': '1080p',
                        '720': '720p',
                        '480': '480p',
                        '360': '360p'}

            sQual = next((sRes[key] for key in sRes if key in sName), 'HD')

            max_size = int(addons.getSetting('scrapers_size_limit'))
            
            try:
                sName = re.split(r"👤", sName)[0].strip()
            except:
                continue

            if (sSize) < max_size:
                sMagnetUrls.append((sName, sLink, str(f'{sSize :.2f}'), sQual))

    return sMagnetUrls