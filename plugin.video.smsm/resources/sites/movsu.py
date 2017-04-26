#-*- coding: utf-8 -*-
#zombi.(@geekzombi)
from resources.lib.gui.hoster import cHosterGui
from resources.lib.handler.hosterHandler import cHosterHandler
from resources.lib.gui.gui import cGui
from resources.lib.gui.guiElement import cGuiElement
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.config import cConfig
from resources.lib.parser import cParser
from resources.lib.util import cUtil
import urllib2,urllib,re
import unicodedata
 
SITE_IDENTIFIER = 'movsu'
SITE_NAME = 'movs4u'
SITE_DESC = 'arabic vod'
 
URL_MAIN = 'http://www.movs4u.com'

MOVIE_EN = ('http://www.movs4u.com/movie/', 'showMovies')
MOVIE_ANIME = ('http://www.movs4u.com/genre/animation/', 'showMovies')
MOVIE_HI = ('http://www.movs4u.com/genre/india-%D8%A7%D9%81%D9%84%D8%A7%D9%85-%D9%87%D9%86%D8%AF%D9%8A%D8%A9/', 'showMovies')

SERIE_EN = ('http://www.movs4u.com/tvshows/', 'showSeries')
ANIM_MOVIES = ('http://www.movs4u.com/genre/%D9%85%D8%AF%D8%A8%D9%84%D8%AC/', 'showMovies')



URL_SEARCH = ('http://www.movs4u.com/?s=', 'showMovies')
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
        sUrl = 'http://www.movs4u.com/?s='+sSearchText
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
 

    sPattern = 'class="item movies"><div class="poster"> <a href="(.+?)"><img src="(.+?)" alt="(.+?)"></a><div class="rating"><span class="icon-star2"></span>(.+?)</div><span class="quality">(.+?)</span>.+?<div class="texto">(.+?)<div'

    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
	
	
    if (aResult[0] == True):
        total = len(aResult[1])
        dialog = cConfig().createDialog(SITE_NAME)
        for aEntry in aResult[1]:
            cConfig().updateDialog(dialog, total)
            if dialog.iscanceled():
                break
 
            sTitle = aEntry[2].replace("&#8217;", "'") 
            sThumbnail = aEntry[1]
            siteUrl = aEntry[0]
            sInfo = str(aEntry[4])+'                                                                                 '+'[COLOR yellow]'+str(aEntry[5])+'[/COLOR]' + aEntry[3]+('/10')



            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl',siteUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumbnail', sThumbnail)

            oGui.addMovie(SITE_IDENTIFIER, 'showLink', sTitle, '', sThumbnail, sInfo, oOutputParameterHandler)
        
        cConfig().finishDialog(dialog)
 
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
 

    sPattern = 'class="item tvshows"><div class="poster"> <span class="ses">(.+?)</span> <span class="esp">(.+?)</span> <a href="(.+?)"><img src="(.+?)" alt="(.+?)"></a><div class="rating"><span class="icon-star2"></span>(.+?)</div></div><div class="data">.+?<div class="texto">(.+?)<div'

    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
	
	
    if (aResult[0] == True):
        total = len(aResult[1])
        dialog = cConfig().createDialog(SITE_NAME)
        for aEntry in aResult[1]:
            cConfig().updateDialog(dialog, total)
            if dialog.iscanceled():
                break
 
            sTitle = aEntry[4].replace("&#8217;", "'") 
            sThumbnail = aEntry[3]
            siteUrl = aEntry[2]
            sInfo = str(aEntry[0])+'-'+str(aEntry[1])+'                                                                                 '+'[COLOR yellow]'+str(aEntry[6])+'[/COLOR]' + aEntry[5]+('/10')



            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl',siteUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumbnail', sThumbnail)

            oGui.addMovie(SITE_IDENTIFIER, 'showSeriesLinks', sTitle, '', sThumbnail, sInfo, oOutputParameterHandler)
        
        cConfig().finishDialog(dialog)
 
        sNextPage = __checkForNextPage(sHtmlContent)
        if (sNextPage != False):
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sNextPage)
            oGui.addDir(SITE_IDENTIFIER, 'showMovies', '[COLOR teal]Next >>>[/COLOR]', 'next.png', oOutputParameterHandler)
 
    if not sSearch:
        oGui.setEndOfDirectory()
 
