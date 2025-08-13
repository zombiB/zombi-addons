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

UA = random_ua.get_phone_ua()
 
SITE_IDENTIFIER = 'qfilm'
SITE_NAME = 'Q-Film'
SITE_DESC = 'arabic vod'

URL_MAIN = siteManager().getUrlMain(SITE_IDENTIFIER)

MOVIE_EN = (f'{URL_MAIN}category.php?cat=english-movies', 'showMovies')
MOVIE_AR = (f'{URL_MAIN}category.php?cat=arabic-movies', 'showMovies')
MOVIE_TURK = (f'{URL_MAIN}category.php?cat=turkish-movies', 'showMovies')
MOVIE_HI = (f'{URL_MAIN}category.php?cat=indian-movies', 'showMovies')
MOVIE_ASIAN = (f'{URL_MAIN}category.php?cat=asian-movies', 'showMovies')
ANIM_MOVIES = (f'{URL_MAIN}category.php?cat=anime-movies', 'showMovies')
MOVIE_DUBBED = (f'{URL_MAIN}category.php?cat=dubbed-movies', 'showMovies')
MOVIE_GENRES = (True, 'moviesGenres')

URL_SEARCH = (f'{URL_MAIN}search.php?keywords=', 'showSeries')
URL_SEARCH_MOVIES = (f'{URL_MAIN}search.php?keywords=', 'showMovies')
FUNCTION_SEARCH = 'showSearch'
 
