# -*- coding: utf-8 -*-

import base64, json, time
import urllib.parse
from resources.lib.gui.hoster import cHosterGui
from resources.lib.gui.gui import cGui
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.comaddon import VSlog, siteManager

SITE_IDENTIFIER = 'daily'
SITE_NAME = '[COLOR orange]Daily IPTV List[/COLOR]'
SITE_DESC = 'Watch IPTV Channels'

URL_MAIN = siteManager().getUrlMain(SITE_IDENTIFIER)

dHost = base64.b64decode('ZXJvdHMueXViLXl0ZWlyYXYuMjA1YS8vOnNwdHRo').decode("utf-8")
sKey = base64.b64decode('d3ZAdkVARyY5TitqWnghYw==').decode("utf-8")
sKey = sKey[::-1]

URL_MAIN = dHost[::-1]
URL_WEB = URL_MAIN
TV_TV = (True, 'showDailyList')

def load():
    oGui = cGui()

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', URL_MAIN)
    oGui.addDir(SITE_IDENTIFIER, 'showDailyList', 'Latest list', 'tv.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()

def showDailyList():
    oGui = cGui()

    sHtmlContent = get_categories()
    oOutputParameterHandler = cOutputParameterHandler() 
    for category in sHtmlContent["data"]:

        siteUrl = category["id"]
        sTitle = category["name"]
        sThumb = ''    
        sDesc = ''
        
        oOutputParameterHandler.addParameter('siteUrl',siteUrl)
        oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
        oOutputParameterHandler.addParameter('sThumb', sThumb)

        oGui.addMisc(SITE_IDENTIFIER, 'showCatList', sTitle, 'listes.png', sThumb, sDesc, oOutputParameterHandler)

    oGui.setEndOfDirectory()

def showCatList():
    oGui = cGui()

    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')

    if sUrl == '9':
        sHtmlContent = get_category(sUrl)
        oOutputParameterHandler = cOutputParameterHandler() 
        for category in sHtmlContent["data"]:

            siteUrl = category["id"]
            sTitle = category["name"]
            sThumb = category["logo"]   
            sDesc = ''
            
            oOutputParameterHandler.addParameter('siteUrl',siteUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)

            oGui.addMisc(SITE_IDENTIFIER, 'showCatList', sTitle, 'listes.png', sThumb, sDesc, oOutputParameterHandler)

    sHtmlContent = get_category_channels(sUrl)
    oOutputParameterHandler = cOutputParameterHandler() 
    for channel in sHtmlContent["data"]:

        siteUrl = channel["id"]
        sTitle = channel["name"]
        sThumb = channel["logo"]   
        sDesc = ''
        
        oOutputParameterHandler.addParameter('siteUrl',siteUrl)
        oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
        oOutputParameterHandler.addParameter('sThumb', sThumb)

        oGui.addMisc(SITE_IDENTIFIER, 'showCHLinks', sTitle, 'listes.png', sThumb, sDesc, oOutputParameterHandler)

    oGui.setEndOfDirectory()

def showCHLinks():
    oGui = cGui()

    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')

    sHtmlContent = get_channel(sUrl)
    oOutputParameterHandler = cOutputParameterHandler() 
    for sLinks in sHtmlContent["data"]:

        sHosterUrl = f'{sLinks["url"]}'       
        oHoster = cHosterGui().checkHoster(sHosterUrl)
        sHosterUrl = sHosterUrl 
        if oHoster:
            oHoster.setDisplayName(sMovieTitle)
            oHoster.setFileName(sMovieTitle)
            cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb, oOutputParameterHandler)

    oGui.setEndOfDirectory()

def extract_domain(url):
  parsed_url = urllib.parse.urlparse(url)
  return parsed_url.netloc

def decrypt(enc, key=sKey):
    enc = base64.b64decode(enc.encode("ascii")).decode("ascii")
    result = ""
    for i in range(len(enc)):
      result = result + chr(ord(enc[i]) ^ ord(key[i % len(key)]))
    return result

def req(path):

    oRequestHandler = cRequestHandler(path)
    oRequestHandler.addHeaderEntry('accept', "application/json")
    oRequestHandler.addHeaderEntry('accept-encoding', "gzip")
    oRequestHandler.addHeaderEntry('User-Agent', "okhttp/4.12.0")
    if '/api/channel/' in path:
        oRequestHandler.enableCache(False)
    sHtmlContent = oRequestHandler.request()
    sHeader = oRequestHandler.getResponseHeader()

    timestamp = str(int(time.time()))
    if "t" in sHeader:
      timestamp = sHeader["t"]

    try:
      return json.loads(decrypt(sHtmlContent, key=sKey + timestamp))

    except Exception:
      return {
        "success": False,
        "error": "can't parse json."
      }

def get_categories():
    return req(f"{URL_MAIN}/api/categories")

def get_category(category_id):
    return req(f"{URL_MAIN}/api/categories/{str(category_id)}")

def get_category_channels(category_id):
    return req(f"{URL_MAIN}/api/categories/{str(category_id)}/channels")

def get_channel(channel_id):
    return req(f"{URL_MAIN}/api/channel/{str(channel_id)}")

def get_events():
    return req(f"{URL_MAIN}/api/events")

def get_event(event_id):
    return req(f"{URL_MAIN}/api/event/{str(event_id)}")

def get_config():
    return req(f"{URL_MAIN}/api/config")