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

SITE_IDENTIFIER = 'moviztime'
SITE_NAME = 'MovizTime'
SITE_DESC = 'arabic vod'

URL_MAIN = siteManager().getUrlMain(SITE_IDENTIFIER)

MOVIE_EN = (f'{URL_MAIN}category/أفلام-أجنبية/', 'showMovies')
MOVIE_HI = (f'{URL_MAIN}category/أفلام-هندية/', 'showMovies')
MOVIE_ASIAN = (f'{URL_MAIN}category/أفلام-آسيوية-مترجمة/', 'showMovies')
MOVIE_TURK = (f'{URL_MAIN}category/أفلام-تركية/', 'showMovies')
MOVIE_GENRES = (True, 'moviesGenres')

SERIE_ASIA = (f'{URL_MAIN}category/مسلسلات-كورية/', 'showSeries')
SERIE_GENRES = (True, 'seriesGenres')

ANIM_MOVIES = (f'{URL_MAIN}category/قائمة-الأنمي-b/أفلام-أنمي/', 'showMovies')
ANIM_NEWS = (URL_MAIN+'category/قائمة-الأنمي-b/مسلسلات-أنمي/' , 'showSeries')

REPLAYTV_NEWS = (f'{URL_MAIN}category/برامج-تلفزيونية/', 'showMovies')

URL_SEARCH = (f'{URL_MAIN}?s=', 'showSeries')
URL_SEARCH_MOVIES = (f'{URL_MAIN}?s=', 'showMovies')
URL_SEARCH_SERIES = (f'{URL_MAIN}?s=', 'showSeries')
FUNCTION_SEARCH = 'showSearch'
 
