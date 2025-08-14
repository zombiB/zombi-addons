# -*- coding: utf-8 -*-

import re, urllib.parse
from resources.lib.gui.hoster import cHosterGui
from resources.lib.gui.gui import cGui
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.comaddon import progress, VSlog, siteManager, addon
from resources.lib.parser import cParser
from resources.lib.util import cUtil
from resources.lib.multihost import cMultiup

SITE_IDENTIFIER = 'shahidu'
SITE_NAME = 'Shahid4U'
SITE_DESC = 'arabic vod'
 
URL_MAIN = siteManager().getUrlMain(SITE_IDENTIFIER)

MOVIE_EN = (f'{URL_MAIN}category/افلام-اجنبي', 'showMovies')
MOVIE_AR = (f'{URL_MAIN}category/افلام-عربي', 'showMovies')
MOVIE_HI = (f'{URL_MAIN}category/افلام-هندي', 'showMovies')
MOVIE_ASIAN = (f'{URL_MAIN}category/افلام-اسيوية', 'showMovies')
MOVIE_TURK = (f'{URL_MAIN}category/افلام-تركية', 'showMovies')
MOVIE_GENRES = (True, 'moviesGenres')

RAMADAN_SERIES = (f'{URL_MAIN}category/مسلسلات-رمضان-2025', 'showSeries')
SERIE_EN = (f'{URL_MAIN}category/مسلسلات-اجنبي', 'showSeries')
SERIE_AR = (f'{URL_MAIN}category/مسلسلات-عربي', 'showSeries')
SERIE_HEND = (f'{URL_MAIN}category/مسلسلات-هندية', 'showSeries')
SERIE_ASIA = (f'{URL_MAIN}category/مسلسلات-اسيوية', 'showSeries')
SERIE_TR = (f'{URL_MAIN}category/مسلسلات-تركية', 'showSeries')
SERIE_GENRES = (True, 'seriesGenres')

ANIM_MOVIES = (f'{URL_MAIN}category/افلام-انمي', 'showMovies')
ANIM_NEWS = (f'{URL_MAIN}category/مسلسلات-انمي' , 'showSeries')

REPLAYTV_NEWS = (f'{URL_MAIN}category/برامج-تلفزيونية', 'showSeries')

DOC_NEWS = (f'{URL_MAIN}genre/وثائقي', 'showMovies')
DOC_SERIES = (f'{URL_MAIN}genre/وثائقي', 'showSeries')

SPORT_WWE = (f'{URL_MAIN}category/عروض-مصارعة', 'showMovies')

URL_SEARCH = (f'{URL_MAIN}search?s=', 'showMovies')
URL_SEARCH_MOVIES = (f'{URL_MAIN}search?s=فيلم%20', 'showMovies')
URL_SEARCH_SERIES = (f'{URL_MAIN}search?s=مسلسل%20', 'showSeries')
URL_SEARCH_ANIMS = (f'{URL_MAIN}search?s=انمي%20', 'showSeries')
FUNCTION_SEARCH = 'showMovies'
 
