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
 
SITE_IDENTIFIER = 'hdarab'
SITE_NAME = 'hd-arab'
SITE_DESC = 'arabic vod'
 
URL_MAIN = 'http://hd-arab.com/'
URL_TVMAIN = 'http://hd-arab.com/tvshows/'
URL_MOVIEMAIN = 'http://hd-arab.com/movies/'

MOVIE_EN = ('http://hd-arab.com/movies/', 'showMovies')
SERIE_NEWS = ('http://hd-arab.com', 'showNews')
SERIE_EN = ('http://hd-arab.com/tvshows/', 'showTvshows')


URL_SEARCH = ('http://www.anyanime.com/?s=', 'showMovies')
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
        sUrl = 'http://www.anyanime.com/?s='+sSearchText
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
 

    #sPattern = 'src="([^<]+)" class=".+?href="([^<]+)">([^<]+)</.+?<div class="movieDesc">([^<]+)</div>'


    sPattern = '<article class="movie-details">.+?<a href="([^<]+)" class="movie-poster ajax_loader">.+?<img data-src="([^<]+)" src=".+?<h2 class="movie-title">([^<]+)</h2>.+?<div class="movie-year">([^<]+)</div>'

    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
	
	
    if (aResult[0] == True):
        total = len(aResult[1])
        dialog = cConfig().createDialog(SITE_NAME)
        for aEntry in aResult[1]:
            cConfig().updateDialog(dialog, total)
            if dialog.iscanceled():
                break
 

            siteUrl = aEntry[0]
            sThumbnail = aEntry[1]
            sInfo = aEntry[3]


            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl',siteUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', str(aEntry[2]))
            oOutputParameterHandler.addParameter('sThumbnail', sThumbnail)
			

            
            if '/tvshows' in siteUrl:
                oGui.addMovie(SITE_IDENTIFIER, 'showSeriesLinks', aEntry[2], '', sThumbnail, sInfo, oOutputParameterHandler) 
            else:
			    oGui.addMovie(SITE_IDENTIFIER, 'showMoviesLinks', aEntry[2], '', sThumbnail, sInfo, oOutputParameterHandler)
        
        cConfig().finishDialog(dialog)
 
        sNextmoviePage = __checkForNextmoviePage(sHtmlContent)
        if (sNextmoviePage != False):
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sNextmoviePage)
            oGui.addDir(SITE_IDENTIFIER, 'showMovies', '[COLOR teal]Next >>>[/COLOR]', 'next.png', oOutputParameterHandler)
 
    if not sSearch:
        oGui.setEndOfDirectory()
		
