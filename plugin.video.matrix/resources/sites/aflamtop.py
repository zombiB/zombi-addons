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

SITE_IDENTIFIER = 'aflamtop'
SITE_NAME = 'Aflam Top'
SITE_DESC = 'arabic vod'
 
URL_MAIN = siteManager().getUrlMain(SITE_IDENTIFIER)

MOVIE_EN = (f'{URL_MAIN}category/افلام/افلام-اجنبية/', 'showMovies')
MOVIE_AR = (f'{URL_MAIN}category/افلام/افلام-عربية/', 'showMovies')
MOVIE_HI = (f'{URL_MAIN}category/افلام/افلام-هندية/', 'showMovies')
MOVIE_ASIAN = (f'{URL_MAIN}category/افلام/افلام-اسيوية/', 'showMovies')
MOVIE_DUBBED = (f'{URL_MAIN}tag/افلام-مدبلجة/', 'showMovies')
MOVIE_CLASSIC = (f'{URL_MAIN}tag/افلام-كلاسيكية/', 'showMovies')
MOVIE_TURK = (f'{URL_MAIN}category/افلام/افلام-تركية/', 'showMovies')
MOVIE_ANNEES = (URL_MAIN, 'showYears')
KID_MOVIES = (f'{URL_MAIN}category/الانيميشن/', 'showMovies')
MOVIE_WORLD = (f'{URL_MAIN}tag/افلام-البوكس-اوفيس/', 'showMovies')

DOC_NEWS = (f'{URL_MAIN}category/افلام/افلام-وثائقية/', 'showMovies')

URL_SEARCH = (f'{URL_MAIN}?s=', 'showMovies')
URL_SEARCH_MOVIES = (f'{URL_MAIN}?s=', 'showMovies')
FUNCTION_SEARCH = 'showMovies'
 
def load():
    oGui = cGui()
    addons = addon()

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', URL_SEARCH[0])
    oGui.addDir(SITE_IDENTIFIER, 'showSearch', addons.VSlang(30078), '1/Search.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', MOVIE_WORLD[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_WORLD[1], 'افلام البوكس اوفيس', '1/Movies.png', oOutputParameterHandler)
   
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_EN[0])
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'أفلام أجنبية', '1/Movies.png', oOutputParameterHandler)
   
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_AR[0])
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'أفلام عربية', '1/Arabic.png', oOutputParameterHandler)
 
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_ASIAN[0])
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'أفلام أسيوية', '1/Asian.png', oOutputParameterHandler)
   
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_HI[0])
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'أفلام هندية', '1/Hindi.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', MOVIE_TURK[0])
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'أفلام تركية', '1/Turkish.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', MOVIE_CLASSIC[0])
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'أفلام كلاسيكية', '1/Classic.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', MOVIE_DUBBED[0])
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'أفلام مدبلجة', '1/Dubbed.png', oOutputParameterHandler) 
 
    oOutputParameterHandler.addParameter('siteUrl', KID_MOVIES[0])
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'أفلام كرتون', '1/1/Anime.png', oOutputParameterHandler)   
    
    oOutputParameterHandler.addParameter('siteUrl', DOC_NEWS[0])
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'أفلام وثائقية', '1/Documentary.png', oOutputParameterHandler) 

    oOutputParameterHandler.addParameter('siteUrl', URL_MAIN)
    oGui.addDir(SITE_IDENTIFIER, 'showPack', 'أقسام الموقع', 'listes.png', oOutputParameterHandler)

    oGui.setEndOfDirectory() 

def showSearch():
    oGui = cGui()
 
    sSearchText = oGui.showKeyBoard()
    if sSearchText:
        sUrl = f'{URL_MAIN}?s={sSearchText}'
        showMovies(sUrl)
        oGui.setEndOfDirectory()
        return

