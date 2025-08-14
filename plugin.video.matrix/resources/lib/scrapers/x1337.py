# -*- coding: utf-8 -*-
import re
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.comaddon import VSlog, addon
from resources.lib.parser import cParser
from resources.lib.util import QuotePlus
from resources.lib import random_ua

UA = random_ua.get_phone_ua()

sStop = 0

def get_links(sType, imdb_id, sTitle, sSeason, sEpisode):

    sMagnetUrls = []
   
    if sType == 'movie':
        sUrl = f'https://1337x.to/category-search/{sTitle}/Movies/1/'

    elif sType == 'tv':
        sUrl = f'https://1337x.to/category-search/{sTitle} S{str(sSeason).zfill(2)}E{str(sEpisode).zfill(2)}/TV/1/'
     
    if 1:
        oRequest = cRequestHandler(sUrl)
        oRequest.addHeaderEntry('User-Agent', UA)
        oRequest.addHeaderEntry('Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8')
        oRequest.addHeaderEntry('Accept-Language', 'en-US,en;q=0.5')
        oRequest.addHeaderEntry('Connection', 'keep-alive')
        oRequest.addHeaderEntry('Upgrade-Insecure-Requests', '1')
        sHtmlContent = oRequest.request()

        data = sHtmlContent.split('<tbody>')[1].split('</tbody>')[0]

        oParser = cParser()
        sPattern = '</a><a\s*href="([^"]+)">(.+?)</a>.+?size.+?>(.+?)<span'
        aResult = oParser.parse(data, sPattern)
        if aResult[0]:  
            for aEntry in aResult[1]:
   
                sName = aEntry[1]
                sLink = f"https://1337x.to{aEntry[0]}"
                sSize = aEntry[2]
            
                sMagnetUrls.append((sName, sLink, sSize))

    return sMagnetUrls