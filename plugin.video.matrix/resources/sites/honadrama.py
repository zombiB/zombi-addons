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
from resources.lib.parser import cParser
from resources.lib.comaddon import progress, VSlog, siteManager, addon
from resources.lib.util import cUtil, Unquote
ADDON = addon()
icons = ADDON.getSetting('defaultIcons')
try:  # Python 2
    import urllib2
    from urllib2 import URLError as UrlError

except ImportError:  # Python 3
    import urllib.request as urllib2
    from urllib.error import URLError as UrlError
	
SITE_IDENTIFIER = 'honadrama'
SITE_NAME = 'HonaDrama'
SITE_DESC = 'arabic vod'

URL_MAIN = siteManager().getUrlMain(SITE_IDENTIFIER)

MOVIE_EN = (URL_MAIN + '/category/%d8%a7%d9%84%d8%a3%d9%81%d9%84%d8%a7%d9%85/%d8%a3%d9%81%d9%84%d8%a7%d9%85-%d8%a3%d8%ac%d9%86%d8%a8%d9%8a%d8%a9/', 'showMovies')
MOVIE_HI = (URL_MAIN + '/category/%d8%a7%d9%84%d8%a3%d9%81%d9%84%d8%a7%d9%85/%d8%a3%d9%81%d9%84%d8%a7%d9%85-%d9%87%d9%86%d8%af%d9%8a%d8%a9/', 'showMovies')
SERIE_EN = (URL_MAIN + '/category/%d9%85%d8%b3%d9%84%d8%b3%d9%84%d8%a7%d8%aa-%d8%a3%d8%ac%d9%86%d8%a8%d9%8a%d8%a9/', 'showSeries')
SERIE_ASIA = (URL_MAIN + '/category/%d8%a7%d9%84%d8%af%d8%b1%d8%a7%d9%85%d8%a7-%d8%a7%d9%84%d9%85%d9%83%d8%b3%d9%8a%d9%83%d9%8a%d8%a9/%d8%a7%d9%84%d9%85%d8%b3%d9%84%d8%b3%d9%84%d8%a7%d8%aa-%d8%a7%d9%84%d9%85%d8%aa%d8%b1%d8%ac%d9%85%d8%a9/', 'showSeries')
SERIE_TR = (URL_MAIN + '/category/%d9%85%d8%b3%d9%84%d8%b3%d9%84%d8%a7%d8%aa/%d9%85%d8%b3%d9%84%d8%b3%d9%84%d8%a7%d8%aa-%d8%aa%d8%b1%d9%83%d9%8a%d8%a9/', 'showSeries')

#DOC_NEWS = (URL_MAIN + '/category/%d9%85%d9%86%d9%88%d8%b9%d8%a7%d8%aa/', 'showMovies')

ANIM_NEWS = (URL_MAIN + '/category/%d8%a7%d9%84%d8%a3%d9%86%d9%85%d9%8a/%d9%85%d8%b3%d9%84%d8%b3%d9%84%d8%a7%d8%aa-%d8%a7%d9%84%d8%a3%d9%86%d9%85%d9%8a/', 'showSeries')

ANIM_MOVIES = (URL_MAIN + '/category/%d8%a7%d9%84%d8%a3%d9%86%d9%85%d9%8a/%d8%a3%d9%81%d9%84%d8%a7%d9%85-%d8%a7%d9%84%d8%a2%d9%86%d9%85%d9%8a/', 'showMovies')

URL_SEARCH = (URL_MAIN + '/?s=', 'showMovies')
URL_SEARCH_MOVIES = (URL_MAIN + '/?s=', 'showMovies')
FUNCTION_SEARCH = 'showMovies'
	
