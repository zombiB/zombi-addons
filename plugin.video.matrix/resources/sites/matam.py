# -*- coding: utf-8 -*-

import time, base64
from resources.lib.gui.hoster import cHosterGui
from resources.lib.gui.gui import cGui
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.comaddon import progress, VSlog, siteManager
from resources.lib.parser import cParser
 
SITE_IDENTIFIER = 'matam'
SITE_NAME = 'Matam TV'
SITE_DESC = 'arabic vod'
 
URL_MAIN = siteManager().getUrlMain(SITE_IDENTIFIER)

ISLAM_SHOWS = (URL_MAIN, 'showSeries')

def load():
    oGui = cGui()

    oOutputParameterHandler = cOutputParameterHandler()
	
    oOutputParameterHandler.addParameter('siteUrl', ISLAM_SHOWS[0])
    oGui.addDir(SITE_IDENTIFIER, 'showSeries', 'دروس و محاضرات', '1/Programs.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()

def showSeries():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')

    current_time = time.time()
    current_time_milliseconds = int(current_time * 1000)
    new_timestamp = current_time_milliseconds + 1000 * 1000 

    oRequestHandler = cRequestHandler(f'{sUrl}json.php?page=json-all-channels&_={new_timestamp}')

    data = oRequestHandler.request(jsonDecode=True)
    oOutputParameterHandler = cOutputParameterHandler()
    filtered_channels = [channel for channel in data["data"] if channel['ls'] == '1']
    filtered_channels.extend([channel for channel in data["data"] if channel['ls'] != '1'])
    for channel in filtered_channels:

            siteUrl = f'{URL_MAIN}{channel["cn"]}'
            sTitle = base64.b64decode(channel["ct"]).decode("utf-8")
            if channel['ls'] == '1':
                 sTitle =  f'[COLOR red]مباشر - [/COLOR]{sTitle}'
            sDesc = base64.b64decode(channel["lt"]).decode("utf-8")
            sThumb = ''

            oOutputParameterHandler.addParameter('siteUrl',siteUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oOutputParameterHandler.addParameter('sDesc', sDesc)

            oGui.addMisc(SITE_IDENTIFIER, 'showLinks', sTitle, 'sites/matam.png', '', sDesc, oOutputParameterHandler)

    oGui.setEndOfDirectory()

def showLinks():
    oGui = cGui()

    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')

    oParser = cParser()
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
          
    sPattern = "yt_vid = '([^']+)"
    aResult = oParser.parse(sHtmlContent, sPattern)
    if aResult[0]:
        for aEntry in aResult[1]:           
            sHosterUrl = f"https://www.youtube.com/embed/{aEntry}"

            oHoster = cHosterGui().checkHoster(sHosterUrl)
            if oHoster:
                oHoster.setDisplayName(sMovieTitle)
                oHoster.setFileName(sMovieTitle)
                cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb)
		               
    oGui.setEndOfDirectory()

