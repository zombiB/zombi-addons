#-*- coding: utf-8 -*-
#zombi.(@geekzombi)
from resources.lib.gui.hoster import cHosterGui
from resources.lib.handler.hosterHandler import cHosterHandler
from resources.lib.gui.gui import cGui
from resources.lib.gui.guiElement import cGuiElement
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.comaddon import progress
from resources.lib.parser import cParser
from resources.lib.util import cUtil
import urllib2,urllib,re,xbmc
import unicodedata
import requests
import sys 
 
SITE_IDENTIFIER = 'shahidu'
SITE_NAME = 'shahid4u'
SITE_DESC = 'arabic vod'
 
URL_MAIN = 'https://shahid4u.cc'

RAMADAN_SERIES = ('https://shahid4u.cc/category/%d9%85%d8%b3%d9%84%d8%b3%d9%84%d8%a7%d8%aa-%d8%b1%d9%85%d8%b6%d8%a7%d9%86-2020-1', 'showSerie')
MOVIE_EN = ('https://shahid4u.cc/category/%d8%a7%d9%81%d9%84%d8%a7%d9%85-%d8%a7%d8%ac%d9%86%d8%a8%d9%8a', 'showMovies')
MOVIE_HI = ('https://shahid4u.cc/category/%D8%A7%D9%81%D9%84%D8%A7%D9%85-%D9%87%D9%86%D8%AF%D9%8A', 'showMovies')
MOVIE_AR = ('https://shahid4u.cc/category/%D8%A7%D9%81%D9%84%D8%A7%D9%85-%D8%B9%D8%B1%D8%A8%D9%8A', 'showMovies')

DOC_NEWS = ('https://shahid4u.cc/genre/Documentary', 'showMovies')
DOC_SERIES = ('https://shahid4u.cc/genre/Documentary', 'showSerie')
SERIE_HEND = ('https://shahid4u.cc/category/%d9%85%d8%b3%d9%84%d8%b3%d9%84%d8%a7%d8%aa-%d9%87%d9%86%d8%af%d9%8a%d8%a9', 'showSerie')

SERIE_TR = ('https://shahid4u.cc/category/%d9%85%d8%b3%d9%84%d8%b3%d9%84%d8%a7%d8%aa-%d8%aa%d8%b1%d9%83%d9%8a%d9%87', 'showSeries')
SERIE_EN = ('https://shahid4u.cc/category/%D9%85%D8%B3%D9%84%D8%B3%D9%84%D8%A7%D8%AA-%D8%A7%D8%AC%D9%86%D8%A8%D9%8A', 'showSerie')
SERIE_AR = ('https://shahid4u.cc/category/%D9%85%D8%B3%D9%84%D8%B3%D9%84%D8%A7%D8%AA-%D8%B9%D8%B1%D8%A8%D9%8A', 'showSerie')
SERIE_GENRES = (True, 'showGenres')
ANIM_NEWS = ('https://shahid4u.cc/category/%D9%85%D8%B3%D9%84%D8%B3%D9%84%D8%A7%D8%AA-%D8%A7%D9%86%D9%85%D9%8A', 'showSerie')
REPLAYTV_NEWS = ('https://shahid4u.cc/category/%D8%A8%D8%B1%D8%A7%D9%85%D8%AC-%D8%AA%D9%84%D9%81%D8%B2%D9%8A%D9%88%D9%86%D9%8A%D8%A9', 'showSerie')


URL_SEARCH = ('https://shahid4u.onl/search?s=', 'showMovies')
URL_SEARCH_MOVIES = ('https://shahid4u.onl/search?s=%D9%81%D9%8A%D9%84%D9%85+', 'showMovies')
URL_SEARCH_SERIES = ('https://shahid4u.onl/search?s=%D9%85%D8%B3%D9%84%D8%B3%D9%84+', 'showSerie')
FUNCTION_SEARCH = 'showMovies'
 