def load():
    oGui = cGui()

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'http://venom/')
    oGui.addDir(SITE_IDENTIFIER, 'showSearch', 'Search Movies', icons + '/Search.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', 'http://venom/')
    oGui.addDir(SITE_IDENTIFIER, 'showSearchSeries', 'Search Series', icons + '/Search.png', oOutputParameterHandler)
    
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_EN[0])
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'أفلام أجنبية', icons + '/Movies.png', oOutputParameterHandler)
   
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_HI[0])
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'أفلام هندية', icons + '/Hindi.png', oOutputParameterHandler)
    
    #oOutputParameterHandler = cOutputParameterHandler()
    #oOutputParameterHandler.addParameter('siteUrl', DOC_NEWS[0])
    #oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'أفلام وثائقية', 'doc.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', SERIE_EN[0])
    oGui.addDir(SITE_IDENTIFIER, 'showSeries', 'مسلسلات أجنبية', icons + '/TVShows.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', SERIE_ASIA[0])
    oGui.addDir(SITE_IDENTIFIER, 'showSeries', 'مسلسلات مكسيكية', icons + '/Latin.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', SERIE_TR[0])
    oGui.addDir(SITE_IDENTIFIER, 'showSeries', 'مسلسلات تركية', icons + '/Turkish.png', oOutputParameterHandler)


    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', ANIM_NEWS[0])
    oGui.addDir(SITE_IDENTIFIER, 'showSeries', 'مسلسلات إنمي', icons + '/Anime.png', oOutputParameterHandler)
  

    oGui.setEndOfDirectory()

def showSearch():
    oGui = cGui()
    sSearchText = oGui.showKeyBoard()
    if sSearchText:
        sUrl = URL_MAIN + '/?s='+sSearchText
        if 'مسلسل' in sUrl:
            showSeries(sUrl)
        showMovies(sUrl)
        oGui.setEndOfDirectory()
        return  
    
def showSearchSeries():
    oGui = cGui()
    sSearchText = oGui.showKeyBoard()
    if sSearchText:
        sUrl = URL_MAIN + '/?s='+sSearchText
        if 'مسلسل' in sUrl:
            showSeries(sUrl)
        showMovies(sUrl)
        oGui.setEndOfDirectory()
        return  

 
def showMovies(sSearch = ''):
    import requests
    oGui = cGui()
    if sSearch:
      sUrl = sSearch
    else:
        oInputParameterHandler = cInputParameterHandler()
        sUrl = oInputParameterHandler.getValue('siteUrl')



    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
 # ([^<]+) .+?
    sPattern = '<div class="movie"><a href="(.+?)">.+?src="(.+?)".+?class="dicr"><h3>(.+?)</h3><p>'

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
 
            sTitle = aEntry[2].replace("مشاهدة","").replace("مسلسل","").replace("انمي","").replace("مترجمة","").replace("مترجم","").replace("برنامج","").replace("فيلم","").replace("والأخيرة","").replace("مدبلج للعربية","مدبلج").replace("مدبلج","[arabic]").replace("والاخيرة","").replace("كاملة","").replace("حلقات كاملة","").replace("اونلاين","").replace("مباشرة","").replace("انتاج ","").replace("جودة عالية","").replace("كامل","").replace("HD","").replace("السلسلة الوثائقية","").replace("الفيلم الوثائقي","").replace("اون لاين","")
            siteUrl = aEntry[0]
            sThumb = aEntry[1]
            sDesc = ''
            sYear = ''


            oOutputParameterHandler.addParameter('siteUrl',siteUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oOutputParameterHandler.addParameter('sYear', sYear)
            oOutputParameterHandler.addParameter('sDesc', sDesc)

            oGui.addTV(SITE_IDENTIFIER, 'showServer', sTitle, '', sThumb, sDesc, oOutputParameterHandler)

        progress_.VSclose(progress_)
 
        sNextPage = __checkForNextPage(sHtmlContent)
        if sNextPage:
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sNextPage)
            oGui.addDir(SITE_IDENTIFIER, 'showMovies', '[COLOR teal]Next >>>[/COLOR]', 'next.png', oOutputParameterHandler)
 
    if not sSearch:
        oGui.setEndOfDirectory()  

 
