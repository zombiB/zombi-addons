#-*- coding: utf-8 -*-
#zombi https://github.com/zombiB/zombi-addons/
from resources.lib.gui.hoster import cHosterGui
from resources.lib.gui.gui import cGui
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.comaddon import progress, VSlog
from resources.lib.parser import cParser
from resources.lib.player import cPlayer
import re
 
SITE_IDENTIFIER = 'akwam'
SITE_NAME = 'akwam'
SITE_DESC = 'arabic vod'
 
URL_MAIN = 'https://akwam.cz'
MOVIE_MOVIE = (True, 'showMenuMovies')
MOVIE_FAM = (URL_MAIN + '/movies?section=0&category=33&rating=0&year=0&language=0&formats=0&quality=0', 'showMovies')
MOVIE_AR = ('https://akwam.co/movies?section=29', 'showMovies')
MOVIE_DUBBED = (URL_MAIN + '/movies?section=0&category=71&rating=0&year=0&language=0&formats=0&quality=0', 'showMovies')
MOVIE_EN = (URL_MAIN + '/movies?section=30', 'showMovies')
MOVIE_HI = (URL_MAIN + '/movies?section=31', 'showMovies')
MOVIE_ASIAN = (URL_MAIN + '/movies?section=33', 'showMovies')
KID_MOVIES = (URL_MAIN + '/movies?category=30', 'showMovies')
MOVIE_TURK = (URL_MAIN + '/movies?section=32', 'showMovies')
MOVIE_TOP = (URL_MAIN + '/movies?section=30&category=0&rating=8&year=0&language=0&formats=0&quality=0', 'showMovies')
RAMADAN_SERIES = (URL_MAIN + '/series?section=0&category=87&rating=0&year=0&language=0&formats=0&quality=0', 'showSeries')
SERIE_EN = (URL_MAIN + '/series?section=30', 'showSeries')
SERIE_AR = (URL_MAIN + '/series?section=29', 'showSeries')
SERIE_HEND = (URL_MAIN + '/series?section=31', 'showSeries')
SERIE_ASIA = (URL_MAIN + '/series?section=33', 'showSeries')
SERIE_TR = (URL_MAIN + '/series?section=32', 'showSeries')
SERIE_DUBBED = (URL_MAIN + '/series?section=30&category=71&rating=0&year=0&language=0&formats=0&quality=0', 'showSeries')

SERIE_TR_AR = (URL_MAIN + '/series?section=32&category=71&rating=0&year=0&language=0&formats=0&quality=0', 'showSeries')
SERIE_HEND_AR = (URL_MAIN + '/series?section=31&category=71&rating=0&year=0&language=0&formats=0&quality=0', 'showSeries')
ANIM_NEWS = (URL_MAIN + '/series?category=30', 'showSeries')

DOC_NEWS = (URL_MAIN + '/movies?category=28', 'showMovies')
DOC_SERIES = (URL_MAIN + '/shows?section=46&category=0&rating=0&year=0&formats=0&quality=0', 'showSeries')

REPLAYTV_NEWS = (URL_MAIN + '/shows?section=42', 'showSeries')
REPLAYTV_PLAY = (URL_MAIN + '/shows?section=45', 'showMovies')

MOVIE_ANNEES = (True, 'showYears')

URL_SEARCH = (URL_MAIN + '/search?q=', 'showSeries')
URL_SEARCH_MOVIES = (URL_MAIN + '/search?section=movie&year=0&rating=0&formats=0&quality=0&q=', 'showMovies')
URL_SEARCH_SERIES = (URL_MAIN + '/search?section=series&year=0&rating=0&formats=0&quality=0&q=', 'showSeriesSearch')
URL_SEARCH_MISC = (URL_MAIN + '/search?q=', 'showSeriesSearch')
FUNCTION_SEARCH = 'showSeries'

