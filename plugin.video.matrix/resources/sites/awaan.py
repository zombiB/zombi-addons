#-*- coding: utf-8 -*-
#zombi https://github.com/zombiB/zombi-addons/
from resources.lib.gui.gui import cGui
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.comaddon import progress, VSlog
from resources.lib.parser import cParser
from resources.lib.player import cPlayer
from resources.lib.gui.guiElement import cGuiElement
import re
 
SITE_IDENTIFIER = 'awaan'
SITE_NAME = 'awaan'
SITE_DESC = 'arabic vod'
 
URL_MAIN = 'http://awaan.ae/'
URL_SERIE = 'https://www.awaan.ae/show/allprograms/30348/%D8%A7%D9%84%D9%85%D8%B3%D9%84%D8%B3%D9%84%D8%A7%D8%AA'

MOVIE_AR = ('https://www.awaan.ae/movies?page=1', 'showMovies')
SERIE_AR = ('https://www.awaan.ae/series?page=1', 'showSeries')

RAMADAN_SERIES = ('https://www.awaan.ae/show/allprograms/214766/%D8%B1%D9%85%D8%B6%D8%A7%D9%86?page=1', 'showSeries')
REPLAYTV_NEWS = ('https://www.awaan.ae/show/allprograms/30350/%D8%AA%D8%B1%D9%81%D9%8A%D9%87?page=1', 'showSeries')
REPLAYTV_PLAY = ('http://awaan.ae/show/205952/%D9%85%D8%B3%D8%B1%D8%AD%D9%8A%D8%A7%D8%AA-%D8%B2%D9%85%D8%A7%D9%86?page=1', 'showEps')
ISLAM_SHOWS = ('https://www.awaan.ae/programs/30349/%D8%A5%D8%B3%D9%84%D8%A7%D9%85%D9%8A%D8%A7%D8%AA?page=1', 'showSeries')

ISLAM_QURAN = ('https://www.awaan.ae/programs/208779/%D8%A7%D9%84%D9%82%D8%B1%D8%A2%D9%86-%D8%A7%D9%84%D9%83%D8%B1%D9%8A%D9%85?page=1', 'showSeries')
URL_SEARCH = ('https://www.awaan.ae/search', 'showMovies')
FUNCTION_SEARCH = 'showMovies'
 
def load():
    oGui = cGui()

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'http://venom/')
    oGui.addDir(SITE_IDENTIFIER, 'showSearch', 'Search', 'search.png', oOutputParameterHandler)
	
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', SERIE_AR[0])
    oGui.addDir(SITE_IDENTIFIER, 'showSeries', 'SERIE_AR', 'anime.png', oOutputParameterHandler)

            
    oGui.setEndOfDirectory()
 