def showSeries(sSearch = ''):
    import requests
    oGui = cGui()
    if sSearch:
      sUrl = sSearch
    else:
        oInputParameterHandler = cInputParameterHandler()
        sUrl = oInputParameterHandler.getValue('siteUrl')



    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
 # ([^<]+) .+?
    sPattern = '<div class="movie"><a href="(.+?)"><div class="your-productSeCndary blog-post-img-thumb"><img alt="(.+?)" src="(.+?)" />'

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
 
            sTitle = aEntry[1].replace("مشاهدة","").replace("مسلسل","").replace("انمي","").replace("مترجمة","").replace("مترجم","").replace("برنامج","").replace("فيلم","").replace("والأخيرة","").replace("مدبلج للعربية","مدبلج").replace("مدبلج","[arabic]").replace("والاخيرة","").replace("كاملة","").replace("حلقات كاملة","").replace("اونلاين","").replace("مباشرة","").replace("انتاج ","").replace("جودة عالية","").replace("كامل","").replace("HD","").replace("السلسلة الوثائقية","").replace("الفيلم الوثائقي","").replace("اون لاين","")
            siteUrl = aEntry[0]
            sThumb = aEntry[2]
            sDesc = ''
            sYear = ''


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
 
	oRequestHandler = cRequestHandler(sUrl)
	sHtmlContent = oRequestHandler.request()
    # .+? ([^<]+)
	sPattern = '   <li><a href="([^<]+)">([^<]+)</a></li>' 

	oParser = cParser()
	aResult = oParser.parse(sHtmlContent, sPattern)
		
	if aResult[0]:
		oOutputParameterHandler = cOutputParameterHandler()
		for aEntry in aResult[1]:
 
			sTitle = sMovieTitle+aEntry[1].replace("الموسم"," S").replace("S "," S").replace("موسم"," S").replace("الأول"," S1")
			siteUrl = aEntry[0]
			sThumb = ''
			sDesc = ""
			
			oOutputParameterHandler.addParameter('siteUrl',siteUrl)
			oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
			oOutputParameterHandler.addParameter('sThumb', sThumb)
			oGui.addSeason(SITE_IDENTIFIER, 'showEps', sTitle, '', sThumb, sDesc, oOutputParameterHandler)
        
	oGui.setEndOfDirectory()
    
def showEps():
    import requests
    oGui = cGui()
   
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')



    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    #print sHtmlContent
   
    oParser = cParser()
     # (.+?) ([^<]+) .+?
    sPattern = '<div class="movie"><a href="(.+?)"><div class="your-productSeCndary blog-post-img-thumb"><img src="(.+?)" class="image"></div>.+?<h3>(.+?)</h3>'

    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
	
    if aResult[0]:
        oOutputParameterHandler = cOutputParameterHandler()    
        for aEntry in aResult[1]:
 

            sTitle = aEntry[2].replace("مشاهدة","").replace("مسلسل","").replace("انمي","").replace("مترجمة","").replace("مترجم","").replace("برنامج","").replace("فيلم","").replace("والأخيرة","").replace("مدبلج للعربية","مدبلج").replace("مدبلج","[arabic]").replace("والاخيرة","").replace("كاملة","").replace("حلقات كاملة","").replace("اونلاين","").replace("مباشرة","").replace("انتاج ","").replace("جودة عالية","").replace("كامل","").replace("HD","").replace("السلسلة الوثائقية","").replace("الفيلم الوثائقي","").replace("اون لاين","")
            siteUrl = aEntry[0]
            sThumb = aEntry[1]
            sDesc = ''
            sYear = ""
			


            oOutputParameterHandler.addParameter('siteUrl',siteUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oGui.addEpisode(SITE_IDENTIFIER, 'showServer', sTitle, sThumb, sThumb, sDesc, oOutputParameterHandler)
               
       
    oGui.setEndOfDirectory() 
 
def showHosters():
    import requests
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')



    oRequestHandler = cRequestHandler(sUrl)
    cook = oRequestHandler.GetCookies()
    oRequestHandler.setRequestType(1)
    oRequestHandler.addHeaderEntry('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:45.0) Gecko/20100101 Firefox/45.0')
    oRequestHandler.addHeaderEntry('origin', 'www.arblionz.org')
    oRequestHandler.addHeaderEntry('Cookie', cook)
    oRequestHandler.addHeaderEntry('X-Requested-With', 'XMLHttpRequest')
    oRequestHandler.addHeaderEntry('Referer', 'https://www.arblionz.org/download/%D9%81%D9%8A%D9%84%D9%85-beyond-the-woods-2020-%D9%85%D8%AA%D8%B1%D8%AC%D9%85-%D8%A7%D9%88%D9%86-%D9%84%D8%A7%D9%8A%D9%86')
    sHtmlContent = oRequestHandler.request()
    # (.+?) .+?        

    sPattern = 'data-src="(.+?)"'
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)

	
    if aResult[0]:
        for aEntry in aResult[1]:
            
            url = aEntry
            sTitle = sMovieTitle
            if url.startswith('//'):
                url = 'http:' + url
            
            sHosterUrl = url 
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
    # (.+?) .+?
    #print sHtmlContent           

    sPattern = 'href="([^<]+)" target'
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)

	
    if aResult[0]:
        for aEntry in aResult[1]:
            
            url = aEntry
            url = url.replace("moshahda","ffsff")
            sTitle = sMovieTitle
            if url.startswith('//'):
                url = 'http:' + url
            
            sHosterUrl = url 
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
			
