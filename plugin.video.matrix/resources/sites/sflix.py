# -*- coding: utf-8 -*-

import re
from urllib.parse import quote_plus
# from Cryptodome.Cipher import AES
# from Cryptodome.Util.Padding import unpad
from resources.lib.gui.hoster import cHosterGui
from resources.lib.gui.gui import cGui
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.lib.comaddon import progress, VSlog, siteManager, addon
from resources.lib.util import urlHostName

SITE_IDENTIFIER = 'sflix'
SITE_NAME = 'sFlix'
SITE_DESC = 'english vod'

URL_MAIN = siteManager().getUrlMain(SITE_IDENTIFIER)

MOVIE_EN = (f'{URL_MAIN}/movie', 'showMovies')
KID_MOVIES = (f'{URL_MAIN}/filter?type=movie&quality=all&release_year=all&genre=3&country=all', 'showMovies')
MOVIE_GENRES = (True, 'moviesGenres')
SERIE_EN = (f'{URL_MAIN}/tv-show', 'showSeries')
ANIM_NEWS = (f'{URL_MAIN}/filter?type=tv&quality=all&release_year=all&genre=3&country=all', 'showSeries')
SERIE_GENRES = (True, 'seriesGenres')

URL_SEARCH_MOVIES = (f'{URL_MAIN}/search/', 'showMovies')
URL_SEARCH_SERIES = (f'{URL_MAIN}/search/', 'showSeries')
FUNCTION_SEARCH = 'showMovies'
	