def showNews(sSearch = ''):
    oGui = cGui()
    if sSearch:
      sUrl = sSearch
    else:
        oInputParameterHandler = cInputParameterHandler()
        sUrl = oInputParameterHandler.getValue('siteUrl')
 
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
 

    #sPattern = 'src="([^<]+)" class=".+?href="([^<]+)">([^<]+)</.+?<div class="movieDesc">([^<]+)</div>'


    sPattern = '<article class="movie-details">.+?<a href="([^<]+)" class="movie-poster ajax_loader">.+?<img data-src="([^<]+)" src=".+?<h2 class="movie-title">([^<]+)</h2>.+?<div class="movie-year">([^<]+)</div>'

    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
	
	
    if (aResult[0] == True):
        total = len(aResult[1])
        dialog = cConfig().createDialog(SITE_NAME)
        for aEntry in aResult[1]:
            cConfig().updateDialog(dialog, total)
            if dialog.iscanceled():
                break
 

            siteUrl = aEntry[0]
            sThumbnail = aEntry[1]
            sInfo = aEntry[3]


            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl',siteUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', str(aEntry[2]))
            oOutputParameterHandler.addParameter('sThumbnail', sThumbnail)
			

            
            if '/tvshows' in siteUrl:
                oGui.addMovie(SITE_IDENTIFIER, 'showSeriesLinks', aEntry[2], '', sThumbnail, sInfo, oOutputParameterHandler) 
            else:
			    oGui.addMovie(SITE_IDENTIFIER, 'showMoviesLinks', aEntry[2], '', sThumbnail, sInfo, oOutputParameterHandler)
        
        cConfig().finishDialog(dialog)
 
        sNextPage = __checkForNextPage(sHtmlContent)
        if (sNextPage != False):
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sNextPage)
            oGui.addDir(SITE_IDENTIFIER, 'showNews', '[COLOR teal]Next >>>[/COLOR]', 'next.png', oOutputParameterHandler)
 
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
 

    #sPattern = 'src="([^<]+)" class=".+?href="([^<]+)">([^<]+)</.+?<div class="movieDesc">([^<]+)</div>'


    sPattern = '<article class="movie-details">.+?<a href="([^<]+)" class="movie-poster ajax_loader">.+?<img data-src="([^<]+)" src=".+?<h2 class="movie-title">([^<]+)</h2>.+?<div class="movie-year">([^<]+)</div>'

    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
	
	
    if (aResult[0] == True):
        total = len(aResult[1])
        dialog = cConfig().createDialog(SITE_NAME)
        for aEntry in aResult[1]:
            cConfig().updateDialog(dialog, total)
            if dialog.iscanceled():
                break
 

            siteUrl = aEntry[0]
            sThumbnail = aEntry[1]
            sInfo = aEntry[3]


            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl',siteUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', str(aEntry[2]))
            oOutputParameterHandler.addParameter('sThumbnail', sThumbnail)
			

            
            if '/tvshows' in siteUrl:
                oGui.addMovie(SITE_IDENTIFIER, 'showSeriesLinks', aEntry[2], '', sThumbnail, sInfo, oOutputParameterHandler) 
            else:
			    oGui.addMovie(SITE_IDENTIFIER, 'showMoviesLinks', aEntry[2], '', sThumbnail, sInfo, oOutputParameterHandler)
        
        cConfig().finishDialog(dialog)
 
        sNexttvPage = __checkForNexttvPage(sHtmlContent)
        if (sNexttvPage != False):
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sNexttvPage)
            oGui.addDir(SITE_IDENTIFIER, 'showMovies', '[COLOR teal]Next >>>[/COLOR]', 'next.png', oOutputParameterHandler)
 
    if not sSearch:
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
    sQua = ''

    sPattern = '<meta itemprop="ratingCount" content=".+?">(.+?)<small>.+?</small>.+?<p itemprop="description">(.+?)</p>.+?class="item-value item-hot">(.+?)</span>'
    aResult = oParser.parse(sHtmlContent, sPattern)
    
    if (aResult[0]):
        sNote = aResult[1][0][0]
        sCom = aResult[1][0][1]
        sQua = aResult[1][0][2]
        sCom = cUtil().removeHtmlTags(sCom)
    if (sNote):
        oGui.addText(SITE_IDENTIFIER,str(sNote)+'  :تقييم الفيلم')
    if (sQua):
        oGui.addText(SITE_IDENTIFIER,str(sQua)+' :الجودة')

    
    
    #Affichage du menu  
    oGui.addText(SITE_IDENTIFIER,'[COLOR olive]_______________[/COLOR]')

    sPattern = '<iframe class="youtube_trailers" src="(.+?)" frameborder="0" allowfullscreen></iframe>'
    aResult = oParser.parse(sHtmlContent, sPattern)
    if (aResult[0] == True):
        total = len(aResult[1])
        dialog = cConfig().createDialog(SITE_NAME)
        for aEntry in aResult[1]:
            cConfig().updateDialog(dialog, total)
            if dialog.iscanceled():
                break

            if aEntry:
                 sHosterUrl = str(aEntry)
                 sMovieTitle2 = 'trailer'
                 oHoster = cHosterGui().checkHoster(sHosterUrl)
                 if (oHoster != False):
                     oHoster.setDisplayName(sMovieTitle2)
                     oHoster.setFileName(sMovieTitle2)
                     cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumbnail)

    
    
    #Affichage du menu  
    oGui.addText(SITE_IDENTIFIER,'[COLOR olive]_______________[/COLOR]')



    #data-src="([^<]+)"data-src="" data-load="no"
    sPattern = 'data-src="([^<]+)" data-load="no"'
    aResult = oParser.parse(sHtmlContent, sPattern)
    
    if (aResult[0] == True):
        total = len(aResult[1])
        dialog = cConfig().createDialog(SITE_NAME)
        for aEntry in aResult[1]:
            cConfig().updateDialog(dialog, total)
            if dialog.iscanceled():
                break

            sTitle = 'شاهد من هنا'
            sUrl= aEntry
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', str(sMovieTitle))
            oOutputParameterHandler.addParameter('sThumbnail', str(sThumbnail))
            oGui.addMovie(SITE_IDENTIFIER, 'showHosters', sTitle, '', sThumbnail, sCom, oOutputParameterHandler)             
    
        cConfig().finishDialog(dialog)

    oGui.setEndOfDirectory()
		
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



    #data-src="([^<]+)"
    sPattern = '<div class="season_episode">.+?<a href=".+?" data-toggle="collapse" class="season_group_btn">.+?<span>.+?</span>(.+?)</a>'
    sPattern = sPattern + '|' + '<a href="([^<]+)">[^<]+<span class="episode_name"><span>([^<]+)</span>([^<]+)</span>[^<]+<span class="episode_air_d">([^<]+)</span>'
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
            elif aEntry[1]:
				sTitle = str(aEntry[2])+str(aEntry[3])
				sUrl= str(aEntry[1])
				sDate= 'aired on '+str(aEntry[4])
				oOutputParameterHandler = cOutputParameterHandler()
				oOutputParameterHandler.addParameter('siteUrl', sUrl)
				oOutputParameterHandler.addParameter('sMovieTitle', str(sMovieTitle))
				oOutputParameterHandler.addParameter('sThumbnail', str(sThumbnail))
				oGui.addMovie(SITE_IDENTIFIER, 'showMoviesLinks', sTitle, '', sThumbnail, sDate, oOutputParameterHandler)             
    
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
 
    sPattern = 'data-src="([^<]+)" data-load="no"'

    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
	
	
    if (aResult[0] == True):
        total = len(aResult[1])
        dialog = cConfig().createDialog(SITE_NAME)
        for aEntry in aResult[1]:
            cConfig().updateDialog(dialog, total)
            if dialog.iscanceled():
                break
 
            sTitle = sMovieTitle
            siteUrl = aEntry
			


            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl',siteUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumbnail', sThumbnail)
            oGui.addMisc(SITE_IDENTIFIER, 'showHosters', sTitle, '', sThumbnail, siteUrl, oOutputParameterHandler)
        
        cConfig().finishDialog(dialog)
       
    oGui.setEndOfDirectory()
	