def load():
    oGui = cGui()
    addons = addon()

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'http://venom/')
    oGui.addDir(SITE_IDENTIFIER, 'showSearch', addons.VSlang(30078), '1/Search.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', 'http://venom/')
    oGui.addDir(SITE_IDENTIFIER, 'showSeriesSearch', addons.VSlang(30079), '1/Search.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', MOVIE_EN[0])
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'أفلام أجنبية', '1/Movies.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', f'{URL_MAIN}category/أفلام-أوروبية/')
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'أفلام أوروبية', '1/Movies.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', MOVIE_HI[0])
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'أفلام هندية', '1/Hindi.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', MOVIE_ASIAN[0])
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'أفلام أسيوية', '1/Asian.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', MOVIE_TURK[0])
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'أفلام تركية', '1/Turkish.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', ANIM_NEWS[0])
    oGui.addDir(SITE_IDENTIFIER, 'showSeries', 'مسلسلات انمي', '1/Anime.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', ANIM_MOVIES[0])
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'أفلام انمي', '1/Anime.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', REPLAYTV_NEWS[0])
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'برامج تلفزيونية', '1/Programs.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', MOVIE_GENRES[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_GENRES[1], 'الأفلام (الأنواع)', '1/Movies.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()
 
def showSeriesSearch():
    oGui = cGui()
 
    sSearchText = oGui.showKeyBoard()
    if sSearchText:
        sUrl = f'{URL_MAIN}?s={sSearchText}'
        showSeries(sUrl)
        oGui.setEndOfDirectory()
        return
 
def showSearch():
    oGui = cGui()
 
    sSearchText = oGui.showKeyBoard()
    if sSearchText:
        sUrl = f'{URL_MAIN}?s={sSearchText}'
        showMovies(sUrl)
        oGui.setEndOfDirectory()
        return

def moviesGenres():
    oGui = cGui()

    liste = []
    liste.append(['اكشن', f'{URL_MAIN}category/%d8%a3%d9%81%d9%84%d8%a7%d9%85-%d8%a3%d8%ac%d9%86%d8%a8%d9%8a%d8%a9/action/'])
    liste.append(['انيميشن', f'{URL_MAIN}category/%d8%a3%d9%86%d9%8a%d9%85%d9%8a%d8%b4%d9%86/'])
    liste.append(['كوميديا', f'{URL_MAIN}category/%d8%a3%d9%81%d9%84%d8%a7%d9%85-%d8%a3%d8%ac%d9%86%d8%a8%d9%8a%d8%a9/comedy/'])
    liste.append(['قصة حقيقية', f'{URL_MAIN}category/%d9%82%d8%b5%d8%a9-%d8%ad%d9%82%d9%8a%d9%82%d9%8a%d8%a9/'])
    liste.append(['دراما', f'{URL_MAIN}category/%d8%a3%d9%81%d9%84%d8%a7%d9%85-%d8%a3%d8%ac%d9%86%d8%a8%d9%8a%d8%a9/drama/'])
    liste.append(['رعب', f'{URL_MAIN}category/%d8%a3%d9%81%d9%84%d8%a7%d9%85-%d8%a3%d8%ac%d9%86%d8%a8%d9%8a%d8%a9/%d8%b1%d8%b9%d8%a8-%d9%85%d8%aa%d8%b1%d8%ac%d9%85/'])
    liste.append(['عائلى', f'{URL_MAIN}category/%d8%b9%d8%a7%d8%a6%d9%84%d9%8a/'])
    liste.append(['حروب', f'{URL_MAIN}category/%d8%ad%d8%b1%d9%88%d8%a8/'])
    liste.append(['الجريمة', f'{URL_MAIN}category/%d8%a3%d9%81%d9%84%d8%a7%d9%85-%d8%a3%d8%ac%d9%86%d8%a8%d9%8a%d8%a9/%d8%a7%d9%81%d9%84%d8%a7%d9%85-%d8%ac%d8%b1%d9%8a%d9%85%d8%a9/'])
    liste.append(['رومانسى', f'{URL_MAIN}category/%d8%a3%d9%81%d9%84%d8%a7%d9%85-%d8%a3%d8%ac%d9%86%d8%a8%d9%8a%d8%a9/%d8%b1%d9%88%d9%85%d8%a7%d9%86%d8%b3%d9%8a/'])
    liste.append(['خيال علمى', f'{URL_MAIN}category/%d8%ae%d9%8a%d8%a7%d9%84-%d8%b9%d9%84%d9%85%d9%8a/'])
    liste.append(['اثارة', f'{URL_MAIN}category/%d8%a7%d8%ab%d8%a7%d8%b1%d8%a9/'])
    liste.append(['وثائقى', f'{URL_MAIN}category/%d9%88%d8%ab%d8%a7%d8%a6%d9%82%d9%8a/'])
    liste.append(['غموض', f'{URL_MAIN}category/%d8%ba%d9%85%d9%88%d8%b6/'])

    for sTitle, sUrl in liste:
        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', sUrl)
        oGui.addDir(SITE_IDENTIFIER, 'showMovies', sTitle, 'genres.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()

def showMovies(sSearch = ''):
    oGui = cGui()
    if sSearch:
      sUrl = sSearch
    else:
        oInputParameterHandler = cInputParameterHandler()
        sUrl = oInputParameterHandler.getValue('siteUrl')

    oParser = cParser()
    oRequestHandler = cRequestHandler(sUrl)
    oRequestHandler.addHeaderEntry('User-Agent', UA)
    sHtmlContent = oRequestHandler.request()
    
    sPattern = '<p class="thumb">.+?href="([^"]+)" title="([^"]+)">.+?src="([^"]+)' 
    aResult = oParser.parse(sHtmlContent, sPattern)
    if aResult[0] :
        total = len(aResult[1])
        progress_ = progress().VScreate(SITE_NAME)
        oOutputParameterHandler = cOutputParameterHandler()
        for aEntry in aResult[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break
 
            if "مسلسل"  in aEntry[1] or "حلقة"  in aEntry[1] or "انمي"  in aEntry[1]:
                continue 
            
            sTitle = cUtil().CleanMovieName(aEntry[1])
            siteUrl = aEntry[0]
            sDesc = ''
            sThumb = aEntry[2]
            sYear = ''
            m = re.search('([0-9]{4})', sTitle)
            if m:
                sYear = str(m.group(0))

            oOutputParameterHandler.addParameter('siteUrl', siteUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oOutputParameterHandler.addParameter('sYear', sYear)
            oOutputParameterHandler.addParameter('sDesc', sDesc)

            if "موسم"  in sTitle or "برنامج"  in sTitle:
                oGui.addTV(SITE_IDENTIFIER, 'showEpisodes', sTitle, '', sThumb, sDesc, oOutputParameterHandler)
            else:
                oGui.addMovie(SITE_IDENTIFIER, 'showHosters2', sTitle, '', sThumb, sDesc, oOutputParameterHandler)

        progress_.VSclose(progress_)
 
        sNextPage = __checkForNextPage(sHtmlContent)
        if sNextPage:
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sNextPage)
            oGui.addDir(SITE_IDENTIFIER, 'showMovies', '[COLOR teal]Next >>>[/COLOR]', 'next.png', oOutputParameterHandler)
 
    if not sSearch:
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
    oRequestHandler.addHeaderEntry('User-Agent', UA)
    sHtmlContent = oRequestHandler.request()
  
    sPattern = '<p class="thumb">.+?href="([^"]+)" title="([^"]+)">.+?src="([^"]+)' 
    aResult = oParser.parse(sHtmlContent, sPattern)
    if aResult[0] :
        total = len(aResult[1])
        progress_ = progress().VScreate(SITE_NAME)
        oOutputParameterHandler = cOutputParameterHandler()
        for aEntry in aResult[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break

            if "فيلم"  in aEntry[1]:
                continue

            siteUrl = aEntry[0]           
            sTitle = cUtil().CleanSeriesName(aEntry[1])
            sThumb = aEntry[2]
            sDesc = ''
            sYear = ''
            m = re.search('([0-9]{4})', sTitle)
            if m:
                sYear = str(m.group(0))
		
            oOutputParameterHandler.addParameter('siteUrl', siteUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sYear', sYear)
            oOutputParameterHandler.addParameter('sThumb', sThumb)

            oGui.addTV(SITE_IDENTIFIER, 'showEpisodes', sTitle, '', sThumb, sDesc, oOutputParameterHandler)

        progress_.VSclose(progress_)

        sNextPage = __checkForNextPage(sHtmlContent)
        if sNextPage:
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sNextPage)
            oGui.addDir(SITE_IDENTIFIER, 'showSeries', '[COLOR teal]Next >>>[/COLOR]', 'next.png', oOutputParameterHandler)
 
    if not sSearch:
        oGui.setEndOfDirectory()
 
def __checkForNextPage(sHtmlContent):
    oParser = cParser()
    sPattern = '<link rel="next" href="([^"]+)'
    aResult = oParser.parse(sHtmlContent, sPattern)
    if aResult[0]:
        return aResult[1][0]

    return False
	
def showEpisodes():
    oGui = cGui()
    
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')

    oParser = cParser() 
    oRequestHandler = cRequestHandler(sUrl)
    oRequestHandler.addHeaderEntry('User-Agent', UA)
    sHtmlContent = oRequestHandler.request()

    sPattern =  '<p class="logo">.+?<a href="([^"]+)' 
    aResult = oParser.parse(sHtmlContent,sPattern)
    if aResult[0]:
        sRefer = aResult[1][0] 

    sPattern = '<div class="title">(.+?)</div>(.+?)</div>'
    aResult = oParser.parse(sHtmlContent, sPattern)
    if aResult[0] :
       
        for aEntry in aResult[1]:
            sServer = aEntry[0]
            sHtmlContent = aEntry[1]

            sPattern = "onclick=.+?.href='([^']+).+?>(.+?)</button>"
            aResult = oParser.parse(sHtmlContent, sPattern)
            if aResult[0] :
                for aEntry in aResult[1]:
 
                    siteUrl = aEntry[0] 
                    sTitle = sServer
                    sTitle = f'{sTitle} {aEntry[1].replace("الحلقة","E").replace("حلقة","E")}'
                    sThumb = sThumb		

                    sHosterUrl = f'{siteUrl}|Referer={sRefer}'
                    oHoster = cHosterGui().checkHoster(sHosterUrl)
                    if oHoster:
                        oHoster.setDisplayName(sTitle)
                        oHoster.setFileName(sTitle)
                        cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb)
       
    oGui.setEndOfDirectory() 
	 
def showHosters2():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')

    oParser = cParser()
    oRequestHandler = cRequestHandler(sUrl)
    oRequestHandler.addHeaderEntry('User-Agent', UA)
    sHtmlContent = oRequestHandler.request()

    sPattern =  '<p class="logo">.+?<a href="([^"]+)' 
    aResult = oParser.parse(sHtmlContent,sPattern)
    if aResult[0]:
        sRefer = aResult[1][0] 

    sPattern = 'data-src="([^"]+)'
    aResult = oParser.parse(sHtmlContent, sPattern)
    if aResult[0]:
        for aEntry in aResult[1]:       
            url = aEntry
            if url.startswith('//'):
                url = f'http:{url}'
            if 'vidhls' in url:
                url = f'{url}|Referer={sRefer}'
            if 'hamml' in url:
                oRequestHandler = cRequestHandler(url)
                oRequestHandler.request()
                sRealUrl = oRequestHandler.getRealUrl()
                url = sRealUrl

            sHosterUrl = url  
            oHoster = cHosterGui().checkHoster(sHosterUrl)
            if oHoster:
               oHoster.setDisplayName(sMovieTitle)
               oHoster.setFileName(sMovieTitle)
               cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb)

    sStart = '<span class="server_btn"'
    sEnd = '<div class="tabs_content"'
    sHtmlContent = oParser.abParse(sHtmlContent, sStart, sEnd)

    sPattern = '<a href="(.+?)" class="download_btn">'
    aResult = oParser.parse(sHtmlContent, sPattern)
    if aResult[0]:
        for aEntry in aResult[1]:
            oRequestHandler = cRequestHandler(aEntry)                        
            sHtmlContent = oRequestHandler.request()

            sStart = '<section id="content">'
            sEnd = '</div>'
            sHtmlContent = oParser.abParse(sHtmlContent, sStart, sEnd)
                
            sPattern = '<a href="(.+?)" class="download_btn"'
            aResult = oParser.parse(sHtmlContent, sPattern)
            if aResult[0]:
                for aEntry in aResult[1]:               
                    sHosterUrl = aEntry.replace(',','')
                    if 'movietime' in sHosterUrl:
                        oHoster = cHosterGui().getHoster('direct_link')
                        if oHoster:
                            oHoster.setDisplayName(sMovieTitle)
                            oHoster.setFileName(sMovieTitle)
                            cHosterGui().showHoster(oGui, oHoster, sHosterUrl , sThumb)
                    else:
                        oHoster = cHosterGui().checkHoster(sHosterUrl)
                        if oHoster:
                            oHoster.setDisplayName(sMovieTitle)
                            oHoster.setFileName(sMovieTitle)
                            cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb)

    oGui.setEndOfDirectory()