def load():
    oGui = cGui()
    addons = addon()

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'http://venom/')
    oGui.addDir(SITE_IDENTIFIER, 'showSearch', addons.VSlang(30078), '1/Search.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', 'http://venom/')
    oGui.addDir(SITE_IDENTIFIER, 'showSeriesSearch', addons.VSlang(30079), '1/Search.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', f'{URL_MAIN}/home')
    oGui.addDir(SITE_IDENTIFIER, 'showHome', 'محتوى الصفحة الرئيسية', '1/Movies.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', MOVIE_EN[0])
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'أفلام أجنبية', '1/Movies.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', KID_MOVIES[0])
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'أفلام انيميشن', '1/1/Anime.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', SERIE_EN[0])
    oGui.addDir(SITE_IDENTIFIER, 'showSeries', 'مسلسلات أجنبية', '1/Movies.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', ANIM_NEWS[0])
    oGui.addDir(SITE_IDENTIFIER, 'showSeries', 'مسلسلات انيميشن', '1/Anime.png', oOutputParameterHandler)  

    oOutputParameterHandler.addParameter('siteUrl', SERIE_GENRES[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_GENRES[1], 'المسلسلات (الأنواع)', '1/TVShows.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', MOVIE_GENRES[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_GENRES[1], 'الأفلام (الأنواع)', '1/Movies.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()

def showSearch():
    oGui = cGui()
    sSearchText = oGui.showKeyBoard()
    if sSearchText:
        sUrl = f"{URL_MAIN}/search/{sSearchText.replace(' ','-')}"
        showMovies(sUrl)
        oGui.setEndOfDirectory()
        return  
    
def showSeriesSearch():
    oGui = cGui()
    sSearchText = oGui.showKeyBoard()
    if sSearchText:
        sUrl = f"{URL_MAIN}/search/{sSearchText.replace(' ','-')}"
        showSeries(sUrl)
        oGui.setEndOfDirectory()
        return  

def seriesGenres():
    oGui = cGui()

    liste = []
    liste.append(['Action', f'{URL_MAIN}/filter?type=tv&quality=all&release_year=all&genre=10&country=all'])
    liste.append(['Adventure', f'{URL_MAIN}/filter?type=tv&quality=all&release_year=all&genre=18&country=all'])
    liste.append(['Animated', f'{URL_MAIN}/filter?type=tv&quality=all&release_year=all&genre=3&country=all'])
    liste.append(['Biography', f'{URL_MAIN}/filter?type=tv&quality=all&release_year=all&genre=37&country=all'])
    liste.append(['Comedy', f'{URL_MAIN}/filter?type=tv&quality=all&release_year=all&genre=7&country=all'])
    liste.append(['Crime', f'{URL_MAIN}/filter?type=tv&quality=all&release_year=all&genre=2&country=all'])
    liste.append(['Drama', f'{URL_MAIN}/filter?type=tv&quality=all&release_year=all&genre=4&country=all'])
    liste.append(['Documentary', f'{URL_MAIN}/filter?type=tv&quality=all&release_year=all&genre=11&country=all'])
    liste.append(['Fantasy', f'{URL_MAIN}/filter?type=tv&quality=all&release_year=all&genre=13&country=all'])
    liste.append(['History', f'{URL_MAIN}/filter?type=tv&quality=all&release_year=all&genre=19&country=all'])
    liste.append(['Horror', f'{URL_MAIN}/filter?type=tv&quality=all&release_year=all&genre=14&country=all'])
    liste.append(['Music', f'{URL_MAIN}/filter?type=tv&quality=all&release_year=all&genre=15&country=all'])
    liste.append(['Mystery', f'{URL_MAIN}/filter?type=tv&quality=all&release_year=all&genre=1&country=all'])
    liste.append(['Romance', f'{URL_MAIN}/filter?type=tv&quality=all&release_year=all&genre=12&country=all'])
    liste.append(['Sci-Fi', f'{URL_MAIN}/filter?type=tv&quality=all&release_year=all&genre=5&country=all'])
    liste.append(['Thriller', f'{URL_MAIN}/filter?type=tv&quality=all&release_year=all&genre=16&country=all'])
    liste.append(['War', f'{URL_MAIN}/filter?type=tv&quality=all&release_year=all&genre=28&country=all'])
    liste.append(['Western', f'{URL_MAIN}/filter?type=tv&quality=all&release_year=all&genre=6&country=all'])

    for sTitle, sUrl in liste:
        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', sUrl)
        oGui.addDir(SITE_IDENTIFIER, 'showSeries', sTitle, 'genres.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()

def moviesGenres():
    oGui = cGui()

    liste = []
    liste.append(['Action', f'{URL_MAIN}/filter?type=movie&quality=all&release_year=all&genre=10&country=all'])
    liste.append(['Adventure', f'{URL_MAIN}/filter?type=movie&quality=all&release_year=all&genre=18&country=all'])
    liste.append(['Animated', f'{URL_MAIN}/filter?type=movie&quality=all&release_year=all&genre=3&country=all'])
    liste.append(['Biography', f'{URL_MAIN}/filter?type=movie&quality=all&release_year=all&genre=37&country=all'])
    liste.append(['Comedy', f'{URL_MAIN}/filter?type=movie&quality=all&release_year=all&genre=7&country=all'])
    liste.append(['Crime', f'{URL_MAIN}/filter?type=movie&quality=all&release_year=all&genre=2&country=all'])
    liste.append(['Drama', f'{URL_MAIN}/filter?type=movie&quality=all&release_year=all&genre=4&country=all'])
    liste.append(['Documentary', f'{URL_MAIN}/filter?type=movie&quality=all&release_year=all&genre=11&country=all'])
    liste.append(['Fantasy', f'{URL_MAIN}/filter?type=movie&quality=all&release_year=all&genre=13&country=all'])
    liste.append(['History', f'{URL_MAIN}/filter?type=movie&quality=all&release_year=all&genre=19&country=all'])
    liste.append(['Horror', f'{URL_MAIN}/filter?type=movie&quality=all&release_year=all&genre=14&country=all'])
    liste.append(['Music', f'{URL_MAIN}/filter?type=movie&quality=all&release_year=all&genre=15&country=all'])
    liste.append(['Mystery', f'{URL_MAIN}/filter?type=movie&quality=all&release_year=all&genre=1&country=all'])
    liste.append(['Romance', f'{URL_MAIN}/filter?type=movie&quality=all&release_year=all&genre=12&country=all'])
    liste.append(['Sci-Fi', f'{URL_MAIN}/filter?type=movie&quality=all&release_year=all&genre=5&country=all'])
    liste.append(['Thriller', f'{URL_MAIN}/filter?type=movie&quality=all&release_year=all&genre=16&country=all'])
    liste.append(['War', f'{URL_MAIN}/filter?type=movie&quality=all&release_year=all&genre=28&country=all'])
    liste.append(['Western', f'{URL_MAIN}/filter?type=movie&quality=all&release_year=all&genre=6&country=all'])

    for sTitle, sUrl in liste:
        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', sUrl)
        oGui.addDir(SITE_IDENTIFIER, 'showMovies', sTitle, 'genres.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()

def showHome():
    oGui = cGui()
      
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')

    oParser = cParser()
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    sStart = '>Trending</h2>'
    sEnd = '</section>'
    sHtmlContent0 = oParser.abParse(sHtmlContent, sStart, sEnd)

    oGui.addText(SITE_IDENTIFIER, u'\u2193' + 'Trending', 'pop.png')

    sPattern = '<div class="film-poster">.+?<img data-src="([^"]+)".+?<a href="([^"]+)".+?title="([^"]+)'
    aResult = oParser.parse(sHtmlContent0, sPattern)
    if aResult[0]:
        total = len(aResult[1])
        progress_ = progress().VScreate(SITE_NAME)
        oOutputParameterHandler = cOutputParameterHandler()    
        for aEntry in aResult[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break
            
            sTitle = aEntry[2]
            siteUrl = f'{URL_MAIN}{aEntry[1]}'
            siteUrl = siteUrl.replace('movie','watch-movie')
            sThumb = aEntry[0]
            sDesc = ''
            sYear = ''

            oOutputParameterHandler.addParameter('siteUrl', siteUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oOutputParameterHandler.addParameter('sYear', sYear)
            oOutputParameterHandler.addParameter('sDesc', sDesc)

            if "tv/"  in aEntry[1]:
                oGui.addTV(SITE_IDENTIFIER, 'showSeasons', sTitle, '', sThumb, sDesc, oOutputParameterHandler)
            else:
                oGui.addTV(SITE_IDENTIFIER, 'showLinks', sTitle, '', sThumb, sDesc, oOutputParameterHandler)

        progress_.VSclose(progress_)

    sStart = '>Latest Movies</h2>'
    sEnd = '</section>'
    sHtmlContent0 = oParser.abParse(sHtmlContent, sStart, sEnd)

    oGui.addText(SITE_IDENTIFIER, u'\u2193' + 'Latest Movies', '1/Movies.png')

    sPattern = '<div class="film-poster">.+?<img data-src="([^"]+)".+?<a href="([^"]+)".+?title="([^"]+)'
    aResult = oParser.parse(sHtmlContent0, sPattern)
    if aResult[0]:
        total = len(aResult[1])
        progress_ = progress().VScreate(SITE_NAME)
        oOutputParameterHandler = cOutputParameterHandler()    
        for aEntry in aResult[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break
            
            sTitle = aEntry[2]
            siteUrl = f'{URL_MAIN}{aEntry[1]}'
            siteUrl = siteUrl.replace('movie','watch-movie')
            sThumb = aEntry[0]
            sDesc = ''
            sYear = ''

            oOutputParameterHandler.addParameter('siteUrl', siteUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oOutputParameterHandler.addParameter('sYear', sYear)
            oOutputParameterHandler.addParameter('sDesc', sDesc)

            oGui.addTV(SITE_IDENTIFIER, 'showLinks', sTitle, '', sThumb, sDesc, oOutputParameterHandler)

        progress_.VSclose(progress_)

    sStart = '>Latest TV Shows</h2>'
    sEnd = '</section>'
    sHtmlContent0 = oParser.abParse(sHtmlContent, sStart, sEnd)

    oGui.addText(SITE_IDENTIFIER, u'\u2193' + 'Latest TV Shows', '1/TVShows.png')

    sPattern = '<div class="film-poster">.+?<img data-src="([^"]+)".+?<a href="([^"]+)".+?title="([^"]+)'
    aResult = oParser.parse(sHtmlContent0, sPattern)
    if aResult[0]:
        total = len(aResult[1])
        progress_ = progress().VScreate(SITE_NAME)
        oOutputParameterHandler = cOutputParameterHandler()    
        for aEntry in aResult[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break
            
            sTitle = aEntry[2]
            siteUrl = f'{URL_MAIN}{aEntry[1]}'
            siteUrl = siteUrl.replace('movie','watch-movie')
            sThumb = aEntry[0]
            sDesc = ''
            sYear = ''

            oOutputParameterHandler.addParameter('siteUrl', siteUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oOutputParameterHandler.addParameter('sYear', sYear)
            oOutputParameterHandler.addParameter('sDesc', sDesc)

            oGui.addTV(SITE_IDENTIFIER, 'showSeasons', sTitle, '', sThumb, sDesc, oOutputParameterHandler)

        progress_.VSclose(progress_)

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
    sHtmlContent = oRequestHandler.request()

    sPattern = '<div class="film-poster">.+?<img data-src="([^"]+)".+?<a href="([^"]+)".+?title="([^"]+)'
    aResult = oParser.parse(sHtmlContent, sPattern)
    if aResult[0]:
        total = len(aResult[1])
        progress_ = progress().VScreate(SITE_NAME)
        oOutputParameterHandler = cOutputParameterHandler()    
        for aEntry in aResult[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break
            if "tv/"  in aEntry[1]:
                continue

            sTitle = aEntry[2]
            siteUrl = f'{URL_MAIN}{aEntry[1]}'
            siteUrl = siteUrl.replace('movie','watch-movie')
            sThumb = aEntry[0]
            sDesc = ''
            sYear = ''

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
    sHtmlContent = oRequestHandler.request()

    sPattern = '<div class="film-poster">.+?<img data-src="([^"]+)".+?<a href="([^"]+)".+?title="([^"]+)'
    aResult = oParser.parse(sHtmlContent, sPattern)
    if aResult[0]:
        total = len(aResult[1])
        progress_ = progress().VScreate(SITE_NAME)
        oOutputParameterHandler = cOutputParameterHandler()    
        for aEntry in aResult[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break
            if "movie/"  in aEntry[1]:
                continue

            sTitle = aEntry[2]
            siteUrl = f'{URL_MAIN}{aEntry[1]}'
            sThumb = aEntry[0]
            sDesc = ''
            sYear = ''

            oOutputParameterHandler.addParameter('siteUrl', siteUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oOutputParameterHandler.addParameter('sYear', sYear)
            oOutputParameterHandler.addParameter('sDesc', sDesc)

            oGui.addTV(SITE_IDENTIFIER, 'showSeasons', sTitle, '', sThumb, sDesc, oOutputParameterHandler)

        progress_.VSclose(progress_)
 
        sNextPage = __checkForNextPage(sHtmlContent)
        if sNextPage:
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sNextPage)
            oGui.addDir(SITE_IDENTIFIER, 'showSeries', '[COLOR teal]Next >>>[/COLOR]', 'next.png', oOutputParameterHandler)
 
    if not sSearch:
        oGui.setEndOfDirectory()  

def showSeasons():
    oGui = cGui()

    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')
    sUrl2 = sUrl

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    oParser = cParser()
    sPattern = 'data-id="(.+?)"'
    aResult = oParser.parse(sHtmlContent, sPattern)
    if aResult[0]:
        oOutputParameterHandler = cOutputParameterHandler()    
        for aEntry in aResult[1]:

            sId = aEntry
            sUrl = f'{URL_MAIN}/ajax/season/list/{sId}'

            oRequestHandler = cRequestHandler(sUrl)
            sHtmlContent = oRequestHandler.request()

            sPattern = '<a data-id="([^"]+)".+?class="dropdown-item ss-item.+?href="([^"]+)">(.+?)</a>'
            aResult = oParser.parse(sHtmlContent, sPattern)
            if aResult[0]:
                oOutputParameterHandler = cOutputParameterHandler()    
                for aEntry in aResult[1]:
                    sSeason = aEntry[2].replace('Season ','S')
                    sTitle = f'{sMovieTitle} {sSeason}'
                    siteUrl = f'{URL_MAIN}/ajax/season/episodes/{aEntry[0]}'
                    sThumb = sThumb
                    sDesc = ''

                    oOutputParameterHandler.addParameter('siteUrl', siteUrl)
                    oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
                    oOutputParameterHandler.addParameter('sThumb', sThumb)
                    oOutputParameterHandler.addParameter('tvUrl',sUrl2)
                    oOutputParameterHandler.addParameter('sDesc', sDesc)

                    oGui.addSeason(SITE_IDENTIFIER, 'showEps', sTitle, '', sThumb, sDesc, oOutputParameterHandler)
 
        oGui.setEndOfDirectory()  
        
def showEps():
    oGui = cGui()
   
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')

    oParser = cParser()
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    sPattern = 'data-id="([^"]+)">.+?<a href="([^"]+)" class="film-poster mb-0">.+?<img src="([^"]+)".+?class="film-poster-img".+?title="([^"]+)'
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
    if aResult[0]:
        oOutputParameterHandler = cOutputParameterHandler()
        for aEntry in aResult[1]:

            siteUrl = f'{URL_MAIN}/ajax/episode/servers/{aEntry[0]}'
            sEpisode = aEntry[3].split(':')[0].replace('Episode ','').replace(':','')
            sEpisode = f"{sMovieTitle}E{int(sEpisode):02d}"
            sTitle = aEntry[3].split(':')[1].replace('Episode','')
            sDisplayTitle = f'{sEpisode} [COLOR coral]{str(sTitle)}[/COLOR]' 
            sThumb = sThumb
            sDesc = ''
			
            oOutputParameterHandler.addParameter('siteUrl', siteUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sDisplayTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oGui.addEpisode(SITE_IDENTIFIER, 'showSeriesLinks', sDisplayTitle, sThumb, sThumb, sDesc, oOutputParameterHandler)
       
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
    oParser = cParser()

    sPattern = 'data-id="(.+?)"'
    aResult = oParser.parse(sHtmlContent, sPattern)
    if aResult[0]:
        for aEntry in aResult[1]:

            sId = aEntry
            sUrl = f'{URL_MAIN}/ajax/episode/list/{sId}'
            oRequestHandler = cRequestHandler(sUrl)
            sHtmlContent = oRequestHandler.request()

    sPattern = 'data-id="([^"]+)".+?<span>(.+?)</span>'
    aResult = oParser.parse(sHtmlContent, sPattern)
    if aResult[0]:
        oOutputParameterHandler = cOutputParameterHandler()
        for aEntry in aResult[1]:
            sId = aEntry[0]
            sHost = aEntry[1]
            sUrl2 = f'{URL_MAIN}/ajax/episode/sources/{sId}'

            sTitle = f'{sMovieTitle} [COLOR coral]{sHost}[/COLOR]'

            oOutputParameterHandler.addParameter('siteUrl', sUrl2)
            oOutputParameterHandler.addParameter('referer', sUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sMovieTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oOutputParameterHandler.addParameter('sHost', sHost)

            oGui.addLink(SITE_IDENTIFIER, 'showHosters', sTitle, sThumb, sTitle, oOutputParameterHandler)

    oGui.setEndOfDirectory()

def showSeriesLinks():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')

    oParser = cParser()    
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    sPattern = 'data-id="([^"]+)".+?<span>(.+?)</span>'
    aResult = oParser.parse(sHtmlContent, sPattern)
    if aResult[0]:
        oOutputParameterHandler = cOutputParameterHandler()
        for aEntry in aResult[1]:
            sId = aEntry[0]
            sHost = aEntry[1]
            sUrl2 = f'{URL_MAIN}/ajax/episode/sources/{sId}'

            sTitle = f'{sMovieTitle} [COLOR coral]{sHost}[/COLOR]'

            oOutputParameterHandler.addParameter('siteUrl', sUrl2)
            oOutputParameterHandler.addParameter('referer', sUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sMovieTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oOutputParameterHandler.addParameter('sHost', sHost)

            oGui.addLink(SITE_IDENTIFIER, 'showHosters', sTitle, sThumb, sTitle, oOutputParameterHandler)

    oGui.setEndOfDirectory()

def showHosters():
    oGui = cGui()

    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')
    sHost = oInputParameterHandler.getValue('sHost')

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    sPattern = '"link":"([^"]+)'
    aResult = re.findall(sPattern, sHtmlContent)
    if aResult:
        sHosterUrl = aResult[0]

        oRequestHandler = cRequestHandler(sHosterUrl)
        oRequestHandler.addHeaderEntry('Referer', sHosterUrl)
        oRequestHandler.addHeaderEntry('X-Requested-With', 'XMLHttpRequest')
        shtml = oRequestHandler.request()

        match = re.search(r'\b[a-zA-Z0-9]{48}\b', shtml) or re.search(r'\b([a-zA-Z0-9]{16})\b.*?\b([a-zA-Z0-9]{16})\b.*?\b([a-zA-Z0-9]{16})\b', shtml)
        nonce = ''.join(match.groups()) if match and match.lastindex == 3 else match.group() if match else None

        sPattern = 'data-id="([^"]+)'
        aResult = re.findall(sPattern, shtml)
        if aResult:
            file_id = aResult[0]

        oRequestHandler = cRequestHandler(f"https://{urlHostName(sHosterUrl)}/embed-1/v3/e-1/getSources?id={file_id}&_k={nonce}")
        oRequestHandler.addHeaderEntry('Referer', sHosterUrl)
        oRequestHandler.addHeaderEntry('X-Requested-With', 'XMLHttpRequest')
        html = oRequestHandler.request(jsonDecode=True)

        sSources = html['sources']

        oRequestHandler = cRequestHandler("https://raw.githubusercontent.com/yogesh-hacker/MegacloudKeys/refs/heads/main/keys.json")
        oRequestHandler.enableCache(False)
        key_data = oRequestHandler.request(jsonDecode=True)
        key = key_data.get("vidstr")

        decode_url = "https://script.google.com/macros/s/AKfycbxHbYHbrGMXYD2-bC-C43D3njIbU-wGiYQuJL61H4vyy6YVXkybMNNEPJNPPuZrD1gRVA/exec"
        if sSources:
            encrypted_data = quote_plus(html['sources'])
            nonce_encoded = quote_plus(nonce)
            key_encoded = quote_plus(key)

            decode_url = f"{decode_url}?encrypted_data={encrypted_data}&nonce={nonce_encoded}&secret={key_encoded}"

            oRequestHandler = cRequestHandler(decode_url)
            response = oRequestHandler.request()

            sHosterUrl = re.search(r'\"file\":\"(.*?)\"', response).group(1) + "|Referer=" + f"https://{urlHostName(sHosterUrl)}/"
        else:
            sHosterUrl = html['sources'][0]['file'] + "|Referer=" + f"https://{urlHostName(sHosterUrl)}/"

        tracks = html['tracks']
        arabic_subtitle = next((track["file"] for track in tracks if "Arabic" in track["label"]), None)
        english_subtitle = next((track["file"] for track in tracks if "English" in track["label"]), None)

        subtitles = arabic_subtitle or english_subtitle or "No subtitles available"

        if subtitles:
            sHosterUrl += f"?sub.info={subtitles}"

        oHoster = cHosterGui().getHoster('streamrapid')
        if oHoster:
            oHoster.setDisplayName(sMovieTitle)
            oHoster.setFileName(sMovieTitle)
            cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb)

    oGui.setEndOfDirectory()

def __checkForNextPage(sHtmlContent):
    oParser = cParser()
    sPattern = 'title="Next" class="page-link" href="([^"]+)"'	
    aResult = oParser.parse(sHtmlContent, sPattern)
    if aResult[0]:
        return URL_MAIN + aResult[1][0]

    return False
