# -*- coding: utf-8 -*-
# zombi https://github.com/zombiB/zombi-addons/

import re
	
from resources.lib.gui.hoster import cHosterGui
from resources.lib.gui.gui import cGui
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.comaddon import progress, VSlog, siteManager, addon
from resources.lib.parser import cParser

ADDON = addon()
icons = ADDON.getSetting('defaultIcons')

SITE_IDENTIFIER = 'tuktukcinema'
SITE_NAME = 'Tuktukcinema'
SITE_DESC = 'arabic vod'
 
URL_MAIN = siteManager().getUrlMain(SITE_IDENTIFIER)
 
MOVIE_PACK = (URL_MAIN , 'showPack')
MOVIE_EN = (URL_MAIN + 'category/movies-33/افلام-اجنبي/', 'showMovies')
MOVIE_HI = (URL_MAIN + 'category/movies-33/افلام-هندى/', 'showMovies')
MOVIE_ASIAN = (URL_MAIN + 'category/movies-33/افلام-اسيوي/', 'showMovies')
MOVIE_TURK = (URL_MAIN + 'category/movies-33/افلام-تركي/', 'showMovies')
KID_MOVIES = (URL_MAIN + 'category/anime-6/افلام-انمي/', 'showMovies')
SERIE_EN = (URL_MAIN + 'category/series-9/مسلسلات-اجنبي/', 'showSeries')


SERIE_HEND = (URL_MAIN + 'category/series-9/مسلسلات-هندي/', 'showSeries')
SERIE_ASIA = (URL_MAIN + 'category/series-9/مسلسلات-أسيوي/', 'showSeries')
SERIE_TR = (URL_MAIN + 'category/series-9/مسلسلات-تركي/', 'showSeries')
ANIM_NEWS = (URL_MAIN + 'category/anime-6/انمي-مترجم/', 'showSeries')
URL_SEARCH = (URL_MAIN + '/search/', 'showMovies')
URL_SEARCH_MOVIES = (URL_MAIN + '/?s=%D9%81%D9%8A%D9%84%D9%85+', 'showMovies')
URL_SEARCH_SERIES = (URL_MAIN + '/?s=%D9%85%D8%B3%D9%84%D8%B3%D9%84+', 'showSeriesSearch')
FUNCTION_SEARCH = 'showSeries'
 
