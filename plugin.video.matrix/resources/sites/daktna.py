# -*- coding: utf-8 -*-

import re
from resources.lib.gui.hoster import cHosterGui
from resources.lib.gui.gui import cGui
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.comaddon import progress, VSlog, siteManager, addon
from resources.lib.parser import cParser
from resources.lib.util import cUtil
from resources.lib import random_ua

UA = random_ua.get_ua()

SITE_IDENTIFIER = 'daktna'
SITE_NAME = 'Daktna'
SITE_DESC = 'arabic vod'
 
URL_MAIN = siteManager().getUrlMain(SITE_IDENTIFIER)

RAMADAN_SERIES = (f'{URL_MAIN}list/series/', 'showSeries')
SERIE_AR = (f'{URL_MAIN}list/series/', 'showSeries')
SERIE_TR = (f'{URL_MAIN}list/series-turkish/', 'showSeries')

MOVIE_EN = (f'{URL_MAIN}list/movies/', 'showSeries')
MOVIE_AR = (f'{URL_MAIN}list/movies/', 'showSeries')

URL_SEARCH = (f'{URL_MAIN}?s=', 'showSeries')
URL_SEARCH_SERIES = (f'{URL_MAIN}?s=', 'showSeries')
FUNCTION_SEARCH = 'showSeriesSearch'
 
