# -*- coding: utf-8 -*-

import re
from resources.lib.gui.hoster import cHosterGui
from resources.lib.gui.gui import cGui
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.comaddon import VSlog, siteManager, addon
from resources.lib.parser import cParser
from resources.lib import random_ua

UA = random_ua.get_ua()

SITE_IDENTIFIER = 'shoofmax'
SITE_NAME = 'ShoofMAX'
SITE_DESC = 'arabic vod'
 
URL_MAIN = siteManager().getUrlMain(SITE_IDENTIFIER)

MOVIE_AR = (f'{URL_MAIN}genre/filter/فيلم/1/yop?country=&subgenre=', 'showMovies')
SERIE_AR = (f'{URL_MAIN}genre/filter/مسلسل/1/yop?country=&subgenre=', 'showSeries')

URL_SEARCH = (f'{URL_MAIN}search?q=', 'showSearchResults')
URL_SEARCH_MOVIES = (f'{URL_MAIN}search?q=', 'showSearchResults')
URL_SEARCH_SERIES = (f'{URL_MAIN}search?q=', 'showSearchResults')
FUNCTION_SEARCH = 'showSearchResults'

def load():
    oGui = cGui()
    addons = addon()

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'http://venom/')
    oGui.addDir(SITE_IDENTIFIER, 'showSearch', addons.VSlang(30078), '1/Search.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', 'http://venom/')
    oGui.addDir(SITE_IDENTIFIER, 'showSearchSeries', addons.VSlang(30079), '1/Search.png', oOutputParameterHandler)
	
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_AR[0])
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'أفلام عربية', '1/Arabic.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', SERIE_AR[0])
    oGui.addDir(SITE_IDENTIFIER, 'showSeries', 'مسلسلات عربية', '1/Arabic.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()
 
def showSearch():
    oGui = cGui()
 
    sSearchText = oGui.showKeyBoard()
    if sSearchText is not False:
        sUrl = f'{URL_MAIN}search?q={sSearchText}'
        showSearchResults(sUrl)
        oGui.setEndOfDirectory()
        return
 
def showSearchSeries():
    oGui = cGui()
 
    sSearchText = oGui.showKeyBoard()
    if sSearchText is not False:
        sUrl = f'{URL_MAIN}search?q={sSearchText}'
        showSearchResults(sUrl)
        oGui.setEndOfDirectory()
        return

def showSearchResults(sSearch = ''):
    oGui = cGui()

    if sSearch:
        sUrl = sSearch
    else:   
        oInputParameterHandler = cInputParameterHandler()
        sUrl = oInputParameterHandler.getValue('siteUrl')

    oParser = cParser()
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    sStart = '<div class="general-body">'
    sEnd = '<script type='
    sHtmlContent = oParser.abParse(sHtmlContent, sStart, sEnd)

    sPattern = '<a href="([^<]+)".+?style="background-image: url\((.+?)\)".+?<span>(.+?)</span>'
    aResult = oParser.parse(sHtmlContent, sPattern)
    if aResult[0]:
        oOutputParameterHandler = cOutputParameterHandler()
        for aEntry in aResult[1]:

            sTitle = aEntry[2]
            siteUrl = f'{URL_MAIN.rstrip("/")}{aEntry[0]}'
            sDesc = ''
            sThumb = aEntry[1]
            sYear = ''
            
            oOutputParameterHandler.addParameter('siteUrl', siteUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('pTitle', re.sub(r"-?\d+\.jpg", "", sThumb.split("/")[-1]))
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oOutputParameterHandler.addParameter('sYear', sYear)
            oOutputParameterHandler.addParameter('sDesc', sDesc)

            if '?ep=' in siteUrl:
                oGui.addTV(SITE_IDENTIFIER, 'showEpisodes', sTitle, '', sThumb, sDesc, oOutputParameterHandler)
            else:
                oGui.addMovie(SITE_IDENTIFIER, 'showHosters', sTitle, '', sThumb, sDesc, oOutputParameterHandler)
        
    if not sSearch:
        oGui.setEndOfDirectory()

def showMovies(sSearch = ''):
    oGui = cGui()

    if sSearch:
      sUrl = sSearch
    else:   
      oInputParameterHandler = cInputParameterHandler()
      sUrl = oInputParameterHandler.getValue('siteUrl')
      sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
      sThumb = oInputParameterHandler.getValue('sThumb')
 
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request(jsonDecode=True)
    
    if sHtmlContent:
        oOutputParameterHandler = cOutputParameterHandler()
        for aEntry in sHtmlContent:            
            sTitle = aEntry['ptitle']
            siteUrl = f"{URL_MAIN}program/{aEntry['pid']}"
            sThumb = f"https://shoofmax-static.b-cdn.net/v2/img/program/main/{aEntry['presbase']}-2.jpg"
            sDesc = ''
            sYear = ''
            m = re.search('([0-9]{4})', sTitle)
            if m:
                sYear = str(m.group(0))

            oOutputParameterHandler.addParameter('siteUrl', siteUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('pTitle', aEntry['presbase'])
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oOutputParameterHandler.addParameter('sYear', sYear)
            oOutputParameterHandler.addParameter('sDesc', sDesc)

            oGui.addMovie(SITE_IDENTIFIER, 'showLinks', sTitle, '', sThumb, sDesc, oOutputParameterHandler)
    
    if not sSearch:
        parts = sUrl.split("/")
        parts[6] = str(int(parts[6]) + 1)
        sNextPage = "/".join(parts)

        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', sNextPage)
        oGui.addDir(SITE_IDENTIFIER, 'showMovies', '[COLOR teal]Next >>>[/COLOR]', 'next.png', oOutputParameterHandler)
 
    oGui.setEndOfDirectory()

def showSeries(sSearch = ''):
    oGui = cGui()

    if sSearch:
      sUrl = sSearch
    else:   
      oInputParameterHandler = cInputParameterHandler()
      sUrl = oInputParameterHandler.getValue('siteUrl')
      sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
      sThumb = oInputParameterHandler.getValue('sThumb')
 
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request(jsonDecode=True)
    
    if sHtmlContent:
        oOutputParameterHandler = cOutputParameterHandler()
        for aEntry in sHtmlContent:            
            sTitle = aEntry['ptitle']
            siteUrl = f"{URL_MAIN}program/{aEntry['pid']}?ep=1"
            sThumb = f"https://shoofmax-static.b-cdn.net/v2/img/program/main/{aEntry['presbase']}-2.jpg"
            sEpisodes = aEntry['pepisodes']
            sDesc = ''
            sYear = ''
            m = re.search('([0-9]{4})', sTitle)
            if m:
                sYear = str(m.group(0))

            oOutputParameterHandler.addParameter('siteUrl', siteUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('pTitle', aEntry['presbase'])
            oOutputParameterHandler.addParameter('sEpisodes', sEpisodes)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oOutputParameterHandler.addParameter('sYear', sYear)
            oOutputParameterHandler.addParameter('sDesc', sDesc)
			
            oGui.addTV(SITE_IDENTIFIER, 'showEpisodes', sTitle, '', sThumb, sDesc, oOutputParameterHandler)

    if not sSearch:
        parts = sUrl.split("/")
        parts[6] = str(int(parts[6]) + 1)
        sNextPage = "/".join(parts)

        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', sNextPage)
        oGui.addDir(SITE_IDENTIFIER, 'showSeries', '[COLOR teal]Next >>>[/COLOR]', 'next.png', oOutputParameterHandler)
    
    oGui.setEndOfDirectory()

def showEpisodes():
    oGui = cGui()
    
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sEpisodes = oInputParameterHandler.getValue('sEpisodes')
    pTitle = oInputParameterHandler.getValue('pTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')

    oParser = cParser() 
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    sPattern = '</select>(.+?)<a class='	
    aResult = oParser.parse(sHtmlContent, sPattern)
    if aResult[0]:
        tEpisodes = re.findall(r'\d+', aResult[1][0])
        sEpisodes = int(tEpisodes[0])

    sUrl = f"{sUrl.split('?ep=')[0]}?ep="

    sEpiList = [f"{sUrl}{episode_number}" for episode_number in range(1, int(sEpisodes) +1)]

    oOutputParameterHandler = cOutputParameterHandler()
    for aEntry in sEpiList:
    
        sTitle = f'{sMovieTitle} E{aEntry.split("?ep=")[1]}'
        siteUrl = aEntry
        sThumb = sThumb
        sDesc = ""
			
        oOutputParameterHandler.addParameter('siteUrl', siteUrl)
        oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
        oOutputParameterHandler.addParameter('pTitle', pTitle)
        oOutputParameterHandler.addParameter('sThumb', sThumb)
        oGui.addEpisode(SITE_IDENTIFIER, 'showLinks', sTitle, '', sThumb, sDesc, oOutputParameterHandler)
 
      
    oGui.setEndOfDirectory()
 
def showLinks():
    oGui = cGui()

    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    pTitle = oInputParameterHandler.getValue('pTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')

    oParser = cParser()
    oRequestHandler = cRequestHandler(sUrl)
    oRequestHandler.addHeaderEntry('User-Agent', UA)
    oRequestHandler.addHeaderEntry('Referer', sUrl)
    sHtmlContent = oRequestHandler.request()

    sPattern = 'origin_link = "([^"]+)'	
    aResult = oParser.parse(sHtmlContent, sPattern)
    if aResult[0]:
        HLS_MAIN = aResult[1][0]

    sPattern = "rendition = '([^']+)"
    aResult = oParser.parse(sHtmlContent, sPattern)
    if aResult[0]:
        for aEntry in aResult[1]: 
            if '?ep=' in sUrl:
                sEp = f'{sUrl.split("?ep=")[1]}' 
                sHosterUrl = f'{HLS_MAIN}/{pTitle}/ep{sEp}/{aEntry}/index.m3u8'
            else:
                sHosterUrl = f'{HLS_MAIN}/{pTitle}/{aEntry}/index.m3u8'
            
            oHoster = cHosterGui().checkHoster(sHosterUrl)
            sDisplayTitle = f'{sMovieTitle} ({aEntry})'
            if oHoster:
                oHoster.setDisplayName(sDisplayTitle)
                oHoster.setFileName(sMovieTitle)
                cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb)

    oGui.setEndOfDirectory()