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
from resources.lib.cloudflare import CloudflareBypass
from resources.lib.cloudflare import NoRedirection

import urllib2,urllib,re,xbmc
import unicodedata
 
SITE_IDENTIFIER = 'aracinema_co'
SITE_NAME = 'aradrama'
SITE_DESC = 'arabic vod'
 
URL_MAIN = 'https://aradramatv.net/'


SERIE_ASIA = ('https://aradramatv.net/category/episodes/new/', 'showEp')


SERIE_TR = ('http://aramosalsal.tv/category/turkish-serie/ts-subtitled/', 'showSerie')
URL_SEARCH = ('http://aracinema.co/?s=', 'showMovies')
URL_SEARCH_MOVIES = ('http://aracinema.co/?s=', 'showMovies')
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
        sUrl = 'http://aracinema.co/?s='+sSearchText
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


 

    #([^<]+).+?
    sPattern ='<a class="first_A" href="([^<]+)" title="([^<]+)"><img src="([^<]+)" alt='
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
	
	
    if (aResult[0] == True):
        total = len(aResult[1])
        progress_ = progress().VScreate(SITE_NAME)
        for aEntry in aResult[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break
 
            sTitle = aEntry[1].decode("utf8")
            sTitle = cUtil().unescape(sTitle).encode("utf8")
            sTitle = sTitle.replace("&#8217;","'").replace("مشاهدة","").replace("مترجم","").replace("فيلم","").replace("اون لاين","")
            siteUrl = str(aEntry[0])
            sThumbnail = str(aEntry[2])
            sInfo = sThumbnail


            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl',siteUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumbnail', sThumbnail)
			

            oGui.addMovie(SITE_IDENTIFIER, 'showMoviesLinks', sTitle, '', sThumbnail, sInfo, oOutputParameterHandler)
        
        progress_.VSclose(progress_)
 
        sNextPage = __checkForNextPage(sHtmlContent)
        if (sNextPage != False):
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sNextPage)
            oGui.addDir(SITE_IDENTIFIER, 'showMovies', '[COLOR teal]Next >>>[/COLOR]', 'next.png', oOutputParameterHandler)
 
    if not sSearch:
        oGui.setEndOfDirectory()

def showEp(sSearch = ''):
    oGui = cGui()
    if sSearch:
      sUrl = sSearch
    else:
        oInputParameterHandler = cInputParameterHandler()
        sUrl = oInputParameterHandler.getValue('siteUrl')
 
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()


 

    # 'src="([^<]+)" class=".+?href="([^<]+)">([^<]+)</.+?<div class="movieDesc">([^<]+)</div>'
    sPattern ='<a class="first_A" href="([^<]+)" title="([^<]+)"><img src="([^<]+)" alt='
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
	
	
    if (aResult[0] == True):
        total = len(aResult[1])
        progress_ = progress().VScreate(SITE_NAME)
        for aEntry in aResult[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break
 
            sTitle = aEntry[1]
            siteUrl = str(aEntry[0])


            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl',siteUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', str(aEntry[1]))
            oOutputParameterHandler.addParameter('sThumbnail', str(aEntry[2]))
			

            oGui.addTV(SITE_IDENTIFIER, 'showHosters', aEntry[1], '', aEntry[2], '', oOutputParameterHandler)
        
        progress_.VSclose(progress_)
 
        sNextPage = __checkForNextPage(sHtmlContent)
        if (sNextPage != False):
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sNextPage)
            oGui.addDir(SITE_IDENTIFIER, 'showMovies', '[COLOR teal]Next >>>[/COLOR]', 'next.png', oOutputParameterHandler)
 
    if not sSearch:
        oGui.setEndOfDirectory()
		
