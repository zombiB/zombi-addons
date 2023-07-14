# -*- coding: utf-8 -*-
#############################################################
# Yonn1981 https://github.com/Yonn1981/Repo
#############################################################

import requests,re

from resources.lib.gui.hoster import cHosterGui
from resources.lib.gui.gui import cGui
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.lib.comaddon import progress, VSlog, siteManager, addon
 
ADDON = addon()
icons = ADDON.getSetting('defaultIcons')

SITE_IDENTIFIER = 'egybest'
SITE_NAME = 'EgyBest'
SITE_DESC = 'arabic vod'
  
URL_MAIN = siteManager().getUrlMain(SITE_IDENTIFIER)

oParser = cParser()
 
oRequestHandler = cRequestHandler(URL_MAIN)
sHtmlContent = oRequestHandler.request()
    # (.+?) ([^<]+)

sPattern = '<meta property="og:url" content="([^"]+)'
aResult = oParser.parse(sHtmlContent, sPattern)
    
if (aResult[0]):
    URL_MAIN = aResult[1][0]+'/'

MOVIE_EN = (URL_MAIN + 'movies?lang=الإنجليزية', 'showMovies')
MOVIE_AR = (URL_MAIN + 'movies?lang=العربية', 'showMovies')
MOVIE_HI = (URL_MAIN + 'movies?lang=الهندية', 'showMovies')
MOVIE_ASIAN = (URL_MAIN + 'movies?lang=الكورية', 'showMovies')
MOVIE_TURK = (URL_MAIN + 'movies?lang=التركية', 'showMovies')
KID_MOVIES = (URL_MAIN + 'movies?genre=14', 'showMovies')
MOVIE_GENRES = (True, 'moviesGenres')
MOVIE_ANNEES = (URL_MAIN + 'movies', 'showYears')

SERIE_EN = (URL_MAIN + 'series?lang=الإنجليزية', 'showSeries')
SERIE_AR = (URL_MAIN + 'series?lang=العربية', 'showSeries')
SERIE_TR = (URL_MAIN + 'series?lang=التركية', 'showSeries')
SERIE_HEND = (URL_MAIN + 'series?lang=الهندية', 'showSeries')
SERIE_ASIA = (URL_MAIN + 'series?lang=الكورية', 'showSeries')
SERIE_GENRES = (True, 'seriesGenres')
SERIE_ANNEES = (URL_MAIN + 'series', 'showSerieYears')

ANIM_NEWS = (URL_MAIN + 'series?genre=40', 'showSeries')
ANIM_MOVIES = (URL_MAIN + 'movies?genre=40', 'showMovies')

URL_SEARCH = (URL_MAIN + 'search?query=', 'showMovies')
URL_SEARCH_MOVIES = (URL_MAIN + 'search?query=', 'showMovies')
URL_SEARCH_SERIES = (URL_MAIN + 'search?query=', 'showSeries')
FUNCTION_SEARCH = 'showMovies'

