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
 
 
SITE_IDENTIFIER = 'aracinema_co'
SITE_NAME = 'aramosalsal'
SITE_DESC = 'arabic vod'
 
URL_MAIN = 'http://aramosalsal.tv'


MOVIE_ASIAN = ('https://aradramtv.com/category/%d8%a7%d9%84%d8%a7%d9%81%d9%84%d8%a7%d9%85-%d8%a7%d9%84%d8%a2%d8%b3%d9%8a%d9%88%d9%8a%d8%a9/', 'showMovies')
SERIE_AR = ('https://aramosalsal.tv/category/%d9%85%d8%b3%d9%84%d8%b3%d9%84%d8%a7%d8%aa-%d8%b1%d9%85%d8%b6%d8%a7%d9%86-2020/', 'showSerie')

SERIE_TR = ('http://aramosalsal.tv/category/turkish-serie/ts-subtitled/', 'showSerie')
SERIE_TR_AR = ('https://aramosalsal.net/category/turkish-serie/ts-doubled/', 'showSerie')
SERIE_ASIA = ('https://aradramtv.com/category/serie/', 'showSerie')
URL_SEARCH = ('http://aracinema.co/?s=', 'showMovies')
URL_SEARCH_MOVIES = ('https://aradramatv.co/?s=', 'showMovies')
URL_SEARCH_SERIES = ('https://aradramatv.co/?s=', 'showSerie')
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
        sUrl = 'https://aradramatv.co/?s='+sSearchText
        showSerie(sUrl)
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


 

    # ([^<]+) .+?
    sPattern ='<article id="post-.+?href="([^<]+)" title="([^<]+)"><img src="([^<]+)" alt=.+?<i class="icon-folder-open mi"></i>([^<]+)</a>.+?<i class="icon-calendar mi"></i>([^<]+)</a>'
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
 
            if "فيلم" not in aEntry[1]:
                continue
 
            sTitle = aEntry[1]
            sTitle = sTitle.replace("&#8217;","'").replace("مشاهدة","").replace("مترجم","").replace("فيلم","").replace("اون لاين","").replace("مشاهدة","").replace("مسلسل","").replace("انمي","").replace("مترجمة","").replace("مترجم","").replace("فيلم","").replace("والأخيرة","").replace("مدبلج للعربية","مدبلج").replace("والاخيرة","").replace("كاملة","").replace("برنامج","").replace("حلقات كاملة","").replace("اونلاين","").replace("مباشرة","").replace("انتاج ","").replace("جودة عالية","").replace("كامل","").replace("HD","").replace("السلسلة الوثائقية","").replace("الفيلم الوثائقي","").replace("اون لاين","")
            siteUrl = aEntry[0]
            sThumb = aEntry[2]
            sDesc = aEntry[3]
            sYear = aEntry[4]


            oOutputParameterHandler.addParameter('siteUrl',siteUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oOutputParameterHandler.addParameter('sYear', sYear)
			

            oGui.addMovie(SITE_IDENTIFIER, 'showLink', sTitle, '', sThumb, sDesc, oOutputParameterHandler)
        
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

    # ([^<]+) .+?
    sPattern ='<article id="post-.+?href="([^<]+)" title="([^<]+)"><img src="([^<]+)" alt=.+?<i class="icon-folder-open mi"></i>([^<]+)</a>.+?<i class="icon-calendar mi"></i>([^<]+)</a>'
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
 
            sTitle = aEntry[1].replace("مشاهدة","").replace("مسلسل","").replace("انمي","").replace("مترجمة","").replace("مترجم","").replace("فيلم","").replace("والأخيرة","").replace("مدبلج للعربية","مدبلج").replace("برنامج","").replace("والاخيرة","").replace("كاملة","").replace("حلقات كاملة","").replace("اونلاين","").replace("مباشرة","").replace("انتاج ","").replace("جودة عالية","").replace("كامل","").replace("HD","").replace("السلسلة الوثائقية","").replace("الفيلم الوثائقي","").replace("اون لاين","")
            siteUrl = aEntry[0]
            sThumb = aEntry[2]
            sDesc = aEntry[3]
            sYear = aEntry[4]
            sDisplayTitle = ('%s (%s)') % (sTitle, sYear)


            oOutputParameterHandler.addParameter('siteUrl',siteUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oOutputParameterHandler.addParameter('sYear', sYear)
			

            oGui.addTV(SITE_IDENTIFIER, 'showEpisodes', sTitle, '', sThumb, sDesc, oOutputParameterHandler)
        
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


 

    # ([^<]+) .+?
    sPattern ='<a class="first_A" href="([^<]+)" title="([^<]+)"><img src="([^<]+)" alt.+?</i>([^<]+)</a>'
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
 
            sTitle = aEntry[1].replace("مشاهدة","").replace("مسلسل","").replace("انمي","").replace("مترجمة","").replace("مترجم","").replace("فيلم","").replace("والأخيرة","").replace("مدبلج للعربية","مدبلج").replace("برنامج","").replace("والاخيرة","").replace("كاملة","").replace("حلقات كاملة","").replace("اونلاين","").replace("مباشرة","").replace("انتاج ","").replace("جودة عالية","").replace("كامل","").replace("HD","").replace("السلسلة الوثائقية","").replace("الفيلم الوثائقي","").replace("اون لاين","")
            sDisplayTitle2 = sTitle.split('الحلقة')[0].split('الموسم')[0].split('مدبلج')[0].split('مسلسل')[0]
            siteUrl = aEntry[0]
            sThumb = aEntry[2]
            sDesc = aEntry[3]


            oOutputParameterHandler.addParameter('siteUrl',siteUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sDisplayTitle2)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
			

            oGui.addTV(SITE_IDENTIFIER, 'showEpisodes', sTitle, '', sThumb, sDesc, oOutputParameterHandler)
        
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
    sThumbnail = oInputParameterHandler.getValue('sThumbnail')
 
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    oParser = cParser()
    
    #Recuperation infos
    sNote = ''

    sPattern = '<p class="<h3>القصة :</h3><p>([^<]+)</p>'
    aResult = oParser.parse(sHtmlContent, sPattern)
    
    if (aResult[0]):
        sNote = aResult[1][0]
            
    sPattern =  'href="([^<]+)" title="">' 
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent,sPattern)
    if (aResult[0] == True):
        m3url = aResult[1][0]
        oRequest = cRequestHandler(m3url)
        sHtmlContent = oRequest.request()
	
     # (.+?) ([^<]+) .+?
    sPattern = '<a class="first_A" href="([^<]+)" title="([^<]+)"><img src="([^<]+)"'

    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
	
	
    if (aResult[0] == True):
        oOutputParameterHandler = cOutputParameterHandler() 
        for aEntry in aResult[1]:
 
            sTitle = aEntry[1].replace("الحلقة "," E").replace("مترجم","").replace("والأخيرة","")
            siteUrl = str(aEntry[0])
            sThumbnail = sThumbnail
            sInfo = sNote
			


            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl',siteUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumbnail', sThumbnail)
            oGui.addEpisode(SITE_IDENTIFIER, 'showHosters', sTitle, '', sThumbnail, sInfo, oOutputParameterHandler)
        
 
        sNextPage = __checkForNextPage(sHtmlContent)
        if (sNextPage != False):
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sNextPage)
            oGui.addDir(SITE_IDENTIFIER, 'showEpisodes', '[COLOR teal]Next >>>[/COLOR]', 'next.png', oOutputParameterHandler)
       
    oGui.setEndOfDirectory()
	

