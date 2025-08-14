# -*- coding: utf-8 -*-

import re
from resources.lib.gui.hoster import cHosterGui
from resources.lib.gui.gui import cGui
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.comaddon import progress, VSlog, siteManager, addon
from resources.sites.wecima import showHosters as showCima
from resources.lib.parser import cParser
from resources.lib.util import Quote, cUtil, urlHostName
from resources.lib import random_ua

UA = random_ua.get_ua()

SITE_IDENTIFIER = 'shoffree'
SITE_NAME = 'Shoffree'
SITE_DESC = 'arabic vod'

URL_MAIN = siteManager().getUrlMain(SITE_IDENTIFIER)

MOVIE_EN = (f'{URL_MAIN}movies?lang=الإنجليزية', 'showMovies')
MOVIE_AR = (f'{URL_MAIN}movies?lang=العربية', 'showMovies')
MOVIE_HI = (f'{URL_MAIN}movies?lang=الهندية', 'showMovies')
MOVIE_ASIAN = (f'{URL_MAIN}movies?lang=الكورية', 'showMovies')
MOVIE_TURK = (f'{URL_MAIN}movies?lang=التركية', 'showMovies')
KID_MOVIES = (f'{URL_MAIN}movies?genre=14', 'showMovies')
MOVIE_GENRES = (True, 'moviesGenres')
MOVIE_ANNEES = (f'{URL_MAIN}movies', 'showYears')

RAMADAN_SERIES = (f'{URL_MAIN}ramadan', 'showSeries')
SERIE_EN = (f'{URL_MAIN}series?lang=الإنجليزية', 'showSeries')
SERIE_AR = (f'{URL_MAIN}series?lang=العربية', 'showSeries')
SERIE_TR = (f'{URL_MAIN}series?lang=التركية', 'showSeries')
SERIE_HEND = (f'{URL_MAIN}series?lang=الهندية', 'showSeries')
SERIE_ASIA = (f'{URL_MAIN}series?lang=الكورية', 'showSeries')
SERIE_GENRES = (True, 'seriesGenres')
SERIE_ANNEES = (f'{URL_MAIN}series', 'showSerieYears')

ANIM_NEWS = (f'{URL_MAIN}series?genre=40', 'showSeries')
ANIM_MOVIES = (f'{URL_MAIN}movies?genre=40', 'showMovies')

URL_SEARCH = (f'{URL_MAIN}search?query=', 'showMovies')
URL_SEARCH_MOVIES = (f'{URL_MAIN}search?query=', 'showMovies')
URL_SEARCH_SERIES = (f'{URL_MAIN}search?query=', 'showSeries')
URL_SEARCH_ANIMS = (f'{URL_MAIN}search?query=', 'showSeries')
FUNCTION_SEARCH = 'showMovies'
 