def load():
    oGui = cGui()

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'http://venom/')
    oGui.addDir(SITE_IDENTIFIER, 'showSearch', 'Search Movies', 'search.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'http://venom/')
    oGui.addDir(SITE_IDENTIFIER, 'showSearchSeries', 'Search Series', 'search.png', oOutputParameterHandler)
            
    oGui.setEndOfDirectory()
 
def showSearch():
    oGui = cGui()
 
    sSearchText = oGui.showKeyBoard()
    if (sSearchText != False):
        sUrl = 'https://shahid4u.onl/search?s=%D9%81%D9%8A%D9%84%D9%85+'+sSearchText
        showMovies(sUrl)
        oGui.setEndOfDirectory()
        return
 
def showSearchSeries():
    oGui = cGui()
 
    sSearchText = oGui.showKeyBoard()
    if (sSearchText != False):
        sUrl = 'https://shahid4u.onl/search?s=%D9%85%D8%B3%D9%84%D8%B3%D9%84+'+sSearchText
        showSerie(sUrl)
        oGui.setEndOfDirectory()
        return
   

def showGenres():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
 
    liste = []
    liste.append( ["مالك بن الريب ","http://https://shahid4u.cc/%D9%85%D8%B3%D9%84%D8%B3%D9%84-%D9%85%D8%A7%D9%84%D9%83-%D8%A8%D9%86-%D8%A7%D9%84%D8%B1%D9%8A%D8%A8-%D8%A7%D9%84%D8%AD%D9%84%D9%82%D8%A9-30-%D9%88%D8%A7%D9%84%D8%A7%D8%AE%D9%8A%D8%B1%D8%A9"] )
    liste.append( ["مسلسلات-رمضان-2016","http://https://shahid4u.cc/category/ramadan/مسلسلات-رمضان-2016/"] )
	            
    for sTitle,sUrl in liste:
        
        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', sUrl)
        oGui.addDir(SITE_IDENTIFIER, 'showSeries', sTitle, 'genres.png', oOutputParameterHandler)
       
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

    sPattern = '<div class="content-box"><a href="([^<]+)" class=.+?data-src="([^<]+)" class="image"></a>.+?<h3>([^<]+)</h3></a><p>([^<]+)</p>'

    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
	
	
    if (aResult[0] == True):
        total = len(aResult[1])
        progress_ = progress().VScreate(SITE_NAME)
        for aEntry in aResult[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break
 
            sTitle = aEntry[2].decode("utf8")
            sTitle = cUtil().unescape(sTitle).encode("utf8")
            sTitle = sTitle.replace("مشاهدة","").replace("مترجمة","").replace("مترجم","").replace("فيلم","").replace("اون لاين","").replace("WEB-DL","").replace("BRRip","").replace("720p","").replace("HD-TC","").replace("HDRip","").replace("HD-CAM","").replace("DVDRip","").replace("BluRay","").replace("1080p","").replace("WEBRip","").replace("WEB-dl","").replace("مترجم ","").replace("مشاهدة وتحميل","").replace("اون لاين","").replace("HD","").replace("كامل","")
            sThumbnail = aEntry[1]
            siteUrl = aEntry[0].replace("film","watch").replace("/episode/","/watch/")
            sInfo = ""
            sYear = ''
            sDub = ''
            m = re.search('([0-9]{4})', sTitle)
            if m:
				sYear = str(m.group(0))
				sTitle = sTitle.replace(sYear,'')
            m = re.search('مدبلج', sTitle)
            if m:
				sDub = str(m.group(0))
				sTitle = sTitle.replace(sDub,'')
            sDisplayTitle = ('%s (%s) [%s]') % (sTitle, sYear, sDub)

            # Filtrer les résultats
            if sSearch and total > 5:
                if cUtil().CheckOccurence(sSearch.replace(URL_SEARCH_MOVIES[0], ''), sTitle) == 0:
                    continue
 


            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl',siteUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumbnail', sThumbnail)

            oGui.addMovie(SITE_IDENTIFIER, 'showServers', sDisplayTitle, '', sThumbnail, sInfo, oOutputParameterHandler)
        
        progress_.VSclose(progress_)
 
        sNextPage = __checkForNextPage(sHtmlContent)
        if (sNextPage != False):
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
 #([^<]+).+?

    sPattern = '<div class="content-box"><a href="([^<]+)" class=.+?data-src="([^<]+)" class="image"></a>.+?<h3>([^<]+)</h3></a><p>([^<]+)</p>'

    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
	
	
    if (aResult[0] == True):
        total = len(aResult[1])
        progress_ = progress().VScreate(SITE_NAME)
        for aEntry in aResult[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break
 
            sTitle = aEntry[2].decode("utf8")
            sTitle = cUtil().unescape(sTitle).encode("utf8")
            sTitle = sTitle.replace("مشاهدة","").replace("مسلسل","").replace("انمي","").replace("مترجمة","").replace("مترجم","").replace("برنامج","").replace("فيلم","").replace("اون لاين","").replace("WEB-DL","").replace("BRRip","").replace("720p","").replace("HD-TC","").replace("HDRip","").replace("HD-CAM","").replace("DVDRip","").replace("BluRay","").replace("1080p","").replace("WEBRip","").replace("WEB-dl","").replace("مترجم ","").replace("والأخيرة","").replace("والاخيرة","").replace("الأخيرة","").replace("الاخيرة","").replace("مشاهدة وتحميل","").replace("اون لاين","").replace("كامل","")
            sThumbnail = aEntry[1]
            siteUrl = aEntry[0]
            sInfo = ""
            sDisplayTitle2 = sTitle.split('الحلقة')[0].split('الموسم')[0]
            sDisplayTitle2 = sDisplayTitle2.split('مدبلج')[0]
            sDisplayTitle = sTitle.replace("الموسم الحادي عشر","S11").replace("الموسم الثاني عشر","S12").replace("الموسم الثالث عشر","S13").replace("الموسم الرابع عشر","S14").replace("الموسم الخامس عشر","S15").replace("الموسم السادس عشر","S16").replace("الموسم السابع عشر","S17").replace("الموسم الثامن عشر","S18").replace("الموسم التاسع عشر","S19").replace("الموسم العشرون","S20").replace("الموسم الحادي و العشرون","S21").replace("الموسم الثاني و العشرون","S22").replace("الموسم الثالث و العشرون","S23").replace("الموسم الرابع والعشرون","S24").replace("الموسم الخامس و العشرون","S25").replace("الموسم السادس والعشرون","S26").replace("الموسم السابع والعشرون","S27").replace("الموسم الثامن والعشرون","S28").replace("الموسم التاسع والعشرون","S29").replace("الموسم الثلاثون","S30").replace("الموسم الحادي و الثلاثون","S31").replace("الموسم الثاني والثلاثون","S32").replace("الموسم الاول","S1").replace("الموسم الثاني","S2").replace("الموسم الثالث","S3").replace("الموسم الثالث","S3").replace("الموسم الرابع","S4").replace("الموسم الخامس","S5").replace("الموسم السادس","S6").replace("الموسم السابع","S7").replace("الموسم الثامن","S8").replace("الموسم التاسع","S9").replace("الموسم العاشر","S10").replace("الموسم","S").replace("S ","S").split('الحلقة')[0]


            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl',siteUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sDisplayTitle2)
            oOutputParameterHandler.addParameter('sThumbnail', sThumbnail)

            oGui.addTV(SITE_IDENTIFIER, 'showEpisodes', sDisplayTitle, '', sThumbnail, sInfo, oOutputParameterHandler)
        
        progress_.VSclose(progress_)
 
        sNextPage = __checkForNextPage(sHtmlContent)
        if (sNextPage != False):
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sNextPage)
            oGui.addDir(SITE_IDENTIFIER, 'showSeries', '[COLOR teal]Next >>>[/COLOR]', 'next.png', oOutputParameterHandler)
 
    if not sSearch:
        oGui.setEndOfDirectory()

def showSerie(sSearch = ''):
    oGui = cGui()
    if sSearch:
      sUrl = sSearch
    else:
        oInputParameterHandler = cInputParameterHandler()
        sUrl = oInputParameterHandler.getValue('siteUrl')
 
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
 

    sPattern = '<div class="content-box"><a href="([^<]+)" class=.+?data-src="([^<]+)" class="image"></a>.+?<h3>([^<]+)</h3></a><p>([^<]+)</p>'

    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
	
	
    if (aResult[0] == True):
        total = len(aResult[1])
        progress_ = progress().VScreate(SITE_NAME)
        for aEntry in aResult[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break
 
            sTitle = aEntry[2].decode("utf8")
            sTitle = cUtil().unescape(sTitle).encode("utf8")
            sTitle = sTitle.replace("مشاهدة","").replace("مسلسل","").replace("انمي","").replace("مترجمة","").replace("مترجم","").replace("برنامج","").replace("فيلم","").replace("اون لاين","").replace("WEB-DL","").replace("BRRip","").replace("720p","").replace("HD-TC","").replace("HDRip","").replace("HD-CAM","").replace("DVDRip","").replace("BluRay","").replace("1080p","").replace("WEBRip","").replace("WEB-dl","").replace("مترجم ","").replace("والأخيرة","").replace("والاخيرة","").replace("الأخيرة","").replace("الاخيرة","").replace("مشاهدة وتحميل","").replace("اون لاين","").replace("كامل","")
            siteUrl = str(aEntry[0])
            sThumbnail = str(aEntry[1])
            sInfo = ""
            sDisplayTitle2 = sTitle.split('الحلقة')[0].split('الموسم')[0]
            sDisplayTitle2 = sDisplayTitle2.split('مدبلج')[0]
            sDisplayTitle = sTitle.replace("الموسم الحادي عشر","S11").replace("الموسم الثاني عشر","S12").replace("الموسم الثالث عشر","S13").replace("الموسم الرابع عشر","S14").replace("الموسم الخامس عشر","S15").replace("الموسم السادس عشر","S16").replace("الموسم السابع عشر","S17").replace("الموسم الثامن عشر","S18").replace("الموسم التاسع عشر","S19").replace("الموسم العشرون","S20").replace("الموسم الحادي و العشرون","S21").replace("الموسم الثاني و العشرون","S22").replace("الموسم الثالث و العشرون","S23").replace("الموسم الرابع والعشرون","S24").replace("الموسم الخامس و العشرون","S25").replace("الموسم السادس والعشرون","S26").replace("الموسم السابع والعشرون","S27").replace("الموسم الثامن والعشرون","S28").replace("الموسم التاسع والعشرون","S29").replace("الموسم الثلاثون","S30").replace("الموسم الحادي و الثلاثون","S31").replace("الموسم الثاني والثلاثون","S32").replace("الموسم الاول","S1").replace("الموسم الثاني","S2").replace("الموسم الثالث","S3").replace("الموسم الثالث","S3").replace("الموسم الرابع","S4").replace("الموسم الخامس","S5").replace("الموسم السادس","S6").replace("الموسم السابع","S7").replace("الموسم الثامن","S8").replace("الموسم التاسع","S9").replace("الموسم العاشر","S10").replace("الموسم","S").replace("S ","S").split('الحلقة')[0]

            # Filtrer les résultats
            if sSearch and total > 5:
                if cUtil().CheckOccurence(sSearch.replace(URL_SEARCH_SERIES[0], ''), sTitle) == 0:
                    continue


            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl',siteUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sDisplayTitle2)
            oOutputParameterHandler.addParameter('sMovieTitle2', sDisplayTitle)
            oOutputParameterHandler.addParameter('sThumbnail', sThumbnail)
			
            oGui.addTV(SITE_IDENTIFIER, 'showEpisodes', sDisplayTitle, '', sThumbnail, sInfo, oOutputParameterHandler)

        progress_.VSclose(progress_)
 
        sNextPage = __checkForNextPage(sHtmlContent)
        if (sNextPage != False):
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sNextPage)
            oGui.addDir(SITE_IDENTIFIER, 'showSerie', '[COLOR teal]Next >>>[/COLOR]', 'next.png', oOutputParameterHandler)
 
    if not sSearch:
        oGui.setEndOfDirectory()

def showEpisodes():
    oGui = cGui()
    
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sMovieTitle2 = oInputParameterHandler.getValue('sMovieTitle2')
    sThumbnail = oInputParameterHandler.getValue('sThumbnail')
 
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
  # ([^<]+) .+?
    sPattern = '<a href="([^<]+)" class="col-6 col-s-4 col-m-3 col-l-1 button-block"><h3>الموسم<span>([^<]+)</span></h3></a>'

    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
	
	
    if (aResult[0] == True):
        total = len(aResult[1])
        progress_ = progress().VScreate(SITE_NAME)
        for aEntry in aResult[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break
 
            sTitle =  str(sMovieTitle)+"S" + aEntry[1]
            siteUrl = str(aEntry[0])+'/episodes'
            sThumbnail = str(sThumbnail)
			


            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl',siteUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumbnail', sThumbnail)
            oGui.addEpisode(SITE_IDENTIFIER, 'showEps', sTitle, '', sThumbnail, '', oOutputParameterHandler)
        
        progress_.VSclose(progress_)
  # ([^<]+) .+?
    sPattern = '<a href="([^<]+)" class="col-6 col-s-4 col-m-3 col-l-1 button-block"><h3>الحلقة <span>([^<]+)</span></h3></a>'

    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
	
	
    if (aResult[0] == True):
        total = len(aResult[1])
        progress_ = progress().VScreate(SITE_NAME)
        for aEntry in aResult[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break
 
            sTitle = "E" + aEntry[1]+str(sMovieTitle2)
            sTitle = sTitle
            siteUrl = str(aEntry[0]).replace("episode","watch")
            sThumbnail = str(sThumbnail)
		
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl',siteUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumbnail', sThumbnail)
            oGui.addEpisode(SITE_IDENTIFIER, 'showServers', sTitle, '', sThumbnail, '', oOutputParameterHandler)
        
        progress_.VSclose(progress_)
  # ([^<]+) .+?
    sPattern = '<a href="([^<]+)" class="col-6 col-s-4 col-m-3 col-l-1 button-block"><h3>الحلقة <span></span></h3></a>'

    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
	
    if (aResult[0] == True):
        total = len(aResult[1])
        progress_ = progress().VScreate(SITE_NAME)
        for aEntry in aResult[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break
 
            sTitle = aEntry.split('/episode/')[1].replace("-"," ")
            sTitle = sTitle.decode("utf8") 
            sTitle = cUtil().unescape(sTitle).encode("utf8")
            sTitle = sTitle.replace("مشاهدة","").replace("مسلسل","").replace("انمي","").replace("مترجمة","").replace("مترجم","").replace("برنامج","").replace("فيلم","").replace("اون لاين","").replace("WEB-DL","").replace("BRRip","").replace("720p","").replace("HD-TC","").replace("HDRip","").replace("HD-CAM","").replace("DVDRip","").replace("BluRay","").replace("1080p","").replace("WEBRip","").replace("WEB-dl","").replace("مترجم ","").replace("والأخيرة","").replace("والاخيرة","").replace("الأخيرة","").replace("الاخيرة","").replace("مشاهدة وتحميل","").replace("اون لاين","").replace("كامل","")
            sTitle = sTitle
            siteUrl = aEntry.replace("/episode/","/watch/")
            sThumbnail = str(sThumbnail)
            sDisplayTitle2 = sTitle.split('الحلقة')[0].split('الموسم')[0]
            sDisplayTitle2 = sDisplayTitle2.split('مدبلج')[0]
            sDisplayTitle = sTitle.replace("الموسم الحادي عشر","S11").replace("الموسم الثاني عشر","S12").replace("الموسم الثالث عشر","S13").replace("الموسم الرابع عشر","S14").replace("الموسم الخامس عشر","S15").replace("الموسم السادس عشر","S16").replace("الموسم السابع عشر","S17").replace("الموسم الثامن عشر","S18").replace("الموسم التاسع عشر","S19").replace("الموسم العشرون","S20").replace("الموسم الحادي و العشرون","S21").replace("الموسم الثاني و العشرون","S22").replace("الموسم الثالث و العشرون","S23").replace("الموسم الرابع والعشرون","S24").replace("الموسم الخامس و العشرون","S25").replace("الموسم السادس والعشرون","S26").replace("الموسم السابع والعشرون","S27").replace("الموسم الثامن والعشرون","S28").replace("الموسم التاسع والعشرون","S29").replace("الموسم الثلاثون","S30").replace("الموسم الحادي و الثلاثون","S31").replace("الموسم الثاني والثلاثون","S32").replace("الموسم الاول","S1").replace("الموسم الثاني","S2").replace("الموسم الثالث","S3").replace("الموسم الثالث","S3").replace("الموسم الرابع","S4").replace("الموسم الخامس","S5").replace("الموسم السادس","S6").replace("الموسم السابع","S7").replace("الموسم الثامن","S8").replace("الموسم التاسع","S9").replace("الموسم العاشر","S10").replace("الحلقة "," E").replace("الموسم","S").replace("S ","S")
			
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl',siteUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumbnail', sThumbnail)
            oGui.addEpisode(SITE_IDENTIFIER, 'showHosters', sDisplayTitle, '', sThumbnail, '', oOutputParameterHandler)
        
        progress_.VSclose(progress_)
 
        sNextPage = __checkForNextPage(sHtmlContent)
        if (sNextPage != False):
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sNextPage)
            oGui.addDir(SITE_IDENTIFIER, 'showEpisodes', '[COLOR teal]Next >>>[/COLOR]', 'next.png', oOutputParameterHandler)
       
    oGui.setEndOfDirectory()