def showLink():
    oGui = cGui()
   
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')
 
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
    
    oParser = cParser()
    
    #Recuperation infos
    sNote = ''

    sPattern = '<h3>القصة :</h3><p>(.+?)</p>'
    aResult = oParser.parse(sHtmlContent, sPattern)
    
    if (aResult[0]):
        sNote = aResult[1][0]
        # (.+?) .+? ([^<]+)
    oParser = cParser()
    # .+? ([^<]+)
    sPattern = '<a class="vc_general vc_btn3 vc_btn3-size-lg vc_btn3-shape-square vc_btn3-style-flat vc_btn3-color-danger" href="(.+?)" title'
    
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)


    #print aResult
   
    if (aResult[0] == True):
        oOutputParameterHandler = cOutputParameterHandler() 
        for aEntry in aResult[1]:
 
            sTitle = sMovieTitle
            sTitle = '[COLOR cyan]'+sTitle+'[/COLOR]'
            siteUrl = aResult[1][0]
            sThumb = sThumb
            sDesc = sNote
 
            oOutputParameterHandler.addParameter('siteUrl', siteUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sMovieTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            
            oGui.addLink(SITE_IDENTIFIER, 'showHosters', sTitle, sThumb, sDesc, oOutputParameterHandler)

       
    oGui.setEndOfDirectory()
       
 
def __checkForNextPage(sHtmlContent):
    sPattern = 'class="current">.+?</span><a href="([^<]+)" class="page"'
	
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
 
    if (aResult[0] == True):
        return aResult[1][0]

    return False

def showHosters():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')
    
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request();
    # (.+?) .+? ([^<]+)
    oParser = cParser()  


    sPattern =  '<a class="first_A" href="([^<]+)" title=' 
    aResult = oParser.parse(sHtmlContent,sPattern)
    if (aResult[0] == True):
        m3url =  aResult[1][0]
        oRequest = cRequestHandler(m3url)
        sHtmlContent = oRequest.request()
               
        
    sPattern = 'src="(.+?)"'
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
	
    if (aResult[0] == True):
        for aEntry in aResult[1]:
            
            url = str(aEntry)
            url = url.replace("?rel=0","")
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
            if (oHoster != False):
                oHoster.setDisplayName(sMovieTitle)
                oHoster.setFileName(sMovieTitle)
                cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb)
				
                
    oGui.setEndOfDirectory()