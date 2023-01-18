# -*- coding: utf-8 -*-
# zombi https://github.com/zombiB/zombi-addons/
import re
from resources.lib.gui.hoster import cHosterGui
from resources.lib.gui.gui import cGui
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.lib.comaddon import progress, VSlog, siteManager	

SITE_IDENTIFIER = 'aflamfree'
SITE_NAME = 'Aflamfree'
SITE_DESC = 'arabic vod'	 
 
URL_MAIN = siteManager().getUrlMain(SITE_IDENTIFIER)
MOVIE_PACK = (URL_MAIN + '/%D8%A7%D9%82%D8%B3%D8%A7%D9%85-%D8%A7%D9%84%D9%85%D9%88%D9%82%D8%B9', 'showPack')
MOVIE_ANNEES = (True, 'showYears')

URL_SEARCH = (URL_MAIN + '/?s=', 'showMoviesearch')
URL_SEARCH_MOVIES = (URL_MAIN + '/?s=', 'showMoviesearch')
FUNCTION_SEARCH = 'showMoviesearch'

def load():
	oGui = cGui()

	oOutputParameterHandler = cOutputParameterHandler()
	oOutputParameterHandler.addParameter('siteUrl', URL_SEARCH[0])
	oGui.addDir(SITE_IDENTIFIER, 'showSearch', 'Search Movies', 'search.png', oOutputParameterHandler)
	
	oOutputParameterHandler.addParameter('siteUrl', MOVIE_PACK[0])
	oGui.addDir(SITE_IDENTIFIER, 'showPack', 'أقسام الموقع', 'icon.png', oOutputParameterHandler)
	
	oGui.setEndOfDirectory()

def showYears():
    oGui = cGui()
    oOutputParameterHandler = cOutputParameterHandler()
    for i in reversed(range(1921, 2022)):
        sYear = str(i)
        oOutputParameterHandler.addParameter('siteUrl', URL_MAIN + '/release-year/' + sYear)  # / inutile
        oGui.addDir(SITE_IDENTIFIER, 'showLive', sYear, 'annees.png', oOutputParameterHandler)
    oGui.setEndOfDirectory()
	
def showSearch():
	oGui = cGui()
	 
	sSearchText = oGui.showKeyBoard()
	if sSearchText is not False:
		sUrl = URL_MAIN + '/?s='+sSearchText
		showMoviesearch(sUrl)
		oGui.setEndOfDirectory()
		return
   
def showMoviesearch(sSearch = ''):
    oGui = cGui()
    oParser = cParser()
    if sSearch:
      sUrl = sSearch
    else:
        oInputParameterHandler = cInputParameterHandler()
        sUrl = oInputParameterHandler.getValue('siteUrl')
 
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
 
    # ([^<]+) .+? 
    sPattern = '<a href="([^<]+)"><div class="image"><img src="([^<]+)" alt="([^<]+)" /><span class="player"></span><span class="imdb"><b><b class="icon-star"></b></b>([^<]+)</span>'

    aResult = oParser.parse(sHtmlContent, sPattern)
		
    if aResult[0] is True:
        total = len(aResult[1])
        progress_ = progress().VScreate(SITE_NAME)
        oOutputParameterHandler = cOutputParameterHandler()
        for aEntry in aResult[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break
 
            sTitle = aEntry[2].replace("مشاهدة","").replace("مسلسل","").replace("انمي","").replace("مترجمة","").replace("مترجم","").replace("فيلم","").replace("والأخيرة","").replace("مدبلج للعربية","مدبلج").replace("والاخيرة","").replace("كاملة","").replace("حلقات كاملة","").replace("اونلاين","").replace("مباشرة","").replace("انتاج ","").replace("جودة عالية","").replace("كامل","").replace("HD","").replace("السلسلة الوثائقية","").replace("الفيلم الوثائقي","").replace("اون لاين","") 
            siteUrl = aEntry[0]
            sThumb = aEntry[1] 
            sYear = ''
            m = re.search('([0-9]{4})', sTitle)
            if m:
                  sYear = str(m.group(0))
                  sTitle = sTitle.replace(sYear,'')
            sDesc = '' 
			
			
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl',siteUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oOutputParameterHandler.addParameter('sYear', sYear)

            oGui.addMovie(SITE_IDENTIFIER, 'showLive2', sTitle, '', sThumb, sDesc, oOutputParameterHandler)
			
        progress_.VSclose(progress_)
 
        sNextPage = __checkForNextPage(sHtmlContent)
        if sNextPage != False:
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sNextPage)
            oGui.addDir(SITE_IDENTIFIER, 'showMoviesearch', '[COLOR teal]Next >>>[/COLOR]', 'next.png', oOutputParameterHandler)
 
    if not sSearch:
        oGui.setEndOfDirectory()
 
def showPack(sSearch = ''):
    oGui = cGui()
    if sSearch:
      sUrl = sSearch
    else:
        oInputParameterHandler = cInputParameterHandler()
        sUrl = oInputParameterHandler.getValue('siteUrl')
 
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
#([^<]+) .+? 

    sPattern = 'style="font-size: large;"><a href="([^<]+)">([^<]+)</a><br />'


    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
	
	
    if aResult[0] is True:
        oOutputParameterHandler = cOutputParameterHandler()
        for aEntry in aResult[1]:
            sTitle = aEntry[1].replace("مشاهدة","").replace("مسلسل","").replace("انمي","").replace("مترجمة","").replace("مترجم","").replace("فيلم","").replace("والأخيرة","").replace("مدبلج للعربية","مدبلج").replace("والاخيرة","").replace("كاملة","").replace("حلقات كاملة","").replace("اونلاين","").replace("مباشرة","").replace("انتاج ","").replace("جودة عالية","").replace("كامل","").replace("HD","").replace("السلسلة الوثائقية","").replace("الفيلم الوثائقي","").replace("اون لاين","") 
            sThumb = aEntry[1]
            siteUrl = aEntry[0]+'/page/1'
            sDesc = ''
			

            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl',siteUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)

            oGui.addMisc(SITE_IDENTIFIER, 'showLive', sTitle, '', sThumb, sDesc, oOutputParameterHandler)
 
        sNextPage = __checkForNextPage(sHtmlContent)
        if sNextPage != False:
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sNextPage)
            oGui.addDir(SITE_IDENTIFIER, 'showPack', '[COLOR teal]Next >>>[/COLOR]', 'next.png', oOutputParameterHandler)
 
    if not sSearch:
        oGui.setEndOfDirectory()
 
      # (.+?) ([^<]+) .+?
