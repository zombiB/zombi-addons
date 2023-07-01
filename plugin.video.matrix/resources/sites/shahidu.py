# -*- coding: utf-8 -*-
#############################################################
# Yonn1981 https://github.com/Yonn1981/Repo
#############################################################

import re	
from resources.lib.gui.hoster import cHosterGui
from resources.lib.gui.gui import cGui
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.comaddon import progress, VSlog, siteManager
from resources.lib.parser import cParser

 
SITE_IDENTIFIER = 'shahidu'
SITE_NAME = 'Shahidu'
SITE_DESC = 'arabic vod'
 
URL_MAIN = siteManager().getUrlMain(SITE_IDENTIFIER)

oParser = cParser()
 
oRequestHandler = cRequestHandler(URL_MAIN)
sHtmlContent = oRequestHandler.request()
    # (.+?) ([^<]+)

sPattern = '<link rel="canonical" href="(.+?)" />'
aResult = oParser.parse(sHtmlContent, sPattern)
    
if (aResult[0]):
    URL_MAIN = aResult[1][0]
    VSlog(URL_MAIN)
RAMADAN_SERIES = (URL_MAIN + '/category/مسلسلات-رمضان-2023', 'showSeries')


MOVIE_EN = (URL_MAIN + '/category/افلام-اجنبي', 'showMovies')
MOVIE_AR = (URL_MAIN + '/category/افلام-عربي', 'showMovies')
MOVIE_HI = (URL_MAIN + '/category/افلام-هندي', 'showMovies')
MOVIE_ASIAN = (URL_MAIN + '/category/افلام-اسيوية', 'showMovies')
MOVIE_TURK = (URL_MAIN + '/category/افلام-تركية', 'showMovies')
MOVIE_GENRES = (True, 'moviesGenres')

SERIE_EN = (URL_MAIN + '/category/مسلسلات-اجنبي', 'showSeries')
SERIE_AR = (URL_MAIN + '/category/مسلسلات-عربي', 'showSeries')
SERIE_HEND = (URL_MAIN + '/category/مسلسلات-هندية', 'showSeries')
SERIE_ASIA = (URL_MAIN + '/category/مسلسلات-اسيوية', 'showSeries')
SERIE_TR = (URL_MAIN + '/category/مسلسلات-تركية', 'showSeries')
SERIE_GENRES = (True, 'seriesGenres')

ANIM_MOVIES = (URL_MAIN + '/category/افلام-انمي', 'showMovies')
ANIM_NEWS = (URL_MAIN+'/category/مسلسلات-انمي' , 'showSeries')

REPLAYTV_NEWS = (URL_MAIN + '/category/برامج-تلفزيونية', 'showSeries')

DOC_NEWS = (URL_MAIN + '/genre/وثائقي', 'showMovies')
DOC_SERIES = (URL_MAIN + '/genre/وثائقي', 'showSeries')

URL_SEARCH = (URL_MAIN + '/search?s=', 'showMovies')
URL_SEARCH_MOVIES = (URL_MAIN + '/search?s=فيلم+', 'showMovies')
URL_SEARCH_SERIES = (URL_MAIN + '/search?s=مسلسل+', 'showSeries')
FUNCTION_SEARCH = 'showMovies'
 
