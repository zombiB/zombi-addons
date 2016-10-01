#-*- coding: utf-8 -*-
#Venom.
#zombi.(@geekzombi)
from resources.lib.gui.hoster import cHosterGui
from resources.lib.handler.hosterHandler import cHosterHandler
from resources.lib.gui.gui import cGui
from resources.lib.gui.guiElement import cGuiElement
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.lib.config import cConfig
from resources.lib.util import cUtil
import re

SITE_IDENTIFIER = 'aflamhq_com'
SITE_NAME = '[COLOR violet]Aflamhq[/COLOR]'
SITE_DESC = 'arabic vod'

URL_MAIN = 'http://www.aflamhq.com'

MOVIE_AR = ('http://www.aflamhq.com/arabic-movies/', 'showMovies')
MOVIE_HI = ('http://www.aflamhq.com/indian-movies/', 'showMovies')
MOVIE_EN = ('http://www.aflamhq.com/english-movies/', 'showMovies')
MOVIE_ANIME = ('http://www.aflamhq.com/anime-movies/', 'showMovies')


SERIE_AR = ('http://www.aflamhq.com/arabic-series/', 'showMovies')
SERIE_EN = ('http://www.aflamhq.com/english-series/', 'showMovies')
SERIE_TR = ('http://www.aflamhq.com/turkish-series/', 'showMovies')
SERIE_GENRES = (True, 'showGenres')

SPORT_NEWS = ('http://www.aflamhq.com/sports/', 'showMovies')

DOC_NEWS = ('http://www.aflamhq.com/documentary-movies/', 'showMovies')

REPLAYTV_NEWS = ('http://www.aflamhq.com/tv-talk-show/', 'showMovies')
REPLAYTV_ISLAM = ('http://www.aflamhq.com/islamic/', 'showMovies')

URL_SEARCH = ('http://www.aflamhq.com/search', 'showMovies')
FUNCTION_SEARCH = 'showMovies'

def load():
    oGui = cGui()

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'http://venom/')
    oGui.addDir(SITE_IDENTIFIER, 'showSearch', 'Recherche', 'search.png', oOutputParameterHandler)
    
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_AR[0])
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'افلام عربي', 'news.png', oOutputParameterHandler)
    
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_HI[0])
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'Films indiens', 'news.png', oOutputParameterHandler)
    
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_EN[0])
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'افلام اجنبي', 'news.png', oOutputParameterHandler)
    
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_ANIME[0])
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'Films animation', 'news.png', oOutputParameterHandler)
    
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'http://venom')
    oGui.addDir(SITE_IDENTIFIER, 'showGenre', 'Films Genres', 'genres.png', oOutputParameterHandler)
    
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', SERIE_AR[0])
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'Series arabes', 'series.png', oOutputParameterHandler)
    
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', SERIE_EN[0])
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'Series anglais', 'series.png', oOutputParameterHandler)
    
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', SERIE_TR[0])
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'Series turques', 'series.png', oOutputParameterHandler)
    
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', SPORT_NEWS[0])
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'sport', 'animesvf.png', oOutputParameterHandler)
    
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', DOC_NEWS[0])
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'افلام وثائقية', 'animesvf.png', oOutputParameterHandler)
    
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', REPLAYTV_NEWS[0])
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'replay news', 'animesvostfr.png', oOutputParameterHandler)
    
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', REPLAYTV_ISLAM[0])
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'replay news', 'animesvostfr.png', oOutputParameterHandler)
    
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'http://')
    oGui.addDir(SITE_IDENTIFIER, 'ReplayTV' ,'Replay TV', 'animesvf.png', oOutputParameterHandler)
            
    oGui.setEndOfDirectory()
  
def showSearch():
    oGui = cGui()
    sSearchText = oGui.showKeyBoard()
    if (sSearchText != False):
            sUrl = 'http://www.aflamhq.com/search'+sSearchText  
            showMovies(sUrl)
            oGui.setEndOfDirectory()
            return  
			
def showGenreSeries(): 
    showGenre("aflamhq.com/ramadan-series/")   
    
