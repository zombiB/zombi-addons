# -*- coding: utf-8 -*-
# zombi https://github.com/zombiB/zombi-addons/

import re
	
from resources.lib.gui.hoster import cHosterGui
from resources.lib.gui.gui import cGui
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.comaddon import VSlog, siteManager, addon
from resources.lib.parser import cParser
from resources.lib.util import Quote
from resources.lib.Styling import getGenreIcon
from resources.lib import random_ua

from bs4 import BeautifulSoup
import requests

UA = random_ua.get_ua()
ADDON = addon()
icons = ADDON.getSetting('defaultIcons')

SITE_IDENTIFIER = 'shoffree'
SITE_NAME = 'Shoffree'
SITE_DESC = 'arabic vod'
 
URL_MAIN = siteManager().getUrlMain(SITE_IDENTIFIER)

oParser = cParser()
 
oRequestHandler = cRequestHandler(URL_MAIN)
sHtmlContent = oRequestHandler.request()
    # (.+?) ([^<]+)

sPattern = '<meta property="og:url" content="(.+?)" />'
aResult = oParser.parse(sHtmlContent, sPattern)
    
if (aResult[0]):
    URL_MAIN = aResult[1][0]
    VSlog(URL_MAIN)

MOVIE_EN = (URL_MAIN + '/movies', 'showMovies')
MOVIE_GENRES = (True, 'showGenresM')
MOVIE_ANNEES= (True, 'showGenresM')
RAMADAN_SERIES = (URL_MAIN + '/ramadan', 'showSeries')
SERIE_EN = (URL_MAIN + '/series', 'showSeries')
SERIE_GENRES = (True, 'showGenresS')
SERIE_ANNEES = (True, 'showGenresS')

ANIM_NEWS = (URL_MAIN + '/anime', 'showSeries')

#URL_SEARCH_MOVIES = (URL_MAIN + '/search?query=', 'showMovies')
#URL_SEARCH_SERIES = (URL_MAIN + '/search?query=', 'showSeries')
FUNCTION_SEARCH = 'showMovies'

s = requests.Session()
        
def load():
    oGui = cGui()

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'http://venom/')
    oGui.addDir(SITE_IDENTIFIER, 'showSearch', 'SEARCH_MOVIES', icons + '/Search.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', 'http://venom/')
    oGui.addDir(SITE_IDENTIFIER, 'showSeriesSearch', 'SEARCH_SERIES', icons + '/Search.png', oOutputParameterHandler)
 
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_EN[0])
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'جميع الافلام', icons + '/MoviesEnglish.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', True)
    oGui.addDir(SITE_IDENTIFIER, 'showGenresM', 'افلام حسب النوع', icons + '/Genres.png', oOutputParameterHandler)
    
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', True)
    oGui.addDir(SITE_IDENTIFIER, 'showLangsM', 'افلام حسب اللغة', icons + '/Movies.png', oOutputParameterHandler)
    
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', SERIE_EN[0])
    oGui.addDir(SITE_IDENTIFIER, 'showSeries', 'جميع المسلسلات', icons + '/TVShowsEnglish.png', oOutputParameterHandler)
    
    oOutputParameterHandler.addParameter('siteUrl', RAMADAN_SERIES[0])
    oGui.addDir(SITE_IDENTIFIER, 'showSeries', 'مسلسلات رمضان', icons + '/Ramadan.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', True)
    oGui.addDir(SITE_IDENTIFIER, 'showGenresS', 'مسلسلات حسب النوع', icons + '/Genres.png', oOutputParameterHandler)
    
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', True)
    oGui.addDir(SITE_IDENTIFIER, 'showLangsS', 'مسلسلات حسب اللغة', icons + '/Genres.png', oOutputParameterHandler)
	
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', ANIM_NEWS[0])
    oGui.addDir(SITE_IDENTIFIER, 'showSeries', 'مسلسلات إنمي', icons + '/Anime.png', oOutputParameterHandler)  

    oGui.setEndOfDirectory()

def main_function(sHtmlContent):
    oParser = cParser()
    sPattern = '<a class="naked" href="([^"]+)'
    aResult = oParser.parse(sHtmlContent, sPattern)    
    if (aResult[0]):
        sMain = aResult[1][0]+'/'
    return sMain
 
def showSearch():
    oGui = cGui()
 
    sSearchText = oGui.showKeyBoard()
    if sSearchText is not False:
        sUrl = URL_MAIN + '/search?query='+sSearchText
        showMovies(sUrl)
        oGui.setEndOfDirectory()
        return
 