def load():
    oGui = cGui()
    addons = addon()

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'http://venom/')
    oGui.addDir(SITE_IDENTIFIER, 'showSeriesSearch', addons.VSlang(30079), '1/Search.png', oOutputParameterHandler)
    
    oOutputParameterHandler.addParameter('siteUrl', RAMADAN_SERIES[0])
    oGui.addDir(SITE_IDENTIFIER, 'showSeries', 'مسلسلات رمضان', '1/Ramadan.png', oOutputParameterHandler)
	
    oOutputParameterHandler.addParameter('siteUrl', SERIE_AR[0])
    oGui.addDir(SITE_IDENTIFIER, 'showSeries', 'مسلسلات عربية', '1/TVShows.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', SERIE_TR[0])
    oGui.addDir(SITE_IDENTIFIER, 'showSeries', 'مسلسلات تركية', '1/TVShows.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', f'{URL_MAIN}list/movies/')
    oGui.addDir(SITE_IDENTIFIER, 'showSeries', 'أفلام', '1/Movies.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()
 
def showSeriesSearch():
    oGui = cGui()
 
    sSearchText = oGui.showKeyBoard()
    if sSearchText:
        sUrl = f'{URL_MAIN}?s={sSearchText}'
        showSeries(sUrl)
        oGui.setEndOfDirectory()
        return
		
def showSeries(sSearch = ''):
    oGui = cGui()
    if sSearch:
      sUrl = sSearch
    else:
        oInputParameterHandler = cInputParameterHandler()
        sUrl = oInputParameterHandler.getValue('siteUrl')

    oParser = cParser()
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
  
    sPattern = '<div class="thumb"><a href="([^"]+)"><img src=".+?" alt="([^"]+)" data-src="([^"]+)'
    aResult = oParser.parse(sHtmlContent, sPattern)	
    itemList = []
    if aResult[0]:
        total = len(aResult[1])
        progress_ = progress().VScreate(SITE_NAME)
        oOutputParameterHandler = cOutputParameterHandler()
        for aEntry in aResult[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break
 
            siteUrl = aEntry[0]
            sTitle = cUtil().CleanSeriesName(aEntry[1])
            sThumb = aEntry[2]
            sDesc = ''
            sYear = ''
            m = re.search('([0-9]{4})', sTitle)
            if m:
                sYear = str(m.group(0))

            if sTitle not in itemList:
                itemList.append(sTitle)				
                oOutputParameterHandler.addParameter('siteUrl',siteUrl)
                oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
                oOutputParameterHandler.addParameter('sYear', sYear)
                oOutputParameterHandler.addParameter('sThumb', sThumb)
                if 'movies/' in sUrl:
                    oGui.addMovie(SITE_IDENTIFIER, 'showHosters', sTitle, '', sThumb, sDesc, oOutputParameterHandler)
                else:
                    oGui.addTV(SITE_IDENTIFIER, 'showEpisodes', sTitle, '', sThumb, sDesc, oOutputParameterHandler)

        progress_.VSclose(progress_)
        
        sNextPage = __checkForNextPage(sHtmlContent)
        if sNextPage:
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sNextPage)
            oGui.addDir(SITE_IDENTIFIER, 'showSeries', '[COLOR teal]Next >>>[/COLOR]', 'next.png', oOutputParameterHandler)
 
    if not sSearch:
        oGui.setEndOfDirectory()
	
def showEpisodes():
    oGui = cGui()
    
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')

    oParser = cParser() 
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    if 'list' in sUrl:
        m3url = sUrl
    else:
        sPattern = '<meta itemprop="position" content="2".+?<a href="([^"]+)'
        aResult = oParser.parse(sHtmlContent, sPattern)
        m3url=''
        if aResult[0]:
            m3url = aResult[1][0] 
            if m3url.startswith('//'):
                m3url = 'https:' + m3url
            if m3url.startswith('#'):
                m3url = sUrl

    oRequestHandler = cRequestHandler(m3url)
    sHtmlContent = oRequestHandler.request()
   
    sPattern = '<div class="thumb"><a href="(.+?)"><img src=".+?" alt="(.+?)" data-src="(.+?)" class='
    aResult = oParser.parse(sHtmlContent, sPattern)
    if aResult[0]:
        total = len(aResult[1])
        progress_ = progress().VScreate(SITE_NAME)
        oOutputParameterHandler = cOutputParameterHandler()
        for aEntry in aResult[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break
 
            siteUrl = aEntry[0]           
            sTitle = cUtil().CleanSeriesName(aEntry[1])
            sThumb = aEntry[2]
            sDesc = ''
            sYear = ''
            m = re.search(r"الحلقة (\d+)", aEntry[1])
            if m:
                sEp = str(m.group(1))
                sTitle = f'{sMovieTitle} E{sEp}'
			
            oOutputParameterHandler.addParameter('siteUrl',siteUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sYear', sYear)
            oOutputParameterHandler.addParameter('sThumb', sThumb)

            oGui.addEpisode(SITE_IDENTIFIER, 'showHosters', sTitle, '', sThumb, sDesc, oOutputParameterHandler)
        progress_.VSclose(progress_)

        sNextPage = __checkForNextPage(sHtmlContent)
        if sNextPage:
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sNextPage)
            oOutputParameterHandler.addParameter('sMovieTitle', sMovieTitle)
            oGui.addDir(SITE_IDENTIFIER, 'showEpisodes', '[COLOR teal]Next >>>[/COLOR]', 'next.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()

def __checkForNextPage(sHtmlContent):
    oParser = cParser()
    sPattern = '<link rel="next" href="([^"]+)'
    aResult = oParser.parse(sHtmlContent, sPattern)
    if aResult[0]:
        return aResult[1][0]

    return False

def showHosters(oInputParameterHandler = False):
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')

    oParser = cParser()
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()    

    sURL_MAIN= URL_MAIN

    sPattern = 'class="logo">\s*<a href="(.+?)">'
    aResult = oParser.parse(sHtmlContent, sPattern)    
    if (aResult[0]):
        sURL_MAIN = aResult[1][0]

    sPattern =  'data-vid="([^"]+)'
    aResult = oParser.parse(sHtmlContent,sPattern)
    if aResult[0]:
        postid = aResult[1][0] 

    oRequestHandler = cRequestHandler(f'{sURL_MAIN}wp-admin/admin-ajax.php?action=video_info&post_id={postid}')
    oRequestHandler.addHeaderEntry('User-Agent', UA)
    oRequestHandler.addHeaderEntry('Referer', sURL_MAIN)
    oRequestHandler.addParameters('action', 'video_info')
    oRequestHandler.addParameters('post_id', postid)
    sHtmlContent = oRequestHandler.request()
             
    sPattern = '"src":"([^"]+)'
    aResult = oParser.parse(sHtmlContent, sPattern)	
    if aResult[0]:
        for aEntry in aResult[1]:
            nUrl = aEntry

            if 'albaplayer' in nUrl:
                oRequestHandler = cRequestHandler(nUrl)
                oRequestHandler.addHeaderEntry('User-Agent', UA)
                oRequestHandler.addHeaderEntry('Referer', sURL_MAIN)
                sHtmlContent = oRequestHandler.request()  

                sPattern = r'<a[^>]+href="([^"]+)"[^>]*>([^<]+)</a>'
                aResult = oParser.parse(sHtmlContent, sPattern)	
                if aResult[0]:
                    oOutputParameterHandler = cOutputParameterHandler()
                    for aEntry in aResult[1]:

                        sHosterUrl = aEntry[0]
                        sLabel = aEntry[1]

                        sDisplayTitle = f'{sMovieTitle}[COLOR orange] - {sLabel}[/COLOR]'      
                        oOutputParameterHandler.addParameter('sHosterUrl', sHosterUrl)
                        oOutputParameterHandler.addParameter('siteUrl', sUrl)
                        oOutputParameterHandler.addParameter('sMovieTitle', sMovieTitle)
                        oOutputParameterHandler.addParameter('sThumb', sThumb)

                        oGui.addLink(SITE_IDENTIFIER, 'showLinks', sDisplayTitle, sThumb, sDisplayTitle, oOutputParameterHandler)
                else:
                    sPattern = '<iframe\s*src="([^"]+)'
                    aResult = oParser.parse(sHtmlContent, sPattern)	
                    if aResult[0]:
                        sHosterUrl = aResult[1][0] 

                        oHoster = cHosterGui().checkHoster(sHosterUrl)
                        if oHoster != False:
                            oHoster.setDisplayName(sMovieTitle)
                            oHoster.setFileName(sMovieTitle)
                            cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb)
            else:
                sHosterUrl = aEntry.replace('\\','')
                if sHosterUrl.startswith('//'):
                    sHosterUrl = f'http:{sHosterUrl}'
                    
                oHoster = cHosterGui().checkHoster(sHosterUrl)
                if oHoster:
                    oHoster.setDisplayName(sMovieTitle)
                    oHoster.setFileName(sMovieTitle)
                    cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb)         

    oGui.setEndOfDirectory()

def showLinks():
    oGui = cGui()

    oInputParameterHandler = cInputParameterHandler()
    sHosterUrl = oInputParameterHandler.getValue('sHosterUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')

    oParser = cParser()
    oRequestHandler = cRequestHandler(sHosterUrl)
    sHtmlContent = oRequestHandler.request()    

    sPattern = '<iframe\s*src="([^"]+)'
    aResult = oParser.parse(sHtmlContent, sPattern)	
    if aResult[0]:

        sHosterUrl = aResult[1][0] 
        if sHosterUrl.startswith('//'):
            sHosterUrl = f'http:{sHosterUrl}'

        oHoster = cHosterGui().checkHoster(sHosterUrl)
        if oHoster != False:
            oHoster.setDisplayName(sMovieTitle)
            oHoster.setFileName(sMovieTitle)
            cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb)

    oGui.setEndOfDirectory()