def __checkForNextPage(sHtmlContent):
    sPattern = 'class="current">.+?</span><a href=(.+?) class'
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
    if (aResult[0] == True):
        aResult = aResult[1][0].replace("'","")
        return aResult

    return False 
 
def showSeriesLinks():
    
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
    sQua = ''
    sSeason = ''


    sPattern = '<meta itemprop="ratingCount" content=".+?">(.+?)<small>.+?</small>.+?<p itemprop="description">(.+?)</p>.+?class="item-value item-hot">(.+?)</span>'
    aResult = oParser.parse(sHtmlContent, sPattern)
    
    if (aResult[0]):
        sNote = aResult[1][0][0]
        sCom = aResult[1][0][1]
        sQua = aResult[1][0][2]
        sCom = cUtil().removeHtmlTags(sCom)
    if (sNote):
        oGui.addText(SITE_IDENTIFIER,str(sNote)+'  :IMDB')
    if (sQua):
        oGui.addText(SITE_IDENTIFIER,str(sQua)+' : وضع المسلسل')

    
    


    
    
    #Affichage du menu  
    oGui.addText(SITE_IDENTIFIER,'[COLOR olive]_______________[/COLOR]')



    #data-src="([^<]+)"class="season_group_btn collapsed" aria-expanded="true"> <span>02</span> Season 02 - Mad Men </a>
    sPattern = 'class="title">([^<]+)<i>([^<]+)</i></span>'
    sPattern = sPattern + '|' + '<img src="([^<]+)"></a></div><div class="numerando">([^<]+)</div><div class="episodiotitle"><a href="([^<]+)">([^<]+)</a><span class="date">([^<]+)</span></div></li>'
    aResult = oParser.parse(sHtmlContent, sPattern)

    if (aResult[0] == True):
        total = len(aResult[1])
        dialog = cConfig().createDialog(SITE_NAME)
        for aEntry in aResult[1]:
            cConfig().updateDialog(dialog, total)
            if dialog.iscanceled():
                break
                        
            if aEntry[0]:
                Saison = str(aEntry[0])
                oOutputParameterHandler = cOutputParameterHandler()
                oOutputParameterHandler.addParameter('sMovieTitle', str(sMovieTitle))
                oOutputParameterHandler.addParameter('sThumbnail', str(sThumbnail))
                oGui.addText(SITE_IDENTIFIER, '[COLOR yellow]'+ Saison + '[/COLOR]')
            elif aEntry[2]:
				sTitle = '[COLOR cyan]'+str(aEntry[3]) + '* [/COLOR]' + str(aEntry[5])
				sUrl= str(aEntry[4])
				sDate= 'aired on '+ str(aEntry[6])
				oOutputParameterHandler = cOutputParameterHandler()
				oOutputParameterHandler.addParameter('siteUrl', sUrl)
				oOutputParameterHandler.addParameter('sMovieTitle', str(sTitle))
				oOutputParameterHandler.addParameter('sThumbnail', str(sThumbnail))
				oGui.addMovie(SITE_IDENTIFIER, 'showLink', sTitle, '', aEntry[2], sDate, oOutputParameterHandler)             
    
        cConfig().finishDialog(dialog)

    oGui.setEndOfDirectory()

def showLink():
    oGui = cGui()
   
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumbnail = oInputParameterHandler.getValue('sThumbnail')

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
	

    sPattern = 'href="([^<]+)" target="_blank">(.+?)</a>'

    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
    
    #fh = open('c:\\test.txt', "w")
    #fh.write(sHtmlContent.replace('\n',''))
    #fh.close()

    #print aResult
   
    if (aResult[0] == True):
        total = len(aResult[1])
        dialog = cConfig().createDialog(SITE_NAME)
        for aEntry in aResult[1]:
            cConfig().updateDialog(dialog, total)
            if dialog.iscanceled():
                break
 
            sTitle = aEntry[1].replace("&#8217;", "'") 
            siteUrl = URL_MAIN + aEntry[0]


 
            #print sUrl
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', siteUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sMovieTitle)
            oOutputParameterHandler.addParameter('sThumbnail', sThumbnail)

            

 
            oGui.addMovie(SITE_IDENTIFIER, 'showHosters', sTitle, '', sThumbnail, '', oOutputParameterHandler)
 
        cConfig().finishDialog(dialog)


    oGui.setEndOfDirectory()
	
