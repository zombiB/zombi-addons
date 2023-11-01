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
from resources.lib.comaddon import progress, VSlog, siteManager, addon
from resources.lib.parser import cParser

ADDON = addon()
icons = ADDON.getSetting('defaultIcons')
 
SITE_IDENTIFIER = 'topcinema'
SITE_NAME = 'TopCinema'
SITE_DESC = 'arabic vod'
 
URL_MAIN = siteManager().getUrlMain(SITE_IDENTIFIER)

MOVIE_EN = (URL_MAIN + 'category/افلام-اجنبي/', 'showMovies')
MOVIE_ASIAN = (URL_MAIN + 'category/افلام-اسيوي/', 'showMovies')
MOVIE_NETFLIX = (URL_MAIN + 'netflix-movies/', 'showMovies')
MOVIE_PACK = (URL_MAIN , 'showPack')
KID_MOVIES = (URL_MAIN + 'category/افلام-انمي/', 'showMovies')

SERIE_EN = (URL_MAIN + 'category/مسلسلات-اجنبي/', 'showSeries')
SERIE_NETFLIX = (URL_MAIN + 'netflix-series/?cat=7', 'showSeries')
SERIE_ASIA = (URL_MAIN + 'category/مسلسلات-اسيوية/', 'showSeries')
ANIM_NEWS = (URL_MAIN + 'category/مسلسلات-انمي/', 'showSeries')

URL_SEARCH = (URL_MAIN + '?s=', 'showMovies')
URL_SEARCH_MOVIES = (URL_MAIN +'?s=', 'showMovies')
URL_SEARCH_SERIES = (URL_MAIN +'?s=', 'showSeries')
FUNCTION_SEARCH = 'showMovies'
 