def __checkForNextPage(sHtmlContent):
    sPattern = '<a href="([^<]+)" rel="next">'
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
    if (aResult[0] == True):
        aResult = URL_MAIN+aResult[1][0]
        return aResult

    return False	

def __checkForNexttvPage(sHtmlContent):
    sPattern = '<a href="([^<]+)" rel="next">'
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
    if (aResult[0] == True):
        aResult = URL_TVMAIN+aResult[1][0]
        return aResult

    return False	

def __checkForNextmoviePage(sHtmlContent):
    sPattern = '<a href="([^<]+)" rel="next">'
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
    if (aResult[0] == True):
        aResult = URL_MOVIEMAIN+aResult[1][0]
        return aResult

    return False


def showHosters():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumbnail = oInputParameterHandler.getValue('sThumbnail')
    
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request();
    #sHtmlContent = sHtmlContent.replace('<iframe src="//www.facebook.com/plugins/like.php','').replace('<iframe src="http://www.facebook.com/plugins/likebox.php','([^<]+)')
               
        
    sPattern = 'key([^<]+)label'
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
	
    if (aResult[0] == True):
        total = len(aResult[1])
        dialog = cConfig().createDialog(SITE_NAME)
        for aEntry in aResult[1]:
            cConfig().updateDialog(dialog, total)
            if dialog.iscanceled():
                break
            
            url = 'https://docs.google.com/file/d/'+str(aEntry)+'/preview?pli=1#t=1'
            url = url.replace('|','')
            if url.startswith('//'):
                url = 'http:' + url
            
            sHosterUrl = url
            oHoster = cHosterGui().checkHoster(sHosterUrl)
            if (oHoster != False):
                oHoster.setDisplayName(sMovieTitle)
                oHoster.setFileName(sMovieTitle)
                cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumbnail)
				

        cConfig().finishDialog(dialog) 
                
    oGui.setEndOfDirectory()