# -*- coding: utf-8 -*-

import re
from resources.lib.gui.hoster import cHosterGui
from resources.lib.gui.gui import cGui
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.comaddon import progress, VSlog, siteManager, addon
from resources.lib.parser import cParser
from resources.lib.util import cUtil, Quote
from resources.lib import random_ua

UA = random_ua.get_ua()

SITE_IDENTIFIER = 'topcinema'
SITE_NAME = 'TopCinema'
SITE_DESC = 'arabic vod'
 
URL_MAIN = siteManager().getUrlMain(SITE_IDENTIFIER)

MOVIE_EN = (f'{URL_MAIN}category/افلام-اجنبي-2/', 'showMovies')
MOVIE_ASIAN = (f'{URL_MAIN}category/افلام-اسيوي/', 'showMovies')
MOVIE_NETFLIX = (f'{URL_MAIN}netflix-movies/', 'showMovies')
MOVIE_PACK = (f'{URL_MAIN}movies-collections/', 'showMovies')
KID_MOVIES = (f'{URL_MAIN}category/افلام-انمي/', 'showMovies')

SERIE_EN = (f'{URL_MAIN}category/مسلسلات-اجنبي-5/', 'showSeries')
SERIE_NETFLIX = (f'{URL_MAIN}netflix-series/?cat=7', 'showSeries')
SERIE_ASIA = (f'{URL_MAIN}category/مسلسلات-اسيوية-4/', 'showSeries')
ANIM_NEWS = (f'{URL_MAIN}category/مسلسلات-انمي/', 'showSeries')

URL_SEARCH = (f'{URL_MAIN}?s=', 'showMovies')
URL_SEARCH_MOVIES = (f'{URL_MAIN}?s=', 'showMovies')
URL_SEARCH_SERIES = (f'{URL_MAIN}?s=', 'showSeries')
FUNCTION_SEARCH = 'showMovies'
 
