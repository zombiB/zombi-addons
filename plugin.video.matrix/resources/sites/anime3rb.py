# -*- coding: utf-8 -*-

import re, json
from resources.lib.gui.hoster import cHosterGui
from resources.lib.gui.gui import cGui
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.comaddon import VSlog, siteManager, addon
from resources.lib.util import cUtil
from resources.lib.parser import cParser
 
SITE_IDENTIFIER = 'anime3rb'
SITE_NAME = 'Anime3rb'
SITE_DESC = 'arabic vod'

URL_MAIN = siteManager().getUrlMain(SITE_IDENTIFIER)
    
ANIM_NEWS = (f'{URL_MAIN}titles/list/tv', 'showSeries')
ANIM_MOVIES = (f'{URL_MAIN}titles/list/movie', 'showMovies')

URL_SEARCH_ANIMS = (f'{URL_MAIN}search?q=', 'showSeries')
FUNCTION_SEARCH = 'showSeries'
 
def load():
    oGui = cGui()
    addons = addon()

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'http://venom/')
    oGui.addDir(SITE_IDENTIFIER, 'showSearch', addons.VSlang(30118), '1/Search.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', ANIM_NEWS[0])
    oGui.addDir(SITE_IDENTIFIER, 'showSeries', 'مسلسلات انمي', '1/Anime.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', ANIM_MOVIES[0])
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'أفلام انمي', '1/Anime.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', f'{URL_MAIN}titles/list/special')
    oGui.addDir(SITE_IDENTIFIER, 'showSeries', 'قائمة الحلقات خاصة', '1/Anime.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', f'{URL_MAIN}titles/list/ova')
    oGui.addDir(SITE_IDENTIFIER, 'showSeries', 'قائمة الأوفا', '1/Anime.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', f'{URL_MAIN}titles/list/ona')
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'قائمة الأونا', '1/Anime.png', oOutputParameterHandler)
            
    oGui.setEndOfDirectory()
 
def showSearch():
    oGui = cGui()
 
    sSearchText = oGui.showKeyBoard()
    if sSearchText:
        sUrl = f'{URL_MAIN}search?q={sSearchText}'
        showSeries(sUrl)
        oGui.setEndOfDirectory()
        return

def showMovies(sSearch = ''):
    oGui = cGui()
    if sSearch:
      sUrl = sSearch
    else:
        oInputParameterHandler = cInputParameterHandler()
        sUrl = oInputParameterHandler.getValue('siteUrl')

    oRequestHandler = cRequestHandler(sUrl)
    oRequestHandler.addHeaderEntry('Referer', URL_MAIN)
    sHtmlContent = oRequestHandler.request()

    json_data = re.search(r'<script type="application/ld\+json">(.*?)</script>', sHtmlContent, re.DOTALL).group(1)
    sHtmlContent = json.loads(json_data)

    anime_list = sHtmlContent["itemListElement"]
    oOutputParameterHandler = cOutputParameterHandler()
    for anime in anime_list:
        sTitle = (anime["item"]["name"]).split('- Anime')[0]
        sThumb = anime["item"]["image"]
        siteUrl = anime["item"]["url"]
 
        sDesc = anime["item"]["description"]
        sYear = ''

        oOutputParameterHandler.addParameter('siteUrl',siteUrl)
        oOutputParameterHandler.addParameter('sMovieTitle',sTitle)
        oOutputParameterHandler.addParameter('sThumb', sThumb)
        oOutputParameterHandler.addParameter('sDesc', sDesc)
        oOutputParameterHandler.addParameter('sYear', sYear)

        oGui.addAnime(SITE_IDENTIFIER, 'showEpisodes', sTitle, '', sThumb, sDesc, oOutputParameterHandler)

    if not sSearch:
        sNextPage = __checkForNextPage(sHtmlContent)
        if sNextPage:
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

    oRequestHandler = cRequestHandler(sUrl)
    oRequestHandler.addHeaderEntry('Referer', URL_MAIN)
    sHtmlContent = oRequestHandler.request()

    json_data = re.search(r'<script type="application/ld\+json">(.*?)</script>', sHtmlContent, re.DOTALL).group(1)
    sHtmlContent = json.loads(json_data)

    anime_list = sHtmlContent["itemListElement"]
    oOutputParameterHandler = cOutputParameterHandler()
    for anime in anime_list:
        
        sTitle = (anime["item"]["name"]).split('- Anime')[0]
        sTitle = cUtil().ConvertSeasons(sTitle)
        sThumb = anime["item"]["image"]
        siteUrl = anime["item"]["url"]
        sDesc = anime["item"]["description"]
        sYear = ''

        oOutputParameterHandler.addParameter('siteUrl',siteUrl)
        oOutputParameterHandler.addParameter('sMovieTitle',sTitle)
        oOutputParameterHandler.addParameter('sThumb', sThumb)
        oOutputParameterHandler.addParameter('sDesc', sDesc)
        oOutputParameterHandler.addParameter('sYear', sYear)
        
        oGui.addAnime(SITE_IDENTIFIER, 'showEpisodes', sTitle, '', sThumb, sDesc, oOutputParameterHandler)
 
    if not sSearch:
        sNextPage = __checkForNextPage(sHtmlContent)
        if sNextPage:
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sNextPage)
            oGui.addDir(SITE_IDENTIFIER, 'showSeries', '[COLOR teal]Next >>>[/COLOR]', 'next.png', oOutputParameterHandler)

        oGui.setEndOfDirectory()
 