def __checkForNextPage(sHtmlContent):
    sPattern = "href='([^<]+)'>.+?Next"
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
    if aResult[0] is True:
        aResult = aResult[1][0]
        return aResult

    return False 
   
def showLive():
    oGui = cGui()
   
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')
 
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
    # (.+?) ([^<]+) .+? 
    sPattern = '<a href="([^<]+)"><div class="image"><img src="([^<]+)" alt="([^<]+)" /><span class="player"></span><span class="imdb"><b><b class="icon-star"></b></b>([^<]+)</span>'
    
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
    
   
    if aResult[0] is True:
        oOutputParameterHandler = cOutputParameterHandler()
        for aEntry in aResult[1]: 
            sTitle = aEntry[2].replace("مشاهدة","").replace("مسلسل","").replace("انمي","").replace("مترجمة","").replace("مترجم","").replace("فيلم","").replace("والأخيرة","").replace("مدبلج للعربية","مدبلج").replace("والاخيرة","").replace("كاملة","").replace("حلقات كاملة","").replace("اونلاين","").replace("مباشرة","").replace("انتاج ","").replace("جودة عالية","").replace("كامل","").replace("HD","").replace("السلسلة الوثائقية","").replace("الفيلم الوثائقي","").replace("اون لاين","") 
            siteUrl = aEntry[0]
            sThumb = aEntry[1]
            sYear = ''
            m = re.search('([1-2][0-9]{3})', sTitle)
            if m:
                  sYear = str(m.group(0))
                  sTitle = sTitle.replace(sYear,'')
            sDesc = ''

            oOutputParameterHandler.addParameter('siteUrl', siteUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oGui.addMovie(SITE_IDENTIFIER, 'showLive2', sTitle, '', sThumb, sDesc, oOutputParameterHandler)        

    # (.+?) ([^<]+) .+? 
    sPattern = '<a href="([^<]+)"><div class="image"><img src="([^<]+)" alt="([^<]+)" /><span class="player"></span></div>'
    
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
    
   
    if aResult[0] is True:
        oOutputParameterHandler = cOutputParameterHandler()
        for aEntry in aResult[1]:
            sTitle = aEntry[2].replace("مشاهدة","").replace("مسلسل","").replace("انمي","").replace("مترجمة","").replace("مترجم","").replace("فيلم","").replace("والأخيرة","").replace("مدبلج للعربية","مدبلج").replace("والاخيرة","").replace("كاملة","").replace("حلقات كاملة","").replace("اونلاين","").replace("مباشرة","").replace("انتاج ","").replace("جودة عالية","").replace("كامل","").replace("HD","").replace("السلسلة الوثائقية","").replace("الفيلم الوثائقي","").replace("اون لاين","") 
            siteUrl = aEntry[0]
            sThumb = aEntry[1] 
            sDesc = "" 
 
            oOutputParameterHandler.addParameter('siteUrl', siteUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oGui.addMovie(SITE_IDENTIFIER, 'showLive2', sTitle, '', sThumb, sDesc, oOutputParameterHandler)
    page = '1'      
    if 'page' in sUrl:   
        page = sUrl.split('/page/')[1]
    page = int(page)+1
    sTitle = 'More' 
    sTitle = '[COLOR red]'+sTitle+'[/COLOR]'
    page = str(page)
    siteUrl = sUrl.split('/page/')[0]
    siteUrl = siteUrl +'/page/'+ page

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl',siteUrl)
    oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
    oGui.addDir(SITE_IDENTIFIER, 'showLive', sTitle,'next.png', oOutputParameterHandler)
    
    oGui.setEndOfDirectory() 
  
def showLive2():
    oGui = cGui()
   
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')
 
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
  
    oParser = cParser()
    # (.+?) ([^<]+) .+? 
    sPattern = '<div id="([^<]+)"> <IFRAME SRC="([^<]+)" webkitAllowFullScreen mozallowfullscreen'
    
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
    
   
    if aResult[0] is True:
        for aEntry in aResult[1]:					
            sTitle = aEntry[0] 
            siteUrl = aEntry[1].replace("r.php?url","r2.php?url") 
    
            oRequestHandler = cRequestHandler(siteUrl)
            sHtmlContent = oRequestHandler.request()

            sPattern = 'source: "([^<]+)", parentId: "#player"'
            aResult1 = re.findall(sPattern, sHtmlContent)
            sPattern = 'content="0; url=([^<]+)" />'
            aResult2 = re.findall(sPattern, sHtmlContent)
            aResult = aResult1 + aResult2

	
            if aResult:
               for aEntry in aResult:       
                   url = aEntry
                   url = url.replace("scrolling=no","")
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
                   if oHoster != False:
                      oHoster.setDisplayName(sMovieTitle)
                      oHoster.setFileName(sMovieTitle)
                      cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb)

       
    oGui.setEndOfDirectory()