def showTvshows(sSearch = ''):
    oGui = cGui()
    if sSearch:
      sUrl = sSearch
    else:
        oInputParameterHandler = cInputParameterHandler()
        sUrl = oInputParameterHandler.getValue('siteUrl')
 
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()


 

    # 'src="([^<]+)" class=".+?href="([^<]+)">([^<]+)</.+?<div class="movieDesc">([^<]+)</div>'
    sPattern ='class="first_A" href="([^<]+)" title="([^<]+)"><img src="([^<]+)" alt.+?<a href="([^<]+)" title="حالة العمل الفني"><i class="icon-feed mi">'
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
	
	
    if (aResult[0] == True):
        total = len(aResult[1])
        progress_ = progress().VScreate(SITE_NAME)
        for aEntry in aResult[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break
 
            sTitle = aEntry[1]
            siteUrl = str(aEntry[0])
            sInfo = str(aEntry[3])
            sThumbnail = aEntry[2]


            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl',siteUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', str(aEntry[1]))
            oOutputParameterHandler.addParameter('sThumbnail', sThumbnail)
			
            if 'stat' in sInfo:
                oGui.addMovie(SITE_IDENTIFIER, 'showMoviesLinks', aEntry[1], '', sThumbnail, sThumbnail, oOutputParameterHandler)
        
        progress_.VSclose(progress_)
 
        sNextPage = __checkForNextPage(sHtmlContent)
        if (sNextPage != False):
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sNextPage)
            oGui.addDir(SITE_IDENTIFIER, 'showMovies', '[COLOR teal]Next >>>[/COLOR]', 'next.png', oOutputParameterHandler)
 
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


 

    # 'src="([^<]+)" class=".+?href="([^<]+)">([^<]+)</.+?<div class="movieDesc">([^<]+)</div>'
    sPattern ='<div class="featured_thumb mb"><a class="first_A" href="([^<]+)" title="([^<]+)"><img src="([^<]+)" alt='
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
	
	
    if (aResult[0] == True):
        total = len(aResult[1])
        progress_ = progress().VScreate(SITE_NAME)
        for aEntry in aResult[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break
 
            sTitle = aEntry[1]
            siteUrl = str(aEntry[0])
            sThumbnail = aEntry[2]


            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl',siteUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', str(aEntry[1]))
            oOutputParameterHandler.addParameter('sThumbnail', str(aEntry[2]))
			

            oGui.addMovie(SITE_IDENTIFIER, 'showSerieLinks', aEntry[1], '', sThumbnail, '', oOutputParameterHandler)
        
        progress_.VSclose(progress_)
 
        sNextPage = __checkForNextPage(sHtmlContent)
        if (sNextPage != False):
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sNextPage)
            oGui.addDir(SITE_IDENTIFIER, 'showMovies', '[COLOR teal]Next >>>[/COLOR]', 'next.png', oOutputParameterHandler)
 
    if not sSearch:
        oGui.setEndOfDirectory() 
		
def showSerieLinks():
    
    oGui = cGui()
    
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumbnail = oInputParameterHandler.getValue('sThumbnail')
 
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()



    #print sUrl
   
    oParser = cParser()
    
    #Recuperation infos
    sNote = ''
    sCom = ''

    sPattern = '<span>تقييم الفيلم : </span>(.+?)</p><h3>القصة :</h3><p>(.+?)</p></div>'
    aResult = oParser.parse(sHtmlContent, sPattern)
    
    if (aResult[0]):
        sNote = aResult[1][0][0]
        sCom = aResult[1][0][1]
        sCom = cUtil().removeHtmlTags(sCom)
    if (sNote):
        oGui.addText(SITE_IDENTIFIER,'تقييم الفيلم : ' + str(sNote))

    
    
    #Affichage du menu  
    oGui.addText(SITE_IDENTIFIER,'[COLOR olive][/COLOR]')



    #<a class="wpb_button_a" title="مشاهدة الحلقات أونلاين" href="http://aracinema.com/category/airing/the-expanse-s2/"><span class="wpb_button  wpb_btn-warning wpb_btn-large">مشاهدة الحلقات أونلاين<
    sPattern = 'class="vc_btn3-container vc_btn3-inline"><a class="vc_general vc_btn3 vc_btn3-size-lg vc_btn3-shape-square vc_btn3-style-flat vc_btn3-color-turquoise" href="([^<]+)" title="">([^<]+)</a></div>'
    aResult = oParser.parse(sHtmlContent, sPattern)
    
    if (aResult[0] == True):
        total = len(aResult[1])
        progress_ = progress().VScreate(SITE_NAME)
        for aEntry in aResult[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break

            sTitle = sMovieTitle +  ' - [COLOR skyblue]' + aEntry[1]+'[/COLOR]'
            sUrl= aEntry[0].replace('http://aracinema.com','http://aracinema.co')
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl',  sUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', str(sMovieTitle))
            oOutputParameterHandler.addParameter('sThumbnail', str(sThumbnail))
            oGui.addMovie(SITE_IDENTIFIER, 'showSeries', sTitle, '', sThumbnail, sCom, oOutputParameterHandler)             
    
        progress_.VSclose(progress_)

    oGui.setEndOfDirectory()
		