def showSearch():
    oGui = cGui()
 
    sSearchText = oGui.showKeyBoard()
    if (sSearchText != False):
        sUrl = 'https://www.awaan.ae/search'+sSearchText
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
 # .+? ([^<]+) (.+?)

    sPattern = '<a href="([^<]+)" class="item">.+?<img class="lozad" data-src="(.+?)" alt="img" title="(.+?)">'

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
 
            sTitle = aEntry[2].replace("مشاهدة","").replace("مسلسل","").replace("انمي","").replace("مترجمة","").replace("مترجم","").replace("برنامج","").replace("فيلم","").replace("والأخيرة","").replace("مدبلج للعربية","مدبلج").replace("والاخيرة","").replace("كاملة","").replace("حلقات كاملة","").replace("اونلاين","").replace("مباشرة","").replace("انتاج ","").replace("جودة عالية","").replace("كامل","").replace("HD","").replace("السلسلة الوثائقية","").replace("الفيلم الوثائقي","").replace("اون لاين","")
            
            siteUrl = aEntry[0]
            sThumbnail = aEntry[1]
            sInfo = ""


            oOutputParameterHandler.addParameter('siteUrl',siteUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumbnail', sThumbnail)
			
            oGui.addMovie(SITE_IDENTIFIER, 'showHosters', sTitle, '', sThumbnail, sInfo, oOutputParameterHandler)

        progress_.VSclose(progress_)
    page = sUrl.split('?page=')[1]
    page = int(page)+1
    sTitle = 'More' 
    sTitle = '[COLOR red]'+sTitle+'[/COLOR]'
    page = str(page)
    siteUrl = sUrl.split('?page=')[0]
    siteUrl = siteUrl +'?page='+ page

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl',siteUrl)
    oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', sTitle,'next.png', oOutputParameterHandler)
 
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
 # .+? ([^<]+) (.+?)

    sPattern = '<div href="(.+?)" class="item info">.+?<img class="lozad" data-src="(.+?)" alt="img" title="(.+?)">'
 
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

            sTitle = aEntry[2].replace("مشاهدة","").replace("مسلسل","").replace("انمي","").replace("مترجمة","").replace("مترجم","").replace("فيلم","").replace("والأخيرة","").replace("مدبلج للعربية","مدبلج").replace("برنامج","").replace("والاخيرة","").replace("كاملة","").replace("حلقات كاملة","").replace("اونلاين","").replace("مباشرة","").replace("انتاج ","").replace("جودة عالية","").replace("كامل","").replace("HD","").replace("السلسلة الوثائقية","").replace("الفيلم الوثائقي","").replace("اون لاين","")
            
            siteUrl = aEntry[0]+'?page=1'
            sThumbnail = aEntry[1]
            sInfo = ''


            oOutputParameterHandler.addParameter('siteUrl',siteUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumbnail', sThumbnail)
			
            oGui.addTV(SITE_IDENTIFIER, 'showEps', sTitle, '', sThumbnail, sInfo, oOutputParameterHandler)

        progress_.VSclose(progress_)
    page = sUrl.split('?page=')[1]
    page = int(page)+1
    sTitle = 'More' 
    sTitle = '[COLOR red]'+sTitle+'[/COLOR]'
    page = str(page)
    siteUrl = sUrl.split('?page=')[0]
    siteUrl = siteUrl +'?page='+ page

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl',siteUrl)
    oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
    oGui.addDir(SITE_IDENTIFIER, 'showSeries', sTitle,'next.png', oOutputParameterHandler)
 
    if not sSearch:
        oGui.setEndOfDirectory()
  
def __checkForNextPage(sHtmlContent):
    sPattern = ''
	
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
 
    if (aResult[0] == True):

        return '?p='+aResult[1][0]
    return False
  
def showEps():
    oGui = cGui()
   
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumbnail = oInputParameterHandler.getValue('sThumbnail')
    sLink = ""
    sLink = sUrl
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
 #  ([^<]+) (.+?) .+?

    sPattern = '<a href="(.+?)" class="item">.+?<img class="lozad" data-src="(.+?)">.+?<h3>(.+?)</h3>'

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

            sTitle = aEntry[2].replace("الحلقة "," E").replace("حلقة "," E").replace("مشاهدة","").replace("مسلسل","").replace("انمي","").replace("مترجمة","").replace("مترجم","").replace("فيلم","").replace("والأخيرة","").replace("مدبلج للعربية","مدبلج").replace("برنامج","").replace("والاخيرة","").replace("كاملة","").replace("حلقات كاملة","").replace("اونلاين","").replace("مباشرة","").replace("انتاج ","").replace("جودة عالية","").replace("كامل","").replace("HD","").replace("السلسلة الوثائقية","").replace("الفيلم الوثائقي","").replace("اون لاين","")
            
            siteUrl = aEntry[0]
            sThumbnail = aEntry[1]
            sInfo = ''
            if ':' in aEntry[2]:
               sTitle = sTitle.split(':')[1]+sMovieTitle


            oOutputParameterHandler.addParameter('siteUrl',siteUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumbnail', sThumbnail)
			
            oGui.addTV(SITE_IDENTIFIER, 'showHosters', sTitle, '', sThumbnail, sInfo, oOutputParameterHandler)

        progress_.VSclose(progress_)
    page = sUrl.split('?page=')[1]
    page = int(page)+1
    sTitle = 'More' 
    sTitle = '[COLOR red]'+sTitle+'[/COLOR]'
    page = str(page)
    siteUrl = sUrl.split('?page=')[0]
    siteUrl = siteUrl +'?page='+ page

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl',siteUrl)
    oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
    oGui.addDir(SITE_IDENTIFIER, 'showSeries', sTitle,'next.png', oOutputParameterHandler)
 
    oGui.setEndOfDirectory() 

def showHosters():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumbnail = oInputParameterHandler.getValue('sThumbnail')
    
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    oParser = cParser()
            
    sPattern =  '<iframe class="iframe-tv" id="iframe-tv" scrolling = "no" src="(.+?)"  allow="autoplay"' 
    aResult = oParser.parse(sHtmlContent,sPattern)
    if (aResult[0] == True):
        m3url = aResult[1][0]
        if m3url.startswith('//'):
           m3url = 'http:' + m3url 	
        oRequest = cRequestHandler(m3url)
        sHtmlContent = oRequest.request()

    oParser = cParser()
       
      # (.+?) ([^<]+) .+?     
    #recup du lien mp4
    sPattern = 'src: "(.+?)",'
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
    
    if (aResult[0] == True):
        
        sUrl = aResult[1][0]
        if sUrl.startswith('//'):
           sUrl = 'http:' + sUrl 
                 
        #on lance video directement
        oGuiElement = cGuiElement()
        oGuiElement.setSiteName(SITE_IDENTIFIER)
        oGuiElement.setTitle(sMovieTitle)
        oGuiElement.setMediaUrl(sUrl)
        oGuiElement.setThumbnail(sThumbnail)

        oPlayer = cPlayer()
        oPlayer.clearPlayList()
        oPlayer.addItemToPlaylist(oGuiElement)
        oPlayer.startPlayer()
        return
    
    else:
        return

    oGui.setEndOfDirectory()	