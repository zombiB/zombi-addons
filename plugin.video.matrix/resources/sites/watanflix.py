# -*- coding: utf-8 -*-

import re
from resources.lib.gui.hoster import cHosterGui
from resources.lib.gui.gui import cGui
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.comaddon import progress, siteManager, addon
from resources.lib.parser import cParser

SITE_IDENTIFIER = 'watanflix'
SITE_NAME = 'Watanflix'
SITE_DESC = 'arabic vod'
 
URL_MAIN = siteManager().getUrlMain(SITE_IDENTIFIER)

MOVIE_AR = (f'{URL_MAIN}/ar/category/الأفلام', 'showSeries')

RAMADAN_SERIES = (f'{URL_MAIN}/ar/category/%D9%85%D8%B3%D9%84%D8%B3%D9%84%D8%A7%D8%AA', 'showSeries')
SERIE_AR = (f'{URL_MAIN}/ar/category/%D9%85%D8%B3%D9%84%D8%B3%D9%84%D8%A7%D8%AA', 'showSeries')
KID_CARTOON = (f'{URL_MAIN}/ar/category/%D8%A3%D8%B7%D9%81%D8%A7%D9%84', 'showSerie')

SERIE_GENRES = (True, 'seriesGenres')

REPLAYTV_NEWS = (f'{URL_MAIN}/ar/category/برامج', 'showSeries')
REPLAYTV_PLAY = (f'{URL_MAIN}/ar/category/مسرحيات', 'showSeries')

URL_SEARCH = (f'{URL_MAIN}/ar/search?q=', 'showSeries')
URL_SEARCH_SERIES = (f'{URL_MAIN}/ar/search?q=', 'showSeriesSearch')
FUNCTION_SEARCH = 'showSeries'
 