def showEpisodes():
    oGui = cGui()
   
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')
    sDesc = oInputParameterHandler.getValue('sDesc')

    oParser = cParser()
    oRequestHandler = cRequestHandler(sUrl)
    oRequestHandler.addHeaderEntry('Referer', URL_MAIN)
    sHtmlContent = oRequestHandler.request()

    sStart = '<div class="videos-list'
    sEnd = '<div class="container'
    sHtmlContent = oParser.abParse(sHtmlContent, sStart, sEnd)

    sPattern = 'href="([^"]+)".+?img src="([^"]+)".+?<span>(.+?)</span>'
    aResult = oParser.parse(sHtmlContent, sPattern)
    if aResult[0]:
        for aEntry in aResult[1]:
            oOutputParameterHandler = cOutputParameterHandler()
            sTitle = aEntry[2]
            sTitle = sMovieTitle + ' E' + re.search(r'الحلق[ةه]\s*(\d+)', sTitle).group(1)
            sThumb = aEntry[1]
            siteUrl = aEntry[0]
            sDesc = ''

            oOutputParameterHandler.addParameter('siteUrl',siteUrl)
            oOutputParameterHandler.addParameter('sMovieTitle',sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oOutputParameterHandler.addParameter('sDesc', sDesc)
        
            oGui.addEpisode(SITE_IDENTIFIER, 'showHosters', sTitle, '', sThumb, sDesc, oOutputParameterHandler)
   
    oGui.setEndOfDirectory() 

def __checkForNextPage(sHtmlContent):
    if 'potentialAction' in sHtmlContent and 'target' in sHtmlContent['potentialAction']: 
        return sHtmlContent['potentialAction']['target'][0] 
    return False

def showHosters():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')

    oRequestHandler = cRequestHandler(sUrl)
    oRequestHandler.addHeaderEntry('Referer', URL_MAIN)
    sHtmlContent = oRequestHandler.request()

    json_data = re.search(r'<script type="application/ld\+json">(.*?)</script>', sHtmlContent, re.DOTALL).group(1)
    VideoContent = json.loads(json_data)

    embed_list = VideoContent["video"]
    for anime in embed_list:
        url = anime["embedUrl"]
        sThumb = anime["thumbnailUrl"]    

        sHosterUrl = url 

        oHoster = cHosterGui().checkHoster(sHosterUrl)
        if oHoster:
            oHoster.setDisplayName(sMovieTitle)
            oHoster.setFileName(sMovieTitle)
            cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb)
            
    oGui.setEndOfDirectory()
