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
        sUrl = f'https://yts.mx/api/v2/list_movies.json?query_term={imdb_id}&page=1&limit=300&order_by=desc&sort_by=rating'

    else:
        return []
     
    if 1:
        oRequest = cRequestHandler(sUrl)
        oRequest.addHeaderEntry('User-Agent', UA)
        oRequest.addHeaderEntry('Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8')
        oRequest.addHeaderEntry('Accept-Language', 'en-US,en;q=0.5')
        oRequest.addHeaderEntry('Connection', 'keep-alive')
        oRequest.addHeaderEntry('Upgrade-Insecure-Requests', '1')
        data = oRequest.request(jsonDecode=True)

        for aEntry in data['data']['movies']:
            sName = aEntry['slug'].replace('-',' ')
            for aResult in aEntry['torrents']:
                sLink = aResult['url']
                
                sSize = aResult['size']
                sQual = aResult['quality']
            
                try:                 
                    sSize = float(sSize.replace('GB','').replace('MB','').replace(",",'').strip())
                    if 'MB' in sSize:
                        sSize = sSize/1000
                except:
                    VSlog('Failed to get size')
                
                max_size = int(addons.getSetting('scrapers_size_limit'))
                
                if (sSize) < max_size:
                    sMagnetUrls.append((sName, sLink, str(sSize), sQual))

    return sMagnetUrls