def load():
    oGui = cGui()

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'http://venom/')
    oGui.addDir(SITE_IDENTIFIER, 'showSearch', 'Search Movies', 'search.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', 'http://venom/')
    oGui.addDir(SITE_IDENTIFIER, 'showSearchSeries', 'Search Series', 'search.png', oOutputParameterHandler)
 
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_EN[0])
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'أفلام أجنبية', 'agnab.png', oOutputParameterHandler)
   
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_AR[0])
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'أفلام عربية', 'arab.png', oOutputParameterHandler)
        
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_HI[0])
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'أفلام هندية', 'hend.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', MOVIE_ASIAN[0])
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'أفلام أسيوية', 'asia.png', oOutputParameterHandler)
   
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_TURK[0])
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'أفلام تركية', 'turk.png', oOutputParameterHandler) 
    
    oOutputParameterHandler.addParameter('siteUrl', DOC_NEWS[0])
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'أفلام وثائقية', 'doc.png', oOutputParameterHandler) 
 
    
    oOutputParameterHandler.addParameter('siteUrl', SERIE_EN[0])
    oGui.addDir(SITE_IDENTIFIER, 'showSeries', 'مسلسلات أجنبية', 'agnab.png', oOutputParameterHandler)

    
    oOutputParameterHandler.addParameter('siteUrl', SERIE_AR[0])
    oGui.addDir(SITE_IDENTIFIER, 'showSeries', 'مسلسلات عربية', 'arab.png', oOutputParameterHandler)

    
    oOutputParameterHandler.addParameter('siteUrl', SERIE_TR[0])
    oGui.addDir(SITE_IDENTIFIER, 'showSeries', 'مسلسلات تركية', 'turk.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', SERIE_ASIA[0])
    oGui.addDir(SITE_IDENTIFIER, 'showSeries', 'مسلسلات أسيوية', 'asia.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', SERIE_HEND[0])
    oGui.addDir(SITE_IDENTIFIER, 'showSeries', 'مسلسلات هندية', 'hend.png', oOutputParameterHandler)
    
    oOutputParameterHandler.addParameter('siteUrl', DOC_SERIES[0])
    oGui.addDir(SITE_IDENTIFIER, 'showSeries', 'مسلسلات وثائقية', 'doc.png', oOutputParameterHandler)
     
    oOutputParameterHandler.addParameter('siteUrl', ANIM_NEWS[0])
    oGui.addDir(SITE_IDENTIFIER, 'showSeries', 'مسلسلات انمي', 'anime.png', oOutputParameterHandler) 

    oOutputParameterHandler.addParameter('siteUrl', ANIM_MOVIES[0])
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'أفلام انمي', 'anime.png', oOutputParameterHandler)
     
    oOutputParameterHandler.addParameter('siteUrl', REPLAYTV_NEWS[0])
    oGui.addDir(SITE_IDENTIFIER, 'showSeries', 'برامج تلفزيونية', 'brmg.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', SERIE_GENRES[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_GENRES[1], 'المسلسلات (الأنواع)', 'mslsl.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_GENRES[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_GENRES[1], 'الأفلام (الأنواع)', 'film.png', oOutputParameterHandler)
 
    oGui.setEndOfDirectory()
 
def showSearch():
    oGui = cGui()
 
    sSearchText = oGui.showKeyBoard()
    if sSearchText:
        sUrl = URL_MAIN + '/search?s='+sSearchText
        showMovies(sUrl)
        oGui.setEndOfDirectory()
        return
 
def showSearchSeries():
    oGui = cGui()
 
    sSearchText = oGui.showKeyBoard()
    if sSearchText:
        sUrl = URL_MAIN + '/search?s='+sSearchText
        showSeries(sUrl)
        oGui.setEndOfDirectory()
        return
   
def seriesGenres():
    oGui = cGui()

    liste = []
    liste.append(['اكشن', URL_MAIN + '/genre/اكشن'])
    liste.append(['انيميشن', URL_MAIN + '/genre/كرتون'])
    liste.append(['مغامرات', URL_MAIN + '/genre/مغامرات'])
    liste.append(['حركة', URL_MAIN + '/genre/حركة'])
    liste.append(['تاريخي', URL_MAIN + '/genre/تاريخي'])
    liste.append(['كوميديا', URL_MAIN + '/genre/كوميدي'])
    liste.append(['موسيقى', URL_MAIN + '/genre/موسيقي'])
    liste.append(['رياضي', URL_MAIN + '/genre/رياضي'])
    liste.append(['دراما', URL_MAIN + '/genre/دراما'])
    liste.append(['رعب', URL_MAIN + '/genre/رعب'])
    liste.append(['عائلى', URL_MAIN + '/genre/عائلي'])
    liste.append(['فانتازيا', URL_MAIN + '/genre/فانتازيا'])
    liste.append(['حروب', URL_MAIN + '/genre/حروب'])
    liste.append(['الجريمة', URL_MAIN + '/genre/جريمة'])
    liste.append(['رومانسى', URL_MAIN + '/genre/رومانسي'])
    liste.append(['خيال علمى', URL_MAIN + '/genre/خيال%20علمي'])
    liste.append(['اثارة', URL_MAIN + '/genre/ﺗﺸﻮﻳﻖ%20ﻭﺇﺛﺎﺭﺓ'])
    liste.append(['وثائقى', URL_MAIN + '/genre/وثائقي'])

    for sTitle, sUrl in liste:

        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', sUrl)
        oGui.addDir(SITE_IDENTIFIER, 'showSeries', sTitle, 'genres.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()

def moviesGenres():
    oGui = cGui()

    liste = []
    liste.append(['اكشن', URL_MAIN + '/genre/اكشن'])
    liste.append(['انيميشن', URL_MAIN + '/genre/كرتون'])
    liste.append(['مغامرات', URL_MAIN + '/genre/مغامرات'])
    liste.append(['حركة', URL_MAIN + '/genre/حركة'])
    liste.append(['تاريخي', URL_MAIN + '/genre/تاريخي'])
    liste.append(['كوميديا', URL_MAIN + '/genre/كوميدي'])
    liste.append(['موسيقى', URL_MAIN + '/genre/موسيقي'])
    liste.append(['رياضي', URL_MAIN + '/genre/رياضي'])
    liste.append(['دراما', URL_MAIN + '/genre/دراما'])
    liste.append(['رعب', URL_MAIN + '/genre/رعب'])
    liste.append(['عائلى', URL_MAIN + '/genre/عائلي'])
    liste.append(['فانتازيا', URL_MAIN + '/genre/فانتازيا'])
    liste.append(['حروب', URL_MAIN + '/genre/حروب'])
    liste.append(['الجريمة', URL_MAIN + '/genre/جريمة'])
    liste.append(['رومانسى', URL_MAIN + '/genre/رومانسي'])
    liste.append(['خيال علمى', URL_MAIN + '/genre/خيال%20علمي'])
    liste.append(['اثارة', URL_MAIN + '/genre/ﺗﺸﻮﻳﻖ%20ﻭﺇﺛﺎﺭﺓ'])
    liste.append(['وثائقى', URL_MAIN + '/genre/وثائقي'])

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
 
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
 # ([^<]+) .+? (.+?)

    sPattern = '<a href="([^"]+)".+?class="fullClick">.+?data-src="([^"]+)".+?<a href="([^"]+)"><h3>(.+?)</h3></a>'

    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
	
	
    if aResult[0]:
        total = len(aResult[1])
        progress_ = progress().VScreate(SITE_NAME)
        oOutputParameterHandler = cOutputParameterHandler()
        for aEntry in aResult[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break
 
            if "episode/" in aEntry[2]:
                continue
            if "مسلسل" in aEntry[3]:
                continue

            sTitle = aEntry[3].replace("مشاهدة","").replace("مترجمة","").replace("مترجم","").replace("فيلم","").replace("اون لاين","").replace("برنامج","").replace("WEB-DL","").replace("BRRip","").replace("720p","").replace("HD-TC","").replace("HDRip","").replace("HD-CAM","").replace("DVDRip","").replace("BluRay","").replace("1080p","").replace("WEBRip","").replace("WEB-dl","").replace("مترجم ","").replace("مشاهدة وتحميل","").replace("اون لاين","").replace("HD","").replace("كامل","")
            sThumb = aEntry[1]
            siteUrl = aEntry[2].replace('film/','download/')
            sDesc = ''
            sYear = ''
            m = re.search('([0-9]{4})', sTitle)
            if m:
                sYear = str(m.group(0))
                sTitle = sTitle.replace(sYear,'')
 


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
 
    if not sSearch:
        oGui.setEndOfDirectory()

def showSeries(sSearch = ''):
    oGui = cGui()
    if sSearch:
      sUrl = sSearch
    else:
        oInputParameterHandler = cInputParameterHandler()
        sUrl = oInputParameterHandler.getValue('siteUrl')
 
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
       # (.+?) ([^<]+) .+?

    sPattern = '<a href="([^"]+)".+?class="fullClick">.+?data-src="([^"]+)".+?<a href="([^"]+)"><h3>(.+?)</h3></a>'
 
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
	
	
    if aResult[0]:
        total = len(aResult[1])
        progress_ = progress().VScreate(SITE_NAME)
        oOutputParameterHandler = cOutputParameterHandler()
        for aEntry in aResult[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break
 
            if "film/" in aEntry[2]:
                continue
            if "post/" in aEntry[2]:
                continue

            if "فيلم" in aEntry[3]:
                continue
            
            sTitle = aEntry[3].replace("مشاهدة","").replace("مسلسل","").replace("انمي","").replace("مترجمة","").replace("مترجم","").replace("برنامج","").replace("مترجمة","").replace("فيلم","").replace("اون لاين","").replace("WEB-DL","").replace("BRRip","").replace("720p","").replace("HD-TC","").replace("HDRip","").replace("HD-CAM","").replace("DVDRip","").replace("BluRay","").replace("1080p","").replace("WEBRip","").replace("WEB-dl","").replace("مترجم ","").replace("مشاهدة وتحميل","").replace("اون لاين","").replace("كامل","")
            siteUrl = aEntry[2]
            sThumb = aEntry[1]
            sDesc = ''
            sYear = ''
            sTitle = sTitle.split('الحلقة')[0].split('الموسم')[0]

            oOutputParameterHandler.addParameter('siteUrl',siteUrl)
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
    oParser = cParser()
 
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    oParser = cParser()

    sStart = '<div class="holder-block">'
    sEnd = '<div class="carousel-slider glide">'
    sHtmlContent = oParser.abParse(sHtmlContent, sStart, sEnd)
    sPattern = '<a href="(.+?)".+?><h3>الموسم<span>(.+?)</span></h3></a>'

    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
    VSlog(aResult)    
    if aResult[0]:
        total = len(aResult[1])
        progress_ = progress().VScreate(SITE_NAME)
        oOutputParameterHandler = cOutputParameterHandler()
        for aEntry in aResult[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break


            sTitle =  " S" + aEntry[1]
            sTitle =  sMovieTitle+sTitle
            siteUrl = aEntry[0]
            sThumb = sThumb
            sDesc = ''
			
            oOutputParameterHandler.addParameter('siteUrl',siteUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oGui.addSeason(SITE_IDENTIFIER, 'showEpisodes', sTitle, '', sThumb, sDesc, oOutputParameterHandler)
        progress_.VSclose(progress_)

    else:

        sStart = '> باقى الحلقات</h2>'
        sEnd = '</div>'
        sHtmlContent = oParser.abParse(sHtmlContent, sStart, sEnd)
        sPattern = '<a href="([^"]+)".+?<span>(.+?)</span></h3></a>'

        oParser = cParser()
        aResult = oParser.parse(sHtmlContent, sPattern)
        VSlog(aResult)
        if aResult[0]:
            total = len(aResult[1])
            progress_ = progress().VScreate(SITE_NAME)
            oOutputParameterHandler = cOutputParameterHandler()
            for aEntry in aResult[1]:
                progress_.VSupdate(progress_, total)
                if progress_.iscanceled():
                    break
 
                sTitle = " E"+aEntry[1]
                sTitle = sMovieTitle+sTitle
                siteUrl = aEntry[0].replace('episode/','download/')
                sThumb = sThumb
                sDesc = ''
			

                oOutputParameterHandler.addParameter('siteUrl',siteUrl)
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
 
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    sPattern = '<a href="([^"]+)".+?<h3>الحلقة<span>(.+?)</span></h3>'

    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
    VSlog(aResult)
    if aResult[0]:
        oOutputParameterHandler = cOutputParameterHandler()
        for aEntry in aResult[1]:
 
            sTitle = " E"+aEntry[1]
            sTitle = sMovieTitle+sTitle
            siteUrl = aEntry[0].replace('episode/','download/')
            sThumb = sThumb
            sDesc = ''
			

            oOutputParameterHandler.addParameter('siteUrl',siteUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oGui.addEpisode(SITE_IDENTIFIER, 'showHosters', sTitle, '', sThumb, sDesc, oOutputParameterHandler)

    sPattern = '<a href="([^"]+)".+?<h3>الحلقة <span>(.+?)</span></h3>'

    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
    VSlog(aResult)
    if aResult[0]:
        oOutputParameterHandler = cOutputParameterHandler()
        for aEntry in aResult[1]:
 
            sTitle = " E"+aEntry[1]
            sTitle = sMovieTitle+sTitle
            siteUrl = aEntry[0].replace('episode/','download/')
            sThumb = sThumb
            sDesc = ''
			

            oOutputParameterHandler.addParameter('siteUrl',siteUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oGui.addEpisode(SITE_IDENTIFIER, 'showHosters', sTitle, '', sThumb, sDesc, oOutputParameterHandler)

        sNextPage = __checkForNextPage(sHtmlContent)
        if sNextPage:
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sNextPage)
            oGui.addDir(SITE_IDENTIFIER, 'showEpisodes', '[COLOR teal]Next >>>[/COLOR]', 'next.png', oOutputParameterHandler)
       
    oGui.setEndOfDirectory()	
    # .+? ([^<]+)	
 
def showHosters():
    oGui = cGui()
    import requests
   
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')

    oRequestHandler = cRequestHandler(sUrl)
    cook = oRequestHandler.GetCookies()
    sHtmlContent = oRequestHandler.request()
    oParser = cParser()

    sPattern = 'postId:"([^"]+)'
    aResult = oParser.parse(sHtmlContent, sPattern)
    
    if (aResult[0]):
        fId = aResult[1][0]

        siteUrl = URL_MAIN + '/ajaxCenter?_action=getdownloadlinks&postId='+fId

        oRequestHandler = cRequestHandler(siteUrl)
        oRequestHandler.addHeaderEntry('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:45.0) Gecko/20100101 Firefox/45.0')
        oRequestHandler.addHeaderEntry('Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8')
        oRequestHandler.addHeaderEntry('X-Requested-With', 'XMLHttpRequest')
        oRequestHandler.addHeaderEntry('Accept-Language', 'fr,fr-FR;q=0.8,en-US;q=0.5,en;q=0.3')
        sHtmlContent = oRequestHandler.request()
                   
        sPattern = 'href="([^"]+)">.+?class="fa fa-desktop"></i>(.+?)</span>'
        oParser = cParser()
        aResult = oParser.parse(sHtmlContent, sPattern)
        if aResult[0]:
                for aEntry in aResult[1]:
            
                    url = aEntry[0]
                    qual = aEntry[1].replace(' ','')
                    sTitle = sMovieTitle+' ['+qual+'p] '
                    if url.startswith('//'):
                       url = 'http:' + url
           
                    sHosterUrl = url 
                    oHoster = cHosterGui().checkHoster(sHosterUrl)
                    if oHoster:
                       oHoster.setDisplayName(sTitle)
                       oHoster.setFileName(sTitle)
                       cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb)

    sUrl = sUrl.replace('download','watch')
    oRequestHandler = cRequestHandler(sUrl)
    cook = oRequestHandler.GetCookies()
    sHtmlContent = oRequestHandler.request()
    oParser = cParser()

    sPattern = 'url: "(.+?)"'
    aResult = oParser.parse(sHtmlContent, sPattern)
    
    if (aResult[0]):
        fId = aResult[1][0]
        fId = fId.split('post_id=')[1]
        VSlog(fId)

        for i in range(0,8):

            siteUrl = URL_MAIN + '/ajaxCenter?_action=getserver&_post_id='+fId+'&serverid='+str(i)

            oRequestHandler = cRequestHandler(siteUrl)
            oRequestHandler.addHeaderEntry('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:45.0) Gecko/20100101 Firefox/45.0')
            oRequestHandler.addHeaderEntry('Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8')
            oRequestHandler.addHeaderEntry('X-Requested-With', 'XMLHttpRequest')
            oRequestHandler.addHeaderEntry('Accept-Language', 'fr,fr-FR;q=0.8,en-US;q=0.5,en;q=0.3')
            sHtmlContent = oRequestHandler.request()

            VSlog(sHtmlContent)                     
            sPattern = '(http[^"]+)'
            oParser = cParser()
            aResult = oParser.parse(sHtmlContent, sPattern)
            if aResult[0]:
                for aEntry in aResult[1]:
            
                    url = aEntry

                    sTitle = sMovieTitle
                    if url.startswith('//'):
                       url = 'http:' + url
           
                    sHosterUrl = url 
                    oHoster = cHosterGui().checkHoster(sHosterUrl)
                    if oHoster:
                       oHoster.setDisplayName(sTitle)
                       oHoster.setFileName(sTitle)
                       cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb)

    oGui.setEndOfDirectory()

def __checkForNextPage(sHtmlContent):
    sPattern = '<li class="active"><a href=".+?<li><a href="([^<]+)">'
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
    if aResult[0]:
        aResult = aResult[1][0]
        return aResult

    return False 