def load():
    oGui = cGui()
    addons = addon()

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'http://venom/')
    oGui.addDir(SITE_IDENTIFIER, 'showSearch', addons.VSlang(30078), '1/Search.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', 'http://venom/')
    oGui.addDir(SITE_IDENTIFIER, 'showSearchSeries', addons.VSlang(30079), '1/Search.png', oOutputParameterHandler)
	
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_EN[0])
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'أفلام أجنبية', '1/Movies.png', oOutputParameterHandler)
         
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_ASIAN[0])
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'أفلام أسيوية', '1/Asian.png', oOutputParameterHandler)  
   
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_NETFLIX[0])
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'أفلام نيتفلكس', 'netflix.png', oOutputParameterHandler)
       
    oOutputParameterHandler.addParameter('siteUrl', KID_MOVIES[0])
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'أفلام كرتون', 'crtoon.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', MOVIE_PACK[0])
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'سلاسل افلام كاملة', 'pack.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', SERIE_EN[0])
    oGui.addDir(SITE_IDENTIFIER, 'showSeries', 'مسلسلات أجنبية', '1/Movies.png', oOutputParameterHandler)
   
    oOutputParameterHandler.addParameter('siteUrl', SERIE_ASIA[0])
    oGui.addDir(SITE_IDENTIFIER, 'showSeries', 'مسلسلات أسيوية', '1/Asian.png', oOutputParameterHandler)
    
    oOutputParameterHandler.addParameter('siteUrl', ANIM_NEWS[0])
    oGui.addDir(SITE_IDENTIFIER, 'showSeries', 'مسلسلات انمي', '1/Anime.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', SERIE_NETFLIX[0])
    oGui.addDir(SITE_IDENTIFIER, 'showSeries', 'مسلسلات نيتفلكس', 'netflix.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', URL_MAIN)
    oGui.addDir(SITE_IDENTIFIER, 'showPack', 'أقسام الموقع', 'listes.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()
 
def showSearch():
    oGui = cGui()
 
    sSearchText = oGui.showKeyBoard()
    if sSearchText is not False:
        sUrl = f'{URL_MAIN}?s={sSearchText}'
        showMovies(sUrl)
        oGui.setEndOfDirectory()
        return
 
def showSearchSeries():
    oGui = cGui()
 
    sSearchText = oGui.showKeyBoard()
    if sSearchText is not False:
        sUrl = f'{URL_MAIN}?s={sSearchText}'
        showSeries(sUrl)
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
            if 'المزيد' in aEntry[1]:
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
			
            if 'serie' in siteUrl or 'مسلسل' in siteUrl:
                oGui.addDir(SITE_IDENTIFIER, 'showSeries', sTitle, sThumb, oOutputParameterHandler)
            else:
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

    if sSearch:
        psearch = sUrl.split('?s=')[1]
        oRequestHandler = cRequestHandler(f'{URL_MAIN}wp-content/themes/movies2023/Ajaxat/Searching.php')
        oRequestHandler.addHeaderEntry('User-Agent', UA)
        oRequestHandler.addHeaderEntry('Referer', URL_MAIN)
        oRequestHandler.addParameters('search', psearch)
        oRequestHandler.addParameters('type', 'movies')
        oRequestHandler.setRequestType(1)
        sHtmlContent = oRequestHandler.request()

    else:
        oRequestHandler = cRequestHandler(sUrl)
        sHtmlContent = oRequestHandler.request()
    
    oParser = cParser()
    sPattern = '<div class="Small--Box"><a href="([^"]+)" title="([^"]+)".+?data-src="([^"]+)'
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
        sNextPage = __checkForNextPage(sHtmlContent)
        if sNextPage:
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sNextPage)
            oGui.addDir(SITE_IDENTIFIER, 'showMovies', '[COLOR teal]Next >>>[/COLOR]', 'next.png', oOutputParameterHandler)
 
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
        sNextPage = __checkForNextPage(sHtmlContent)
        if sNextPage:
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sNextPage)
            oGui.addDir(SITE_IDENTIFIER, 'showassemblies', '[COLOR teal]Next >>>[/COLOR]', 'next.png', oOutputParameterHandler)
    
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

    oParser = cParser() 

    if sSearch:
        psearch = sUrl.split('?s=')[1]
        oRequestHandler = cRequestHandler(f'{URL_MAIN}wp-content/themes/movies2023/Ajaxat/Searching.php')
        oRequestHandler.addHeaderEntry('User-Agent', UA)
        oRequestHandler.addHeaderEntry('Referer', URL_MAIN)
        oRequestHandler.addParameters('search', psearch)
        oRequestHandler.addParameters('type', 'series')
        oRequestHandler.setRequestType(1)
        sHtmlContent = oRequestHandler.request()

    else:    
        oRequestHandler = cRequestHandler(sUrl)
        sHtmlContent = oRequestHandler.request()

    sPattern = '<div class="Small--Box">.+?href="([^"]+)" title="([^"]+)".+?data-src="([^"]+)'
    aResult = oParser.parse(sHtmlContent, sPattern)
    if aResult[0] is True:
        total = len(aResult[1])
        progress_ = progress().VScreate(SITE_NAME)
        oOutputParameterHandler = cOutputParameterHandler()
        for aEntry in aResult[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break
 
            sTitle = (cUtil().CleanMovieName(aEntry[1])).replace('الحلقة ','E').replace('حلقة ','E')
            sTitle = cUtil().ConvertSeasons(sTitle)
            siteUrl = aEntry[0]
            sThumb = aEntry[2]
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
			
            oGui.addTV(SITE_IDENTIFIER, 'showSeasons', sTitle, '', sThumb, sDesc, oOutputParameterHandler)

        progress_.VSclose(progress_)

    if not sSearch:
        sNextPage = __checkForNextPage(sHtmlContent)
        if sNextPage:
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sNextPage)
            oGui.addDir(SITE_IDENTIFIER, 'showSeries', '[COLOR teal]Next >>>[/COLOR]', 'next.png', oOutputParameterHandler)
 
        oGui.setEndOfDirectory()