def showGenres():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
 
    liste = []
    liste.append( ["ramadan series","http://www.aflamhq.com/ramadan-series/"] )

    
	            
    for sTitle,sUrl in liste:
        
        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', sUrl)
        oGui.addDir(SITE_IDENTIFIER, 'showMovies', sTitle, 'genres.png', oOutputParameterHandler)
       
    oGui.setEndOfDirectory() 


def showMovies(sSearch = ''):
    oGui = cGui()
    if sSearch:
      sUrl = sSearch
    else:
        oInputParameterHandler = cInputParameterHandler()
        sUrl = oInputParameterHandler.getValue('siteUrl')

   
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request();
    sHtmlContent = sHtmlContent.replace('&quot;', '"')
	#(.+?) ([^<]+)
    sPattern = 'title="([^<]+)" class="img-hover">.+?<img src="([^<]+)" alt="" />              <p>([^<]+)</p>.+?</a>.+?<div class="down-info">.+?<a href="([^<]+)"'
 
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
    if (aResult[0] == True):
        total = len(aResult[1])
        dialog = cConfig().createDialog(SITE_NAME)
        for aEntry in aResult[1]:
            cConfig().updateDialog(dialog, total)
            if dialog.iscanceled():
                break


            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', str(aEntry[3]))
            oOutputParameterHandler.addParameter('sMovieTitle', str(aEntry[0]))
            oOutputParameterHandler.addParameter('sThumbnail', str(aEntry[1]))

            oGui.addMisc(SITE_IDENTIFIER, 'showSeries', aEntry[0], '', aEntry[1], aEntry[2], oOutputParameterHandler)

        cConfig().finishDialog(dialog)
            
        sNextPage = __checkForNextPage(sHtmlContent)
        if (sNextPage != False):
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sNextPage)
            oGui.addDir(SITE_IDENTIFIER, 'showMovies', '[COLOR teal]Next >>>[/COLOR]', 'next.png', oOutputParameterHandler)

    if not sSearch:
        oGui.setEndOfDirectory()


def __checkForNextPage(sHtmlContent):
    sPattern = "<li><a href='([^<]+)' class='next'>التالي</a></li>      </ul>"
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
    if (aResult[0] == True):
        #print aResult[1][0]
        return aResult[1][0]

    return False
  
def showSeries():
    oGui = cGui()
   
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumbnail = oInputParameterHandler.getValue('sThumbnail')
 
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
    #(.+?)
    sPattern = '<a class="download" href="(.+?)">(.+?)</a>'
    
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
 
            #print sUrl
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', str(aEntry[0]))
            oOutputParameterHandler.addParameter('sMovieTitle', sMovieTitle)
            oOutputParameterHandler.addParameter('sThumbnail', sThumbnail)
            

 
            oGui.addMovie(SITE_IDENTIFIER, 'showLinks', sMovieTitle, '', sThumbnail, '', oOutputParameterHandler)
 
        cConfig().finishDialog(dialog)
       
    oGui.setEndOfDirectory()  
	