def showEps():
    oGui = cGui()
    
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumbnail = oInputParameterHandler.getValue('sThumbnail')
 
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
  # ([^<]+) .+?
    sPattern = '<a href="([^<]+)" data-src="([^<]+)" class="image"></a>.+?<em>(.+?)</em></span>'

    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
	
	
    if (aResult[0] == True):
        total = len(aResult[1])
        progress_ = progress().VScreate(SITE_NAME)
        for aEntry in aResult[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break
 
            sTitle = "E" + aEntry[2]+str(sMovieTitle)
            siteUrl = str(aEntry[0]).replace("episode","watch")
            sThumbnail = aEntry[1]
			


            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl',siteUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumbnail', sThumbnail)
            oGui.addEpisode(SITE_IDENTIFIER, 'showServers', sTitle, '', sThumbnail, '', oOutputParameterHandler)
        
        progress_.VSclose(progress_)
 
        sNextPage = __checkForNextPage(sHtmlContent)
        if (sNextPage != False):
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sNextPage)
            oGui.addDir(SITE_IDENTIFIER, 'showEpisodes', '[COLOR teal]Next >>>[/COLOR]', 'next.png', oOutputParameterHandler)
       
    oGui.setEndOfDirectory()	
    # .+? ([^<]+)	
def __checkForNextPage(sHtmlContent):
    sPattern = '<li class="active"><a href="javascript:;">.+?</a></li><li><a href="([^<]+)">'
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
    if (aResult[0] == True):
        aResult = aResult[1][0]
        return aResult

    return False 
 