def showMenuMovies():
    oGui = cGui()

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', URL_SEARCH_MOVIES[0])
    oGui.addDir(SITE_IDENTIFIER, 'showSearch', 'Search', 'search.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()
	
def load():
    oGui = cGui()

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'http://venom/')
    oGui.addDir(SITE_IDENTIFIER, 'showSearch', 'Search Movies', 'search.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', 'http://venom/')
    oGui.addDir(SITE_IDENTIFIER, 'showSearchSeries', 'Search Series', 'search.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', 'http://venom/')
    oGui.addDir(SITE_IDENTIFIER, 'showSearchAll', 'Search All', 'search.png', oOutputParameterHandler)
    
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_EN[0])
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'أفلام أجنبية', 'film.png', oOutputParameterHandler)
   
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_AR[0])
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'أفلام عربية', 'film.png', oOutputParameterHandler)
 
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_ASIAN[0])
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'أفلام أسيوية', 'film.png', oOutputParameterHandler)
   
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_TURK[0])
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'أفلام تركية', 'film.png', oOutputParameterHandler)
    
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_HI[0])
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'أفلام هندية', 'film.png', oOutputParameterHandler)
    
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', KID_MOVIES[0])
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'أفلام كرتون', 'crtoon.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', DOC_NEWS[0])
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'أفلام وثائقية', 'doc.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', SERIE_EN[0])
    oGui.addDir(SITE_IDENTIFIER, 'showSeries', 'مسلسلات أجنبية', 'mslsl.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', SERIE_AR[0])
    oGui.addDir(SITE_IDENTIFIER, 'showSeries', 'مسلسلات عربية', 'mslsl.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', SERIE_ASIA[0])
    oGui.addDir(SITE_IDENTIFIER, 'showSeries', 'مسلسلات أسيوية', 'mslsl.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', SERIE_TR[0])
    oGui.addDir(SITE_IDENTIFIER, 'showSeries', 'مسلسلات تركية', 'mslsl.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', SERIE_HEND[0])
    oGui.addDir(SITE_IDENTIFIER, 'showSeries', 'مسلسلات هندية', 'mslsl.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', ANIM_NEWS[0])
    oGui.addDir(SITE_IDENTIFIER, 'showSeries', 'مسلسلات إنمي', 'anime.png', oOutputParameterHandler)
  
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', SERIE_DUBBED[0])
    oGui.addDir(SITE_IDENTIFIER, 'showSeries', 'مسلسلات مدبلجة', 'mslsl.png', oOutputParameterHandler)  

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', SERIE_TR_AR[0])
    oGui.addDir(SITE_IDENTIFIER, 'showSeries', 'مسلسلات تركية مدبلجة', 'mslsl.png', oOutputParameterHandler)
    
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', SERIE_HEND_AR[0])
    oGui.addDir(SITE_IDENTIFIER, 'showSeries', 'مسلسلات هندية مدبلجة', 'mslsl.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', DOC_SERIES[0])
    oGui.addDir(SITE_IDENTIFIER, 'showSeries', 'مسلسلات وثائقية', 'doc.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', REPLAYTV_NEWS[0])
    oGui.addDir(SITE_IDENTIFIER, 'showSeries', 'برامج تلفزيونية', 'brmg.png', oOutputParameterHandler)
	
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', REPLAYTV_PLAY[0])
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'مسرحيات', 'msrh.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()

def showYears():
    oGui = cGui()
    oOutputParameterHandler = cOutputParameterHandler()
    for i in reversed(range(1925, 2022)):
        sYear = str(i)
        oOutputParameterHandler.addParameter('siteUrl', URL_MAIN + '/movies?section=0&category=0&rating=0&language=0&formats=0&quality=0&year=' + sYear)  # / inutile
        oGui.addDir(SITE_IDENTIFIER, 'showMovies', sYear, 'annees.png', oOutputParameterHandler)
    oGui.setEndOfDirectory()
 
