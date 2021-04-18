#-*- coding: utf-8 -*-
#zombi
from resources.lib.gui.hoster import cHosterGui
from resources.lib.handler.hosterHandler import cHosterHandler
from resources.lib.gui.gui import cGui
from resources.lib.gui.guiElement import cGuiElement
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.comaddon import progress, isMatrix
from resources.lib.parser import cParser
from resources.lib.util import cUtil
import re
import unicodedata
 
SITE_IDENTIFIER = 'animeslayer'
SITE_NAME = 'animeslayer'
SITE_DESC = 'arabic vod'
 
URL_MAIN = 'https://app.anime-slayer.com'
ANIM_NEWS = ('https://app.anime-slayer.com/episode', 'showSeries')

ANIM_MOVIES = ('https://app.anime-slayer.com/anime-type/movie', 'showMovies')
KID_CARTOON = ('https://app.anime-slayer.com/anime-category/%d8%a7%d9%84%d8%a7%d9%86%d9%85%d9%8a-%d8%a7%d9%84%d9%85%d8%af%d8%a8%d9%84%d8%ac', 'showMovies')

URL_SEARCH = ('https://app.anime-slayer.com/?search_param=animes&s=', 'showMovies')
URL_SEARCH_SERIES = ('https://app.anime-slayer.com/?search_param=animes&s=', 'showMovies')
FUNCTION_SEARCH = 'showMovies'
 
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
        sUrl = 'https://app.anime-slayer.com/?search_param=animes&s='+sSearchText
        showMovies(sUrl)
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
 # ([^<]+) .+? (.+?)
    sPattern = '<img class="img-responsive" src="([^<]+)" alt="([^<]+)" /><a href="([^<]+)" class="overlay"></a>.+?data-content="([^<]+)">'

    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
	
	
    if (aResult[0] == True):
        total = len(aResult[1])
        progress_ = progress().VScreate(SITE_NAME)
        for aEntry in aResult[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break
 
            sTitle = str(aEntry[1]).replace("مشاهدة","").replace("مسلسل","").replace("انمي","").replace("مترجمة","").replace("مترجم","").replace("فيلم","").replace("والأخيرة","").replace("مدبلج للعربية","مدبلج").replace("مدبلج","[مدبلج]").replace("والاخيرة","").replace("كاملة","").replace("حلقات كاملة","").replace("اونلاين","").replace("مباشرة","").replace("انتاج ","").replace("جودة عالية","").replace("كامل","").replace("HD","").replace("السلسلة الوثائقية","").replace("الفيلم الوثائقي","").replace("اون لاين","")
            
            siteUrl = str(aEntry[2])
            sThumb = str(aEntry[0]).replace("(","").replace(")","")
            sDesc = str(aEntry[3])


            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl',siteUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
			
            oGui.addMovie(SITE_IDENTIFIER, 'showEpisodes', sTitle, '', sThumb, sDesc, oOutputParameterHandler)

        progress_.VSclose(progress_)
 
        sNextPage = __checkForNextPage(sHtmlContent)
        if (sNextPage != False):
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sNextPage)
            oGui.addDir(SITE_IDENTIFIER, 'showMovies', '[COLOR teal]Next >>>[/COLOR]', 'next.png', oOutputParameterHandler)
 
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
     # (.+?) ([^<]+) .+?
    sPattern = '<div class="episodes-card-title"><h3><a href="([^<]+)">([^<]+)</a></h3>'

    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
	
    if (aResult[0] == True):
        total = len(aResult[1])
        progress_ = progress().VScreate(SITE_NAME)
        for aEntry in aResult[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break
 
            sTitle = sMovieTitle+' '+aEntry[1]
            siteUrl = str(aEntry[0])
            sThumb = sThumb
            sDesc = ''
			


            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl',siteUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sMovieTitle2', sMovieTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oGui.addEpisode(SITE_IDENTIFIER, 'showHosters', sTitle, '', sThumb, sDesc, oOutputParameterHandler)
        
        progress_.VSclose(progress_)
		
        sNextPage = __checkForNextPage(sHtmlContent)
        if (sNextPage != False):
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sNextPage)
            oGui.addDir(SITE_IDENTIFIER, 'showEpisodes', '[COLOR teal]Next >>>[/COLOR]', 'next.png', oOutputParameterHandler)
       
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
    sPattern = '<div class="episodes-card-title"><h3><a href="([^<]+)">([^<]+)</a></h3>.+?<img class="img-responsive" src="([^<]+)" alt="([^<]+)" />.+?data-content="([^<]+)">'
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
	
	
    if (aResult[0] == True):
        total = len(aResult[1])
        progress_ = progress().VScreate(SITE_NAME)
        for aEntry in aResult[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break
 
            sTitle = str(aEntry[3])
            
            sEp = aEntry[1].replace("الحلقة","E").replace(" ","")
            if isMatrix(): 
               sEp = str(aEntry[1].encode('latin-1'),'utf-8').replace("الحلقة","E").replace(" ","")
            siteUrl = str(aEntry[0])
            sThumb = str(aEntry[2]).replace("(","").replace(")","")
            sDesc = str(aEntry[4])
            sDisplayTitle = ('%s %s') % (sTitle, sEp)


            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl',siteUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sMovieTitle2', sDisplayTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
			
            oGui.addTV(SITE_IDENTIFIER, 'showHosters', sDisplayTitle, '', sThumb, sDesc, oOutputParameterHandler)

        progress_.VSclose(progress_)
 
        sNextPage = __checkForNextPage(sHtmlContent)
        if (sNextPage != False):
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sNextPage)
            oGui.addDir(SITE_IDENTIFIER, 'showSeries', '[COLOR teal]Next >>>[/COLOR]', 'next.png', oOutputParameterHandler)
 
    if not sSearch:
        oGui.setEndOfDirectory()


 
 