def showServer():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')
    
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    oParser = cParser()
            
# ([^<]+) .+? (.+?)
    sPattern =  '<link itemprop="embedURL" href="([^<]+)">' 
    aResult = oParser.parse(sHtmlContent,sPattern)
    if aResult[0]:
        murl =  aResult[1][0]
        oRequest = cRequestHandler(murl)
        sHtmlContent = oRequest.request()
  
    oParser = cParser()
				     
    # (.+?) ([^<]+) .+?
    sPattern = 'data-server="([^<]+)" data-q="([^<]+)">' 
    aResult = oParser.parse(sHtmlContent, sPattern)

   
    if aResult[0]:
        for aEntry in aResult[1]:


            sId = URL_MAIN + '/wp-admin/admin-ajax.php?action=serverPost&server='+aEntry[0]+'&q='+aEntry[1]

            siteUrl = sId
			
            oRequestHandler = cRequestHandler(siteUrl)
            oRequestHandler.addHeaderEntry('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:45.0) Gecko/20100101 Firefox/45.0')
            oRequestHandler.addHeaderEntry('Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8')
            oRequestHandler.addHeaderEntry('X-Requested-With', 'XMLHttpRequest')
            oRequestHandler.addHeaderEntry('Accept-Language', 'fr,fr-FR;q=0.8,en-US;q=0.5,en;q=0.3')
            sData = oRequestHandler.request()
   
            sPattern = '<iframe.+?src="([^<]+)"' 
            oParser = cParser()
            aResult = oParser.parse(sData, sPattern)
	
            if aResult[0]:
               for aEntry in aResult[1]:
        
                   url = aEntry
                   sTitle = " "
                   sThumb = sThumb
                   if 'govid' in url:
                      url = url.replace("play","down").replace("embed-","")
                   if url.startswith('//'):
                      url = 'http:' + url
								            
                   sHosterUrl = url
                   if 'nowvid' in sHosterUrl:
                       sHosterUrl = sHosterUrl + "|Referer=" + URL_MAIN 
                   if 'userload' in sHosterUrl:
                       sHosterUrl = sHosterUrl + "|Referer=" + URL_MAIN
                   if 'moshahda' in sHosterUrl:
                       sHosterUrl = sHosterUrl + "|Referer=" + URL_MAIN
                   if 'mystream' in sHosterUrl:
                       sHosterUrl = sHosterUrl + "|Referer=" + URL_MAIN    
                   oHoster = cHosterGui().checkHoster(sHosterUrl)
                   if oHoster:
                      sDisplayTitle = sMovieTitle
                      oHoster.setDisplayName(sDisplayTitle)
                      oHoster.setFileName(sMovieTitle)
                      cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb)

       
    oGui.setEndOfDirectory()  

def __checkForNextPage(sHtmlContent):
#    sPattern = 'class="next page-numbers" href="(.+?)"'
    sPattern = '<li class="active"><a href=.+?<a href="(.+?)"'	
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
 
    if aResult[0]:
        return aResult[1][0]

    return False