def load():
    oGui = cGui()
    addons = addon()

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'http://venom/')
    oGui.addDir(SITE_IDENTIFIER, 'showSearch', addons.VSlang(30078), '1/Search.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', 'http://venom/')
    oGui.addDir(SITE_IDENTIFIER, 'showSearchSeries', addons.VSlang(30079), '1/Search.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', RAMADAN_SERIES[0])
    oGui.addDir(SITE_IDENTIFIER, 'showSeries', 'رمضان', '1/Ramadan.png', oOutputParameterHandler) 

    oOutputParameterHandler.addParameter('siteUrl', MOVIE_EN[0])
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'أفلام أجنبية', '1/Movies.png', oOutputParameterHandler)
   
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_AR[0])
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'أفلام عربية', '1/Arabic.png', oOutputParameterHandler)
        
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_HI[0])
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'أفلام هندية', '1/Hindi.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', MOVIE_ASIAN[0])
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'أفلام أسيوية', '1/Asian.png', oOutputParameterHandler)
   
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_TURK[0])
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'أفلام تركية', '1/Turkish.png', oOutputParameterHandler) 
    
    oOutputParameterHandler.addParameter('siteUrl', DOC_NEWS[0])
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'أفلام وثائقية', '1/Documentary.png', oOutputParameterHandler) 
    
    oOutputParameterHandler.addParameter('siteUrl', SERIE_EN[0])
    oGui.addDir(SITE_IDENTIFIER, 'showSeries', 'مسلسلات أجنبية', '1/Movies.png', oOutputParameterHandler)
    
    oOutputParameterHandler.addParameter('siteUrl', SERIE_AR[0])
    oGui.addDir(SITE_IDENTIFIER, 'showSeries', 'مسلسلات عربية', '1/Arabic.png', oOutputParameterHandler)
   
    oOutputParameterHandler.addParameter('siteUrl', SERIE_TR[0])
    oGui.addDir(SITE_IDENTIFIER, 'showSeries', 'مسلسلات تركية', '1/Turkish.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', SERIE_ASIA[0])
    oGui.addDir(SITE_IDENTIFIER, 'showSeries', 'مسلسلات أسيوية', '1/Asian.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', SERIE_HEND[0])
    oGui.addDir(SITE_IDENTIFIER, 'showSeries', 'مسلسلات هندية', '1/Hindi.png', oOutputParameterHandler)
    
    oOutputParameterHandler.addParameter('siteUrl', DOC_SERIES[0])
    oGui.addDir(SITE_IDENTIFIER, 'showSeries', 'مسلسلات وثائقية', '1/Documentary.png', oOutputParameterHandler)
     
    oOutputParameterHandler.addParameter('siteUrl', ANIM_NEWS[0])
    oGui.addDir(SITE_IDENTIFIER, 'showSeries', 'مسلسلات انمي', '1/Anime.png', oOutputParameterHandler) 

    oOutputParameterHandler.addParameter('siteUrl', ANIM_MOVIES[0])
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'أفلام انمي', '1/Anime.png', oOutputParameterHandler)
     
    oOutputParameterHandler.addParameter('siteUrl', REPLAYTV_NEWS[0])
    oGui.addDir(SITE_IDENTIFIER, 'showSeries', 'برامج تلفزيونية', '1/Programs.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', SPORT_WWE[0])
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'مصارعة', '1/WWE.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', SERIE_GENRES[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_GENRES[1], 'المسلسلات (الأنواع)', '1/TVShows.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', MOVIE_GENRES[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_GENRES[1], 'الأفلام (الأنواع)', '1/Movies.png', oOutputParameterHandler)
 
    oGui.setEndOfDirectory()
 
def showSearch():
    oGui = cGui()
 
    sSearchText = oGui.showKeyBoard()
    if sSearchText:
        sUrl = f'{URL_MAIN}search?s={sSearchText}'
        showMovies(sUrl)
        oGui.setEndOfDirectory()
        return
 
def showSearchSeries():
    oGui = cGui()
 
    sSearchText = oGui.showKeyBoard()
    if sSearchText:
        sUrl = f'{URL_MAIN}search?s={sSearchText}'
        showSeries(sUrl)
        oGui.setEndOfDirectory()
        return
   
def seriesGenres():
    oGui = cGui()

    liste = []
    liste.append(['اكشن', f'{URL_MAIN}genre/اكشن'])
    liste.append(['انيميشن', f'{URL_MAIN}genre/كرتون'])
    liste.append(['مغامرات', f'{URL_MAIN}genre/مغامرات'])
    liste.append(['حركة', f'{URL_MAIN}genre/حركة'])
    liste.append(['تاريخي', f'{URL_MAIN}genre/تاريخي'])
    liste.append(['كوميديا', f'{URL_MAIN}genre/كوميدي'])
    liste.append(['موسيقى', f'{URL_MAIN}genre/موسيقي'])
    liste.append(['رياضي', f'{URL_MAIN}genre/رياضي'])
    liste.append(['دراما', f'{URL_MAIN}genre/دراما'])
    liste.append(['رعب', f'{URL_MAIN}genre/رعب'])
    liste.append(['عائلى', f'{URL_MAIN}genre/عائلي'])
    liste.append(['فانتازيا', f'{URL_MAIN}genre/فانتازيا'])
    liste.append(['حروب', f'{URL_MAIN}genre/حروب'])
    liste.append(['الجريمة', f'{URL_MAIN}genre/جريمة'])
    liste.append(['رومانسى', f'{URL_MAIN}genre/رومانسي'])
    liste.append(['خيال علمى', f'{URL_MAIN}genre/خيال%20علمي'])
    liste.append(['اثارة', f'{URL_MAIN}genre/ﺗﺸﻮﻳﻖ%20ﻭﺇﺛﺎﺭﺓ'])
    liste.append(['وثائقى', f'{URL_MAIN}genre/وثائقي'])

    for sTitle, sUrl in liste:

        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', sUrl)
        oGui.addDir(SITE_IDENTIFIER, 'showSeries', sTitle, 'genres.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()

def moviesGenres():
    oGui = cGui()

    liste = []
    liste.append(['اكشن', f'{URL_MAIN}genre/اكشن'])
    liste.append(['انيميشن', f'{URL_MAIN}genre/كرتون'])
    liste.append(['مغامرات', f'{URL_MAIN}genre/مغامرات'])
    liste.append(['حركة', f'{URL_MAIN}genre/حركة'])
    liste.append(['تاريخي', f'{URL_MAIN}genre/تاريخي'])
    liste.append(['كوميديا', f'{URL_MAIN}genre/كوميدي'])
    liste.append(['موسيقى', f'{URL_MAIN}genre/موسيقي'])
    liste.append(['رياضي', f'{URL_MAIN}genre/رياضي'])
    liste.append(['دراما', f'{URL_MAIN}genre/دراما'])
    liste.append(['رعب', f'{URL_MAIN}genre/رعب'])
    liste.append(['عائلى', f'{URL_MAIN}genre/عائلي'])
    liste.append(['فانتازيا', f'{URL_MAIN}genre/فانتازيا'])
    liste.append(['حروب', f'{URL_MAIN}genre/حروب'])
    liste.append(['الجريمة', f'{URL_MAIN}genre/جريمة'])
    liste.append(['رومانسى', f'{URL_MAIN}genre/رومانسي'])
    liste.append(['خيال علمى', f'{URL_MAIN}genre/خيال%20علمي'])
    liste.append(['اثارة', f'{URL_MAIN}genre/ﺗﺸﻮﻳﻖ%20ﻭﺇﺛﺎﺭﺓ'])
    liste.append(['وثائقى', f'{URL_MAIN}genre/وثائقي'])

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
    oRequestHandler.disableSSL()
    sHtmlContent = oRequestHandler.request()

    sStart = '<div class="container">'
    sEnd = '<div class="footer">'
    sHtmlContent = oParser.abParse(sHtmlContent, sStart, sEnd)

    sPattern = r'href="([^"]+)".+?url\(([^)]+)\).+?<p class="title">\s*(.*?)\s*</p>.+?<p class="description">\s*(.*?)\s*</p>'
    aResult = oParser.parse(sHtmlContent, sPattern)
    if aResult[0]:
        total = len(aResult[1])
        progress_ = progress().VScreate(SITE_NAME)
        oOutputParameterHandler = cOutputParameterHandler()
        for aEntry in aResult[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break
 
            if "episode" in aEntry[0] or "season" in aEntry[0]or "series" in aEntry[0]:
                continue
            if "مسلسل" in aEntry[2]:
                continue

            sTitle = cUtil().CleanMovieName(aEntry[2])
            if 'http' not in aEntry[1]:
                sThumb = f'{URL_MAIN}{aEntry[1]}'
            else:
                sThumb = aEntry[1]
            if 'http' not in aEntry[0]:
                siteUrl = f"{URL_MAIN}{aEntry[0].replace('film/','download/').replace('post/','download/')}"
            else:
                siteUrl = aEntry[0].replace('film/','download/').replace('post/','download/')
            sYear = ''
            m = re.search('([0-9]{4})', sTitle)
            if m:
                sYear = str(m.group(0))

            sDesc = ''
            if aEntry[3]:
                sDesc = str(aEntry[3])

            oOutputParameterHandler.addParameter('siteUrl', siteUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oOutputParameterHandler.addParameter('sYear', sYear)
            oOutputParameterHandler.addParameter('sDesc', sDesc)

            oGui.addMovie(SITE_IDENTIFIER, 'showHosters', sTitle, '', sThumb, sDesc, oOutputParameterHandler)
        
        progress_.VSclose(progress_)
 
    if not sSearch:
        sPattern = r"updateQuery\('page', (\d+)\)"
        aResult = oParser.parse(sHtmlContent, sPattern)

        if aResult[0]:
            oOutputParameterHandler = cOutputParameterHandler()
            
            oUrl = urllib.parse.urlparse(sUrl)
            oQuery = urllib.parse.parse_qs(oUrl.query)
            oQuery.pop('page', None)
            sBaseUrl = oUrl._replace(query=urllib.parse.urlencode(oQuery, doseq=True)).geturl()

            for aEntry in sorted(set(aResult[1])):
                sTitle = f'[COLOR red]Page: {aEntry}[/COLOR]'
                sPageUrl = f'{sBaseUrl}?page={aEntry}'

                oOutputParameterHandler.addParameter('siteUrl', sPageUrl)
                oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
                
                oGui.addDir(SITE_IDENTIFIER, 'showMovies', sTitle, 'next.png', oOutputParameterHandler)

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

    sStart = '<div class="container">'
    sEnd = '<div class="footer">'
    sHtmlContent = oParser.abParse(sHtmlContent, sStart, sEnd)

    sPattern = r'href="([^"]+)".+?url\(([^)]+)\).+?<p class="title">\s*(.*?)\s*</p>.+?<p class="description">\s*(.*?)\s*</p>'
    sPattern += r'.+?<p class="description">\s*(.*?)\s*</p>' 
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
 
            if "film/" in aEntry[0] or "post/" in aEntry[0]:
                continue
            if "فيلم" in aEntry[2]:
                continue
            
            sTitle = cUtil().CleanSeriesName(aEntry[2])
            sTitle = re.sub(r"S\d{1,2}", "", sTitle)
            if 'http' not in aEntry[1]:
                sThumb = f'{URL_MAIN}{aEntry[1]}'
            else:
                sThumb = aEntry[1]
            if 'http' not in aEntry[0]:
                siteUrl = f"{URL_MAIN}{aEntry[0].replace('film/','download/')}"
            else:
                siteUrl = aEntry[0].replace('film/','download/')
            sDesc = ''
            if aEntry[3]:
                sDesc = str(aEntry[3])
            sYear = ''

            if sTitle not in itemList:
                itemList.append(sTitle)			
                oOutputParameterHandler.addParameter('siteUrl', siteUrl)
                oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
                oOutputParameterHandler.addParameter('sThumb', sThumb)
                oOutputParameterHandler.addParameter('sYear', sYear)
                oOutputParameterHandler.addParameter('sDesc', sDesc)
			
                oGui.addTV(SITE_IDENTIFIER, 'showSeasons', sTitle, '', sThumb, sDesc, oOutputParameterHandler)

        progress_.VSclose(progress_)
 
    if not sSearch:
        sPattern = r"updateQuery\('page', (\d+)\)"
        aResult = oParser.parse(sHtmlContent, sPattern)

        if aResult[0]:
            oOutputParameterHandler = cOutputParameterHandler()
            
            oUrl = urllib.parse.urlparse(sUrl)
            oQuery = urllib.parse.parse_qs(oUrl.query)
            oQuery.pop('page', None)
            sBaseUrl = oUrl._replace(query=urllib.parse.urlencode(oQuery, doseq=True)).geturl()

            for aEntry in sorted(set(aResult[1])):
                sTitle = f'[COLOR red]Page: {aEntry}[/COLOR]'
                sPageUrl = f'{sBaseUrl}?page={aEntry}'

                oOutputParameterHandler.addParameter('siteUrl', sPageUrl)
                oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
                
                oGui.addDir(SITE_IDENTIFIER, 'showSeries', sTitle, 'next.png', oOutputParameterHandler)

        oGui.setEndOfDirectory()

def showSeasons():
    oGui = cGui()
   
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')
    oParser = cParser()

    oParser = cParser() 
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    sStart = 'جميع المواسم'
    sEnd = '<hr class'
    sHtmlContent = oParser.abParse(sHtmlContent, sStart, sEnd)

    sPattern = '<a href="(.+?)".+?>الموسم</span>.+?>(.+?)</span>'
    aResult = oParser.parse(sHtmlContent, sPattern) 
    if aResult[0]:
        total = len(aResult[1])
        progress_ = progress().VScreate(SITE_NAME)
        oOutputParameterHandler = cOutputParameterHandler()
        for aEntry in aResult[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break

            sTitle =  f'{sMovieTitle} S{aEntry[1]}'
            if 'http' not in aEntry[0]:
                siteUrl = f'{URL_MAIN}{aEntry[0]}'
            else:
                siteUrl = aEntry[0]
            sThumb = sThumb
            sDesc = ''
			
            oOutputParameterHandler.addParameter('siteUrl', siteUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oGui.addSeason(SITE_IDENTIFIER, 'showEpisodes', sTitle, '', sThumb, sDesc, oOutputParameterHandler)
        progress_.VSclose(progress_)

    else:
        sPattern = 'href="([^"]+)" class="epss.+?</span>.+?>(.+?)</span>'
        aResult = oParser.parse(sHtmlContent, sPattern)
        if aResult[0]:
            total = len(aResult[1])
            progress_ = progress().VScreate(SITE_NAME)
            oOutputParameterHandler = cOutputParameterHandler()
            for aEntry in aResult[1]:
                progress_.VSupdate(progress_, total)
                if progress_.iscanceled():
                    break
 
                sTitle = f'{sMovieTitle} E{aEntry[1]}'
                if 'http' not in aEntry[0]:
                    siteUrl = f"{URL_MAIN}{aEntry[0].replace('episode/','download/')}"
                else:
                    siteUrl = aEntry[0].replace('episode/','download/')
                sThumb = sThumb
                sDesc = ''

                oOutputParameterHandler.addParameter('siteUrl', siteUrl)
                oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
                oOutputParameterHandler.addParameter('sThumb', sThumb)
                oGui.addEpisode(SITE_IDENTIFIER, 'showHosters', sTitle, '', sThumb, sDesc, oOutputParameterHandler)

            progress_.VSclose(progress_)
       
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

    sPattern = 'href="([^"]+)" class="epss.+?</span>.+?>(.+?)</span>'
    aResult = oParser.parse(sHtmlContent, sPattern)
    if aResult[0]:
        oOutputParameterHandler = cOutputParameterHandler()
        for aEntry in aResult[1]:
            if "season/" in aEntry[0]:
                continue 

            sTitle = f'{sMovieTitle} E{aEntry[1]}'
            if 'http' not in aEntry[0]:
                siteUrl = f"{URL_MAIN}{aEntry[0].replace('episode/','download/')}"
            else:
                siteUrl = aEntry[0].replace('episode/','download/')
            sThumb = sThumb
            sDesc = ''			

            oOutputParameterHandler.addParameter('siteUrl', siteUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oGui.addEpisode(SITE_IDENTIFIER, 'showHosters', sTitle, '', sThumb, sDesc, oOutputParameterHandler)
      
    oGui.setEndOfDirectory()		
 
def showHosters():
    oGui = cGui()
   
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')

    oParser = cParser()
    sUrl2 = sUrl.replace('/download/','/watch/')
    oRequestHandler = cRequestHandler(sUrl2)
    sHtmlContent1 = oRequestHandler.request()

    sPattern = '"url":"([^"]+)",'
    aResult = oParser.parse(sHtmlContent1, sPattern)
    if aResult[0]:
        for aEntry in aResult[1]:            
            url = aEntry.replace('\\','')
            if url.startswith('//'):
                url = 'http:' + url
           
            sHosterUrl = url 
            oHoster = cHosterGui().checkHoster(sHosterUrl)
            if oHoster:
                oHoster.setDisplayName(sMovieTitle)
                oHoster.setFileName(sMovieTitle)
                cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb)

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    sStart = 'class="down-container">'
    sEnd = '<button style='
    sHtmlContent0 = oParser.abParse(sHtmlContent, sStart, sEnd)

    sPattern = '<div class="qual">.+?</i>(.+?)</h1>(.+?)<hr/>'
    aResult = oParser.parse(sHtmlContent0, sPattern)
    if aResult[0] :    
        for aEntry in aResult[1]:
            sQual = aEntry[0].replace("سيرفرات تحميل","").strip()
            sHtmlContent1 = aEntry[1]

            sPattern = 'href="([^"]+)'
            aResult = oParser.parse(sHtmlContent1, sPattern)	
            if aResult[0] :
                oOutputParameterHandler = cOutputParameterHandler()
                for aEntry in aResult[1]:            
                    url = aEntry
                    if url.startswith('//'):
                        url = 'http:' + url		   

                    sHosterUrl = url
                    if 'multiup' in sHosterUrl:
                        try:
                            if '1080' in sQual:
                                data = cMultiup().GetUrls(sHosterUrl)
                                if data is not False:
                                    for item in data:
                                        sHosterUrl = item.split(',')[0].split('=')[1]
                                        sLabel = item.split('label=')[1]

                                        sDisplayTitle = f'{sMovieTitle} [COLOR coral] [{sQual}][/COLOR][COLOR orange] -{sLabel}[/COLOR]'     
                                        oOutputParameterHandler.addParameter('sHosterUrl', sHosterUrl)
                                        oOutputParameterHandler.addParameter('siteUrl', sUrl)
                                        oOutputParameterHandler.addParameter('sQual', sQual)
                                        oOutputParameterHandler.addParameter('sMovieTitle', sMovieTitle)
                                        oOutputParameterHandler.addParameter('sThumb', sThumb)

                                        oGui.addLink(SITE_IDENTIFIER, 'showLinks', sDisplayTitle, sThumb, sDisplayTitle, oOutputParameterHandler)
                        except:
                            VSlog('Failed tp parse')
                            
                    oHoster = cHosterGui().checkHoster(sHosterUrl)
                    if oHoster:
                        sDisplayTitle = f'{sMovieTitle} [COLOR coral]({sQual}p)[/COLOR]'
                        oHoster.setDisplayName(sDisplayTitle)
                        oHoster.setFileName(sMovieTitle)
                        cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb)

    oGui.setEndOfDirectory()

def showLinks():
    oGui = cGui()

    oInputParameterHandler = cInputParameterHandler()
    sHosterUrl = oInputParameterHandler.getValue('sHosterUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')

    oHoster = cHosterGui().checkHoster(sHosterUrl)
    if oHoster:
        oHoster.setDisplayName(sMovieTitle)
        oHoster.setFileName(sMovieTitle)
        cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb)

    oGui.setEndOfDirectory()