def load():
    oGui = cGui()

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'http://venom/')
    oGui.addDir(SITE_IDENTIFIER, 'showSearch', 'SEARCH MOVIES', icons + '/Search.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', 'http://venom/')
    oGui.addDir(SITE_IDENTIFIER, 'showSearchSeries', 'SEARCH SERIES', icons + '/Search.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_EN[0])
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'أفلام أجنبية', icons + '/MoviesEnglish.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_AR[0])
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'أفلام عربية', icons + '/Arabic.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_ASIAN[0])
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'أفلام أسيوية', icons + '/Asian.png', oOutputParameterHandler)
   
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_TURK[0])
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'أفلام تركية', icons + '/Turkish.png', oOutputParameterHandler)
    
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_HI[0])
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'أفلام هندية', icons + '/Hindi.png', oOutputParameterHandler) 
 
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', KID_MOVIES[0])
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'أفلام كرتون', icons + '/Cartoon.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', URL_MAIN + 'trending/movie?t=movie')
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'الأفلام الرائجة', icons + '/Movies.png', oOutputParameterHandler)	

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', SERIE_EN[0])
    oGui.addDir(SITE_IDENTIFIER, 'showSeries', 'مسلسلات أجنبية', icons + '/TVShowsEnglish.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', SERIE_AR[0])
    oGui.addDir(SITE_IDENTIFIER, 'showSeries', 'مسلسلات عربية', icons + '/Arabic.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', SERIE_ASIA[0])
    oGui.addDir(SITE_IDENTIFIER, 'showSeries', 'مسلسلات أسيوية', icons + '/TVShowsKorean.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', SERIE_TR[0])
    oGui.addDir(SITE_IDENTIFIER, 'showSeries', 'مسلسلات تركية', icons + '/Turkish.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', SERIE_HEND[0])
    oGui.addDir(SITE_IDENTIFIER, 'showSeries', 'مسلسلات هندية', icons + '/Hindi.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', URL_MAIN + 'trending/serie?t=serie')
    oGui.addDir(SITE_IDENTIFIER, 'showSeries', 'المسلسلات الرائجة', icons + '/TVShows.png', oOutputParameterHandler)	

    oOutputParameterHandler.addParameter('siteUrl', ANIM_MOVIES[0])
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'افلام انمي', icons + '/Cartoon.png', oOutputParameterHandler)
  
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', ANIM_NEWS[0])
    oGui.addDir(SITE_IDENTIFIER, 'showSeries', 'مسلسلات انمي', icons + '/Anime.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', SERIE_GENRES[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_GENRES[1], 'المسلسلات (الأنواع)', icons + '/TVShows.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_GENRES[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_GENRES[1], 'الأفلام (الأنواع)', icons + '/Movies.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', URL_MAIN + 'movies')
    oGui.addDir(SITE_IDENTIFIER, 'showYears', 'أفلام (بالسنوات)', 'annees.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', URL_MAIN + 'series')
    oGui.addDir(SITE_IDENTIFIER, 'showSerieYears', 'مسلسلات (بالسنوات)', 'annees.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', URL_MAIN + 'movies')
    oGui.addDir(SITE_IDENTIFIER, 'showLang', 'أفلام (حسب اللغة)', icons + '/Movies.png', oOutputParameterHandler)	

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', URL_MAIN + 'series')
    oGui.addDir(SITE_IDENTIFIER, 'showSerieLang', 'مسلسلات (حسب اللغة)', icons + '/TVShows.png', oOutputParameterHandler)	

    oGui.setEndOfDirectory()

	
def showSearch():
    oGui = cGui()
 
    sSearchText = oGui.showKeyBoard()
    if sSearchText:
        sUrl = URL_MAIN + 'search?query='+sSearchText
        showMovies(sUrl)
        oGui.setEndOfDirectory()
        return
 
def showSearchSeries():
    oGui = cGui()
 
    sSearchText = oGui.showKeyBoard()
    if sSearchText:
        sUrl = URL_MAIN + 'search?query='+sSearchText
        showSeries(sUrl)
        oGui.setEndOfDirectory()
        return

def showYears():
    oGui = cGui()
    
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
 
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    oParser = cParser()
     # (.+?) ([^<]+) .+?
    sStart = '<option selected value> السنة </option>'
    sEnd = '</select>'
    sHtmlContent = oParser.abParse(sHtmlContent, sStart, sEnd)

    sPattern = '<option value="([^"]+)"'
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
	

    if aResult[0]:
        oOutputParameterHandler = cOutputParameterHandler()    
        for aEntry in reversed(aResult[1]):
 
            sYear = aEntry
            oOutputParameterHandler.addParameter('siteUrl', URL_MAIN + 'movies?year=' + sYear) 
            oGui.addDir(SITE_IDENTIFIER, 'showMovies', sYear, 'annees.png', oOutputParameterHandler)
    oGui.setEndOfDirectory()

def showSerieYears():
    oGui = cGui()
    
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
 
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    oParser = cParser()
     # (.+?) ([^<]+) .+?
    sStart = '<option selected value> السنة </option>'
    sEnd = '</select>'
    sHtmlContent = oParser.abParse(sHtmlContent, sStart, sEnd)

    sPattern = '<option value="([^"]+)"'
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
	
    if aResult[0]:
        oOutputParameterHandler = cOutputParameterHandler()    
        for aEntry in reversed(aResult[1]):
 
            sYear = aEntry
            oOutputParameterHandler.addParameter('siteUrl', URL_MAIN + 'series?year=' + sYear) 
            oGui.addDir(SITE_IDENTIFIER, 'showSeries', sYear, 'annees.png', oOutputParameterHandler)
    oGui.setEndOfDirectory()

def showLang():
    oGui = cGui()
    
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
 
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    oParser = cParser()
     # (.+?) ([^<]+) .+?
    sStart = '<option selected value> اللغة </option>'
    sEnd = '</select>'
    sHtmlContent = oParser.abParse(sHtmlContent, sStart, sEnd)

    sPattern = '<option value="([^"]+)"'
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
	

    if aResult[0]:
        oOutputParameterHandler = cOutputParameterHandler()    
        for aEntry in aResult[1]:
 
            sYear = aEntry
            oOutputParameterHandler.addParameter('siteUrl', URL_MAIN + 'movies?lang=' + sYear) 
            oGui.addDir(SITE_IDENTIFIER, 'showMovies', sYear, 'annees.png', oOutputParameterHandler)
    oGui.setEndOfDirectory()

def showSerieLang():
    oGui = cGui()
    
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
 
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    oParser = cParser()
     # (.+?) ([^<]+) .+?
    sStart = '<option selected value> اللغة </option>'
    sEnd = '</select>'
    sHtmlContent = oParser.abParse(sHtmlContent, sStart, sEnd)

    sPattern = '<option value="([^"]+)"'
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
	
    if aResult[0]:
        oOutputParameterHandler = cOutputParameterHandler()    
        for aEntry in aResult[1]:
 
            sYear = aEntry
            oOutputParameterHandler.addParameter('siteUrl', URL_MAIN + 'series?lang=' + sYear) 
            oGui.addDir(SITE_IDENTIFIER, 'showSeries', sYear, 'annees.png', oOutputParameterHandler)
    oGui.setEndOfDirectory()

def seriesGenres():
    oGui = cGui()

    liste = []
    liste.append(['اكشن', URL_MAIN + 'series?genre=8'])
    liste.append(['انيميشن', URL_MAIN + 'series?genre=14'])
    liste.append(['مغامرات', URL_MAIN + 'series?genre=12'])
    liste.append(['غموض', URL_MAIN + 'series?genre=7'])
    liste.append(['تاريخي', URL_MAIN + 'series?genre=28'])
    liste.append(['كوميديا', URL_MAIN + 'series?genre=16'])
    liste.append(['موسيقى', URL_MAIN + 'series?genre=20'])
    liste.append(['رياضي', URL_MAIN + 'series?genre=25'])
    liste.append(['دراما', URL_MAIN + 'series?genre=6'])
    liste.append(['رعب', URL_MAIN + 'series?genre=9'])
    liste.append(['عائلى', URL_MAIN + 'series?genre=15'])
    liste.append(['فانتازيا', URL_MAIN + 'series?genre=38'])
    liste.append(['حروب', URL_MAIN + 'series?genre=36'])
    liste.append(['الجريمة', URL_MAIN + 'series?genre=17'])
    liste.append(['رومانسى', URL_MAIN + 'series?genre=5'])
    liste.append(['خيال علمى', URL_MAIN + 'series?genre=13'])
    liste.append(['اثارة', URL_MAIN + 'series?genre=11'])
    liste.append(['وثائقى', URL_MAIN + 'series?genre=19'])

    for sTitle, sUrl in liste:

        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', sUrl)
        oGui.addDir(SITE_IDENTIFIER, 'showSeries', sTitle, 'genres.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()

def moviesGenres():
    oGui = cGui()

    liste = []
    liste.append(['اكشن', URL_MAIN + 'movies?genre=8'])
    liste.append(['انيميشن', URL_MAIN + 'movies?genre=14'])
    liste.append(['مغامرات', URL_MAIN + 'movies?genre=12'])
    liste.append(['غموض', URL_MAIN + 'movies?genre=7'])
    liste.append(['تاريخي', URL_MAIN + 'movies?genre=28'])
    liste.append(['كوميديا', URL_MAIN + 'movies?genre=16'])
    liste.append(['موسيقى', URL_MAIN + 'movies?genre=20'])
    liste.append(['رياضي', URL_MAIN + 'movies?genre=25'])
    liste.append(['دراما', URL_MAIN + 'movies?genre=6'])
    liste.append(['رعب', URL_MAIN + 'movies?genre=9'])
    liste.append(['عائلى', URL_MAIN + 'movies?genre=15'])
    liste.append(['فانتازيا', URL_MAIN + 'movies?genre=38'])
    liste.append(['حروب', URL_MAIN + 'movies?genre=36'])
    liste.append(['الجريمة', URL_MAIN + 'movies?genre=17'])
    liste.append(['رومانسى', URL_MAIN + 'movies?genre=5'])
    liste.append(['خيال علمى', URL_MAIN + 'movies?genre=13'])
    liste.append(['اثارة', URL_MAIN + 'movies?genre=11'])
    liste.append(['وثائقى', URL_MAIN + 'movies?genre=19'])

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
 # ([^<]+) .+?

    sPattern = '<a class="block" href="([^"]+)".+?src="([^"]+)".+?title="([^"]+)'

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

            if 'serie/' in aEntry[0]:
                continue 

            sTitle = aEntry[2].replace("مشاهدة","").replace("مسلسل","").replace("انمي","").replace("مترجمة","").replace("مترجم","").replace("فيلم","").replace("والأخيرة","").replace("مدبلج للعربية","مدبلج").replace("والاخيرة","").replace("كاملة","").replace("حلقات كاملة","").replace("اونلاين","").replace("مباشرة","").replace("انتاج ","").replace("جودة عالية","").replace("كامل","").replace("HD","").replace("السلسلة الوثائقية","").replace("الفيلم الوثائقي","").replace("اون لاين","")
            siteUrl = aEntry[0]
            sThumb = aEntry[1].replace('/w342','/w500')
            if sThumb.startswith('//'):
                sThumb = "https:"+aEntry[1]
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
			
            oGui.addMovie(SITE_IDENTIFIER, 'showHosters', sTitle, '', sThumb, sDesc, oOutputParameterHandler)

        progress_.VSclose(progress_)
    if not sSearch:
        sNextPage = __checkForNextPageM(sHtmlContent, sUrl)
        if sNextPage:
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sNextPage)
            oGui.addDir(SITE_IDENTIFIER, 'showMovies', '[COLOR teal]Next >>>[/COLOR]', 'next.png', oOutputParameterHandler)
 
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
 # ([^<]+) .+?

    sPattern = '<a class="block" href="([^"]+)".+?src="([^"]+)".+?title="([^"]+)'

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

            if 'movie/' in aEntry[0]:
                continue 
            
            sTitle = aEntry[2].replace("مشاهدة","").replace("مترجمة","").replace("مترجم","").replace("فيلم","").replace("اون لاين","").replace("مشاهدة","").replace("مسلسل","").replace("انمي","").replace("مترجمة","").replace("مترجم","").replace("فيلم","").replace("والأخيرة","").replace("مدبلج للعربية","مدبلج").replace("والاخيرة","").replace("كاملة","").replace("حلقات كاملة","").replace("اونلاين","").replace("مباشرة","").replace("انتاج ","").replace("جودة عالية","").replace("كامل","").replace("HD","").replace("السلسلة الوثائقية","").replace("الفيلم الوثائقي","").replace("اون لاين","")
            sTitle = sTitle.replace("الموسم العاشر","S10").replace("الموسم الحادي عشر","S11").replace("الموسم الثاني عشر","S12").replace("الموسم الثالث عشر","S13").replace("الموسم الرابع عشر","S14").replace("الموسم الخامس عشر","S15").replace("الموسم السادس عشر","S16").replace("الموسم السابع عشر","S17").replace("الموسم الثامن عشر","S18").replace("الموسم التاسع عشر","S19").replace("الموسم العشرون","S20").replace("الموسم الحادي و العشرون","S21").replace("الموسم الثاني و العشرون","S22").replace("الموسم الثالث و العشرون","S23").replace("الموسم الرابع والعشرون","S24").replace("الموسم الخامس و العشرون","S25").replace("الموسم السادس والعشرون","S26").replace("الموسم السابع والعشرون","S27").replace("الموسم الثامن والعشرون","S28").replace("الموسم التاسع والعشرون","S29").replace("الموسم الثلاثون","S30").replace("الموسم الحادي و الثلاثون","S31").replace("الموسم الثاني والثلاثون","S32").replace("الموسم الاول","S1").replace("الموسم الثاني","S2").replace("الموسم الثالث","S3").replace("الموسم الثالث","S3").replace("الموسم الرابع","S4").replace("الموسم الخامس","S5").replace("الموسم السادس","S6").replace("الموسم السابع","S7").replace("الموسم الثامن","S8").replace("الموسم التاسع","S9").replace("الموسم","S").replace("موسم","S").replace("S ","S").split('الحلقة')[0]
            siteUrl = aEntry[0]
            sThumb = aEntry[1].replace('/w342','/w500')
            if sThumb.startswith('//'):
                sThumb = "https:"+aEntry[1]
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
			
            oGui.addTV(SITE_IDENTIFIER, 'showSeasons', sTitle, '', sThumb, sDesc, oOutputParameterHandler)

        progress_.VSclose(progress_)
    if not sSearch:
        sNextPage = __checkForNextPageS(sHtmlContent, sUrl)
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
 
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    oParser = cParser()
     # (.+?) ([^<]+) .+?
    sStart = '<h2 class="main-title clearfix">المواسم</h2>'
    sEnd = '</article>'
    sHtmlContent = oParser.abParse(sHtmlContent, sStart, sEnd)

    sPattern = '<a class="block" href="([^"]+)".+?data-src="([^"]+)".+?title="([^"]+)'

    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
	
	
    if aResult[0] is True:
        oOutputParameterHandler = cOutputParameterHandler()    
        for aEntry in aResult[1]:
 
            sTitle =  aEntry[2].replace("مشاهدة","").replace("الأخيرة","").replace("مسلسل","").replace("انمي","").replace("مترجمة","").replace("الاخيرة","").replace("مترجم","").replace(" الحادي عشر","11").replace(" الثاني عشر","12").replace(" الثالث عشر","13").replace(" الرابع عشر","14").replace(" الخامس عشر","15").replace(" السادس عشر","16").replace(" السابع عشر","17").replace(" الثامن عشر","18").replace(" التاسع عشر","19").replace(" العشرون","20").replace(" الحادي و العشرون","21").replace(" الثاني و العشرون","22").replace(" الثالث و العشرون","23").replace(" الرابع والعشرون","24").replace(" الخامس و العشرون","25").replace(" السادس والعشرون","26").replace(" السابع والعشرون","27").replace(" الثامن والعشرون","28").replace(" التاسع والعشرون","29").replace(" الثلاثون","30").replace(" الحادي و الثلاثون","31").replace(" الثاني والثلاثون","32").replace(" الاول","1").replace(" الثاني","2").replace(" الثانى","2").replace(" الثالث","3").replace(" الرابع","4").replace(" الخامس","5").replace(" السادس","6").replace(" السابع","7").replace(" الثامن","8").replace(" التاسع","9").replace(" العاشر","10").replace("الموسم","S")
            siteUrl = aEntry[0]
            sThumb = aEntry[1].replace('/w342','/w500')
            sDesc = ''
            if sThumb.startswith('//'):
                sThumb = "https:"+aEntry[1]
			


            oOutputParameterHandler.addParameter('siteUrl',siteUrl)
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
 
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    oParser = cParser()
     # (.+?) ([^<]+) .+?
    sStart = '<h2 class="main-title clearfix">الحلقات</h2>'
    sEnd = '</article>'
    sHtmlContent = oParser.abParse(sHtmlContent, sStart, sEnd)

    sPattern = '<a href="([^"]+)">(.+?)</a>'
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
	
	
    if aResult[0]:
        oOutputParameterHandler = cOutputParameterHandler()    
        for aEntry in aResult[1]:
 
            sTitle = aEntry[1].replace("الموسم","S").replace("(الاخيرة)","").split('الحلقة')[-1].replace("ى","").replace("ة","").replace("E ","E").replace(' - ', '')
            sTitle = ' E'+sTitle
            sTitle = sMovieTitle+sTitle
            siteUrl = aEntry[0].encode('utf-8').decode('utf-8')
            sThumb = sThumb
            sDesc = ''
			
            oOutputParameterHandler.addParameter('siteUrl',siteUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oGui.addEpisode(SITE_IDENTIFIER, 'showHosters', sTitle, '', sThumb, sDesc, oOutputParameterHandler) 


    sPattern = '<a class="block" href="([^"]+)".+?data-src="([^"]+)".+?title="([^"]+)'
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
	
	
    if aResult[0]:
        oOutputParameterHandler = cOutputParameterHandler()    
        for aEntry in aResult[1]:
 
            sTitle = aEntry[2].replace("الموسم","S").replace("(الاخيرة)","").split('الحلقة')[-1].replace("ى","").replace("ة","").replace("E ","E").replace(' - ', '')
            sTitle = ' E'+sTitle
            sTitle = sMovieTitle+sTitle
            siteUrl = aEntry[0].encode('utf-8').decode('utf-8')
            sThumb = aEntry[1]
            sDesc = ''
			
            oOutputParameterHandler.addParameter('siteUrl',siteUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oGui.addEpisode(SITE_IDENTIFIER, 'showHosters', sTitle, '', sThumb, sDesc, oOutputParameterHandler) 
      
    oGui.setEndOfDirectory()

 
 
def __checkForNextPageM(sHtmlContent, sUrl):
    sPattern = '<a href="([^<]+)" class="btn btn-primary btn-lg btn-block'
	
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
 
    if aResult[0]:
        return sUrl+'&'+aResult[1][0]

    return False

def __checkForNextPageS(sHtmlContent, sUrl):
    sPattern = '<a href="([^<]+)" class="btn btn-primary btn-lg btn-block'
	
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
 
    if aResult[0]:
        return sUrl+'&'+aResult[1][0]

    return False

def showHosters():
    oGui = cGui()
    import base64
    import requests


    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')
    if "الحلقة" in sUrl:
        rUrl1 = sUrl.split("/")[7]
        rUrl = sUrl.replace(rUrl1, '')
    else:
        rUrl1 = sUrl.split("/")[5]
        rUrl = sUrl.replace(rUrl1, '')

    oRequestHandler = cRequestHandler(sUrl)
    St=requests.Session()
    sHtmlContent1 = oRequestHandler.request()

    oParser = cParser()
    sPattern = '<iframe.+?src="([^"]+)'

    oParser = cParser()
    aResult = oParser.parse(sHtmlContent1, sPattern)

    if aResult[0]:
                    for aEntry in aResult[1]:
                        if "embed/" in aEntry:
                            url = aEntry
                            sHosterUrl = url+"eeggyy"
                            if "youtube" in sHosterUrl:
                                sTitle = 'Trailer'
                                sHosterUrl = url.split('?')[0]
                            else:
                                sTitle = sMovieTitle
                            oHoster = cHosterGui().checkHoster(sHosterUrl)
                            if oHoster:
                                sDisplayTitle = sTitle
                                oHoster.setDisplayName(sDisplayTitle)
                                oHoster.setFileName(sMovieTitle)
                                if "youtube" in sHosterUrl:
                                    cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb)
                                else:
                                    cHosterGui().showHoster(oGui, oHoster, sHosterUrl + "|Referer=" + rUrl, sThumb)
                                
                        if "stream/" in aEntry:
                            aurl = aEntry

                            cook = oRequestHandler.GetCookies()
                            hdr = {'Sec-Fetch-Mode' : 'navigate','Cookie' : cook,'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36 Edg/114.0.1823.58','Referer' : rUrl}
                            sHtmlContent = St.get(aurl,headers=hdr)
                            sHtmlContent = sHtmlContent.content
                            
                            sPattern = '<source src="([^"]+)".+?size="([^"]+)'
                            oParser = cParser()
                            aResult = oParser.parse(sHtmlContent, sPattern)

                            if aResult[0]:
                                for aEntry in aResult[1]:
            
                                    url = aEntry[0]
                                    qual = aEntry[1]
                                    sHosterUrl = url

                                    sTitle = ('%s  [COLOR coral](%sp)[/COLOR]') % (sMovieTitle, qual)
                                    oHoster = cHosterGui().checkHoster(sHosterUrl)
                                    if oHoster:
                                        sDisplayTitle = sTitle
                                        oHoster.setDisplayName(sDisplayTitle)
                                        oHoster.setFileName(sMovieTitle)
                                        cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb)

    sPattern =  'name="codes" value="(.+?)">' 
    aResult = oParser.parse(sHtmlContent1,sPattern)
    if aResult[0] is True:
        mcode = aResult[1][0] 

    sPattern = '<section class="code"><form action="(.+?)" method="post">'

    aResult = oParser.parse(sHtmlContent1,sPattern)
    if aResult[0] is True:
        murl2 = aResult[1][0] 

        import requests
        s = requests.Session()            
        headers = {'user-agent': 'Mozilla/5.0 (iPad; CPU OS 13_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) CriOS/87.0.4280.77 Mobile/15E148 Safari/604.1',
							'origin': "https://egy-best.site",
							'referer': rUrl}
        data = {'codes':mcode}
        r = s.post(murl2,data = data)
        sHtmlContent = r.content.decode('utf8')
   
        sPattern = '"iframe_a" href="([^"]+)'
        oParser = cParser()
        aResult = oParser.parse(sHtmlContent, sPattern)

	
        if aResult[0]:
           for aEntry in reversed(aResult[1]):
               if 'http' not in aEntry:
                    continue          
               url = aEntry
               sThumb = sThumb
               if url.startswith('//'):
                  url = 'http:' + url
								            
               sHosterUrl = url
               if 'userload' in sHosterUrl:
                  sHosterUrl = sHosterUrl + "|Referer=" + URL_MAIN
               if 'egy-best' in sHosterUrl:
                  sHosterUrl = sHosterUrl + "|Referer=" + murl2
               if 'mystream' in sHosterUrl:
                  sHosterUrl = sHosterUrl + "|Referer=" + URL_MAIN    
               oHoster = cHosterGui().checkHoster(sHosterUrl)
               if oHoster != False:
                  oHoster.setDisplayName(sMovieTitle)
                  oHoster.setFileName(sMovieTitle)
                  cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb)


    sPattern = '<div class="tr flex-start">.+?</div>.+?<div>(.+?)</div>.+?<a href="([^"]+)'

    oParser = cParser()
    aResult = oParser.parse(sHtmlContent1, sPattern)

    if aResult[0]:
           for aEntry in aResult[1]:
                refer = aEntry[1].split("/d")[0]
                url = aEntry[1]
                qual = aEntry[0].split('p')[0]
                oRequestHandler = cRequestHandler(url)
                sHtmlContent = oRequestHandler.request()
                St=requests.Session()

                sPattern = '<iframe.+?src="([^"]+)'
                oParser = cParser()
                aResult = oParser.parse(sHtmlContent, sPattern)

                if aResult[0]:
                    for aEntry in aResult[1]:
            
                        url = aEntry   
                        
                        cook = oRequestHandler.GetCookies()
                        hdr = {'Sec-Fetch-Mode' : 'navigate','Cookie' : cook,'User-Agent' : 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Mobile Safari/537.36 Edg/114.0.1823.67','Referer' : refer}
                        sHtmlContent = St.get(url,headers=hdr)
                        sHtmlContent = sHtmlContent.content.decode('utf8')
               
                        sPattern = '<a href="([^"]+)'
                        oParser = cParser()
                        aResult = oParser.parse(sHtmlContent, sPattern)

                        if aResult[0]:
                                for aEntry in aResult[1]:
            
                                    url = aEntry
                                    sHosterUrl = url

                                    sTitle = ('%s  [COLOR coral](%sp)[/COLOR]') % (sMovieTitle, qual)
                                    oHoster = cHosterGui().checkHoster(sHosterUrl)
                                    if oHoster:
                                        sDisplayTitle = sTitle
                                        oHoster.setDisplayName(sDisplayTitle)
                                        oHoster.setFileName(sMovieTitle)
                                        cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb)

                sPattern = 'Watch</button><a href="([^"]+)'
                oParser = cParser()
                aResult = oParser.parse(sHtmlContent, sPattern)

	
                if aResult[0]:
                    for aEntry in aResult[1]:
            
                        url = aEntry
                        sTitle = ('%s  [COLOR coral](%sp)[/COLOR]') % (sMovieTitle, qual)
                        if url.startswith('//'):
                            url = 'http:' + url
				            
                        sHosterUrl = url 
                        oHoster = cHosterGui().checkHoster(sHosterUrl)
                        if oHoster:
                            sDisplayTitle = sTitle
                            oHoster.setDisplayName(sDisplayTitle)
                            oHoster.setFileName(sMovieTitle)
                            cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb)
    oGui.setEndOfDirectory()