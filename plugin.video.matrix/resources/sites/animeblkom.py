#-*- coding: utf-8 -*-
#zombi https://github.com/zombiB/zombi-addons/
from resources.lib.gui.hoster import cHosterGui
from resources.lib.gui.gui import cGui
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.comaddon import progress, isMatrix
from resources.lib.parser import cParser
import re
 
SITE_IDENTIFIER = 'animeblkom'
SITE_NAME = 'animeblkom'
SITE_DESC = 'arabic vod'
 
URL_MAIN = 'https://blkom.com'
ANIM_NEWS = ('https://blkom.com/anime-list', 'showSeries')

ANIM_MOVIES = ('https://blkom.com/movie-list', 'showMovies')
URL_SEARCH_SERIES = ('https://blkom.com/search?query=', 'showSeries')
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
        sUrl = 'https://blkom.com/search?query='+sSearchText
        showSeries(sUrl)
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
     # (.+?) ([^<]+) .+?

    sPattern = '<img class="lazy" data-original="([^<]+)" alt.+?<div class="name"> <a href="([^<]+)">([^<]+)</a> </div> <div class="overlay">.+?<div class="story-text"> <p>([^<]+)</p>.+?<div class="badge red" title=.+?>(.+?)</'

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
 
            sTitle = str(aEntry[2]).replace("مشاهدة","").replace("مسلسل","").replace("انمي","").replace("مترجمة","").replace("مترجم","").replace("فيلم","").replace("والأخيرة","").replace("مدبلج للعربية","مدبلج").replace("مدبلج","[مدبلج]").replace("والاخيرة","").replace("كاملة","").replace("حلقات كاملة","").replace("اونلاين","").replace("مباشرة","").replace("انتاج ","").replace("جودة عالية","").replace("كامل","").replace("HD","").replace("السلسلة الوثائقية","").replace("الفيلم الوثائقي","").replace("اون لاين","")
            
            sTitle = sTitle.replace("poster","")
            siteUrl = URL_MAIN+str(aEntry[1])
            sThumbnail = URL_MAIN+str(aEntry[0])
            sInfo = aEntry[3]
            sInfo = '[COLOR yellow]'+aEntry[3]+'[/COLOR]'
            sYear = aEntry[4]
			
            oOutputParameterHandler.addParameter('siteUrl',siteUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumbnail', sThumbnail)
            oOutputParameterHandler.addParameter('sInfo', sInfo)
            oOutputParameterHandler.addParameter('sYear', sYear)
            if '/watch/' in siteUrl:
                oGui.addMovie(SITE_IDENTIFIER, 'showHosters', sTitle, '', sThumbnail, sInfo, oOutputParameterHandler) 
            else:
                oGui.addMovie(SITE_IDENTIFIER, 'showEps', sTitle, '', sThumbnail, sInfo, oOutputParameterHandler)
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
     # (.+?) ([^<]+) .+?
    sPattern = '<img class="lazy" data-original="([^<]+)" alt.+?<div class="name"> <a href="([^<]+)">([^<]+)</a> </div> <div class="overlay">.+?<div class="story-text"> <p>([^<]+)</p>.+?<div class="badge red" title=.+?>(.+?)</'
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
 
            sTitle = str(aEntry[2]).replace("مشاهدة","").replace("مسلسل","").replace("انمي","").replace("مترجمة","").replace("مترجم","").replace("فيلم","").replace("والأخيرة","").replace("مدبلج للعربية","مدبلج").replace("مدبلج","[مدبلج]").replace("والاخيرة","").replace("كاملة","").replace("حلقات كاملة","").replace("اونلاين","").replace("مباشرة","").replace("انتاج ","").replace("جودة عالية","").replace("كامل","").replace("HD","").replace("السلسلة الوثائقية","").replace("الفيلم الوثائقي","").replace("اون لاين","")
            siteUrl = URL_MAIN+str(aEntry[1])
            sThumbnail = URL_MAIN+str(aEntry[0])
            sInfo = aEntry[3]
            sYear = aEntry[4]

            oOutputParameterHandler.addParameter('siteUrl',siteUrl)
            oOutputParameterHandler.addParameter('sMovieTitle',sTitle)
            oOutputParameterHandler.addParameter('sThumbnail', sThumbnail)
            oOutputParameterHandler.addParameter('sInfo', sInfo)
            oOutputParameterHandler.addParameter('sYear', sYear)
            if '/watch/' in siteUrl:
                oGui.addTV(SITE_IDENTIFIER, 'showHosters', sTitle, '', sThumbnail, sInfo, oOutputParameterHandler) 
            else:
                oGui.addTV(SITE_IDENTIFIER, 'showEpisodes', sTitle, '', sThumbnail, sInfo, oOutputParameterHandler)

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
    sThumbnail = oInputParameterHandler.getValue('sThumbnail')
    sInfo = oInputParameterHandler.getValue('sInfo')
 
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
    # (.+?) .+?
    sPattern = '<li class="episode-link.+?href="([^<]+)"> <span>الحلقة</span> <span class="separator">:</span> <span>([^<]+)<'
    
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)

    if (aResult[0] == True):
        oOutputParameterHandler = cOutputParameterHandler() 
        for aEntry in aResult[1]:
 
            sTitle = " E"+aEntry[1]
            sTitle = sTitle+sMovieTitle
            siteUrl = URL_MAIN+str(aEntry[0])
            sThumbnail = str(sThumbnail)
            sInfo = sInfo
 
            oOutputParameterHandler.addParameter('siteUrl', siteUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumbnail', sThumbnail)
            

 
            oGui.addEpisode(SITE_IDENTIFIER, 'showHosters', sTitle, '', sThumbnail, sInfo, oOutputParameterHandler)

       
    oGui.setEndOfDirectory() 

 
def __checkForNextPage(sHtmlContent):
    sPattern = '<a class="page-link" href="([^<]+)" rel="next" '
	
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
 
    if (aResult[0] == True):
        #print aResult[1][0]
        return aResult[1][0]

    return False

def showHosters():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumbnail = oInputParameterHandler.getValue('sThumbnail')
    
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    # (.+?) .+? ([^<]+)
                

    sPattern = '<div class="item"> <span class="([^<]+)">'
    sPattern = sPattern + '|' + '<a data-src="([^<]+)">([^<]+)</a>'
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)

	
    if (aResult[0] == True):
            for aEntry in aResult[1]:



                sSub = aEntry[0].replace('active',"")
                sSub = sSub+' ترجمة'
            
                if aEntry[0]:
                   oGui.addText(SITE_IDENTIFIER,'[COLOR coral]'+sSub+'[/COLOR]')
                   
        
                if aEntry[1]:
                    url = str(aEntry[1])
                    sTitle = ''
                    if url.startswith('//'):
                       url = 'https:' + url
            
                    sHosterUrl = url 
                    if 'userload' in sHosterUrl:
                        sHosterUrl = sHosterUrl + "|Referer=" + URL_MAIN
                    if 'moshahda' in sHosterUrl:
                        sHosterUrl = sHosterUrl + "|Referer=" + URL_MAIN
                    if 'mystream' in sHosterUrl:
                        sHosterUrl = sHosterUrl + "|Referer=" + URL_MAIN  
                    oHoster = cHosterGui().checkHoster(sHosterUrl)
                    if (oHoster != False):
                       sDisplayTitle = sMovieTitle+sTitle
                       oHoster.setDisplayName(sDisplayTitle)
                       oHoster.setFileName(sMovieTitle)
                       cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumbnail)
				
    # (.+?) .+? ([^<]+)
               

    sPattern = '<div class="col-xs-12 col-md-2 quality-icon ([^<]+)"'
    sPattern = sPattern + '|' + '<a href="([^<]+)" target="_blank"'
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)


	
    if (aResult[0] == True):
            for aEntry in aResult[1]:


 


                sSub = aEntry[0]
            
                if aEntry[0]:
                   oGui.addText(SITE_IDENTIFIER,'[COLOR coral]'+sSub+'[/COLOR]')
                   
        
                if aEntry[1]:
                    url = str(aEntry[1])
                    sTitle = ''
                    if url.startswith('//'):
                       url = 'https:' + url
            
                    sHosterUrl = url 
                    if 'userload' in sHosterUrl:
                        sHosterUrl = sHosterUrl + "|Referer=" + URL_MAIN
                    if 'moshahda' in sHosterUrl:
                        sHosterUrl = sHosterUrl + "|Referer=" + URL_MAIN
                    if 'mystream' in sHosterUrl:
                        sHosterUrl = sHosterUrl + "|Referer=" + URL_MAIN   
                    oHoster = cHosterGui().checkHoster(sHosterUrl)
                    if (oHoster != False):
                        sDisplayTitle = sMovieTitle+sTitle
                        oHoster.setDisplayName(sDisplayTitle)
                        oHoster.setFileName(sMovieTitle)
                        cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumbnail)
				
    oGui.setEndOfDirectory()