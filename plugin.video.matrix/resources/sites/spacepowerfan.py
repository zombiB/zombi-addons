#-*- coding: utf-8 -*-
#zombi https://github.com/zombiB/zombi-addons/
import re
	
from resources.lib.gui.hoster import cHosterGui
from resources.lib.gui.gui import cGui
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.comaddon import progress, isMatrix
from resources.lib.parser import cParser
 
SITE_IDENTIFIER = 'spacepowerfan'
SITE_NAME = 'spacepowerfan'
SITE_DESC = 'arabic vod'
 
URL_MAIN = 'https://www.spacepowerfan.com/'

ANIM_MOVIES = ('https://spacepowerfan.com/%d8%a3%d9%81%d9%84%d8%a7%d9%85/', 'showMovies')
ANIM_NEWS = ('https://spacepowerfan.com/%d9%85%d8%b3%d9%84%d8%b3%d9%84%d8%a7%d8%aa/', 'showSeries')

URL_SEARCH = ('https://spacepowerfan.com/?s=', 'showSeries')
FUNCTION_SEARCH = 'showSeries'
 
def load():
    oGui = cGui()

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'http://venom/')
    oGui.addDir(SITE_IDENTIFIER, 'showSearch', 'Recherche', 'search.png', oOutputParameterHandler)

            
    oGui.setEndOfDirectory()
 
def showSearch():
    oGui = cGui()
 
    sSearchText = oGui.showKeyBoard()
    if (sSearchText != False):
        sUrl = 'https://spacepowerfan.com/?s='+sSearchText
        showSeries(sUrl)
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
 # ([^<]+) .+? (.+?)
    sPattern = '<article.+?href="([^<]+)"><div.+?data-lazy-src="([^<]+)" />.+?class="Title">([^<]+)</h3><span class="Year">(.+?)</span>.+?class="Description"><p>([^<]+)</p>'
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
 
            sTitle = str(aEntry[2]).replace("مشاهدة","").replace("مسلسل","").replace("انمي","").replace("مترجمة","").replace("مترجم","").replace("فيلم","").replace("مدبلج بالعربية","مدبلج").replace("مدبلج للعربية","مدبلج").replace("مدبلج بالعربي","مدبلج").replace("مدبلج","[مدبلج]")
            siteUrl = str(aEntry[0])
            sThumb = str(aEntry[1]).replace('"',"").replace("&quot;","").replace("amp;","")
            sDesc = str(aEntry[4])
            sYear = aEntry[3]
            sDub = ''
            sDisplayTitle = ('%s [%s]') % (sTitle, sDub)
            oOutputParameterHandler.addParameter('siteUrl',siteUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
			
            oGui.addMovie(SITE_IDENTIFIER, 'showServers', sDisplayTitle, '', sThumb, sDesc, oOutputParameterHandler)

        progress_.VSclose(progress_)
 
        sNextPage = __checkForNextPage(sHtmlContent)
        if (sNextPage != False):
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
    oParser = cParser()
     # (.+?) ([^<]+) .+?
    sStart = '<div class="Top">'
    sEnd = '<div class="WebDescription">'
    sHtmlContent = oParser.abParse(sHtmlContent, sStart, sEnd)
    sPattern = 'class="TPost C"> <a href="(.+?)">.+?data-lazy-src="(.+?)".+?class="Title">(.+?)</'

    aResult = oParser.parse(sHtmlContent, sPattern)
	
	
    if (aResult[0] == True):
        total = len(aResult[1])
        progress_ = progress().VScreate(SITE_NAME)
        oOutputParameterHandler = cOutputParameterHandler()   
        for aEntry in aResult[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break
 
            sTitle = aEntry[2].replace("مشاهدة","").replace("مسلسل","").replace("أنمي","").replace("انمي","").replace("مترجمة","").replace("مترجم","").replace("فيلم","").replace("مدبلج بالعربية","").replace("مدبلج للعربية","").replace("مدبلج بالعربي","").replace("مدبلج","")
            siteUrl = aEntry[0]
            sThumb = aEntry[1]
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
    import requests
    
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')

    HEADERS = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:52.0) Gecko/20100101 Firefox/52.0',
                   'referer': 'https://spacepowerfan.com/%d9%85%d8%b3%d9%84%d8%b3%d9%84%d8%a7%d8%aa/',
                   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'}
    St=requests.Session()
    
    if not isMatrix(): 
       sHtmlContent = St.get(sUrl).content
    
    if isMatrix(): 
       sHtmlContent = St.get(sUrl).content.decode('utf-8')
    

    oParser = cParser()
     # (.+?) ([^<]+) .+?
    sPattern = '<noscript><img src="([^<]+)" alt=".+?"></noscript>.+?</td> <td class="MvTbTtl"><a href="([^<]+)">([^<]+)</a>'
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
	
    if (aResult[0] == True):
        oOutputParameterHandler = cOutputParameterHandler()   
        for aEntry in aResult[1]:
 
            sTitle = aEntry[2].replace("الحلقة "," E").replace("حلقة "," E")
            sTitle = sTitle+sMovieTitle
            siteUrl = str(aEntry[1])
            sThumb = aEntry[0]
            sDesc = ""
			


            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl',siteUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oGui.addEpisode(SITE_IDENTIFIER, 'showServers', sTitle, '', sThumb, sDesc, oOutputParameterHandler)
        
 
        sNextPage = __checkForNextPage(sHtmlContent)
        if (sNextPage != False):
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sNextPage)
            oGui.addDir(SITE_IDENTIFIER, 'showEpisodes', '[COLOR teal]Next >>>[/COLOR]', 'next.png', oOutputParameterHandler)
       
    oGui.setEndOfDirectory()
	
def __checkForNextPage(sHtmlContent):
    sPattern = "<a class='blog-pager-older-link' href='([^<]+)' id"
	
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
 
    if (aResult[0] == True):
        #print aResult[1][0]
        return aResult[1][0]

    return False
	 
def showServers():
    oGui = cGui()
    import requests
   
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')
    sDesc = oInputParameterHandler.getValue('sDesc')

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
   
    oParser = cParser()
    #Recuperation infos
    sId = ''
     # (.+?) ([^<]+) .+?
    sPattern = '<iframe.+?src=(.+?) frameborder'
    aResult = oParser.parse(sHtmlContent, sPattern)
    
    if (aResult[0]):
        for aEntry in aResult[1]:
            sId = aEntry.replace('"',"").replace("&quot;","").replace("amp;","")
            sgn = requests.Session()
            data = sgn.get(sId).content
            sHtmlContent2 = data    
            sPattern = 'src="(.+?)" frameborder'
            oParser = cParser()
            aResult = oParser.parse(sHtmlContent2, sPattern)
            if (aResult[0] == True):
                for aEntry in aResult[1]:
                    url = aEntry
                    sTitle = sMovieTitle
                    if url.startswith('//'):
                       url = 'http:' + url
                       
                    sHosterUrl = url 
                    oHoster = cHosterGui().checkHoster(sHosterUrl)
                    if (oHoster != False):
                       oHoster.setDisplayName(sMovieTitle)
                       oHoster.setFileName(sMovieTitle)
                       cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb)
				
				       
    oGui.setEndOfDirectory()