# -*- coding: utf-8 -*-
# zombi https://github.com/zombiB/zombi-addons/

import re
	
from resources.lib.gui.hoster import cHosterGui
from resources.lib.gui.gui import cGui
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.lib.comaddon import progress,VSlog, siteManager, dialog, addon
from resources.lib.util import cUtil, Unquote, urlEncode, Quote
from resources.lib.Styling import getFunc, getThumb, getGenreIcon
import json
import requests
from resources.lib.SQLiteCache import SqliteCache
db = SqliteCache()

try:  # Python 2
    import urllib2
    from urllib2 import URLError as UrlError

except ImportError:  # Python 3
    import urllib.request as urllib2
    from urllib.error import URLError as UrlError

ADDON = addon()
icons = ADDON.getSetting('defaultIcons')

SITE_IDENTIFIER = 'MatrixTV'
SITE_NAME = 'MatrixTV'
SITE_DESC = 'Live IPTV Channels'

URL_MAIN = siteManager().getUrlMain(SITE_IDENTIFIER)

TV_GROUPS = ('http://venom/', 'showGroups')

TV_CHANNELS = ('http://venom/', 'showAllChannels')

Streams = 'api/streams.json'
Channels = 'api/channels.json'
Categories = 'api/categories.json'
Languages = 'api/languages.json'
Countries = 'api/countries.json'
Regions = 'api/regions.json'

def getChannels():
    CachedChannels = db.get("MatrixTV")
    if CachedChannels is None:
        ChannelsJSON = requests.get(URL_MAIN + Channels).json()
        StreamsJSON = requests.get(URL_MAIN + Streams).json()
        ChannelsList = []

        for ch in ChannelsJSON:
            if 'ara' in ch['languages']:
                for stream in StreamsJSON:
                    if stream['channel'] ==ch['id']:
                        try: 
                            Cat = ch['categories'][0]
                        except:
                            Cat = 'Undefined'
                        channel = {
                            'name' : ch['name'],
                            'logo' : ch['logo'],
                            'country' : ch['country'],
                            'cat' : Cat,
                            'url' : stream['url'],
                            'referrer' : stream['http_referrer'],
                            'ua' : stream['user_agent']
                            }
                        ChannelsList.append(channel)
    
        forcaching = {"sUrl": "MatrixTV", "val": ChannelsList}
        db.set(forcaching, 7*24*60*60)
        return ChannelsList
    else:
        return CachedChannels

def load():
    oGui = cGui()

    oOutputParameterHandler = cOutputParameterHandler()

    oOutputParameterHandler.addParameter('siteUrl', TV_GROUPS[0])
    oGui.addDir(SITE_IDENTIFIER, TV_GROUPS[1], 'Groups', icons + '/Groups.png', oOutputParameterHandler)
    
    oOutputParameterHandler.addParameter('siteUrl', TV_CHANNELS[0])
    oGui.addDir(SITE_IDENTIFIER, TV_CHANNELS[1], 'All Channels', icons + '/Channels.png', oOutputParameterHandler)
    
    oGui.setEndOfDirectory()

def showGroups():
    oGui = cGui()
    oOutputParameterHandler = cOutputParameterHandler()
    
    ChannelsList = getChannels()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    CatsList = []
    Count = 0
    for aEntry in ChannelsList:
        CatsList.append(aEntry['cat'])
        
    CatsList = list(set(CatsList))
    
    CatsCounter = dict(zip(CatsList, [0]*len(CatsList)))
    
    for Cat in CatsList:
        for Ch in ChannelsList:
            if Ch['cat'] == Cat:
                CatsCounter[Cat] = CatsCounter[Cat] + 1

    for aEntry in CatsList:
        if aEntry not in [None,""," "]:
            sTitle = aEntry.title() + ' (' + str(CatsCounter[aEntry]) + ')'
            oOutputParameterHandler.addParameter('siteUrl',  sUrl) 
            oOutputParameterHandler.addParameter('sTitle',  sTitle) 
            oOutputParameterHandler.addParameter('sTitle2',  aEntry.title()) 
            
            oOutputParameterHandler.addParameter('sThumb',  '') 
            
            oGui.addDir(SITE_IDENTIFIER, 'showChannels', sTitle, getGenreIcon(sTitle), oOutputParameterHandler)
    oGui.setEndOfDirectory()


def showChannels():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    SelectedCat = oInputParameterHandler.getValue('sTitle2')
    
    ChannelsList = getChannels()

    for aEntry in ChannelsList:
      
        if SelectedCat in aEntry['cat'].title():
            
            sHosterUrl = aEntry['url']
   
            if aEntry['referrer'] not in [None, 'none', '']:
                sHosterUrl = sHosterUrl + '|Referrer=' + aEntry['referrer']
     
            if aEntry['ua'] not in [None, 'none', '']:
                sHosterUrl = sHosterUrl + '|User-Agent=' + aEntry['ua']
            
            oHoster = cHosterGui().checkHoster(sHosterUrl)
            
            if oHoster:
                oHoster.setDisplayName(aEntry['name'])
                oHoster.setFileName(SelectedCat)
                cHosterGui().showHoster(oGui, oHoster, sHosterUrl, aEntry['logo'])
            else:
               VSlog("URL ["+sHosterUrl+"] has no hoster resolver")

    oGui.setEndOfDirectory()

def showAllChannels():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    SelectedCat = oInputParameterHandler.getValue('sTitle2')

    ChannelsList = getChannels()

    for aEntry in ChannelsList:

        sHosterUrl = aEntry['url']
        if aEntry['referrer'] not in [None, 'none', '']:
            sHosterUrl = sHosterUrl + '|Referrer=' + aEntry['referrer']
        if aEntry['ua'] not in [None, 'none', '']:
            sHosterUrl = sHosterUrl + '|User-Agent=' + aEntry['ua']
            
        oHoster = cHosterGui().checkHoster(sHosterUrl)
        
        if oHoster:
            oHoster.setDisplayName(aEntry['name'])
            oHoster.setFileName(SelectedCat)
            cHosterGui().showHoster(oGui, oHoster, sHosterUrl, aEntry['logo'])
        else:
           VSlog("URL ["+sHosterUrl+"] has no hoster resolver")

    oGui.setEndOfDirectory()