def load():
    oGui = cGui()
    addons = addon()

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'http://venom/')
    oGui.addDir(SITE_IDENTIFIER, 'showSearch', addons.VSlang(30078), '1/Search.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', 'http://venom/')
    oGui.addDir(SITE_IDENTIFIER, 'showSeriesSearch', addons.VSlang(30079), '1/Search.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', RAMADAN_SERIES[0])
    oGui.addDir(SITE_IDENTIFIER, 'showSeries', 'رمضان', '1/Ramadan.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', MOVIE_EN[0])
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'أفلام أجنبية', '1/Movies.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', MOVIE_AR[0])
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'أفلام عربية', '1/Arabic.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', MOVIE_ASIAN[0])
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'أفلام أسيوية', '1/Asian.png', oOutputParameterHandler)
   
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_TURK[0])
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'أفلام تركية', '1/Turkish.png', oOutputParameterHandler)
    
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_HI[0])
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'أفلام هندية', '1/Hindi.png', oOutputParameterHandler) 
 
    oOutputParameterHandler.addParameter('siteUrl', KID_MOVIES[0])
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'أفلام كرتون', 'crtoon.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', SERIE_EN[0])
    oGui.addDir(SITE_IDENTIFIER, 'showSeries', 'مسلسلات أجنبية', '1/Movies.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', SERIE_AR[0])
    oGui.addDir(SITE_IDENTIFIER, 'showSeries', 'مسلسلات عربية', '1/Arabic.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', SERIE_ASIA[0])
    oGui.addDir(SITE_IDENTIFIER, 'showSeries', 'مسلسلات أسيوية', '1/Asian.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', SERIE_TR[0])
    oGui.addDir(SITE_IDENTIFIER, 'showSeries', 'مسلسلات تركية', '1/Turkish.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', SERIE_HEND[0])
    oGui.addDir(SITE_IDENTIFIER, 'showSeries', 'مسلسلات هندية', '1/Hindi.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', ANIM_MOVIES[0])
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'افلام انمي', '1/Anime.png', oOutputParameterHandler)
  
    oOutputParameterHandler.addParameter('siteUrl', ANIM_NEWS[0])
    oGui.addDir(SITE_IDENTIFIER, 'showSeries', 'مسلسلات انمي', '1/Anime.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', SERIE_GENRES[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_GENRES[1], 'المسلسلات (الأنواع)', '1/TVShows.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', MOVIE_GENRES[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_GENRES[1], 'الأفلام (الأنواع)', '1/Movies.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', f'{URL_MAIN}movies')
    oGui.addDir(SITE_IDENTIFIER, 'showYears', 'أفلام (بالسنوات)', '1/Calendar.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', f'{URL_MAIN}series')
    oGui.addDir(SITE_IDENTIFIER, 'showSerieYears', 'مسلسلات (بالسنوات)', '1/Calendar.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', f'{URL_MAIN}movies')
    oGui.addDir(SITE_IDENTIFIER, 'showLang', 'أفلام (حسب اللغة)', '1/Movies.png', oOutputParameterHandler)	

    oOutputParameterHandler.addParameter('siteUrl', f'{URL_MAIN}series')
    oGui.addDir(SITE_IDENTIFIER, 'showSerieLang', 'مسلسلات (حسب اللغة)', '1/TVShows.png', oOutputParameterHandler)	

    oGui.setEndOfDirectory()

def showSearch():
    oGui = cGui()
 
    sSearchText = oGui.showKeyBoard()
    if sSearchText is not False:
        sUrl = f'{URL_MAIN}search?query={sSearchText}'
        showMovies(sUrl)
        oGui.setEndOfDirectory()
        return
 
def showSeriesSearch():
    oGui = cGui()
 
    sSearchText = oGui.showKeyBoard()
    if sSearchText is not False:
        sUrl = f'{URL_MAIN}search?query={sSearchText}'
        showSeries(sUrl)
        oGui.setEndOfDirectory()
        return

def showYears():
    oGui = cGui()
    
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')

    oParser = cParser()
    oRequestHandler = cRequestHandler(URL_MAIN)
    sHtmlContent = oRequestHandler.request()

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    sStart = '<option selected value> السنة </option>'
    sEnd = '</select>'
    sHtmlContent = oParser.abParse(sHtmlContent, sStart, sEnd)

    sPattern = '<option value="([^"]+)"'
    aResult = oParser.parse(sHtmlContent, sPattern)
    if aResult[0]:
        oOutputParameterHandler = cOutputParameterHandler()    
        for aEntry in reversed(aResult[1]):
 
            sYear = aEntry
            oOutputParameterHandler.addParameter('siteUrl', f'{URL_MAIN}movies?year={sYear}') 
            oGui.addDir(SITE_IDENTIFIER, 'showMovies', sYear, '1/Calendar.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()

def showSerieYears():
    oGui = cGui()
    
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')

    oParser = cParser()
    oRequestHandler = cRequestHandler(URL_MAIN)
    sHtmlContent = oRequestHandler.request()

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    sStart = '<option selected value> السنة </option>'
    sEnd = '</select>'
    sHtmlContent = oParser.abParse(sHtmlContent, sStart, sEnd)

    sPattern = '<option value="([^"]+)"'
    aResult = oParser.parse(sHtmlContent, sPattern)	
    if aResult[0]:
        oOutputParameterHandler = cOutputParameterHandler()    
        for aEntry in reversed(aResult[1]):
 
            sYear = aEntry
            oOutputParameterHandler.addParameter('siteUrl', f'{URL_MAIN}series?year={sYear}') 
            oGui.addDir(SITE_IDENTIFIER, 'showSeries', sYear, '1/Calendar.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()

def showLang():
    oGui = cGui()
    
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')

    oParser = cParser()
    oRequestHandler = cRequestHandler(URL_MAIN)
    sHtmlContent = oRequestHandler.request()

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    sStart = '<option selected value> اللغة </option>'
    sEnd = '</select>'
    sHtmlContent = oParser.abParse(sHtmlContent, sStart, sEnd)

    sPattern = '<option value="([^"]+)"'
    aResult = oParser.parse(sHtmlContent, sPattern)
    if aResult[0]:
        oOutputParameterHandler = cOutputParameterHandler()    
        for aEntry in aResult[1]:
 
            sYear = aEntry
            oOutputParameterHandler.addParameter('siteUrl', f'{URL_MAIN}movies?lang={sYear}') 
            oGui.addDir(SITE_IDENTIFIER, 'showMovies', sYear, '1/Calendar.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()

def showSerieLang():
    oGui = cGui()
    
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')

    oParser = cParser()
    oRequestHandler = cRequestHandler(URL_MAIN)
    sHtmlContent = oRequestHandler.request()

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    sStart = '<option selected value> اللغة </option>'
    sEnd = '</select>'
    sHtmlContent = oParser.abParse(sHtmlContent, sStart, sEnd)

    sPattern = '<option value="([^"]+)"'
    aResult = oParser.parse(sHtmlContent, sPattern)
    if aResult[0]:
        oOutputParameterHandler = cOutputParameterHandler()    
        for aEntry in aResult[1]:
 
            sYear = aEntry
            oOutputParameterHandler.addParameter('siteUrl', f'{URL_MAIN}series?lang={sYear}') 
            oGui.addDir(SITE_IDENTIFIER, 'showSeries', sYear, '1/Calendar.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()

def seriesGenres():
    oGui = cGui()

    liste = []
    liste.append(['اكشن', f'{URL_MAIN}series?genre=8'])
    liste.append(['انيميشن', f'{URL_MAIN}series?genre=14'])
    liste.append(['مغامرات', f'{URL_MAIN}series?genre=12'])
    liste.append(['غموض', f'{URL_MAIN}series?genre=7'])
    liste.append(['تاريخي', f'{URL_MAIN}series?genre=28'])
    liste.append(['كوميديا', f'{URL_MAIN}series?genre=16'])
    liste.append(['موسيقى', f'{URL_MAIN}series?genre=20'])
    liste.append(['رياضي', f'{URL_MAIN}series?genre=25'])
    liste.append(['دراما', f'{URL_MAIN}series?genre=6'])
    liste.append(['رعب', f'{URL_MAIN}series?genre=9'])
    liste.append(['عائلى', f'{URL_MAIN}series?genre=15'])
    liste.append(['فانتازيا', f'{URL_MAIN}series?genre=38'])
    liste.append(['حروب', f'{URL_MAIN}series?genre=36'])
    liste.append(['الجريمة', f'{URL_MAIN}series?genre=17'])
    liste.append(['رومانسى', f'{URL_MAIN}series?genre=5'])
    liste.append(['خيال علمى', f'{URL_MAIN}series?genre=13'])
    liste.append(['اثارة', f'{URL_MAIN}series?genre=11'])
    liste.append(['وثائقى', f'{URL_MAIN}series?genre=19'])

    for sTitle, sUrl in liste:

        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', sUrl)
        oGui.addDir(SITE_IDENTIFIER, 'showSeries', sTitle, 'genres.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()

def moviesGenres():
    oGui = cGui()

    liste = []
    liste.append(['اكشن', f'{URL_MAIN}movies?genre=8'])
    liste.append(['انيميشن', f'{URL_MAIN}movies?genre=14'])
    liste.append(['مغامرات', f'{URL_MAIN}movies?genre=12'])
    liste.append(['غموض', f'{URL_MAIN}movies?genre=7'])
    liste.append(['تاريخي', f'{URL_MAIN}movies?genre=28'])
    liste.append(['كوميديا', f'{URL_MAIN}movies?genre=16'])
    liste.append(['موسيقى', f'{URL_MAIN}movies?genre=20'])
    liste.append(['رياضي', f'{URL_MAIN}movies?genre=25'])
    liste.append(['دراما', f'{URL_MAIN}movies?genre=6'])
    liste.append(['رعب', f'{URL_MAIN}movies?genre=9'])
    liste.append(['عائلى', f'{URL_MAIN}movies?genre=15'])
    liste.append(['فانتازيا', f'{URL_MAIN}movies?genre=38'])
    liste.append(['حروب', f'{URL_MAIN}movies?genre=36'])
    liste.append(['الجريمة', f'{URL_MAIN}movies?genre=17'])
    liste.append(['رومانسى', f'{URL_MAIN}movies?genre=5'])
    liste.append(['خيال علمى', f'{URL_MAIN}movies?genre=13'])
    liste.append(['اثارة', f'{URL_MAIN}movies?genre=11'])
    liste.append(['وثائقى', f'{URL_MAIN}movies?genre=19'])

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
    oRequestHandler = cRequestHandler(URL_MAIN)
    sHtmlContent = oRequestHandler.request()

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    sPattern = '<div class="BlockItem.+?<a href="(.+?)" title="(.+?)">.+?data-src="(.+?)" alt='
    aResult = oParser.parse(sHtmlContent, sPattern)
    if aResult[0] is True:
        total = len(aResult[1])
        progress_ = progress().VScreate(SITE_NAME)
        oOutputParameterHandler = cOutputParameterHandler() 
        for aEntry in aResult[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break
            if 'serie/' in aEntry[0] or 'episode/' in aEntry[0]:
                continue 

            sTitle = cUtil().CleanMovieName(aEntry[1])
            siteUrl = aEntry[0]
            sThumb = aEntry[2].replace('/w342','/w500')
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
			
            oGui.addMovie(SITE_IDENTIFIER, 'showHosters', sTitle, '', sThumb, sDesc, oOutputParameterHandler)

        progress_.VSclose(progress_)
 
        sNextPage = __checkForNextPage(sHtmlContent, sUrl)
        if sNextPage != False:
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
    oRequestHandler = cRequestHandler(URL_MAIN)
    sHtmlContent = oRequestHandler.request()

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    sPattern = '<div class="BlockItem.+?<a href="(.+?)" title="(.+?)">.+?data-src="(.+?)" alt='
    aResult = oParser.parse(sHtmlContent, sPattern)
    itemList = []		
    if aResult[0] is True:
        total = len(aResult[1])
        progress_ = progress().VScreate(SITE_NAME)
        oOutputParameterHandler = cOutputParameterHandler() 
        for aEntry in aResult[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break
            if 'movie/' in aEntry[0]:
                continue 
 
            sTitle = cUtil().CleanSeriesName(aEntry[1])
            siteUrl = aEntry[0]
            sThumb = aEntry[2].replace('/w342','/w500')
            sDesc = ''

            if sTitle not in itemList:
                itemList.append(sTitle)	
                oOutputParameterHandler.addParameter('siteUrl', siteUrl)
                oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
                oOutputParameterHandler.addParameter('sThumb', sThumb)
                oOutputParameterHandler.addParameter('sDesc', sDesc)
                oGui.addTV(SITE_IDENTIFIER, 'showSeasons', sTitle, '', sThumb, sDesc, oOutputParameterHandler)

        progress_.VSclose(progress_)

        sNextPage = __checkForNextPage(sHtmlContent, sUrl)
        if sNextPage != False:
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
    oParser = cParser()
 
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    sStart = '>المواسم</div>'
    sEnd = '<section class="text-center"'
    sHtmlContent1 = oParser.abParse(sHtmlContent, sStart, sEnd)

    sPattern = '<a href="(.+?)" title="(.+?)">.+?data-src="(.+?)" alt='
    aResult = oParser.parse(sHtmlContent1, sPattern) 
    if aResult[0] is True:
        oOutputParameterHandler = cOutputParameterHandler() 
        for aEntry in aResult[1]:
            sTitle = (cUtil().ConvertSeasons(aEntry[1])).replace("-"," ")
            siteUrl = aEntry[0]
            sThumb = aEntry[2].replace('/w342','/w500')
            sDesc = ""

            oOutputParameterHandler.addParameter('siteUrl', siteUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sMovieUrl', sUrl)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oGui.addSeason(SITE_IDENTIFIER, 'showEps', sTitle, '', sThumb, sDesc, oOutputParameterHandler)

    else:
        sPattern = '<a class="sku" href="(.+?)">(.+?)<em>(.+?)</em>'
        aResult = oParser.parse(sHtmlContent, sPattern)
        if aResult[0] is True:
            oOutputParameterHandler = cOutputParameterHandler() 
            for aEntry in aResult[1]:

                sTitle = f'{sMovieTitle} E{aEntry[2].replace(" ","")}'
                siteUrl = aEntry[0]
                sThumb = sThumb
                sDesc = ''
                sHost = ''

                oOutputParameterHandler.addParameter('siteUrl', siteUrl)
                oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
                oOutputParameterHandler.addParameter('sHost', sHost)
                oOutputParameterHandler.addParameter('sThumb', sThumb)
 
                oGui.addEpisode(SITE_IDENTIFIER, 'showHosters', sTitle, '', sThumb, sDesc, oOutputParameterHandler)

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

    sPattern = '<a class="sku" href="(.+?)">(.+?)<em>(.+?)</em>'
    aResult = oParser.parse(sHtmlContent, sPattern)
    if aResult[0] is True:
        oOutputParameterHandler = cOutputParameterHandler() 
        for aEntry in aResult[1]:

            sTitle = f'{sMovieTitle} E{aEntry[2].replace(" ","")}'
            siteUrl = aEntry[0]
            sThumb = sThumb
            sDesc = ''
            sHost = ''

            oOutputParameterHandler.addParameter('siteUrl', siteUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sHost', sHost)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
 
            oGui.addEpisode(SITE_IDENTIFIER, 'showHosters', sTitle, '', sThumb, sDesc, oOutputParameterHandler)
       
    oGui.setEndOfDirectory() 
 
def __checkForNextPage(sHtmlContent, sUrl):
    oParser = cParser()
    sPattern = '<a class="page-link" href="([^"]+)">التالي</a>'
    aResult = oParser.parse(sHtmlContent, sPattern)
    if aResult[0]:
        return f'{sUrl}&{aResult[1][0]}'

    return False

def showHosters():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')

    if 'movie' in sUrl:
        sUrl = sUrl.rsplit("/",1)[0] + '/single-movie?watch=1'
    oParser = cParser()
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    sPattern =  '<form action="([^"]+)' 
    aResult = oParser.parse(sHtmlContent,sPattern)
    if aResult[0]:
        maction = aResult[1][0] 

        sPattern =  'name="url" value="([^"]+)' 
        aResult = oParser.parse(sHtmlContent,sPattern)
        if aResult[0]:
            for aEntry in aResult[1]:
                murl = aEntry

                sUrl2 = f'{maction}?id={murl}'
                oRequestHandler = cRequestHandler(sUrl2)
                sHtmlContent = oRequestHandler.request()

    sPattern =  'name="key" value="([^"]+)' 
    aResult = oParser.parse(sHtmlContent,sPattern)
    if aResult[0]:
        mkey = aResult[1][0] 

        oRequestHandler = cRequestHandler(sUrl)
        oRequestHandler.addHeaderEntry('User-Agent', UA)
        oRequestHandler.addHeaderEntry('Referer', f'https://{urlHostName(maction)}/')
        oRequestHandler.addHeaderEntry('Origin', f'https://{urlHostName(maction)}')
        oRequestHandler.addHeaderEntry('Host', urlHostName(sUrl))
        oRequestHandler.addParameters('key', mkey)
        oRequestHandler.setRequestType(1)
        sHtmlContent = oRequestHandler.request()

    sPattern = 'data-embed="([^"]+)'
    aResult = oParser.parse(sHtmlContent, sPattern)
    if aResult[0]:
        for aEntry in aResult[1]:
            url = aEntry
            if '?url' in url:
                url = url.split('?url=')[1]
            if 'shofcd' in url or 'shoffree' in url:
                try:
                    from urllib.parse import urlparse, parse_qs
                    import base64
                    sMain = siteManager().getUrlMain('wecima')
                    sKey = parse_qs(urlparse(url).query)['key'][0]
                    eUrl = f'{sMain}watch/' + base64.b64decode(sKey).decode("utf-8") + '/'

                    oOutputParameterHandler = cOutputParameterHandler()

                    oOutputParameterHandler.addParameter('siteUrl', eUrl)
                    oOutputParameterHandler.addParameter('sMovieTitle', sMovieTitle)
                    oOutputParameterHandler.addParameter('sThumb', sThumb)
                    oGui.addMovie(SITE_IDENTIFIER, 'showCima', f'{sMovieTitle} [COLOR gold] - سيرفر خاص[/COLOR]', '', sThumb, '', oOutputParameterHandler)

                except:
                    url = ''
            
            else:
                sHosterUrl = url
                if 'userload' in sHosterUrl:
                    sHosterUrl = f'{sHosterUrl}|Referer={URL_MAIN}'
                if 'shoffree' in sHosterUrl:
                    sHosterUrl = f'{sHosterUrl}|Referer={sUrl}'

                oHoster = cHosterGui().checkHoster(sHosterUrl)
                if oHoster:
                    oHoster.setDisplayName(sMovieTitle)
                    oHoster.setFileName(sMovieTitle)
                    cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb)

    oGui.setEndOfDirectory()