def load():
    oGui = cGui()
    addons = addon()

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', URL_SEARCH[0])
    oGui.addDir(SITE_IDENTIFIER, 'showSearch', addons.VSlang(30078), '1/Search.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', MOVIE_EN[0])
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'أفلام أجنبية', '1/Movies.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', MOVIE_AR[0])
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'أفلام عربية', '1/Arabic.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', MOVIE_HI[0])
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'أفلام هندية', '1/Hindi.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', MOVIE_TURK[0])
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'أفلام تركية', '1/Turkish.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', MOVIE_ASIAN[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_ASIAN[1], 'افلام آسيوية', '1/Asian.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', ANIM_MOVIES[0])
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'أفلام انيميشن', '1/1/Anime.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', f'{URL_MAIN}category.php?cat=adult-movies')
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'للكبار فقط +18', '1/Movies.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', MOVIE_GENRES[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_GENRES[1], 'الأفلام (الأنواع)', '1/Movies.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()
 
def showSearch():
    oGui = cGui()
 
    sSearchText = oGui.showKeyBoard()
    if sSearchText:
        sUrl = f'{URL_MAIN}search.php?keywords={sSearchText}'
        showMovies(sUrl)
        oGui.setEndOfDirectory()
        return

def moviesGenres():
    oGui = cGui()

    liste = []
    liste.append(['اكشن', f'{URL_MAIN}category.php?cat=action-movies'])
    liste.append(['انيميشن', f'{URL_MAIN}category.php?cat=anime-movies'])
    liste.append(['مغامرات', f'{URL_MAIN}category.php?cat=adventure-movies'])
    liste.append(['غموض', f'{URL_MAIN}category.php?cat=mystery-movies'])
    liste.append(['تاريخي', f'{URL_MAIN}category.php?cat=historical-movies'])
    liste.append(['كوميديا', f'{URL_MAIN}category.php?cat=comedy-movies'])
    liste.append(['موسيقى', f'{URL_MAIN}category.php?cat=musical-movies'])
    liste.append(['سيرة ذاتية', f'{URL_MAIN}category.php?cat=biography-movies'])
    liste.append(['دراما', f'{URL_MAIN}category.php?cat=drama-movies'])
    liste.append(['رعب', f'{URL_MAIN}category.php?cat=horror-movies'])
    liste.append(['عائلى', f'{URL_MAIN}category.php?cat=family-movies'])
    liste.append(['فانتازيا', f'{URL_MAIN}category.php?cat=fantasy-movies'])
    liste.append(['حروب', f'{URL_MAIN}category.php?cat=war-movies'])
    liste.append(['الجريمة', f'{URL_MAIN}category.php?cat=crime-movies'])
    liste.append(['رومانسى', f'{URL_MAIN}category.php?cat=romance-movies'])
    liste.append(['خيال علمى', f'{URL_MAIN}category.php?cat=sci-fi-movies'])
    liste.append(['اثارة', f'{URL_MAIN}category.php?cat=thriller-movies'])
    liste.append(['وثائقى', f'{URL_MAIN}category.php?cat=documentary-movies'])

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

    sPattern = '<div class="thumbnail">.+?<a href=["\']([^"\']+)["\']\s*title=["\']([^"\']+)["\'].+?data-echo=["\']([^"\']+)'
    aResult = oParser.parse(sHtmlContent, sPattern)
    if aResult[0] :
        total = len(aResult[1])
        progress_ = progress().VScreate(SITE_NAME)
        oOutputParameterHandler = cOutputParameterHandler()
        for aEntry in aResult[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break 
            
            sTitle = cUtil().CleanMovieName(aEntry[1])
            siteUrl = aEntry[0].replace("watch.php","view.php")
            sDesc = ""
            sThumb = aEntry[2]
            sYear = ''
            m = re.search('([0-9]{4})', sTitle)
            if m:
                sYear = str(m.group(0))

            oOutputParameterHandler.addParameter('siteUrl',siteUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oOutputParameterHandler.addParameter('sYear', sYear)
            oOutputParameterHandler.addParameter('sDesc', sDesc)

            oGui.addMovie(SITE_IDENTIFIER, 'showHosters', sTitle, '', sThumb, sDesc, oOutputParameterHandler)

        progress_.VSclose(progress_)
 
        sNextPage = __checkForNextPage(sHtmlContent)
        if sNextPage:
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sNextPage)
            oGui.addDir(SITE_IDENTIFIER, 'showMovies', '[COLOR teal]Next >>>[/COLOR]', 'next.png', oOutputParameterHandler)

        progress_.VSclose(progress_)
 
    if not sSearch:
        oGui.setEndOfDirectory()

def __checkForNextPage(sHtmlContent):
    oParser = cParser()
    sPattern = '<li class="active"><a href="#".+?<li class><a href="([^"]+)'
    aResult = oParser.parse(sHtmlContent, sPattern)
    if aResult[0] :      
        return URL_MAIN+aResult[1][0]

    return False
	 
def showHosters():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')

    oParser = cParser()
    oRequestHandler = cRequestHandler(sUrl)
    oRequestHandler.addHeaderEntry('User-Agent', UA)
    sHtmlContent = oRequestHandler.request()     

    sPattern = '<iframe src=["\']([^"\']+)["\']'
    aResult = oParser.parse(sHtmlContent, sPattern)
    if aResult[0] :
        for aEntry in aResult[1]:
            
            sHosterUrl = aEntry
            if sHosterUrl.startswith('//'):
                sHosterUrl = f'http:{sHosterUrl}'
            if 'qvid' in sHosterUrl or 'filmey' in sHosterUrl:
                oRequestHandler = cRequestHandler(sHosterUrl)
                oRequestHandler.addHeaderEntry('User-Agent', UA)
                sHtmlContent = oRequestHandler.request()  
                
                sPattern = 'href="([^"]+)" role="button">(.+?)</a>'
                aResult = oParser.parse(sHtmlContent, sPattern)
                if aResult[0] :
                    oOutputParameterHandler = cOutputParameterHandler()
                    for aEntry in aResult[1]:
                        sLink = aEntry[0]
                        sServer = aEntry[1]
                        
                        sDisplayTitle = f'{sMovieTitle} [COLOR orange] - {sServer}[/COLOR]'   
                        oOutputParameterHandler.addParameter('sHosterUrl', sLink)
                        oOutputParameterHandler.addParameter('siteUrl', sUrl)
                        oOutputParameterHandler.addParameter('sMovieTitle', sMovieTitle)
                        oOutputParameterHandler.addParameter('sThumb', sThumb)

                        oGui.addLink(SITE_IDENTIFIER, 'showLinks', sDisplayTitle, sThumb, '', oOutputParameterHandler)
            else:
                if 'userload' in sHosterUrl:
                    sHosterUrl = f'{sHosterUrl}|Referer={URL_MAIN}'
 
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
    oRequestHandler.addHeaderEntry('User-Agent', UA)
    sHtmlContent = oRequestHandler.request()     

    sPattern = '<iframe src=["\']([^"\']+)["\']'
    aResult = oParser.parse(sHtmlContent, sPattern)
    if aResult[0] :
        for aEntry in aResult[1]:
            
            sHosterUrl = aEntry  
            oHoster = cHosterGui().checkHoster(sHosterUrl)
            if oHoster:
                oHoster.setDisplayName(sMovieTitle)
                oHoster.setFileName(sMovieTitle)
                cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb)

    oGui.setEndOfDirectory()