def showServers():
    oGui = cGui()
   
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumbnail = oInputParameterHandler.getValue('sThumbnail')
 
    oGui.addText(SITE_IDENTIFIER,'[COLOR olive]-------سيرفرات المشاهدة--------[/COLOR]')

    oRequestHandler = cRequestHandler(sUrl)
    oRequestHandler.addHeaderEntry('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:45.0) Gecko/20100101 Firefox/45.0')
    oRequestHandler.addHeaderEntry('Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8')
    oRequestHandler.addHeaderEntry('X-Requested-With', 'XMLHttpRequest')
    oRequestHandler.addHeaderEntry('Accept-Language', 'fr,fr-FR;q=0.8,en-US;q=0.5,en;q=0.3')
    sHtmlContent = oRequestHandler.request()
   
    oParser = cParser()

    sId='0'
    # (.+?) ([^<]+)

    sPattern = 'url: "([^<]+)",.+?data: {serverid: id},'
    aResult = oParser.parse(sHtmlContent, sPattern)

   
    if (aResult[0] == True):
        total = len(aResult[1])
        progress_ = progress().VScreate(SITE_NAME)
        for aEntry in aResult[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break

            sId = str(aEntry)

        for i in range(0,8):

            sTitle = 'server '+': '+str(i)
            siteUrl1 = sId+'&serverid='+str(i)
            sInfo = ""

            #print siteUrl 
            oRequestHandler = cRequestHandler(siteUrl1)
            oRequestHandler.addHeaderEntry('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:45.0) Gecko/20100101 Firefox/45.0')
            oRequestHandler.addHeaderEntry('Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8')
            oRequestHandler.addHeaderEntry('X-Requested-With', 'XMLHttpRequest')
            oRequestHandler.addHeaderEntry('Accept-Language', 'fr,fr-FR;q=0.8,en-US;q=0.5,en;q=0.3')
            sHtmlContent4 = oRequestHandler.request()
            sPattern = "([^<]+)"
            oParser = cParser()
            aResult = oParser.parse(sHtmlContent4, sPattern)
            if (aResult[0] == True):
				total = len(aResult[1])
				progress_ = progress().VScreate(SITE_NAME)
				for aEntry in aResult[1]:
					progress_.VSupdate(progress_, total)
					if progress_.iscanceled():
						break
            
					url = str(aEntry)
					sTitle = sMovieTitle
					if url.startswith('//'):
						url = 'http:' + url
				
					
            
					sHosterUrl = url 
					oHoster = cHosterGui().checkHoster(sHosterUrl)
					if (oHoster != False):
						sDisplayTitle = sTitle
						oHoster.setDisplayName(sDisplayTitle)
						oHoster.setFileName(sMovieTitle)
						cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumbnail)

	    #Affichage du menu  
    oGui.addText(SITE_IDENTIFIER,'[COLOR olive]-------سيرفرات التحميل--------[/COLOR]')
   
    #Recuperation infos
    sId = ''
    sUrl2 = ''

    sPattern = '&_post_id=([^<]+)",'
    aResult = oParser.parse(sHtmlContent, sPattern)
    
    if (aResult[0]):
        sId = aResult[1][0]
        sUrl2 = 'https://shahid4u.cc/ajaxCenter?_action=getdownloadlinks&postId='+sId



        oRequestHandler = cRequestHandler(sUrl2)
        oRequestHandler.addHeaderEntry('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:45.0) Gecko/20100101 Firefox/45.0')
        oRequestHandler.addHeaderEntry('Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8')
        oRequestHandler.addHeaderEntry('X-Requested-With', 'XMLHttpRequest')
        oRequestHandler.addHeaderEntry('Accept-Language', 'fr,fr-FR;q=0.8,en-US;q=0.5,en;q=0.3')
        sHtmlContent2 = oRequestHandler.request()


    # (.+?) .+? ([^<]+)        	
        sPattern = 'href="([^<]+)">'
        oParser = cParser()
        aResult = oParser.parse(sHtmlContent2, sPattern)

	
        if (aResult[0] == True):
            total = len(aResult[1])
            progress_ = progress().VScreate(SITE_NAME)
            for aEntry in aResult[1]:
                progress_.VSupdate(progress_, total)
                if progress_.iscanceled():
                    break
            
                url = str(aEntry)
                sTitle = sMovieTitle
                if url.startswith('//'):
                   url = 'http:' + url
				
					
            
                sHosterUrl = url 
                oHoster = cHosterGui().checkHoster(sHosterUrl)
                if (oHoster != False):
                   sDisplayTitle = sTitle
                   oHoster.setDisplayName(sDisplayTitle)
                   oHoster.setFileName(sMovieTitle)
                   cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumbnail)
      
    oGui.setEndOfDirectory()
 