def load():
    oGui = cGui()
    addons = addon()

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'http://venom/')
    oGui.addDir(SITE_IDENTIFIER, 'showSearch', addons.VSlang(30330), '1/Search.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', MOVIE_AR[0])
    oGui.addDir(SITE_IDENTIFIER, 'showSeries', 'أفلام عربية', '1/Arabic.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', SERIE_AR[0])
    oGui.addDir(SITE_IDENTIFIER, 'showSeries', 'مسلسلات عربية', '1/Arabic.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', REPLAYTV_NEWS[0])
    oGui.addDir(SITE_IDENTIFIER, 'showSeries', 'برامج تلفزيونية', '1/Programs.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', KID_CARTOON[0])
    oGui.addDir(SITE_IDENTIFIER, 'showSeries', 'مسلسلات كرتون', 'crtoon.png', oOutputParameterHandler) 

    oOutputParameterHandler.addParameter('siteUrl', REPLAYTV_PLAY[0])
    oGui.addDir(SITE_IDENTIFIER, 'showSeries', 'مسرحيات', 'msrh.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', SERIE_GENRES[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_GENRES[1], 'المسلسلات (الأنواع)', '1/TVShows.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()
 
def showSearch():
    oGui = cGui()
 
    sSearchText = oGui.showKeyBoard()
    if sSearchText:
        sUrl = f'{URL_MAIN}/ar/search?q={sSearchText}'
        showSeriesSearch(sUrl)
        oGui.setEndOfDirectory()
        return
 
def showSeriesSearch(sSearch = ''):
    oGui = cGui()
    if sSearch:
      sUrl = sSearch
    else:
        oInputParameterHandler = cInputParameterHandler()
        sUrl = oInputParameterHandler.getValue('siteUrl')

    oParser = cParser() 
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
    if "title" in sHtmlContent:
        sHtmlContent = sHtmlContent.encode("utf8",errors='ignore').decode("unicode_escape")


    sPattern = ',"title":"(.+?)",.+?,"url":"(.+?)","class'
    aResult = oParser.parse(sHtmlContent, sPattern)
    if aResult[0]:
        total = len(aResult[1])
        progress_ = progress().VScreate(SITE_NAME)
        oOutputParameterHandler = cOutputParameterHandler()
        for aEntry in aResult[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break
 
            sTitle = aEntry[0]
            siteUrl = aEntry[1]
            sThumb = ""
            sYear = ""
            sDesc = ""

            oOutputParameterHandler.addParameter('siteUrl',siteUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oOutputParameterHandler.addParameter('sYear', sYear)
            oOutputParameterHandler.addParameter('sDesc', sDesc)
			
            oGui.addTV(SITE_IDENTIFIER, 'showHosters', sTitle, '', sThumb, sDesc, oOutputParameterHandler)

        progress_.VSclose(progress_)
 
        sNextPage = __checkForNextPage(sHtmlContent)
        if sNextPage:
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sNextPage)
            oGui.addDir(SITE_IDENTIFIER, 'showSeriesSearch', '[COLOR teal]Next >>>[/COLOR]', 'next.png', oOutputParameterHandler)
 
    if not sSearch:
        oGui.setEndOfDirectory()
   
def seriesGenres():
    oGui = cGui()

    liste = []
    liste.append(['دراما', f'{URL_MAIN}/ar/type/'])
    liste.append(['كوميدي', f'{URL_MAIN}/ar/type/'])
    liste.append(['حارة-شامية', f'{URL_MAIN}/ar/type/'])
    liste.append(['رومنسي', f'{URL_MAIN}/ar/type/'])
    liste.append(['اجتماعي', f'{URL_MAIN}/ar/type/'])
    liste.append(['تاريخي-سيرة-ذاتيه-وثائقي', f'{URL_MAIN}/ar/type/'])
    liste.append(['رعب', f'{URL_MAIN}/ar/type/'])
    liste.append(['أكشن', f'{URL_MAIN}/ar/type/'])
    liste.append(['رياضي', f'{URL_MAIN}/ar/type/'])
    liste.append(['غموض-تشويق', f'{URL_MAIN}/ar/type/'])
    liste.append(['مقابلات-تلفزيونية', f'{URL_MAIN}/ar/type/'])
    liste.append(['ديني', f'{URL_MAIN}/ar/type/'])
    liste.append(['طبخ', f'{URL_MAIN}/ar/type/'])

    for sTitle, sUrl in liste:

        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', sUrl + sTitle)
        oGui.addDir(SITE_IDENTIFIER, 'showSeries', sTitle, 'genres.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()
 
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

    sPattern = 'title="<h4>.+?</h4><br> <span>([^<]+)</span>".+?data-content=" <div>(.+?)<br/>.+?<a href="([^<]+)" class="v-link" >.+?<div  class="video_img"><img alt="([^<]+)"  class="" src="([^<]+)"></div>'
    aResult = oParser.parse(sHtmlContent, sPattern)
    if aResult[0]:
        total = len(aResult[1])
        progress_ = progress().VScreate(SITE_NAME)
        oOutputParameterHandler = cOutputParameterHandler()
        for aEntry in aResult[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break
 
            sTitle = aEntry[3]
            siteUrl = aEntry[2]
            sThumb = aEntry[4]
            sDesc = aEntry[1]
            sYear = aEntry[0]
            sDisplayTitle = f'{sTitle} ({sYear})'

            oOutputParameterHandler.addParameter('siteUrl', siteUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sYear', sYear)
            oOutputParameterHandler.addParameter('sDesc', sDesc)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
			
            oGui.addTV(SITE_IDENTIFIER, 'showHosters', sDisplayTitle, '', sThumb, sDesc, oOutputParameterHandler)

        progress_.VSclose(progress_)
 
        sNextPage = __checkForNextPage(sHtmlContent)
        if sNextPage:
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sNextPage)
            oGui.addDir(SITE_IDENTIFIER, 'showSeries', '[COLOR teal]Next >>>[/COLOR]', 'next.png', oOutputParameterHandler)
 
    if not sSearch:
        oGui.setEndOfDirectory()
 
def showSerie(sSearch = ''):
    oGui = cGui()
    if sSearch:
      sUrl = sSearch
    else:
        oInputParameterHandler = cInputParameterHandler()
        sUrl = oInputParameterHandler.getValue('siteUrl')

    oParser = cParser() 
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    sPattern = 'data-content=" <div>(.+?)<br/>.+?<a href="([^<]+)" class="v-link" >.+?<div  class="video_img"><img alt="([^<]+)"  class="" src="([^<]+)"></div'
    aResult = oParser.parse(sHtmlContent, sPattern)
    if aResult[0]:
        total = len(aResult[1])
        progress_ = progress().VScreate(SITE_NAME)
        oOutputParameterHandler = cOutputParameterHandler()
        for aEntry in aResult[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break
				
            sTitle = aEntry[2]      
            siteUrl = aEntry[1]
            sThumb = aEntry[3]
            sDesc = aEntry[0]
            sYear = ""

            oOutputParameterHandler.addParameter('siteUrl', siteUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oOutputParameterHandler.addParameter('sYear', sYear)
            oOutputParameterHandler.addParameter('sDesc', sDesc)
			
            oGui.addTV(SITE_IDENTIFIER, 'showHosters', sTitle, '', sThumb, sDesc, oOutputParameterHandler)

        progress_.VSclose(progress_)
 
        sNextPage = __checkForNextPage(sHtmlContent)
        if sNextPage:
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sNextPage)
            oGui.addDir(SITE_IDENTIFIER, 'showSerie', '[COLOR teal]Next >>>[/COLOR]', 'next.png', oOutputParameterHandler)
 
    if not sSearch:
        oGui.setEndOfDirectory()
  
def __checkForNextPage(sHtmlContent):
    oParser = cParser()
    sPattern = 'href="([^<]+)" rel="next">'
    aResult = oParser.parse(sHtmlContent, sPattern)
    if aResult[0]:    
        return aResult[1][0]

    return False

def showHosters():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')

    oParser = cParser()    
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    sStart = '<ul class="seasons">'
    sEnd = '</ul>'
    sHtmlContent0 = oParser.abParse(sHtmlContent, sStart, sEnd)

    sPattern = '<a href="([^"]+)" >(.+?)</a>'
    aResult = oParser.parse(sHtmlContent0, sPattern)  
    if aResult[0]:
        oOutputParameterHandler = cOutputParameterHandler() 
        for aEntry in aResult[1]:
 
            sTitle = aEntry[1]
            siteUrl = aEntry[0]
            sThumb = sThumb
            sDesc = ''
 
            oOutputParameterHandler.addParameter('siteUrl', siteUrl)
            oOutputParameterHandler.addParameter('sTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)

            oGui.addSeason(SITE_IDENTIFIER, 'showHosters', sTitle, '', '', sDesc, oOutputParameterHandler)

    sStart = '<div id="slidingSeries"'
    sEnd = '<div class="clearfix"></div>'
    sHtmlContent = oParser.abParse(sHtmlContent, sStart, sEnd)

    sPattern = '<a href="([^"]+)".+?<img src="([^"]+)".+?<div><p><b>([^<]+)</b><br/>([^<]+)</p></div>'
    aResult = oParser.parse(sHtmlContent, sPattern)
    if aResult[0]:
        for aEntry in aResult[1]:
            
            sTitle = aEntry[2].replace("الجزء ","S").replace("الأول","1").replace("الاول","1").replace("الثاني","2").replace("الثانى","2").replace("الثالث","3").replace("الرابع","4").replace("الخامس","5").replace("السادس","6").replace("السابع","7").replace("الثامن","8").replace("التاسع","9") + aEntry[3].replace("الحلقة "," E")                
            sThumb = aEntry[1]
            url = str(aEntry[0])
            if url.startswith('//'):
                url = f'http:{url}'
            
            sHosterUrl = url
            oHoster = cHosterGui().checkHoster(sHosterUrl)
            if oHoster:
                oHoster.setDisplayName(sTitle)
                oHoster.setFileName(sTitle)
                cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb)
				
    oGui.setEndOfDirectory()                