def load():
    oGui = cGui()
    addons = addon()

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'http://venom/')
    oGui.addDir(SITE_IDENTIFIER, 'showSearch', addons.VSlang(30078), icons + '/Search.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', 'http://venom/')
    oGui.addDir(SITE_IDENTIFIER, 'showSearchSeries', addons.VSlang(30079), icons + '/Search.png', oOutputParameterHandler)
	
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_EN[0])
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'أفلام أجنبية', icons + '/MoviesEnglish.png', oOutputParameterHandler)
         
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_ASIAN[0])
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'أفلام أسيوية', icons + '/Asian.png', oOutputParameterHandler)  
   
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_NETFLIX[0])
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'أفلام نيتفلكس', icons + '/MoviesEnglish.png', oOutputParameterHandler)
       
    oOutputParameterHandler.addParameter('siteUrl', KID_MOVIES[0])
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'أفلام كرتون', icons + '/Cartoon.png', oOutputParameterHandler)
    
    oOutputParameterHandler.addParameter('siteUrl', SERIE_EN[0])
    oGui.addDir(SITE_IDENTIFIER, 'showSeries', 'مسلسلات أجنبية', icons + '/TVShowsEnglish.png', oOutputParameterHandler)
   
    oOutputParameterHandler.addParameter('siteUrl', SERIE_ASIA[0])
    oGui.addDir(SITE_IDENTIFIER, 'showSeries', 'مسلسلات أسيوية', icons + '/Asian.png', oOutputParameterHandler)
    
    oOutputParameterHandler.addParameter('siteUrl', ANIM_NEWS[0])
    oGui.addDir(SITE_IDENTIFIER, 'showSeries', 'مسلسلات انمي', icons + '/Anime.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', SERIE_NETFLIX[0])
    oGui.addDir(SITE_IDENTIFIER, 'showSeries', 'مسلسلات نيتفلكس', icons + '/TVShowsEnglish.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', MOVIE_PACK[0])
    oGui.addDir(SITE_IDENTIFIER, 'showPack', 'أقسام الموقع', icons + '/All.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()
 
def showSearch():
    oGui = cGui()
 
    sSearchText = oGui.showKeyBoard()
    if sSearchText is not False:
        sUrl = URL_MAIN + '?s=فيلم+'+sSearchText
        showMovies(sUrl)
        oGui.setEndOfDirectory()
        return
 
def showSearchSeries():
    oGui = cGui()
 
    sSearchText = oGui.showKeyBoard()
    if sSearchText is not False:
        sUrl = URL_MAIN + '?s=مسلسل+'+sSearchText
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

    sPattern = '<a href="([^<]+)">([^<]+)</a>'
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
	
    if aResult[0] is True:
        oOutputParameterHandler = cOutputParameterHandler()
        for aEntry in aResult[1]:
            if 'المزيد' in aEntry[1]:
                continue
            sTitle = aEntry[1].replace("مشاهدة","").replace("مترجمة","").replace("مترجم","").replace("فيلم","").replace("والأخيرة","").replace("مدبلج للعربية","مدبلج").replace("والاخيرة","").replace("كاملة","").replace("حلقات كاملة","").replace("اونلاين","").replace("مباشرة","").replace("انتاج ","").replace("جودة عالية","").replace("كامل","").replace("HD","").replace("السلسلة الوثائقية","").replace("الفيلم الوثائقي","").replace("اون لاين","") 
            sThumb = aEntry[1]
            siteUrl = aEntry[0]

            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl',siteUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
			
            if 'serie' in siteUrl or 'مسلسل' in siteUrl:
                oGui.addDir(SITE_IDENTIFIER, 'showSeries', sTitle, sThumb, oOutputParameterHandler)
            else:
                oGui.addDir(SITE_IDENTIFIER, 'showMovies', sTitle, sThumb, oOutputParameterHandler)
 
        sNextPage = __checkForNextPage(sHtmlContent)
        if sNextPage:
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sNextPage)
            oGui.addDir(SITE_IDENTIFIER, 'showSeries', '[COLOR teal]Next >>>[/COLOR]', 'next.png', oOutputParameterHandler)
 
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

    sPattern = '<div class="Small--Box"><a href="([^"]+)" title="([^"]+)".+?data-src="([^"]+)'
    aResult = oParser.parse(sHtmlContent, sPattern)
    if aResult[0] is True:
        oOutputParameterHandler = cOutputParameterHandler()
        for aEntry in aResult[1]:
 
            sTitle = aEntry[1].replace("مشاهدة","").replace("مسلسل","").replace("انمي","").replace("مترجمة","").replace("مترجم","").replace("فيلم","").replace("والأخيرة","").replace("مدبلج للعربية","مدبلج").replace("والاخيرة","").replace("كاملة","").replace("حلقات كاملة","").replace("اونلاين","").replace("مباشرة","").replace("انتاج ","").replace("جودة عالية","").replace("كامل","").replace("HD","").replace("السلسلة الوثائقية","").replace("الفيلم الوثائقي","").replace("اون لاين","").replace("الموسم العاشر","S10").replace("الموسم الحادي عشر","S11").replace("الموسم الثاني عشر","S12").replace("الموسم الثالث عشر","S13").replace("الموسم الرابع عشر","S14").replace("الموسم الخامس عشر","S15").replace("الموسم السادس عشر","S16").replace("الموسم السابع عشر","S17").replace("الموسم الثامن عشر","S18").replace("الموسم التاسع عشر","S19").replace("الموسم العشرون","S20").replace("الموسم الحادي و العشرون","S21").replace("الموسم الثاني و العشرون","S22").replace("الموسم الثالث و العشرون","S23").replace("الموسم الرابع والعشرون","S24").replace("الموسم الخامس و العشرون","S25").replace("الموسم السادس والعشرون","S26").replace("الموسم السابع والعشرون","S27").replace("الموسم الثامن والعشرون","S28").replace("الموسم التاسع والعشرون","S29").replace("الموسم الثلاثون","S30").replace("الموسم الحادي و الثلاثون","S31").replace("الموسم الثاني والثلاثون","S32").replace("الموسم الاول","S1").replace("الموسم الثاني","S2").replace("الموسم الثالث","S3").replace("الموسم الثالث","S3").replace("الموسم الرابع","S4").replace("الموسم الخامس","S5").replace("الموسم السادس","S6").replace("الموسم السابع","S7").replace("الموسم الثامن","S8").replace("الموسم التاسع","S9").replace("الموسم","S").replace("S ","S").replace("الحلقة "," E")
            siteUrl = aEntry[0]
            sThumb = re.sub(r'-\d+x\d{0,3}','', aEntry[2])  
            sDesc = ''
            sYear = ''
            m = re.search('([0-9]{4})', sTitle)
            if m:
               sYear = str(m.group(0))
               sTitle = sTitle.replace(sYear,'')
            sDisplayTitle = ('%s (%s)') % (sTitle, sYear)


            oOutputParameterHandler.addParameter('siteUrl',siteUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oOutputParameterHandler.addParameter('sYear', sYear)
            oOutputParameterHandler.addParameter('sDesc', sDesc)

            if 'assemblies' in siteUrl :			
                oGui.addMovie(SITE_IDENTIFIER, 'showassemblies', sDisplayTitle, '', sThumb, sDesc, oOutputParameterHandler)
            elif 'serie' in siteUrl or 'مسلسل' in siteUrl:
                oGui.addTV(SITE_IDENTIFIER, 'showSeasons', sDisplayTitle, '', sThumb, sDesc, oOutputParameterHandler)
            else:
                siteUrl = aEntry[0]+'/watch'
                oOutputParameterHandler.addParameter('siteUrl',siteUrl)
                oGui.addMovie(SITE_IDENTIFIER, 'showLinks', sDisplayTitle, '', sThumb, sDesc, oOutputParameterHandler)
    

        sNextPage = __checkForNextPage(sHtmlContent)
        if sNextPage:
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sNextPage)
            oGui.addDir(SITE_IDENTIFIER, 'showMovies', '[COLOR teal]Next >>>[/COLOR]', 'next.png', oOutputParameterHandler)
 
    if not sSearch:
        oGui.setEndOfDirectory()