def showMoviesLinks():
    
    oGui = cGui()
    
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumbnail = oInputParameterHandler.getValue('sThumbnail')
 
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()



    #print sUrl
   
    oParser = cParser()
    
    #Recuperation infos
    sNote = ''
    sCom = ''

    sPattern = '<span>تقييم الفيلم : </span>(.+?)</p><h3>القصة :</h3><p>(.+?)</p></div>'
    aResult = oParser.parse(sHtmlContent, sPattern)
    
    if (aResult[0]):
        sNote = aResult[1][0][0]
        sCom = aResult[1][0][1]
        sCom = cUtil().removeHtmlTags(sCom)
    if (sNote):
        oGui.addText(SITE_IDENTIFIER,'تقييم الفيلم : ' + str(sNote))

    
    
    #Affichage du menu  
    oGui.addText(SITE_IDENTIFIER,'[COLOR olive][/COLOR]')



    #<a class="wpb_button_a" title="مشاهدة الحلقات أونلاين" href="http://aracinema.com/category/airing/the-expanse-s2/"><span class="wpb_button  wpb_btn-warning wpb_btn-large">مشاهدة الحلقات أونلاين<
    sPattern = '<a class="wpb_button_a" title="([^<]+)" href="([^<]+)"><span class="wpb_button  wpb_btn-warning wpb_btn-large">'
    aResult = oParser.parse(sHtmlContent, sPattern)
    
    if (aResult[0] == True):
        total = len(aResult[1])
        progress_ = progress().VScreate(SITE_NAME)
        for aEntry in aResult[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break

            sTitle = sMovieTitle +  ' - [COLOR skyblue]' + aEntry[0]+'[/COLOR]'
            sUrl= aEntry[1].replace('http://aracinema.com','http://aracinema.co')
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl',  sUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', str(sMovieTitle))
            oOutputParameterHandler.addParameter('sThumbnail', str(sThumbnail))
            oGui.addMovie(SITE_IDENTIFIER, 'showSeries', sTitle, '', sThumbnail, sCom, oOutputParameterHandler)             
    
        progress_.VSclose(progress_)

    oGui.setEndOfDirectory()
		
def showSeason():
    oGui = cGui()
    
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumbnail = oInputParameterHandler.getValue('sThumbnail')
 
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()


 
    sPattern = 'class="wpb_button_a" title="([^<]+)" href="([^<]+)"><span class'

    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
	
	
    if (aResult[0] == True):
        total = len(aResult[1])
        progress_ = progress().VScreate(SITE_NAME)
        for aEntry in aResult[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break
 
            sTitle = aEntry[0]
            siteUrl = str(aEntry[1])
			


            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl',siteUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', str(aEntry[0]))
            oOutputParameterHandler.addParameter('sThumbnail', sThumbnail)
            oGui.addMovie(SITE_IDENTIFIER, 'showSeries', aEntry[0], '', sThumbnail, '', oOutputParameterHandler)
        
        progress_.VSclose(progress_)
       
    oGui.setEndOfDirectory()
	
def showSeries():
    oGui = cGui()
    
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumbnail = oInputParameterHandler.getValue('sThumbnail')
 
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()


 
    sPattern = '<a href="([^<]+)" class="([^<]+)" title="([^<]+)<'

    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
	
	
    if (aResult[0] == True):
        total = len(aResult[1])
        progress_ = progress().VScreate(SITE_NAME)
        for aEntry in aResult[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break
 
            sTitle = aEntry[1] + aEntry[2]
            siteUrl = str(aEntry[0])
			


            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl',siteUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sMovieTitle)
            oOutputParameterHandler.addParameter('sThumbnail', sThumbnail)

            oGui.addMovie(SITE_IDENTIFIER, 'showSeries', aEntry[1], '', sThumbnail, '', oOutputParameterHandler)
        
        progress_.VSclose(progress_)


 
    sPattern = 'class="first_A" href="([^<]+)" title="([^<]+)"><img src="([^<]+)" alt'

    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
	
	
    if (aResult[0] == True):
        total = len(aResult[1])
        progress_ = progress().VScreate(SITE_NAME)
        for aEntry in aResult[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break
 
            sTitle = aEntry[1]
            siteUrl = str(aEntry[0])
			


            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl',siteUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sMovieTitle)
            oOutputParameterHandler.addParameter('sThumbnail', sThumbnail)

            oGui.addMovie(SITE_IDENTIFIER, 'showHosters', aEntry[1], '', sThumbnail, '', oOutputParameterHandler)
        
        progress_.VSclose(progress_)
       
    oGui.setEndOfDirectory()
 
       
 #.+?([^<]+) 
 
 
def __checkForNextPage(sHtmlContent):
    sPattern = 'class="current">.+?</span><a href="([^<]+)" class="page"'
	
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
    sHtmlContent = oRequestHandler.request();


    #sHtmlContent = sHtmlContent.replace('<iframe src="//www.facebook.com/plugins/like.php','').replace('<iframe src="http://www.facebook.com/plugins/likebox.php','')
               
        
    sPattern = 'src="([^<]+)"'
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
            if url.startswith('//'):
                url = 'http:' + url
            
            sHosterUrl = url
            oHoster = cHosterGui().checkHoster(sHosterUrl)
            if (oHoster != False):
                oHoster.setDisplayName(sMovieTitle)
                oHoster.setFileName(sMovieTitle)
                cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumbnail)
				

        progress_.VSclose(progress_) 
                
    oGui.setEndOfDirectory()