def showHosters():
    oGui = cGui()
    import requests
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sMovieTitle2 = oInputParameterHandler.getValue('sMovieTitle')
    sThumbnail = oInputParameterHandler.getValue('sThumbnail')
    sInfo = oInputParameterHandler.getValue('sInfo')

    #print sHtmlContent 

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

   
    oParser = cParser()
    # ([^<]+) (.+?)       

    sPattern = 'data-embedd="(.+?)">'
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)

	
    if (aResult[0] == True):
			total = len(aResult[1])
			progress_ = progress().VScreate(SITE_NAME)
			for aEntry in aResult[1]:
				progress_.VSupdate(progress_, total)
				if progress_.iscanceled():
					break
            
				url = str(aEntry)
				sTitle =  sMovieTitle
				if 'vidcloud' in url:
					sTitle = " (vidcloud)"
				if url.startswith('//'):
					url = 'http:' + url
				
					
            
				sHosterUrl = url 
				oHoster = cHosterGui().checkHoster(sHosterUrl)
				if (oHoster != False):
					sDisplayTitle = sTitle
					oHoster.setDisplayName(sDisplayTitle)
					oHoster.setFileName(sMovieTitle)
					cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumbnail)
				

			progress_.VSclose(progress_)
                
    oGui.setEndOfDirectory()