def showassemblies():
	oGui = cGui()
    
	oInputParameterHandler = cInputParameterHandler()
	sUrl = oInputParameterHandler.getValue('siteUrl')
	sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
	sThumb = oInputParameterHandler.getValue('sThumb')
 
	oRequestHandler = cRequestHandler(sUrl)
	sHtmlContent = oRequestHandler.request()
	oParser = cParser()

	sStart = '<section class="tabContents">'
	sEnd = '</section>'
	sHtmlContent = oParser.abParse(sHtmlContent, sStart, sEnd)   

	sPattern = '<div class="Small--Box">.+?href="([^"]+)" title="([^"]+)".+?data-src="([^"]+)'
	aResult = oParser.parse(sHtmlContent, sPattern)
	if aResult[0] is True:
         oOutputParameterHandler = cOutputParameterHandler()
         for aEntry in aResult[1]:
 
            sTitle = aEntry[1].replace("مشاهدة","").replace("مسلسل","").replace("انمي","").replace("مترجمة","").replace("مترجم","").replace("فيلم","").replace("والأخيرة","").replace("مدبلج للعربية","مدبلج").replace("والاخيرة","").replace("كاملة","").replace("حلقات كاملة","").replace("اونلاين","").replace("مباشرة","").replace("انتاج ","").replace("جودة عالية","").replace("كامل","").replace("HD","").replace("السلسلة الوثائقية","").replace("الفيلم الوثائقي","").replace("اون لاين","").replace("الموسم العاشر","S10").replace("الموسم الحادي عشر","S11").replace("الموسم الثاني عشر","S12").replace("الموسم الثالث عشر","S13").replace("الموسم الرابع عشر","S14").replace("الموسم الخامس عشر","S15").replace("الموسم السادس عشر","S16").replace("الموسم السابع عشر","S17").replace("الموسم الثامن عشر","S18").replace("الموسم التاسع عشر","S19").replace("الموسم العشرون","S20").replace("الموسم الحادي و العشرون","S21").replace("الموسم الثاني و العشرون","S22").replace("الموسم الثالث و العشرون","S23").replace("الموسم الرابع والعشرون","S24").replace("الموسم الخامس و العشرون","S25").replace("الموسم السادس والعشرون","S26").replace("الموسم السابع والعشرون","S27").replace("الموسم الثامن والعشرون","S28").replace("الموسم التاسع والعشرون","S29").replace("الموسم الثلاثون","S30").replace("الموسم الحادي و الثلاثون","S31").replace("الموسم الثاني والثلاثون","S32").replace("الموسم الاول","S1").replace("الموسم الثاني","S2").replace("الموسم الثالث","S3").replace("الموسم الثالث","S3").replace("الموسم الرابع","S4").replace("الموسم الخامس","S5").replace("الموسم السادس","S6").replace("الموسم السابع","S7").replace("الموسم الثامن","S8").replace("الموسم التاسع","S9").replace("الموسم","S").replace("S ","S").replace("الحلقة "," E")
            siteUrl = aEntry[0]+'/watch'
            sThumb = re.sub(r'-\d+x\d{0,3}','', aEntry[2])  
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

            oGui.addMovie(SITE_IDENTIFIER, 'showLinks', sTitle, '', sThumb, sDesc, oOutputParameterHandler)

         sNextPage = __checkForNextPage(sHtmlContent)
         if sNextPage:
             oOutputParameterHandler = cOutputParameterHandler()
             oOutputParameterHandler.addParameter('siteUrl', sNextPage)
             oGui.addDir(SITE_IDENTIFIER, 'showassemblies', '[COLOR teal]Next >>>[/COLOR]', 'next.png', oOutputParameterHandler)
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
    sPattern = '<div class="Small--Box">.+?href="([^"]+)" title="([^"]+)".+?data-src="([^"]+)'

    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
	
	
    if aResult[0] is True:
        oOutputParameterHandler = cOutputParameterHandler()
        for aEntry in aResult[1]:
 
            sTitle = aEntry[1].replace("مشاهدة","").replace("مسلسل","").replace("انمي","").replace("مترجمة","").replace("مترجم","").replace("فيلم","").replace("والأخيرة","").replace("مدبلج للعربية","مدبلج").replace("والاخيرة","").replace("كاملة","").replace("حلقات كاملة","").replace("اونلاين","").replace("مباشرة","").replace("انتاج ","").replace("جودة عالية","").replace("كامل","").replace("HD","").replace("السلسلة الوثائقية","").replace("الفيلم الوثائقي","").replace("اون لاين","").replace(" والأخيرة","")
            sYear = ''
            m = re.search('([0-9]{4})', sTitle)
            if m:
                sYear = str(m.group(0))
                sTitle = sTitle.replace(sYear,'')
            siteUrl = aEntry[0]
            sThumb = aEntry[2]
            sDesc = ''
            sDisplayTitle = sTitle.replace("الموسم العاشر","").replace("الموسم الحادي عشر","").replace("الموسم الثاني عشر","").replace("الموسم الثالث عشر","").replace("الموسم الرابع عشر","").replace("الموسم الخامس عشر","").replace("الموسم السادس عشر","").replace("الموسم السابع عشر","").replace("الموسم الثامن عشر","").replace("الموسم التاسع عشر","").replace("الموسم العشرون","").replace("الموسم الحادي و العشرون","").replace("الموسم الثاني و العشرون","").replace("الموسم الثالث و العشرون","S23").replace("الموسم الرابع والعشرون","").replace("الموسم الخامس و العشرون","").replace("الموسم السادس والعشرون","").replace("الموسم السابع والعشرون","").replace("الموسم الثامن والعشرون","").replace("الموسم التاسع والعشرون","").replace("الموسم الثلاثون","").replace("الموسم الحادي و الثلاثون","").replace("الموسم الثاني والثلاثون","").replace("الموسم الاول","").replace("الموسم الثاني","").replace("الموسم الثالث","").replace("الموسم الثالث","").replace("الموسم الرابع","").replace("الموسم الخامس","").replace("الموسم السادس","").replace("الموسم السابع","").replace("الموسم الثامن","").replace("الموسم التاسع","").replace("الموسم","").replace("S ","").replace("الحلقة","").replace("1","").replace("2","").replace("3","").replace("4","").replace("5","").replace("6","").replace("7","").replace("8","").replace("9","").replace("10","").replace("11","").replace("12","").replace("13","").replace("14","").replace("15","").replace("16","").replace("17","").replace("18","").replace("19","").replace("20","").replace("21","").replace("22","").replace("23","").replace("24","").replace("25","").replace("26","").replace("27","").replace("28","").replace("29","").replace("30","").replace("0","").replace("season","")



            oOutputParameterHandler.addParameter('siteUrl',siteUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sDisplayTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oOutputParameterHandler.addParameter('sYear', sYear)
            oOutputParameterHandler.addParameter('sDesc', sDesc)
			
            oGui.addTV(SITE_IDENTIFIER, 'showSeasons', sDisplayTitle, '', sThumb, sDesc, oOutputParameterHandler)


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
 
	oRequestHandler = cRequestHandler(sUrl)
	sHtmlContent = oRequestHandler.request()
    # .+? ([^<]+)
	sPattern = '<div class="Small--Box Season">.+?href="([^"]+)" title.+?<span>الموسم</span>(.+?)</div>'
	sPattern += '.+?data-src(.+?)</div>'

	oParser = cParser()
	aResult = oParser.parse(sHtmlContent, sPattern)
		
	if aResult[0] is True:
		oOutputParameterHandler = cOutputParameterHandler()
		for aEntry in aResult[1]:
 
			sTitle = sMovieTitle + ' S'+aEntry[1]
			siteUrl = aEntry[0]
			sThumb = aEntry[2].replace('=','')
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

	oParser = cParser()

	sStart = '<section class="tabContents">'
	sEnd = '</section>'
	sHtmlContent = oParser.abParse(sHtmlContent, sStart, sEnd)   

	sPattern = 'href="([^"]+)".+?class="epnum">.+?<span>الحلقة</span>(.+?)</div>'

	oParser = cParser()
	aResult = oParser.parse(sHtmlContent, sPattern)
	
	
	if aResult[0] is True:
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
			oGui.addEpisode(SITE_IDENTIFIER, 'showLinks', sTitle, '', sThumb, sDesc, oOutputParameterHandler)
        
	oGui.setEndOfDirectory()
  
     # (.+?)
def __checkForNextPage(sHtmlContent):
    sPattern = '<li class="active"><a href=.+?<a href="(.+?)"'	
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
 
    if aResult[0]:
        return aResult[1][0]

def showLinks():
    oGui = cGui()
    import requests

    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')

    sUrl2 = sUrl.replace('/watch','/download')
    oRequestHandler = cRequestHandler(sUrl)
    oRequestHandler.addHeaderEntry('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:45.0) Gecko/20100101 Firefox/45.0')
    oRequestHandler.addHeaderEntry('Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8')
    oRequestHandler.addHeaderEntry('X-Requested-With', 'XMLHttpRequest')
    oRequestHandler.addHeaderEntry('Accept-Language', 'fr,fr-FR;q=0.8,en-US;q=0.5,en;q=0.3')
    sHtmlContent = oRequestHandler.request()
          
    sPattern = 'data-id="(.+?)" data-server="([^"]+)".+?<span>(.+?)</span>'
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)

    if aResult[0]:
        oOutputParameterHandler = cOutputParameterHandler()
        for aEntry in aResult[1]:           
            Serv = aEntry[1]
            Sid = aEntry[0]
            sHost = aEntry[2]

            sTitle = ('%s [COLOR coral]%s[/COLOR]') % (sMovieTitle, sHost)

            oOutputParameterHandler.addParameter('siteUrl', sUrl)
            oOutputParameterHandler.addParameter('Serv', Serv)
            oOutputParameterHandler.addParameter('Sid', Sid)
            oOutputParameterHandler.addParameter('sMovieTitle', sMovieTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oOutputParameterHandler.addParameter('sHost', sHost)

            oGui.addLink(SITE_IDENTIFIER, 'showHosters', sTitle, sThumb, '', oOutputParameterHandler)
		               
    oGui.setEndOfDirectory()

def showHosters():
    oGui = cGui()
    import requests

    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')
    Serv = oInputParameterHandler.getValue('Serv')
    Sid = oInputParameterHandler.getValue('Sid')

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    sPattern = '<a class="Logo--Area" href="([^"]+)'	
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
 
    if aResult[0]:
        URL_MAIN = aResult[1][0]

    s = requests.Session()            
    headers = {'user-agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Mobile Safari/537.36 Edg/115.0.1901.203',
    'origin': URL_MAIN,
    'referer': URL_MAIN,
    'Sec-Fetch-Mode':'cors',
    'X-Requested-With':'XMLHttpRequest',
    'Sec-Fetch-Dest':'empty',
    'Sec-Fetch-Site':'same-origin'}

    data = {'id':Sid,'i':Serv}
    r = s.post((URL_MAIN+'/wp-content/themes/movies2023/Ajaxat/Single/Server.php'),data=data,headers=headers)
    sHtmlContent = r.content

    sPattern = '<iframe src="([^"]+)'
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
    if aResult:
        sHosterUrl = aResult[1][0]

        if 'vidtube' in sHosterUrl:
            sHosterUrl = sHosterUrl + "|Referer=" + URL_MAIN
        if 'updown' in sHosterUrl:
            sHosterUrl = sHosterUrl + "|Referer=" + URL_MAIN

        oHoster = cHosterGui().checkHoster(sHosterUrl)
        if oHoster:
            oHoster.setDisplayName(sMovieTitle)
            oHoster.setFileName(sMovieTitle)
            cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb)

    oGui.setEndOfDirectory()