def __checkForNextPage(sHtmlContent):
    sPattern = '<li><a href="([^<]+)"><span aria-hidden='
	
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
    sMovieTitle2 = oInputParameterHandler.getValue('sMovieTitle2')
    sThumb = oInputParameterHandler.getValue('sThumb')
    
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request();

    oParser = cParser()       


    # (.+?) .+? ([^<]+)
               

    sPattern = 'data-ep-url="([^<]+)">'
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)


    #print aResult

	
    if (aResult[0] == True):
            total = len(aResult[1])
            progress_ = progress().VScreate(SITE_NAME)
            for aEntry in aResult[1]:
                progress_.VSupdate(progress_, total)
                if progress_.iscanceled():
                   break
        
                url = aEntry
                sTitle = ''

                if 'thevideo.me' in url:
                    sTitle = " (thevideo.me)"
                if 'flashx' in url:
                    sTitle = " (flashx)"
                if 'streamcherry' in url:
                    sTitle = " (streamcherry)"
                if url.startswith('//'):
                    url = 'https:' + url
				
					
            
                sHosterUrl = url 
                oHoster = cHosterGui().checkHoster(sHosterUrl)
                if (oHoster != False):
                    sDisplayTitle = sMovieTitle2
                    oHoster.setDisplayName(sDisplayTitle)
                    oHoster.setFileName(sMovieTitle)
                    cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb)

    sPattern = 'class="btn btn-default" href="([^<]+)">'
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)


    #print aResult

	
    if (aResult[0] == True):
            total = len(aResult[1])
            progress_ = progress().VScreate(SITE_NAME)
            for aEntry in aResult[1]:
                progress_.VSupdate(progress_, total)
                if progress_.iscanceled():
                   break
        
                url = aEntry
                sTitle = ''

                if 'thevideo.me' in url:
                   sTitle = " (thevideo.me)"
                if 'flashx' in url:
                   sTitle = " (flashx)"
                if 'streamcherry' in url:
                   sTitle = " (streamcherry)"
                if url.startswith('//'):
                   url = 'https:' + url
				
					
            
                sHosterUrl = url 
                oHoster = cHosterGui().checkHoster(sHosterUrl)
                if (oHoster != False):
                   sDisplayTitle = sMovieTitle2
                   oHoster.setDisplayName(sDisplayTitle)
                   oHoster.setFileName(sMovieTitle)
                   cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb)
				


    sPattern = 'class="all-episodes-head">(.+?)<div class="search-in-episodes-list">'  
    
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern) 
     

    if (aResult[0] == True):
        sHtmlContent2 = aResult[1][0]

        oGui.addText(SITE_IDENTIFIER,'[COLOR olive]-------قائمه الحلقات --------[/COLOR]')
    # (.+?) .+? ([^<]+)
        sPattern = '<li><a href="([^<]+)">([^<]+)</a></li>'

        oParser = cParser()
        aResult = oParser.parse(sHtmlContent2, sPattern)
    

    #print aResult
   
        if (aResult[0] == True):
            total = len(aResult[1])
            progress_ = progress().VScreate(SITE_NAME)
            for aEntry in aResult[1]:
                progress_.VSupdate(progress_, total)
                if progress_.iscanceled():
                   break
 
                sEp = aEntry[1].replace("الحلقة","E").replace(" ","") 
                if isMatrix():            
                   sEp = str(aEntry[1].encode('latin-1'),'utf-8').replace("الحلقة","E").replace(" ","")
                sTitle = str(sMovieTitle)+" "+sEp
                siteUrl = aEntry[0]
                sThumbnail = ""
                sInfo = ""
 
            #print sUrl
                oOutputParameterHandler = cOutputParameterHandler()
                oOutputParameterHandler.addParameter('siteUrl', siteUrl)
                oOutputParameterHandler.addParameter('sMovieTitle', sMovieTitle)
                oOutputParameterHandler.addParameter('sMovieTitle2', sTitle)
                oOutputParameterHandler.addParameter('sThumbnail', sThumbnail)
                oGui.addEpisode(SITE_IDENTIFIER, 'showHosters', sTitle, '', sThumbnail, sInfo, oOutputParameterHandler)        
           
                
    oGui.setEndOfDirectory()	