def load():
    oGui = cGui()

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'http://venom/')
    oGui.addDir(SITE_IDENTIFIER, 'showSearch', 'Search Movies', icons + '/Search.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', 'http://venom/')
    oGui.addDir(SITE_IDENTIFIER, 'showSearchSeries', 'Search Series', icons + '/Search.png', oOutputParameterHandler)

	
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_PACK[0])
    oGui.addDir(SITE_IDENTIFIER, 'showPack', 'أقسام الموقع', icons + '/Icon.png', oOutputParameterHandler)
	
	

    oOutputParameterHandler.addParameter('siteUrl', MOVIE_EN[0])
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'أفلام أجنبية', icons + '/MoviesEnglish.png', oOutputParameterHandler)



    oOutputParameterHandler.addParameter('siteUrl', MOVIE_ASIAN[0])
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'أفلام أسيوية', icons + '/Asian.png', oOutputParameterHandler)


    oOutputParameterHandler.addParameter('siteUrl', MOVIE_TURK[0])
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'أفلام تركية', icons + '/Turkish.png', oOutputParameterHandler)


    oOutputParameterHandler.addParameter('siteUrl', MOVIE_HI[0])
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'أفلام هندية', icons + '/Hindi.png', oOutputParameterHandler)


    oOutputParameterHandler.addParameter('siteUrl', KID_MOVIES[0])
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'أفلام كرتون', icons + '/Cartoon.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', SERIE_EN[0])
    oGui.addDir(SITE_IDENTIFIER, 'showSeries', 'مسلسلات أجنبية', icons + '/TVShowsEnglish.png', oOutputParameterHandler)




    oOutputParameterHandler.addParameter('siteUrl', SERIE_ASIA[0])
    oGui.addDir(SITE_IDENTIFIER, 'showSeries', 'مسلسلات أسيوية', icons + '/Asian.png', oOutputParameterHandler)


    oOutputParameterHandler.addParameter('siteUrl', SERIE_TR[0])
    oGui.addDir(SITE_IDENTIFIER, 'showSeries', 'مسلسلات تركية', icons + '/Turkish.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', ANIM_NEWS[0])
    oGui.addDir(SITE_IDENTIFIER, 'showSeries', 'مسلسلات إنمي', icons + '/Anime.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', SERIE_HEND[0])
    oGui.addDir(SITE_IDENTIFIER, 'showSeries', 'مسلسلات هندية', icons + '/Hindi.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()
 
def showSearch():
    oGui = cGui()
 
    sSearchText = oGui.showKeyBoard()
    if sSearchText:
        sUrl = URL_MAIN + '/?s='+sSearchText+'+%D9%81%D9%8A%D9%84%D9%85'
        showMovies(sUrl)
        oGui.setEndOfDirectory()
        return
 
def showSearchSeries():
    oGui = cGui()
 
    sSearchText = oGui.showKeyBoard()
    if sSearchText:
        sUrl = URL_MAIN + '/?s='+sSearchText+'+%D9%85%D8%B3%D9%84%D8%B3%D9%84'
        showSeries(sUrl)
        oGui.setEndOfDirectory()
        return

def showPack(sSearch = ''):
    oGui = cGui()
    if sSearch:
      sUrl = sSearch
    else:
        oInputParameterHandler = cInputParameterHandler()
        sUrl = oInputParameterHandler.getValue('siteUrl')
 
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
# ([^<]+) .+? 

    sPattern = '<a href="([^<]+)">([^<]+)</a>'


    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
	
	
    if aResult[0]:
        oOutputParameterHandler = cOutputParameterHandler()
        for aEntry in aResult[1]:
            sTitle = aEntry[1].replace("مشاهدة","").replace("مترجمة","").replace("مترجم","").replace("فيلم","").replace("والأخيرة","").replace("مدبلج للعربية","مدبلج").replace("والاخيرة","").replace("كاملة","").replace("حلقات كاملة","").replace("اونلاين","").replace("مباشرة","").replace("انتاج ","").replace("جودة عالية","").replace("كامل","").replace("HD","").replace("السلسلة الوثائقية","").replace("الفيلم الوثائقي","").replace("اون لاين","") 
            sThumb = aEntry[1]
            siteUrl = aEntry[0]
            sDesc = ''
			

            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl',siteUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
			
            if 'sercat' in siteUrl:
                oGui.addDir(SITE_IDENTIFIER, 'showSeries', sTitle, sThumb, oOutputParameterHandler)
            else:
                oGui.addDir(SITE_IDENTIFIER, 'showMovies', sTitle, sThumb, oOutputParameterHandler)
 
        sNextPage = __checkForNextPage(sHtmlContent)
        if sNextPage:
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sNextPage)
            oGui.addDir(SITE_IDENTIFIER, 'showPack', '[COLOR teal]Next >>>[/COLOR]', icons + '/next.png', oOutputParameterHandler)
 
    if not sSearch:
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
 
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
    
    oParser = cParser()

    # (.+?) .+? ([^<]+)   
    sPattern = '<div class="Block--Item.+?href="([^<]+)" title="(.+?)">.+?src="(.+?)" alt='
    aResult = oParser.parse(sHtmlContent, sPattern)
    if aResult[0]:
        total = len(aResult[1])
        progress_ = progress().VScreate(SITE_NAME)
        oOutputParameterHandler = cOutputParameterHandler()
        for aEntry in aResult[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break
 
            sTitle = aEntry[1].replace("مشاهدة","").replace("مسلسل","").replace("انمي","").replace("مترجمة","").replace("مترجم","").replace("فيلم","").replace("والأخيرة","").replace("مدبلج للعربية","مدبلج").replace("والاخيرة","").replace("كاملة","").replace("حلقات كاملة","").replace("اونلاين","").replace("مباشرة","").replace("انتاج ","").replace("جودة عالية","").replace("كامل","").replace("HD","").replace("السلسلة الوثائقية","").replace("الفيلم الوثائقي","").replace("اون لاين","").replace("الموسم العاشر","S10").replace("الموسم الحادي عشر","S11").replace("الموسم الثاني عشر","S12").replace("الموسم الثالث عشر","S13").replace("الموسم الرابع عشر","S14").replace("الموسم الخامس عشر","S15").replace("الموسم السادس عشر","S16").replace("الموسم السابع عشر","S17").replace("الموسم الثامن عشر","S18").replace("الموسم التاسع عشر","S19").replace("الموسم العشرون","S20").replace("الموسم الحادي و العشرون","S21").replace("الموسم الثاني و العشرون","S22").replace("الموسم الثالث و العشرون","S23").replace("الموسم الرابع والعشرون","S24").replace("الموسم الخامس و العشرون","S25").replace("الموسم السادس والعشرون","S26").replace("الموسم السابع والعشرون","S27").replace("الموسم الثامن والعشرون","S28").replace("الموسم التاسع والعشرون","S29").replace("الموسم الثلاثون","S30").replace("الموسم الحادي و الثلاثون","S31").replace("الموسم الثاني والثلاثون","S32").replace("الموسم الاول","S1").replace("الموسم الثاني","S2").replace("الموسم الثالث","S3").replace("الموسم الثالث","S3").replace("الموسم الرابع","S4").replace("الموسم الخامس","S5").replace("الموسم السادس","S6").replace("الموسم السابع","S7").replace("الموسم الثامن","S8").replace("الموسم التاسع","S9").replace("الموسم","S").replace("S ","S").replace("الحلقة "," E")
            siteUrl = aEntry[0]+'/watch'
            sThumb = aEntry[2]
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
  # ([^<]+) .+?

    sPattern = '<li><a href="([^<]+)">([^<]+)</a></li>'
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
 
            sTitle = aEntry[1]
            
            sTitle =  "PAGE " + sTitle
            sTitle =   '[COLOR red]'+sTitle+'[/COLOR]'
            siteUrl = aEntry[0]
            sThumb = ""


            oOutputParameterHandler.addParameter('siteUrl',siteUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
			
            oGui.addDir(SITE_IDENTIFIER, 'showMovies', sTitle, '', oOutputParameterHandler)

        progress_.VSclose(progress_)
 
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
 # ([^<]+) .+?
    sPattern = '<div class="Block--Item.+?href="([^<]+)" title="(.+?)">.+?src="(.+?)" alt='

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
 
            sTitle = aEntry[1].replace("مشاهدة","").replace("مسلسل","").replace("انمي","").replace("مترجمة","").replace("مترجم","").replace("فيلم","").replace("والأخيرة","").replace("مدبلج للعربية","مدبلج").replace("والاخيرة","").replace("كاملة","").replace("حلقات كاملة","").replace("اونلاين","").replace("مباشرة","").replace("انتاج ","").replace("جودة عالية","").replace("كامل","").replace("HD","").replace("السلسلة الوثائقية","").replace("الفيلم الوثائقي","").replace("اون لاين","")
            sYear = ''
           
            m = re.search('([0-9]{4})', sTitle)
            if m:
                sYear = str(m.group(0))
                sTitle = sTitle.replace(sYear,'')
            siteUrl = aEntry[0]+'/watch/'
            sThumb = aEntry[2]
            sDesc = ''
            sDisplayTitle = sTitle.replace("الموسم العاشر","S10").replace("الموسم الحادي عشر","S11").replace("الموسم الثاني عشر","S12").replace("الموسم الثالث عشر","S13").replace("الموسم الرابع عشر","S14").replace("الموسم الخامس عشر","S15").replace("الموسم السادس عشر","S16").replace("الموسم السابع عشر","S17").replace("الموسم الثامن عشر","S18").replace("الموسم التاسع عشر","S19").replace("الموسم العشرون","S20").replace("الموسم الحادي و العشرون","S21").replace("الموسم الثاني و العشرون","S22").replace("الموسم الثالث و العشرون","S23").replace("الموسم الرابع والعشرون","S24").replace("الموسم الخامس و العشرون","S25").replace("الموسم السادس والعشرون","S26").replace("الموسم السابع والعشرون","S27").replace("الموسم الثامن والعشرون","S28").replace("الموسم التاسع والعشرون","S29").replace("الموسم الثلاثون","S30").replace("الموسم الحادي و الثلاثون","S31").replace("الموسم الثاني والثلاثون","S32").replace("الموسم الاول","S1").replace("الموسم الثاني","S2").replace("الموسم الثالث","S3").replace("الموسم الثالث","S3").replace("الموسم الرابع","S4").replace("الموسم الخامس","S5").replace("الموسم السادس","S6").replace("الموسم السابع","S7").replace("الموسم الثامن","S8").replace("الموسم التاسع","S9").replace("الموسم","S").replace("S ","S").replace("الحلقة "," E")

            oOutputParameterHandler.addParameter('siteUrl',siteUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sDisplayTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oOutputParameterHandler.addParameter('sYear', sYear)
            oOutputParameterHandler.addParameter('sDesc', sDesc)
			
            oGui.addEpisode(SITE_IDENTIFIER, 'showHosters', sDisplayTitle, '', sThumb, sDesc, oOutputParameterHandler)

        progress_.VSclose(progress_)
  # ([^<]+) .+?

    sPattern = '<li><a class="page-numbers" href="(.+?)">(.+?)</a></li>'

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
 
            sTitle = aEntry[1]           
            sTitle =  "PAGE " + sTitle
            sTitle =   '[COLOR red]'+sTitle+'[/COLOR]'
            siteUrl = URL_MAIN + aEntry[0]
            sThumb = ""


            oOutputParameterHandler.addParameter('siteUrl',siteUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
			
            oGui.addDir(SITE_IDENTIFIER, 'showSeriesSearch', sTitle, '', oOutputParameterHandler)

        progress_.VSclose(progress_)
 
        sNextPage = __checkForNextPage(sHtmlContent)
        if sNextPage:
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sNextPage)
            oGui.addDir(SITE_IDENTIFIER, 'showSeriesSearch', '[COLOR teal]Next >>>[/COLOR]', icons + '/next.png', oOutputParameterHandler)
 
    if not sSearch:
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
 
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
 # ([^<]+) .+? (.+?)
    sPattern = '<div class="Block--Item"><a href="([^<]+)" title=""><div class="Poster--Block"><img src="https://w.tuktukcinema.net/wp-content/themes/Elshaikh/no.png" alt="([^<]+)" data-src="([^<]+)"></div>.+?</li></ul><h3>.+?</h3></div></a></div>'

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
 
            sTitle = aEntry[1].replace("مشاهدة","").replace("مسلسل","").replace("انمي","").replace("مترجمة","").replace("مترجم","").replace("فيلم","").replace("والأخيرة","").replace("مدبلج للعربية","مدبلج").replace("والاخيرة","").replace("كاملة","").replace("حلقات كاملة","").replace("اونلاين","").replace("مباشرة","").replace("انتاج ","").replace("جودة عالية","").replace("كامل","").replace("HD","").replace("السلسلة الوثائقية","").replace("الفيلم الوثائقي","").replace("اون لاين","").replace(" والأخيرة","")
            sYear = ''
            m = re.search('([0-9]{4})', sTitle)
            if m:
                sYear = str(m.group(0))
                sTitle = sTitle.replace(sYear,'')
            siteUrl = aEntry[0]
            sThumb = aEntry[2]
            sDesc = ''
            sDisplayTitle = sTitle.replace("الموسم العاشر","S10").replace("الموسم الحادي عشر","S11").replace("الموسم الثاني عشر","S12").replace("الموسم الثالث عشر","S13").replace("الموسم الرابع عشر","S14").replace("الموسم الخامس عشر","S15").replace("الموسم السادس عشر","S16").replace("الموسم السابع عشر","S17").replace("الموسم الثامن عشر","S18").replace("الموسم التاسع عشر","S19").replace("الموسم العشرون","S20").replace("الموسم الحادي و العشرون","S21").replace("الموسم الثاني و العشرون","S22").replace("الموسم الثالث و العشرون","S23").replace("الموسم الرابع والعشرون","S24").replace("الموسم الخامس و العشرون","S25").replace("الموسم السادس والعشرون","S26").replace("الموسم السابع والعشرون","S27").replace("الموسم الثامن والعشرون","S28").replace("الموسم التاسع والعشرون","S29").replace("الموسم الثلاثون","S30").replace("الموسم الحادي و الثلاثون","S31").replace("الموسم الثاني والثلاثون","S32").replace("الموسم الاول","S1").replace("الموسم الثاني","S2").replace("الموسم الثالث","S3").replace("الموسم الثالث","S3").replace("الموسم الرابع","S4").replace("الموسم الخامس","S5").replace("الموسم السادس","S6").replace("الموسم السابع","S7").replace("الموسم الثامن","S8").replace("الموسم التاسع","S9").replace("الموسم","S").replace("S ","S").replace("الحلقة "," E")


            oOutputParameterHandler.addParameter('siteUrl',siteUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sDisplayTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oOutputParameterHandler.addParameter('sYear', sYear)
            oOutputParameterHandler.addParameter('sDesc', sDesc)
			
            oGui.addTV(SITE_IDENTIFIER, 'showSeasons', sDisplayTitle, '', sThumb, sDesc, oOutputParameterHandler)

        progress_.VSclose(progress_)

 
    if not sSearch:
        oGui.setEndOfDirectory()

def showSeasons():
	oGui = cGui()
    
	oInputParameterHandler = cInputParameterHandler()
	sUrl = oInputParameterHandler.getValue('siteUrl')
	sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
	sThumb = oInputParameterHandler.getValue('sThumb')
 
	oRequestHandler = cRequestHandler(sUrl)
	sHtmlContent = oRequestHandler.request()
    # .+? ([^<]+)
	sPattern = '<div class="Block--Item"><a href="([^<]+)" title=""><div class="Poster--Block"><img src="https://w.tuktukcinema.net/wp-content/themes/Elshaikh/no.png" alt="([^<]+)" data-srccs="([^<]+)"></div>'

	oParser = cParser()
	aResult = oParser.parse(sHtmlContent, sPattern)
		
	if aResult[0]:
		oOutputParameterHandler = cOutputParameterHandler()
		for aEntry in aResult[1]:
 
			sTitle = sMovieTitle+aEntry[1].replace("الموسم","S").replace("S ","S")
			siteUrl = aEntry[0]
			sThumb = aEntry[2]
			sDesc = ""
			
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
    # .+? ([^<]+) (.+?)
	sPattern = '<a href="(.+?)" title=.+?<div class="epnum"><span>الحلقة</span>(.+?)</div></a>'

	oParser = cParser()
	aResult = oParser.parse(sHtmlContent, sPattern)
	
	
	if aResult[0]:
		oOutputParameterHandler = cOutputParameterHandler()
		for aEntry in aResult[1]:
 
			sTitle = "E"+aEntry[1].replace("E ","E")
			sTitle = sMovieTitle+sTitle
			siteUrl = aEntry[0]+'/watch/'
			sThumb = ""
			sDesc = ""
			
			oOutputParameterHandler.addParameter('siteUrl',siteUrl)
			oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
			oOutputParameterHandler.addParameter('sThumb', sThumb)
			oGui.addEpisode(SITE_IDENTIFIER, 'showHosters', sTitle, '', sThumb, sDesc, oOutputParameterHandler)
        
	oGui.setEndOfDirectory()
  
     # (.+?)
def __checkForNextPage(sHtmlContent):
    sPattern = '<li><a href="([^<]+)">الصفحة التالية &laquo;</a></li>'
	
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
 
    if aResult[0]:
        return aResult[1][0]
    sPattern = 'href="(.+?)">&laquo;</a>'
	
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
 
    if aResult[0]:
        return aResult[1][0]
    return False

def showHosters():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')

    oRequestHandler = cRequestHandler(sUrl)
    oRequestHandler.addHeaderEntry('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:45.0) Gecko/20100101 Firefox/45.0')
    oRequestHandler.addHeaderEntry('Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8')
    oRequestHandler.addHeaderEntry('X-Requested-With', 'XMLHttpRequest')
    oRequestHandler.addHeaderEntry('Accept-Language', 'fr,fr-FR;q=0.8,en-US;q=0.5,en;q=0.3')
    sHtmlContent = oRequestHandler.request()
    # (.+?) ([^<]+) .+?
              
    sPattern = 'data-link="(.+?)" class='
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)

    if aResult[0]:
        for aEntry in aResult[1]:           
            url = aEntry
            sTitle = " " 
            if url.startswith('//'):
               url = 'http:' + url
								
            sHosterUrl = url 
            if '?download_' in sHosterUrl:
               sHosterUrl = sHosterUrl.replace("moshahda","ffsff")
               sHosterUrl = sHosterUrl + "|Referer=" + URL_MAIN 
            if 'userload' in sHosterUrl:
                sHosterUrl = sHosterUrl + "|Referer=" + URL_MAIN
            if 'moshahda' in sHosterUrl:
                sHosterUrl = sHosterUrl + "|Referer=" + URL_MAIN 
            if 'mystream' in sHosterUrl:
                sHosterUrl = sHosterUrl + "|Referer=" + URL_MAIN  
            oHoster = cHosterGui().checkHoster(sHosterUrl)
            if oHoster:
                oHoster.setDisplayName(sMovieTitle)
                oHoster.setFileName(sMovieTitle)
                cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb)
    # (.+?) ([^<]+) .+?

    sPattern = '<a target="_blank" href="(.+?)" class="download--direct"><i class="fa fa-download"></i><span>(.+?)</span>'
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)

    if aResult[0]:
        for aEntry in aResult[1]:           
            url = aEntry[0]
            sTitle = sMovieTitle+'('+aEntry[1]+')' 
            if url.startswith('//'):
               url = 'http:' + url
								
            sHosterUrl = url 
            if '?download_' in sHosterUrl:
               sHosterUrl = sHosterUrl.replace("moshahda","ffsff")
               sHosterUrl = sHosterUrl + "|Referer=" + URL_MAIN 
            if 'userload' in sHosterUrl:
               sHosterUrl = sHosterUrl + "|Referer=" + URL_MAIN
            if 'moshahda' in sHosterUrl:
               sHosterUrl = sHosterUrl + "|Referer=" + URL_MAIN 
            if 'mystream' in sHosterUrl:
               sHosterUrl = sHosterUrl + "|Referer=" + URL_MAIN  
            oHoster = cHosterGui().checkHoster(sHosterUrl)
            if oHoster:
               oHoster.setDisplayName(sTitle)
               oHoster.setFileName(sMovieTitle)
               cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb)
    # (.+?) ([^<]+) .+?

    sPattern = '<a target="_NEW" href="(.+?)" class="download--item">'
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)

    if aResult[0]:
        for aEntry in aResult[1]:           
            url = aEntry
            sTitle = " " 
            if url.startswith('//'):
               url = 'http:' + url
								
            sHosterUrl = url 
            if '?download_' in sHosterUrl:
              sHosterUrl = sHosterUrl.replace("moshahda","ffsff")
              sHosterUrl = sHosterUrl + "|Referer=" + URL_MAIN 
            if 'userload' in sHosterUrl:
              sHosterUrl = sHosterUrl + "|Referer=" + URL_MAIN
            if 'moshahda' in sHosterUrl:
              sHosterUrl = sHosterUrl + "|Referer=" + URL_MAIN 
            if 'mystream' in sHosterUrl:
              sHosterUrl = sHosterUrl + "|Referer=" + URL_MAIN  
            oHoster = cHosterGui().checkHoster(sHosterUrl)
            if oHoster:
               oHoster.setDisplayName(sMovieTitle)
               oHoster.setFileName(sMovieTitle)
               cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb)
				                     
				               
    oGui.setEndOfDirectory()