def showPack():
    oGui = cGui()

    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
 
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    sPattern = '<a href="([^<]+)">([^<]+)</a>'
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
	
    if aResult[0] is True:
        oOutputParameterHandler = cOutputParameterHandler()
        for aEntry in aResult[1]:
            keywords = ['المزيد', 'اشترك', 'طلبات', 'الرئيسية'] 
            if any(keyword in aEntry[1] for keyword in keywords): 
                continue

            sTitle = aEntry[1]
            sTitle = re.sub(r"[^\w\s]", "", sTitle)
            sThumb = ''
            siteUrl = aEntry[0]
            if siteUrl.startswith('/'):
                siteUrl = f'{URL_MAIN}{siteUrl}'

            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', siteUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
			
            oGui.addDir(SITE_IDENTIFIER, 'showMovies', sTitle, sThumb, oOutputParameterHandler)
 
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
    sHtmlContent = oRequestHandler.request()
    
    oParser = cParser()
    sPattern = '<div class="Small--Box">\s*<a href="([^"]+)" title="([^"]+)".+?data-src="([^"]+)'
    aResult = oParser.parse(sHtmlContent, sPattern)
    if aResult[0] is True:
        total = len(aResult[1])
        progress_ = progress().VScreate(SITE_NAME)
        oOutputParameterHandler = cOutputParameterHandler()
        for aEntry in aResult[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break
            if 'serie' in aEntry[0] or 'مسلسل' in aEntry[0]:
                continue
            
            sTitle = cUtil().CleanMovieName(aEntry[1])
            siteUrl = aEntry[0]
            sThumb = re.sub(r'-\d+x\d{0,3}','', aEntry[2])  
            sDesc = ''
            sYear = ''
            m = re.search('([0-9]{4})', sTitle)
            if m:
               sYear = str(m.group(0))

            oOutputParameterHandler.addParameter('siteUrl', siteUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oOutputParameterHandler.addParameter('sYear', sYear)
            oOutputParameterHandler.addParameter('sDesc', sDesc)

            if 'assemblies' in siteUrl :			
                oGui.addMovie(SITE_IDENTIFIER, 'showassemblies', sTitle, '', sThumb, sDesc, oOutputParameterHandler)
            else:
                siteUrl = aEntry[0]+'/watch'
                oOutputParameterHandler.addParameter('siteUrl',siteUrl)
                oGui.addMovie(SITE_IDENTIFIER, 'showLinks', sTitle, '', sThumb, sDesc, oOutputParameterHandler)
    
        progress_.VSclose(progress_)

    if not sSearch:
        sStart = '<div class="pagination">'
        sEnd = '<footer>'
        sHtmlContent = oParser.abParse(sHtmlContent, sStart, sEnd)

        sPattern = 'href="([^"]+)">(.+?)</a>'
        aResult = oParser.parse(sHtmlContent, sPattern)
        if aResult[0]:
            for aEntry in aResult[1]:

                sTitle =   f'[COLOR red]Page: {aEntry[1]}[/COLOR]'
                siteUrl = aEntry[0]

                oOutputParameterHandler = cOutputParameterHandler()
                oOutputParameterHandler.addParameter('siteUrl',siteUrl)
			
                oGui.addDir(SITE_IDENTIFIER, 'showMovies', sTitle, 'next.png', oOutputParameterHandler) 
 
        oGui.setEndOfDirectory()

def showassemblies():
    oGui = cGui()

    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
    oParser = cParser()

    sStart = '<section class="tabContents">'
    sEnd = '</section>'
    sHtmlContent = oParser.abParse(sHtmlContent, sStart, sEnd)

    sPattern = '<div class="Small--Box">.+?href="([^"]+)" title="([^"]+)".+?data-src="([^"]+)'
    aResult = oParser.parse(sHtmlContent, sPattern)
    if aResult[0]:
        total = len(aResult[1])
        progress_ = progress().VScreate(SITE_NAME)
        oOutputParameterHandler = cOutputParameterHandler()
        for aEntry in aResult[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break

            sTitle = (cUtil().CleanMovieName(aEntry[1])).replace('الحلقة ','E').replace('حلقة ','E')
            sTitle = cUtil().ConvertSeasons(sTitle)
            siteUrl = aEntry[0]+'/watch'
            sThumb = re.sub(r'-\d+x\d{0,3}','', aEntry[2])
            sDesc = ''
            sYear = ''
            m = re.search('([0-9]{4})', sTitle)
            if m:
                sYear = str(m.group(0))
                sTitle = sTitle.replace(sYear,'')
            
            oOutputParameterHandler.addParameter('siteUrl', siteUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oOutputParameterHandler.addParameter('sYear', sYear)
            oOutputParameterHandler.addParameter('sDesc', sDesc)

            oGui.addMovie(SITE_IDENTIFIER, 'showLinks', sTitle, '', sThumb, sDesc, oOutputParameterHandler)
        
        progress_.VSclose(progress_)
   
    oGui.setEndOfDirectory()

def showLinks():
    oGui = cGui()

    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')

    oParser = cParser()
    oRequestHandler = cRequestHandler(sUrl)
    oRequestHandler.addHeaderEntry('User-Agent', UA)
    oRequestHandler.addHeaderEntry('Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8')
    oRequestHandler.addHeaderEntry('X-Requested-With', 'XMLHttpRequest')
    oRequestHandler.addHeaderEntry('Accept-Language', 'fr,fr-FR;q=0.8,en-US;q=0.5,en;q=0.3')
    sHtmlContent = oRequestHandler.request()
          
    sStart = '<div class="WatchArea active">'
    sEnd = '<footer>'
    sHtmlContent = oParser.abParse(sHtmlContent, sStart, sEnd) 

    sPattern = 'data-watch="([^"]+)".+?</span>(.+?)<noscript>'
    aResult = oParser.parse(sHtmlContent, sPattern)
    if aResult[0]:
        for aEntry in aResult[1]:  
            if URL_MAIN in aEntry[0]:
                continue

            sHosterUrl = aEntry[0]
            sHost = aEntry[1]

            if 'vidtube' in sHost or 'vidhidepro' in sHost or 'updown' in sHost:
                sHosterUrl = f'{sHosterUrl}|Referer={URL_MAIN}'

            oHoster = cHosterGui().checkHoster(sHosterUrl)
            if oHoster:
                oHoster.setDisplayName(sMovieTitle)
                oHoster.setFileName(sMovieTitle)
                cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb)

    oRequestHandler = cRequestHandler(sUrl.replace('/watch','/download'))
    oRequestHandler.addHeaderEntry('User-Agent', UA)
    oRequestHandler.addHeaderEntry('X-Requested-With', 'XMLHttpRequest')
    sHtmlContent = oRequestHandler.request()

    sStart = '<div class="WatchArea active">'
    sEnd = '<footer>'
    sHtmlContent = oParser.abParse(sHtmlContent, sStart, sEnd) 

    sPattern = 'href="([^"]+)".+?<em>(.+?)</em>'
    aResult = oParser.parse(sHtmlContent, sPattern)
    if aResult[0]:
        for aEntry in aResult[1]:  
            if URL_MAIN in aEntry[0]:
                continue

            sHosterUrl = aEntry[0]
            sHost = aEntry[1]

            if 'vidtube' in sHost or 'vidhidepro' in sHost or 'updown' in sHost:
                sHosterUrl = f'{sHosterUrl}|Referer={URL_MAIN}'

            oHoster = cHosterGui().checkHoster(sHosterUrl)
            if oHoster:
                oHoster.setDisplayName(sMovieTitle)
                oHoster.setFileName(sMovieTitle)
                cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb)

    oGui.setEndOfDirectory()

def showHosters():
    oGui = cGui()

    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')
    Serv = oInputParameterHandler.getValue('Serv')
    Sid = oInputParameterHandler.getValue('Sid')
    sHost = oInputParameterHandler.getValue('sHost')

    oParser = cParser()
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    sPattern = '<a class="Logo--Area" href="([^"]+)'	
    aResult = oParser.parse(sHtmlContent, sPattern)
    if aResult[0]:
        URL_MAIN = aResult[1][0]

    oRequestHandler = cRequestHandler(URL_MAIN+'/wp-content/themes/movies2023/Ajaxat/Single/Server.php')
    oRequestHandler.addHeaderEntry('Sec-Fetch-Mode', 'cors')
    oRequestHandler.addHeaderEntry('X-Requested-With', 'XMLHttpRequest')
    oRequestHandler.addHeaderEntry('Sec-Fetch-Dest', 'empty')
    oRequestHandler.addHeaderEntry('Sec-Fetch-Site', 'same-origin')
    oRequestHandler.addHeaderEntry('User-Agent', UA)
    oRequestHandler.addHeaderEntry('Referer', URL_MAIN)
    oRequestHandler.addHeaderEntry('Origin', URL_MAIN)
    oRequestHandler.addParameters('id', Sid)
    oRequestHandler.addParameters('i', Serv)
    oRequestHandler.setRequestType(1)
    sHtmlContent = oRequestHandler.request()

    sPattern = '<iframe src="([^"]+)'
    aResult = oParser.parse(sHtmlContent, sPattern)
    if aResult:
        sHosterUrl = aResult[1][0]

        if 'vidtube' in sHosterUrl or 'vidhidepro' in sHosterUrl or 'updown' in sHosterUrl or 'katomen' in sHosterUrl or 'StreamWish' in sHost:
            sHosterUrl = f'{sHosterUrl}|Referer={URL_MAIN}'

        oHoster = cHosterGui().checkHoster(sHosterUrl)
        if oHoster:
            oHoster.setDisplayName(sMovieTitle)
            oHoster.setFileName(sMovieTitle)
            cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb)

    oGui.setEndOfDirectory()