def showSeasons():
	oGui = cGui()
    
	oInputParameterHandler = cInputParameterHandler()
	sUrl = oInputParameterHandler.getValue('siteUrl')
	sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
	sThumb = oInputParameterHandler.getValue('sThumb')

	oParser = cParser()
	oRequestHandler = cRequestHandler(sUrl)
	sHtmlContent = oRequestHandler.request()

	sPattern = '<div class="Small--Box Season">.+?href="([^"]+)" title.+?<span>الموسم</span>(.+?)</div>'
	sPattern += '.+?data-src(.+?)</div>'
	aResult = oParser.parse(sHtmlContent, sPattern)	
	if aResult[0] is True:
		oOutputParameterHandler = cOutputParameterHandler()
		for aEntry in aResult[1]:
 
			sTitle = f'{sMovieTitle} S{aEntry[1]}'
			siteUrl = aEntry[0]
			sThumb = aEntry[2].replace('=','')
			sDesc = ""
			
			oOutputParameterHandler.addParameter('siteUrl', siteUrl)
			oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
			oOutputParameterHandler.addParameter('sThumb', sThumb)
			oGui.addSeason(SITE_IDENTIFIER, 'showEpisodes', sTitle, '', sThumb, sDesc, oOutputParameterHandler)
        
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

	sStart = '<section class="tabContents">'
	sEnd = '</section>'
	sHtmlContent = oParser.abParse(sHtmlContent, sStart, sEnd)   

	sPattern = 'href="([^"]+)".+?class="epnum">.+?<span>الحلقة</span>(.+?)</div>'
	aResult = oParser.parse(sHtmlContent, sPattern)
	if aResult[0] is True:
		oOutputParameterHandler = cOutputParameterHandler()
		for aEntry in aResult[1]:
 
			sTitle = f'{sMovieTitle} E{aEntry[1].replace("E ","E")}'
			siteUrl = f'{aEntry[0]}/watch/'
			sThumb = ""
			sDesc = ""
			
			oOutputParameterHandler.addParameter('siteUrl', siteUrl)
			oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
			oOutputParameterHandler.addParameter('sThumb', sThumb)
			oGui.addEpisode(SITE_IDENTIFIER, 'showLinks', sTitle, '', sThumb, sDesc, oOutputParameterHandler)
        
	oGui.setEndOfDirectory()
  
def __checkForNextPage(sHtmlContent):
    oParser = cParser()    
    sPattern = '<li class="active"><a href=.+?<a href="(.+?)"'	
    aResult = oParser.parse(sHtmlContent, sPattern)
    if aResult[0]:
        return aResult[1][0]

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
          
    sPattern = 'data-id="(.+?)" data-server="([^"]+)".+?<span>(.+?)</span>'
    aResult = oParser.parse(sHtmlContent, sPattern)
    if aResult[0]:
        oOutputParameterHandler = cOutputParameterHandler()
        for aEntry in aResult[1]:  

            Serv = aEntry[1]
            Sid = aEntry[0]
            sHost = aEntry[2]
            sTitle = f'{sMovieTitle} [COLOR coral]{sHost}[/COLOR]'

            oOutputParameterHandler.addParameter('siteUrl', sUrl)
            oOutputParameterHandler.addParameter('Serv', Serv)
            oOutputParameterHandler.addParameter('Sid', Sid)
            oOutputParameterHandler.addParameter('sMovieTitle', sMovieTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oOutputParameterHandler.addParameter('sHost', sHost)

            oGui.addLink(SITE_IDENTIFIER, 'showHosters', sTitle, sThumb, sTitle, oOutputParameterHandler)

    oRequestHandler = cRequestHandler(sUrl.replace('/watch','/download'))
    oRequestHandler.addHeaderEntry('User-Agent', UA)
    oRequestHandler.addHeaderEntry('Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8')
    oRequestHandler.addHeaderEntry('X-Requested-With', 'XMLHttpRequest')
    oRequestHandler.addHeaderEntry('Accept-Language', 'fr,fr-FR;q=0.8,en-US;q=0.5,en;q=0.3')
    sHtmlContent = oRequestHandler.request()

    sStart = '<div class="DownloadBox">'
    sEnd = '<script'
    sHtmlContent = oParser.abParse(sHtmlContent, sStart, sEnd) 

    sPattern = 'href="([^"]+)".+?<span>(.+?)</span>'
    aResult = oParser.parse(sHtmlContent, sPattern)
    if aResult[0]:
        oOutputParameterHandler = cOutputParameterHandler()
        for aEntry in aResult[1]:  
            if URL_MAIN in aEntry[0]:
                continue

            sHosterUrl = aEntry[0]

            if any(sHost in sHosterUrl for sHost in ['vidtube', 'vidhidepro', 'updown', 'ma2d', 'katomen']):
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