def showEpisodes():
    oGui = cGui()
   
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumbnail = oInputParameterHandler.getValue('sThumbnail')

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
	

    sPattern = '<a href="([^<]+)">([^<]+)</a> ??? ?? ??? ???? ??????? ????? ???????.</center>'

    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
    
    #fh = open('c:\\test.txt', "w")
    #fh.write(sHtmlContent.replace('\n',''))
    #fh.close()

    #print aResult
   
    if (aResult[0] == True):
        total = len(aResult[1])
        dialog = cConfig().createDialog(SITE_NAME)
        for aEntry in aResult[1]:
            cConfig().updateDialog(dialog, total)
            if dialog.iscanceled():
                break
 
            sTitle = aEntry[1].replace("&#8217;", "'") 
            siteUrl = aEntry[0]


 
            #print sUrl
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', siteUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumbnail', sThumbnail)

            

 
            oGui.addMovie(SITE_IDENTIFIER, 'showEps', sTitle, '', sThumbnail, '', oOutputParameterHandler)
 
        cConfig().finishDialog(dialog)


    oGui.setEndOfDirectory()

def showEps():
    oGui = cGui()
   
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumbnail = oInputParameterHandler.getValue('sThumbnail')

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
	

    sPattern = '<div class="movie-wrap"><a href="(.+?)"><img width="435" height="623" src="(.+?)" class="attachment-movie size-movie wp-post-image" alt=""/>.+?<h1 style="bottom: 0">(.+?)</h1>'

    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
    
    #fh = open('c:\\test.txt', "w")
    #fh.write(sHtmlContent.replace('\n',''))
    #fh.close()

    #print aResult
   
    if (aResult[0] == True):
        total = len(aResult[1])
        dialog = cConfig().createDialog(SITE_NAME)
        for aEntry in aResult[1]:
            cConfig().updateDialog(dialog, total)
            if dialog.iscanceled():
                break
 
            sTitle = aEntry[2].replace("&#8217;", "'") 
            sThumbnail = aEntry[1]
            siteUrl = aEntry[0]
            sInfo = sTitle

 
            #print sUrl
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', siteUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumbnail', sThumbnail)

            

 
            oGui.addMovie(SITE_IDENTIFIER, 'showHosters', sTitle, '', sThumbnail, sInfo, oOutputParameterHandler)
 
        cConfig().finishDialog(dialog)
       
    oGui.setEndOfDirectory()
	
def showHosters():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumbnail = oInputParameterHandler.getValue('sThumbnail')
    
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request();
    #sHtmlContent = sHtmlContent.replace('<iframe src="//www.facebook.com/plugins/like.php','').replace('<iframe src="http://www.facebook.com/plugins/likebox.php','([^<]+)')
               
        
    sPattern = '<center><a href="([^<]+)" rel="nofollow"><img src="http://movs4u.com/d/d-([^<]+).png"></a></center>'
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)

	
    if (aResult[0] == True):
			total = len(aResult[1])
			dialog = cConfig().createDialog(SITE_NAME)
			for aEntry in aResult[1]:
				cConfig().updateDialog(dialog, total)
				if dialog.iscanceled():
					break
            
				url = str(aEntry[0])
				Squality = str(aEntry[1])
				sTitle = '[' + Squality + '] ' + sMovieTitle
				if url.startswith('//'):
					url = 'http:' + url
            
				sHosterUrl = url
				oHoster = cHosterGui().checkHoster(sHosterUrl)
				if (oHoster != False):
					sDisplayTitle = cUtil().DecoTitle(sTitle)
					oHoster.setDisplayName(sDisplayTitle)
					oHoster.setFileName(sTitle)
					cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumbnail)
				

			cConfig().finishDialog(dialog)
    
    else:
        
        #sPattern = '<li style.+?>(.+?)</li>|<li title=""><a href="([^<]+)">([^<]+)</a></li>'
        sPattern = '<center><a href="(.+?)" rel'
        
        aResult = oParser.parse(sHtmlContent, sPattern)
        if (aResult[0] == True):
			total = len(aResult[1])
			dialog = cConfig().createDialog(SITE_NAME)
			for aEntry in aResult[1]:
				cConfig().updateDialog(dialog, total)
				if dialog.iscanceled():
					break
            
				sHosterUrl = str(aEntry)
				oHoster = cHosterGui().checkHoster(sHosterUrl)
				if (oHoster != False):
					oHoster.setDisplayName(sMovieTitle)
					oHoster.setFileName(sMovieTitle)
					cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumbnail)         
    
			cConfig().finishDialog(dialog)


    oGui.setEndOfDirectory() 