# -*- coding: utf-8 -*-
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.comaddon import VSlog, addon
from resources.lib.util import QuotePlus
from resources.lib import random_ua

UA = random_ua.get_phone_ua()

def get_links(sType, imdb_id, sTitle, sSeason, sEpisode):
    addons = addon()
   
    if sType == 'movie':
        return []

    else:
        torrents = ''
        for pages in range(0,5):
            sUrl = 'https://eztv.yt/api/get-torrents?imdb_id=%s&limit=100&page=%s'%(imdb_id.replace('tt',''),str(pages))

            try:
                oRequest = cRequestHandler(sUrl)
                oRequest.addHeaderEntry('User-Agent', UA)
                oRequest.addHeaderEntry('Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8')
                oRequest.addHeaderEntry('Accept-Language', 'en-US,en;q=0.5')
                oRequest.addHeaderEntry('Connection', 'keep-alive')
                oRequest.addHeaderEntry('Upgrade-Insecure-Requests', '1')
                data = oRequest.request()
            
                if 'torrents' in data:
                    torrents = torrents + data
            except:
                VSlog('Failed')

        if torrents:
                sMagnetUrls = []
                from resources.lib.parser import cParser
                oParser = cParser()
                sPattern = '"filename":"([^"]+)","torrent_url":"([^"]+)".+?"size_bytes":"([^"]+)"'
                aResult = oParser.parse(torrents, sPattern) 
                if aResult[0]:
                    for aEntry in aResult[1]:

                        sLink = aEntry[1]
                        sName = aEntry[0]
                        sSize = aEntry[2]

                        sRes = {    '4k': '2160p',
                                    '2160': '2160p',
                                    '1080': '1080p',
                                    '720': '720p',
                                    '480': '480p',
                                    '360': '360p'}

                        sQual = next((sRes[key] for key in sRes if key in sName), 'HD')

                        try:                 
                            sSize=(float(sSize)/(1024*1024*1024))
                        except:
                            VSlog('Failed to get size')
                        
                        max_size = int(addons.getSetting('scrapers_size_limit'))
                        
                        if (sSize) < max_size:
                            sMagnetUrls.append((sName, sLink, str(f'{sSize :.2f} GB'), sQual))

    return sMagnetUrls