def showSeriesSearch():
    oGui = cGui()
 
    sSearchText = oGui.showKeyBoard()
    if sSearchText is not False:
        sUrl = URL_MAIN + '/search?query='+sSearchText
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
    URL_MAIN2 = main_function(sHtmlContent)

    if URL_MAIN2:
        sUrl = sUrl.replace(URL_MAIN, URL_MAIN2)

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
            oOutputParameterHandler.addParameter('siteUrl', URL_MAIN + 'movies?year=' + sYear) 
            oGui.addDir(SITE_IDENTIFIER, 'showMovies', sYear, 'annees.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()

def showSerieYears():
    oGui = cGui()
    
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')

    oParser = cParser()
    oRequestHandler = cRequestHandler(URL_MAIN)
    sHtmlContent = oRequestHandler.request()
    URL_MAIN2 = main_function(sHtmlContent)

    if URL_MAIN2:
        sUrl = sUrl.replace(URL_MAIN, URL_MAIN2)

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
            oOutputParameterHandler.addParameter('siteUrl', URL_MAIN + 'series?year=' + sYear) 
            oGui.addDir(SITE_IDENTIFIER, 'showSeries', sYear, 'annees.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()

def showLang():
    oGui = cGui()
    
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')

    oParser = cParser()
    oRequestHandler = cRequestHandler(URL_MAIN)
    sHtmlContent = oRequestHandler.request()
    URL_MAIN2 = main_function(sHtmlContent)

    if URL_MAIN2:
        sUrl = sUrl.replace(URL_MAIN, URL_MAIN2)

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
            oOutputParameterHandler.addParameter('siteUrl', URL_MAIN + 'movies?lang=' + sYear) 
            oGui.addDir(SITE_IDENTIFIER, 'showMovies', sYear, 'annees.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()

def showSerieLang():
    oGui = cGui()
    
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')

    oParser = cParser()
    oRequestHandler = cRequestHandler(URL_MAIN)
    sHtmlContent = oRequestHandler.request()
    URL_MAIN2 = main_function(sHtmlContent)

    if URL_MAIN2:
        sUrl = sUrl.replace(URL_MAIN, URL_MAIN2)

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

    oParser = cParser()
    oRequestHandler = cRequestHandler(URL_MAIN)
    sHtmlContent = oRequestHandler.request()
    URL_MAIN2 = main_function(sHtmlContent)

    if URL_MAIN2:
        sUrl = sUrl.replace(URL_MAIN, URL_MAIN2)

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    sPattern = '<div class="BlockItem.+?<a href="(.+?)" title="(.+?)">.+?data-src="(.+?)" alt='
    aResult = oParser.parse(sHtmlContent, sPattern)
    if aResult[0] is True:
        oOutputParameterHandler = cOutputParameterHandler() 
        for aEntry in aResult[1]:
            if 'serie/' in aEntry[0] or 'episode/' in aEntry[0]:
                continue 

            sTitle = aEntry[1].replace("مشاهدة","").replace("برنامج","").replace("مترجم","").replace("فيلم","").replace("اون لاين","").replace("WEB-DL","").replace("BRRip","").replace("720p","").replace("HD-TC","").replace("HDRip","").replace("HD-CAM","").replace("DVDRip","").replace("BluRay","").replace("1080p","").replace("WEBRip","").replace("WEB-dl","").replace("4K","").replace("All","").replace("BDRip","").replace("HDCAM","").replace("HDTC","").replace("HDTV","").replace("HD","").replace("720","").replace("HDCam","").replace("Full HD","").replace("1080","").replace("HC","").replace("Web-dl","").replace("مدبلج للعربية","").replace("مدبلج","").replace("عرض","").replace("الرو","")
            siteUrl = aEntry[0]
            sThumb = aEntry[2].replace('/w342','/w500')
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
    URL_MAIN2 = main_function(sHtmlContent)

    if URL_MAIN2:
        sUrl = sUrl.replace(URL_MAIN, URL_MAIN2)

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    sPattern = '<div class="BlockItem.+?<a href="(.+?)" title="(.+?)">.+?data-src="(.+?)" alt='
    aResult = oParser.parse(sHtmlContent, sPattern)
    itemList = []		
    if aResult[0] is True:
        oOutputParameterHandler = cOutputParameterHandler() 
        for aEntry in aResult[1]:
            if 'movie/' in aEntry[0]:
                continue 
 
            sTitle = aEntry[1].replace("مشاهدة","").replace("مسلسل","").replace("انمي","").replace("مترجمة","").replace("مترجم","").replace("برنامج","").replace("فيلم","").replace("اون لاين","").replace("WEB-DL","").replace("BRRip","").replace("720p","").replace("HD-TC","").replace("HDRip","").replace("HD-CAM","").replace("DVDRip","").replace("BluRay","").replace("1080p","").replace("WEBRip","").replace("WEB-dl","").replace("مترجم ","").replace("مشاهدة وتحميل","").replace("اون لاين","").replace("مدبلج للعربية","مدبلج")
            siteUrl = aEntry[0]
            sThumb = aEntry[2].replace('/w342','/w500')
            sDesc = ''
            sTitle = sTitle.replace("الموسم العاشر","S10").replace("الموسم الحادي عشر","S11").replace("الموسم الثاني عشر","S12").replace("الموسم الثالث عشر","S13").replace("الموسم الرابع عشر","S14").replace("الموسم الخامس عشر","S15").replace("الموسم السادس عشر","S16").replace("الموسم السابع عشر","S17").replace("الموسم الثامن عشر","S18").replace("الموسم التاسع عشر","S19").replace("الموسم العشرون","S20").replace("الموسم الحادي و العشرون","S21").replace("الموسم الثاني و العشرون","S22").replace("الموسم الثالث و العشرون","S23").replace("الموسم الرابع والعشرون","S24").replace("الموسم الخامس و العشرون","S25").replace("الموسم السادس والعشرون","S26").replace("الموسم السابع والعشرون","S27").replace("الموسم الثامن والعشرون","S28").replace("الموسم التاسع والعشرون","S29").replace("الموسم الثلاثون","S30").replace("الموسم الحادي و الثلاثون","S31").replace("الموسم الثاني والثلاثون","S32").replace("الموسم الأول","S1").replace("الموسم الاول","S1").replace("الموسم الثانى","S2").replace("الموسم الثاني","S2").replace("الموسم الثالث","S3").replace("الموسم الثالث","S3").replace("الموسم الرابع","S4").replace("الموسم الخامس","S5").replace("الموسم السادس","S6").replace("الموسم السابع","S7").replace("الموسم الثامن","S8").replace("الموسم التاسع","S9").replace("الموسم","S").replace("موسم","S").replace("S ","S").split('الحلقة')[0]

            if sTitle not in itemList:
                itemList.append(sTitle)	
                oOutputParameterHandler.addParameter('siteUrl',siteUrl)
                oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
                oOutputParameterHandler.addParameter('sThumb', sThumb)
                oOutputParameterHandler.addParameter('sDesc', sDesc)
                oGui.addTV(SITE_IDENTIFIER, 'showSeasons', sTitle, '', sThumb, sDesc, oOutputParameterHandler)


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
            sTitle = aEntry[1].replace("-"," ").replace("مشاهدة","").replace("مسلسل","").replace("انمي","").replace("مترجمة","").replace("مترجم","").replace("كامل","").replace("برنامج","").replace("فيلم","").replace("الموسم العاشر","S10").replace("الموسم الحادي عشر","S11").replace("الموسم الثاني عشر","S12").replace("الموسم الثالث عشر","S13").replace("الموسم الرابع عشر","S14").replace("الموسم الخامس عشر","S15").replace("الموسم السادس عشر","S16").replace("الموسم السابع عشر","S17").replace("الموسم الثامن عشر","S18").replace("الموسم التاسع عشر","S19").replace("الموسم العشرون","S20").replace("الموسم الحادي و العشرون","S21").replace("الموسم الثاني و العشرون","S22").replace("الموسم الثالث و العشرون","S23").replace("الموسم الرابع والعشرون","S24").replace("الموسم الخامس و العشرون","S25").replace("الموسم السادس والعشرون","S26").replace("الموسم السابع والعشرون","S27").replace("الموسم الثامن والعشرون","S28").replace("الموسم التاسع والعشرون","S29").replace("الموسم الثلاثون","S30").replace("الموسم الحادي و الثلاثون","S31").replace("الموسم الثاني والثلاثون","S32").replace("الموسم الاول","S1").replace("الموسم الأول","S1").replace("الموسم الثاني","S2").replace("الموسم الثالث","S3").replace("الموسم الثالث","S3").replace("الموسم الرابع","S4").replace("الموسم الخامس","S5").replace("الموسم السادس","S6").replace("الموسم السابع","S7").replace("الموسم الثامن","S8").replace("الموسم التاسع","S9").replace("الموسم","S").replace("موسم","S").replace("S ","S")
            siteUrl = aEntry[0]
            sThumb = aEntry[2].replace('/w342','/w500')
            sDesc = ""

            oOutputParameterHandler.addParameter('siteUrl',siteUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sMovieUrl', sUrl)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oGui.addSeason(SITE_IDENTIFIER, 'showEps', sTitle, '', sThumb, sDesc, oOutputParameterHandler)

    else:
        sPattern = '<a class="sku" href="(.+?)" title=.+?data-src="(.+?)" alt.+?class="episode" style="display: inline;">.+?<i>(.+?)</i></span>'
        aResult = oParser.parse(sHtmlContent, sPattern)
        if aResult[0] is True:
            oOutputParameterHandler = cOutputParameterHandler() 
            for aEntry in aResult[1]:

                sEp =  "E"+aEntry[2].replace(" ","")
                sTitle = sMovieTitle+sEp
                siteUrl = aEntry[0]
                sThumb = aEntry[1].replace('/w342','/w500')
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

    sPattern = '<a class="sku" href="(.+?)" title=.+?data-src="(.+?)" alt.+?class="episode" style="display: inline;">.+?<i>(.+?)</i></span>'
    aResult = oParser.parse(sHtmlContent, sPattern)
    if aResult[0] is True:
        oOutputParameterHandler = cOutputParameterHandler() 
        for aEntry in aResult[1]:

            sEp =  "E"+aEntry[2].replace(" ","")
            sTitle = sMovieTitle+sEp
            siteUrl = aEntry[0]
            sThumb = aEntry[1].replace('/w342','/w500')
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
        return sUrl+'&'+aResult[1][0]

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

    sMain = main_function(sHtmlContent)
    if sMain:
        URL_MAIN = sMain

    sPattern =  '<span id="loader" class="loader hidden">.+?href="([^"]+)' 
    aResult = oParser.parse(sHtmlContent,sPattern)
    if aResult[0]:
        mshort = aResult[1][0] 

    oRequestHandler = cRequestHandler(mshort)
    oRequestHandler.addHeaderEntry('User-Agent', UA)
    oRequestHandler.addHeaderEntry('Referer', sUrl.encode("utf-8"))
    oRequestHandler.addHeaderEntry('Host', "shoffree.net")
    sHtmlContent = oRequestHandler.request()

    sPattern =  'name="key" value="([^"]+)' 
    aResult = oParser.parse(sHtmlContent,sPattern)
    if aResult[0]:
        mkey = aResult[1][0]

    oRequestHandler = cRequestHandler(sUrl.encode("utf-8"))
    oRequestHandler.addHeaderEntry('User-Agent', UA)
    oRequestHandler.addHeaderEntry('Referer', mshort)
    oRequestHandler.addHeaderEntry('Host', "shoffree.net")
    oRequestHandler.addParameters('key', mkey)
    oRequestHandler.setRequestType(1)
    sHtmlContent = oRequestHandler.request()

    sPattern = 'data-embed="([^"]+)'
    aResult = oParser.parse(sHtmlContent, sPattern)
    if aResult[0]:
        for aEntry in aResult[1]:
            if 'http' not in aEntry:
                continue          
            url = aEntry
            if 'role/' in url:
                xcode = url.rsplit("/",2)[1]
                if 'movie/' in sUrl:
                    url = f'https://r.site-panel.click/stream/{xcode}/movie?role=' + "|Referer=" + URL_MAIN
                else:
                    url = f'https://r.site-panel.click/stream/{xcode}/episode?role=' + "|Referer=" + URL_MAIN

            sHosterUrl = url
            if 'userload' in sHosterUrl:
                sHosterUrl = sHosterUrl + "|Referer=" + URL_MAIN
            if 'shoffree' in sHosterUrl:
                sHosterUrl = sHosterUrl + "|Referer=" + sUrl
            if 'mystream' in sHosterUrl:
                sHosterUrl = sHosterUrl + "|Referer=" + URL_MAIN    
            oHoster = cHosterGui().checkHoster(sHosterUrl)
            if oHoster != False:
                oHoster.setDisplayName(sMovieTitle)
                oHoster.setFileName(sMovieTitle)
                cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb)

    oGui.setEndOfDirectory()