def showLinks():
    oGui = cGui()
   
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumbnail = oInputParameterHandler.getValue('sThumbnail')
 
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
   
    oParser = cParser()
    sPattern = 'color="Lime"><b><font size="7">(.+?)</font>'
    sPattern = sPattern + '|' + 'Youwatch.+?target="(.+?)">(.+?)</a>'
    sPattern = sPattern + '|' + 'Uptobox.+?target="(.+?)">(.+?)</a>'
    sPattern = sPattern + '|' + 'openload.+?target="(.+?)">(.+?)</a>'
    sPattern = sPattern + '|' + 'Vodlocker.+?target="(.+?)">(.+?)</a>'
    sPattern = sPattern + '|' + 'color="DarkOrange".+?target="(.+?)">(.+?)</a>'
    aResult = oParser.parse(sHtmlContent, sPattern)
   
    Saison = '0'
   
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
                oGui.addMisc(SITE_IDENTIFIER, 'showLinks', '[COLOR red]'+ aEntry[0] + '[/COLOR]', 'series.png', sThumbnail, aEntry[2], oOutputParameterHandler)
            elif aEntry[2]:
                sTitle = 'Youwatch'
                sMovieTitle = sMovieTitle.replace('480p & 720p & 1080p','') 
                sUrl= str(aEntry[2]).replace('<b>','').replace('</b>','')
                
                oOutputParameterHandler = cOutputParameterHandler()
                oOutputParameterHandler.addParameter('siteUrl', sUrl)
                oOutputParameterHandler.addParameter('sMovieTitle', sMovieTitle)
                oOutputParameterHandler.addParameter('sThumbnail', str(sThumbnail))
                oGui.addTV(SITE_IDENTIFIER, 'showHosters', sTitle, '', aEntry[0], '', oOutputParameterHandler)
            elif aEntry[4]:
                sTitle = 'Uptobox'
                sMovieTitle = sMovieTitle.replace('480p & 720p & 1080p','') 
                sUrl= str(aEntry[4]).replace('<b>','').replace('</b>','')
                
                oOutputParameterHandler = cOutputParameterHandler()
                oOutputParameterHandler.addParameter('siteUrl', sUrl)
                oOutputParameterHandler.addParameter('sMovieTitle', sMovieTitle)
                oOutputParameterHandler.addParameter('sThumbnail', str(sThumbnail))
                oGui.addTV(SITE_IDENTIFIER, 'showHosters', sTitle, '', aEntry[0], '', oOutputParameterHandler)
            elif aEntry[6]:
                sTitle = 'openload'
                sMovieTitle = sMovieTitle.replace('480p & 720p & 1080p','') 
                sUrl= str(aEntry[6]).replace('<b>','').replace('</b>','')
                
                oOutputParameterHandler = cOutputParameterHandler()
                oOutputParameterHandler.addParameter('siteUrl', sUrl)
                oOutputParameterHandler.addParameter('sMovieTitle', sMovieTitle)
                oOutputParameterHandler.addParameter('sThumbnail', str(sThumbnail))
                oGui.addTV(SITE_IDENTIFIER, 'showHosters', sTitle, '', aEntry[0], '', oOutputParameterHandler)
            elif aEntry[8]:
                sTitle = 'Vodlocker'
                sMovieTitle = sMovieTitle.replace('480p & 720p & 1080p','') 
                sUrl= str(aEntry[8]).replace('<b>','').replace('</b>','')
                
                oOutputParameterHandler = cOutputParameterHandler()
                oOutputParameterHandler.addParameter('siteUrl', sUrl)
                oOutputParameterHandler.addParameter('sMovieTitle', sMovieTitle)
                oOutputParameterHandler.addParameter('sThumbnail', str(sThumbnail))
                oGui.addTV(SITE_IDENTIFIER, 'showHosters', sTitle, '', aEntry[0], '', oOutputParameterHandler)
            else:
                sTitle = 'online'
                sMovieTitle = sMovieTitle.replace('480p & 720p & 1080p','') 
                sUrl= str(aEntry[10]).replace('<b>','').replace('</b>','')
                
                oOutputParameterHandler = cOutputParameterHandler()
                oOutputParameterHandler.addParameter('siteUrl', sUrl)
                oOutputParameterHandler.addParameter('sMovieTitle', sMovieTitle)
                oOutputParameterHandler.addParameter('sThumbnail', str(sThumbnail))
                oGui.addTV(SITE_IDENTIFIER, 'showHosters', sTitle, '', aEntry[0], '', oOutputParameterHandler)
    #(.+?)
    
 
        cConfig().finishDialog(dialog)
       
    oGui.setEndOfDirectory()
	
#<a target="_blank" href="(.+?)"
def showHosters():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumbnail = oInputParameterHandler.getValue('sThumbnail')
    
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request();
    #sHtmlContent = sHtmlContent.replace('<iframe src="//www.facebook.com/plugins/like.php','').replace('<iframe src="http://www.facebook.com/plugins/likebox.php','')
               
        
    sPattern = '<a target="_blank" href="(.+?)"'
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
	
    if (aResult[0] == True):
        total = len(aResult[1])
        dialog = cConfig().createDialog(SITE_NAME)
        for aEntry in aResult[1]:
            cConfig().updateDialog(dialog, total)
            if dialog.iscanceled():
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
				

        cConfig().finishDialog(dialog) 
                
    oGui.setEndOfDirectory()
    