def showSearchAll():
    oGui = cGui()
 
    sSearchText = oGui.showKeyBoard()
    if (sSearchText != False):
        sUrl = URL_MAIN + '/search?q='+sSearchText
        showSeriesSearch(sUrl)
        oGui.setEndOfDirectory()
        return  
 
def showSearch():
    oGui = cGui()
 
    sSearchText = oGui.showKeyBoard()
    if (sSearchText != False):
        sUrl = URL_MAIN + '/search?section=movie&year=0&rating=0&formats=0&quality=0&q='+sSearchText
        showMovies(sUrl)
        oGui.setEndOfDirectory()
        return
 
def showSearchSeries():
    oGui = cGui()
 
    sSearchText = oGui.showKeyBoard()
    if (sSearchText != False):
        sUrl = URL_MAIN + '/search?section=series&year=0&rating=0&formats=0&quality=0&q='+sSearchText
        showSeriesSearch(sUrl)
        oGui.setEndOfDirectory()
        return  

 
def showMovies(sSearch = ''):
    oGui = cGui()
    if sSearch:
      sUrl = sSearch
    else:
        oInputParameterHandler = cInputParameterHandler()
        sUrl = oInputParameterHandler.getValue('siteUrl')
 
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
    

 # ([^<]+) .+?
    sPattern = '<span class="label quality">([^<]+)</span>.+?<a href="([^<]+)" class="box">.+?data-src="([^<]+)" class="img-fluid w-100 lazy" alt="(.+?)".+?<span class="badge badge-pill badge-secondary ml-1">([^<]+)</span>'

    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
	
	
    if (aResult[0] == True):
        total = len(aResult[1])
        progress_ = progress().VScreate(SITE_NAME)
        oOutputParameterHandler = cOutputParameterHandler()
        for aEntry in aResult[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break
 
            sTitle = aEntry[3].replace("مشاهدة","").replace("مسلسل","").replace("انمي","").replace("مترجمة","").replace("مترجم","").replace("فيلم","").replace("والأخيرة","").replace("مدبلج للعربية","مدبلج").replace("برنامج","").replace("والاخيرة","").replace("كاملة","").replace("حلقات كاملة","").replace("اونلاين","").replace("مباشرة","").replace("انتاج ","").replace("جودة عالية","").replace("كامل","").replace("HD","").replace("السلسلة الوثائقية","").replace("الفيلم الوثائقي","").replace("اون لاين","")
            siteUrl = aEntry[1]
            sThumb = aEntry[2]
            sDesc = ''
            sQua = aEntry[0]
            sYear = aEntry[4]


            oOutputParameterHandler.addParameter('siteUrl',siteUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oOutputParameterHandler.addParameter('sYear', sYear)
            oOutputParameterHandler.addParameter('sDesc', sDesc)
			
            oGui.addMovie(SITE_IDENTIFIER, 'showHosters', sTitle, '', sThumb, sDesc, oOutputParameterHandler)

        progress_.VSclose(progress_)
 
        sNextPage = __checkForNextPage(sHtmlContent)
        oOutputParameterHandler = cOutputParameterHandler()
        if (sNextPage != False):
            oOutputParameterHandler.addParameter('siteUrl', sNextPage)
            oGui.addDir(SITE_IDENTIFIER, 'showMovies', '[COLOR teal]Next >>>[/COLOR]', 'next.png', oOutputParameterHandler)
 
    if not sSearch:
        oGui.setEndOfDirectory()

 
def showSeriesSearch(sSearch = ''):
    oGui = cGui()
    if sSearch:
      sUrl = sSearch
    else:
        oInputParameterHandler = cInputParameterHandler()
        sUrl = oInputParameterHandler.getValue('siteUrl')
 
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
 # ([^<]+) .+? (.+?)
    sPattern = '<span class="label quality">(.+?)</span>.+?<a href="(.+?)" class="box">.+?data-src="(.+?)" class="img-fluid w-100 lazy" alt="(.+?)".+?<span class="badge badge-pill badge-secondary ml-1">(.+?)</span>'

    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
	
	
    if (aResult[0] == True):
        total = len(aResult[1])
        progress_ = progress().VScreate(SITE_NAME)
        oOutputParameterHandler = cOutputParameterHandler()
        for aEntry in aResult[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break
 
            sTitle = aEntry[3].replace("مشاهدة","").replace("مسلسل","").replace("انمي","").replace("مترجمة","").replace("مترجم","").replace("برنامج","").replace("فيلم","").replace("والأخيرة","").replace("مدبلج للعربية","مدبلج").replace("والاخيرة","").replace("كاملة","").replace("حلقات كاملة","").replace("اونلاين","").replace("مباشرة","").replace("انتاج ","").replace("جودة عالية","").replace("كامل","").replace("HD","").replace("السلسلة الوثائقية","").replace("الفيلم الوثائقي","").replace("اون لاين","")
            siteUrl = aEntry[1]
            sThumb = aEntry[2]
            sYear = aEntry[4]
            sDisplayTitle = sTitle.replace("الموسم العاشر","S10").replace("الموسم الحادي عشر","S11").replace("الموسم الثاني عشر","S12").replace("الموسم الثالث عشر","S13").replace("الموسم الرابع عشر","S14").replace("الموسم الخامس عشر","S15").replace("الموسم السادس عشر","S16").replace("الموسم السابع عشر","S17").replace("الموسم الثامن عشر","S18").replace("الموسم السابع والعشرون","S27").replace("الموسم التاسع عشر","S19").replace("الموسم العشرون","S20").replace("الموسم الحادي و العشرون","S21").replace("الموسم الثاني و العشرون","S22").replace("الموسم الثالث و العشرون","S23").replace("الموسم الرابع والعشرون","S24").replace("الموسم الخامس و العشرون","S25").replace("الموسم السادس والعشرون","S26").replace("الموسم السابع والعشرون","S27").replace("الموسم الثامن والعشرون","S28").replace("الموسم التاسع والعشرون","S29").replace("الموسم الثلاثون","S30").replace("الموسم الحادي و الثلاثون","S31").replace("الموسم الثاني والثلاثون","S32").replace("الموسم الثالث و الثلاثون","S33").replace("الموسم الاول","S1").replace("الموسم الثاني","S2").replace("الموسم الثالث","S3").replace("الموسم الثالث","S3").replace("الموسم الرابع","S4").replace("الموسم الخامس","S5").replace("الموسم السادس","S6").replace("الموسم السابع","S7").replace("الموسم الثامن","S8").replace("الموسم التاسع","S9").replace("الموسم","S").replace("S ","S")
            sDesc = ''

            oOutputParameterHandler.addParameter('siteUrl',siteUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sDisplayTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            if '/movie/' in siteUrl:
                oGui.addMovie(SITE_IDENTIFIER, 'showHosters', sDisplayTitle, '', sThumb, sDesc, oOutputParameterHandler) 
            else:
                oGui.addTV(SITE_IDENTIFIER, 'showEpisodes', sDisplayTitle, '', sThumb, sDesc, oOutputParameterHandler)

        progress_.VSclose(progress_)
 
        sNextPage = __checkForNextPage(sHtmlContent)
        if (sNextPage != False):
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sNextPage)
            oGui.addDir(SITE_IDENTIFIER, 'showSeries', '[COLOR teal]Next >>>[/COLOR]', 'next.png', oOutputParameterHandler)
 
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
 # ([^<]+) .+? (.+?)
    sPattern = '<span class="label quality">([^<]+)</span>.+?<a href="([^<]+)" class="box">.+?data-src="([^<]+)" class="img-fluid w-100 lazy" alt="(.+?)".+?<span class="badge badge-pill badge-secondary ml-1">([^<]+)</span>'

    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
	
	
    if (aResult[0] == True):
        total = len(aResult[1])
        progress_ = progress().VScreate(SITE_NAME)
        oOutputParameterHandler = cOutputParameterHandler()
        for aEntry in aResult[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break
 
            sTitle = aEntry[3].replace("مشاهدة","").replace("مسلسل","").replace("انمي","").replace("مترجمة","").replace("مترجم","").replace("برنامج","").replace("فيلم","").replace("والأخيرة","").replace("مدبلج للعربية","مدبلج").replace("والاخيرة","").replace("كاملة","").replace("حلقات كاملة","").replace("اونلاين","").replace("مباشرة","").replace("انتاج ","").replace("جودة عالية","").replace("كامل","").replace("HD","").replace("السلسلة الوثائقية","").replace("الفيلم الوثائقي","").replace("اون لاين","")
            siteUrl = aEntry[1]
            sThumb = aEntry[2]
            sYear = aEntry[4]
            sTitle = sTitle.replace("الموسم العاشر","S10").replace("الموسم الحادي عشر","S11").replace("الموسم الثاني عشر","S12").replace("الموسم الثالث عشر","S13").replace("الموسم الرابع عشر","S14").replace("الموسم الخامس عشر","S15").replace("الموسم السادس عشر","S16").replace("الموسم السابع عشر","S17").replace("الموسم الثامن عشر","S18").replace("الموسم التاسع عشر","S19").replace("الموسم العشرون","S20").replace("الموسم الحادي و العشرون","S21").replace("الموسم الثاني و العشرون","S22").replace("الموسم الثالث و العشرون","S23").replace("الموسم الرابع والعشرون","S24").replace("الموسم الخامس و العشرون","S25").replace("الموسم السادس والعشرون","S26").replace("الموسم السابع و العشرون","S27").replace("الموسم الثامن والعشرون","S28").replace("الموسم التاسع والعشرون","S29").replace("الموسم الثلاثون","S30").replace("الموسم الحادي و الثلاثون","S31").replace("الموسم الثاني والثلاثون","S32").replace("الموسم الثالث و الثلاثون","S33").replace("الموسم الاول","S1").replace("الموسم الثاني","S2").replace("الموسم الثالث","S3").replace("الموسم الثالث","S3").replace("الموسم الرابع","S4").replace("الموسم الخامس","S5").replace("الموسم السادس","S6").replace("الموسم السابع","S7").replace("الموسم الثامن","S8").replace("الموسم التاسع","S9")
            sDesc = ''


            oOutputParameterHandler.addParameter('siteUrl',siteUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
			
            oGui.addTV(SITE_IDENTIFIER, 'showEpisodes', sTitle, '', sThumb, sDesc, oOutputParameterHandler)

        progress_.VSclose(progress_)
 
        sNextPage = __checkForNextPage(sHtmlContent)
        if (sNextPage != False):
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
 
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    oParser = cParser()

    sStart = 'id="series-episodes">'
    sEnd = '<div class="widget-4 widget widget-style-1 more mb-4">'
    sHtmlContent = oParser.abParse(sHtmlContent, sStart, sEnd)
  
     # (.+?) ([^<]+) .+?
    sPattern = 'class="text-white">(.+?)</a>.+?<a href="(.+?)">.+?<img src="(.+?)" class="img-fluid" alt='
    aResult = oParser.parse(sHtmlContent, sPattern)
	
    if (aResult[0] == True):
        oOutputParameterHandler = cOutputParameterHandler()
        for aEntry in aResult[1]:
 
            sEp = aEntry[0].split(':')[0]
            sEp = sEp.replace("الحلقة "," E")
            sTitle = sMovieTitle+sEp
            siteUrl = aEntry[1]
            sThumb = aEntry[2]
            sDesc = ''
			


            oOutputParameterHandler.addParameter('siteUrl',siteUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oGui.addEpisode(SITE_IDENTIFIER, 'showHosters', str(sTitle), '', sThumb, sDesc, oOutputParameterHandler)
        

    # .+? ([^<]+)
    sPattern = '<a href="http([^<]+)/watch/(.+?)"'
    
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
    
   
    if (aResult[0] == True):
        oOutputParameterHandler = cOutputParameterHandler()
        for aEntry in aResult[1]: 
            sTitle = sMovieTitle
            siteUrl = sUrl
            sThumb = sThumb
            sDesc = ""
 
            oOutputParameterHandler.addParameter('siteUrl', siteUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sMovieTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oOutputParameterHandler.addParameter('sDesc', sDesc)
            

 
            oGui.addMovie(SITE_IDENTIFIER, 'showHosters', sTitle, '', sThumb, sDesc, oOutputParameterHandler)
 
       
    oGui.setEndOfDirectory()
	
      # (.+?) ([^<]+) .+?
 
def __checkForNextPage(sHtmlContent):
    sPattern = 'href="([^<]+)" rel="next"'	 
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
 
    if (aResult[0] == True):
        return aResult[1][0]

    return False

UA = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:82.0) Gecko/20100101 Firefox/82.0'

####################################################################
def RecapchaBypass():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')
    
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request();

    oParser = cParser()       
    sPattern =  '<a href="http([^<]+)/watch/(.+?)"'
    aResult = oParser.parse(sHtmlContent,sPattern)
    if (aResult[0] == True):
        for aEntry in aResult[1]:
            m3url =  'http'+aEntry[0]+'/watch/' + aEntry[1]
        oRequest = cRequestHandler(m3url)
        sHtmlContent1 = oRequest.request()

    oParser = cParser()       
    sPattern =  '<a href="(.+?)" target="_blank".+?class="download-link"' 
    aResult = oParser.parse(sHtmlContent1,sPattern)
    if (aResult[0] == True):
        m3url =  aResult[1][0]
        oRequest = cRequestHandler(m3url)
        sHtmlContent1 = oRequest.request()

    from resolveurl.plugins.lib.captcha_lib import do_captcha
    test = do_captcha(sHtmlContent1)
    sPattern =  "readonly>(.+?)'}"
    aResult = oParser.parse(test,sPattern)
    if (aResult[0] == True):
        testurl =  aResult[1][0]

    data = 'subform=unlock&g-recaptcha-response=' + testurl
    oRequestHandler = cRequestHandler(m3url)
    cook = oRequestHandler.GetCookies()
    cookies = cook + '; ' + 'XSRF-TOKEN=' + testurl + '; akwam_session=' + testurl + ';'
    oRequestHandler.setRequestType(1)
    oRequestHandler.addHeaderEntry('User-Agent', UA)
    oRequestHandler.addHeaderEntry('Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8')
    oRequestHandler.addHeaderEntry('Accept-Language', 'fr,fr-FR;q=0.8,en-US;q=0.5,en;q=0.3')
    oRequestHandler.addHeaderEntry('Accept-Encoding', 'gzip')
    oRequestHandler.addHeaderEntry('Referer', m3url)
    oRequestHandler.addHeaderEntry('Content-Type', 'application/x-www-form-urlencoded')
    oRequestHandler.addHeaderEntry('cookies', cookies)
    sHtmlContent = oRequestHandler.request()

    sPattern = '<source.+?src="(.+?)"'

    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)

    if (aResult[0] == True):

        for aEntry in aResult[1]:
            sHosterUrl = aEntry
            oHoster = cHosterGui().checkHoster(sHosterUrl)
            if (oHoster != False):
                oHoster.setDisplayName(sMovieTitle)
                oHoster.setFileName(sMovieTitle)
                cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb)
    oGui.setEndOfDirectory()
###############################################################

def showHosters():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')
    
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
    

    oParser = cParser()       
    sPattern =  '<a href="http([^<]+)/watch/(.+?)"'
    aResult = oParser.parse(sHtmlContent,sPattern)
    if (aResult[0] == True):
        for aEntry in aResult[1]:
            m3url =  'http'+aEntry[0]+'/watch/' + aEntry[1]
        oRequest = cRequestHandler(m3url)
        sHtmlContent1 = oRequest.request()
 
      # (.+?) ([^<]+) .+?
    oParser = cParser()       
    sPattern =  '<a href="(.+?)" target="_blank"' 
    aResult = oParser.parse(sHtmlContent1,sPattern)
    if (aResult[0] == True):
        m3url =  aResult[1][0]
        oRequest = cRequestHandler(m3url)
        sHtmlContent1 = oRequest.request()


    # (.+?) .+? ([^<]+)
               

    sPattern = '<source.+?src="(.+?)".+?type="video/mp4".+?size="(.+?)"'
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent1, sPattern)

	
    if (aResult[0] == True):
            for aEntry in aResult[1]:
        
                url = aEntry[0]
                sHost = aEntry[1].replace('"',"")				
                sTitle = ('%s  [COLOR coral]%sp[/COLOR]') % (sMovieTitle, sHost)
                if url.startswith('//'):
                   url = 'https:' + url
				            
                sHosterUrl = url 
                oHoster = cHosterGui().checkHoster(sHosterUrl)
                if (oHoster != False):
                    oHoster.setDisplayName(sTitle)
                    oHoster.setFileName(sMovieTitle)
                    cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb)     

    # (.+?) .+? ([^<]+)
    sPattern = '<a href="http([^<]+)/link/(.+?)".+?class="font-size-14 mr-auto">(.+?)</span>'

    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
   
    if (aResult[0] == True):
        oOutputParameterHandler = cOutputParameterHandler()
        for aEntry in aResult[1]:
 
            sTitle =  ' ['+aEntry[2]+'] '
            sTitle =  sMovieTitle+sTitle
            siteUrl = 'http'+aEntry[0]+'/link/' + aEntry[1]
            sThumbnail = ""
            sInfo = ""

            oOutputParameterHandler.addParameter('siteUrl', siteUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sMovieTitle)
            oOutputParameterHandler.addParameter('sThumbnail', sThumbnail)
            oGui.addLink(SITE_IDENTIFIER, 'showHosters1', sTitle, sThumbnail, sInfo, oOutputParameterHandler)            
                
    oGui.setEndOfDirectory()	
def showHosters1():
    oGui = cGui()
    
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumbnail = oInputParameterHandler.getValue('sThumbnail')

    UA = 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:68.0) Gecko/20100101 Firefox/68.0'
    
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request(); 
    oParser = cParser()
    #recup du lien mp4
    sPattern =  '<!-- APP_DOMAIN_ALTERNATIVE.+?href="(.+?)"' 
    aResult = oParser.parse(sHtmlContent,sPattern)
    if (aResult[0] == True):
        m3url =  aResult[1][0]
        oRequest = cRequestHandler(m3url)
        sHtmlContent = oRequest.request() 

    oParser = cParser()       
    sPattern =  '<!-- APP_DOMAIN_ALTERNATIVE.+?href="(.+?)"' 
    aResult = oParser.parse(sHtmlContent,sPattern)
    if (aResult[0] == True):
        m3url =  aResult[1][0]
        oRequest = cRequestHandler(m3url)
        sHtmlContent = oRequest.request()
		    # (.+?) .+? ([^<]+)
    sPattern =  '<a href="([^<]+)" download class="link btn btn-light"><span ' 
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
    
    if (aResult[0] == True):
        
        sUrl = str(aResult[1][0])+ '|AUTH=TLS&verifypeer=false'+ '&User-Agent='+ UA
                 
        #on lance video directement
        oGuiElement = cGuiElement()
        oGuiElement.setSiteName(SITE_IDENTIFIER)
        oGuiElement.setTitle(sMovieTitle)
        oGuiElement.setMediaUrl(sUrl)
        oGuiElement.setThumbnail(sThumbnail)

        oPlayer = cPlayer()
        oPlayer.clearPlayList()
        oPlayer.addItemToPlaylist(oGuiElement)
        oPlayer.startPlayer()
        return
    
    else:
        return
    oGui.setEndOfDirectory()