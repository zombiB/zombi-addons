#-*- coding: utf-8 -*-
#zombi.
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

SITE_IDENTIFIER = 'filmey_tv'
SITE_NAME = '[COLOR violet]filmey.tv[/COLOR]'
SITE_DESC = 'arabic vod'

URL_MAIN = 'http://filmey.tv/'

MOVIE_AR = ('http://filmey.tv/%D8%A7%D9%81%D9%84%D8%A7%D9%85-%D8%B9%D8%B1%D8%A8%D9%8A-dep1.html', 'showMovies')
MOVIE_HI = ('http://filmey.tv/%D8%A7%D9%81%D9%84%D8%A7%D9%85-%D9%87%D9%86%D8%AF%D9%8A-dep16.html', 'showMovies')
MOVIE_TURK = ('http://filmey.tv/%D8%A7%D9%81%D9%84%D8%A7%D9%85-%D8%AA%D8%B1%D9%83%D9%8A-dep35.html', 'showMovies')
MOVIE_EN = ('http://filmey.tv/%D8%A7%D9%81%D9%84%D8%A7%D9%85-%D8%A7%D8%AC%D9%86%D8%A8%D9%8A-dep2.html', 'showMovies')
MOVIE_ANIME = ('http://filmey.tv/%D8%A7%D9%86%D9%85%D9%8A-dep30.html', 'showMovies')


SERIE_AR = ('http://filmey.tv/%D9%85%D8%B3%D9%84%D8%B3%D9%84%D8%A7%D8%AA-%D8%B9%D8%B1%D8%A8%D9%8A-dep22.html', 'showMovies')
SERIE_EN = ('http://filmey.tv/%D9%85%D8%B3%D9%84%D8%B3%D9%84%D8%A7%D8%AA-%D8%A7%D8%AC%D9%86%D8%A8%D9%8A-%D9%85%D8%AA%D8%B1%D8%AC%D9%85%D8%A9-dep23.html', 'showMovies')
SERIE_TR = ('http://filmey.tv/%D9%85%D8%B3%D9%84%D8%B3%D9%84%D8%A7%D8%AA-%D8%AA%D8%B1%D9%83%D9%8A%D8%A9-%D9%85%D8%AF%D8%A8%D9%84%D8%AC%D8%A9-dep24.html', 'showMovies')

SPORT_NEWS = ('http://filmey.tv/%D8%B1%D9%8A%D8%A7%D8%B6%D8%A9-dep13.html', 'showMovies')


URL_SEARCH = ('http://filmey.tv/-search.html', 'showMovies')
FUNCTION_SEARCH = 'showMovies'

def load():
    oGui = cGui()

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'http://venom/')
    oGui.addDir(SITE_IDENTIFIER, 'showSearch', 'Recherche', 'search.png', oOutputParameterHandler)
    
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_AR[0])
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'arabic', 'news.png', oOutputParameterHandler)
    
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_HI[0])
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'Films indiens', 'news.png', oOutputParameterHandler)
    
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_EN[0])
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'english', 'news.png', oOutputParameterHandler)
    
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_ANIME[0])
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'Films animation', 'news.png', oOutputParameterHandler)
    
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
    oOutputParameterHandler.addParameter('siteUrl', 'http://')
    oGui.addDir(SITE_IDENTIFIER, 'ReplayTV' ,'Replay TV', 'animesvf.png', oOutputParameterHandler)
            
    oGui.setEndOfDirectory()
  
def showSearch():
    oGui = cGui()
    sSearchText = oGui.showKeyBoard()
    if (sSearchText != False):
            sUrl = 'http://filmey.tv/'+sSearchText+'-search.html'  
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
    sHtmlContent = oRequestHandler.request();
    sHtmlContent = sHtmlContent.replace('&quot;', '"')
	#(.+?) ([^<]+)
    sPattern = "downloadaa.+?href='([^<]+)' itemprop=.+?>تحميل</a></div>.+?<a href='.+?'><img itemprop=.+?src='([^<]+)' alt=([^<]+) class=.+?itemprop=.+?><span>([^<]+)"
 
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
    if (aResult[0] == True):
        total = len(aResult[1])
        dialog = cConfig().createDialog(SITE_NAME)
        for aEntry in aResult[1]:
            cConfig().updateDialog(dialog, total)
            if dialog.iscanceled():
                break

            sUrl = URL_MAIN+str(aEntry[0])
            sTitle = str(aEntry[2]).replace('"','')

            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumbnail', str(aEntry[1]))

            oGui.addMovie(SITE_IDENTIFIER, 'showSeries', sTitle, '', aEntry[1], aEntry[3], oOutputParameterHandler)

        cConfig().finishDialog(dialog)
            
        sNextPage = __checkForNextPage(sHtmlContent)
        if (sNextPage != False):
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sNextPage)
            oGui.addDir(SITE_IDENTIFIER, 'showMovies', '[COLOR teal]Next >>>[/COLOR]', 'next.png', oOutputParameterHandler)

    if not sSearch:
        oGui.setEndOfDirectory()


def __checkForNextPage(sHtmlContent):
    sPattern = ""
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
    sPattern = "<a href='([^<]+)' class='redirect_link'>([^<]+)</a>"
    
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
    sPattern = 'face="Impact"><font size="6">(.+?)</font>'
    sPattern = sPattern + '|' + 'color="SlateGray">E<font color="Blue">(.+?)</font>'
    sPattern = sPattern + '|' + '<font color="Blue"><b><font face="Comic Sans MS">(.+?)<'
    sPattern = sPattern + '|' + 'Estream.+?rel="nofollow" href="(.+?)"'
    sPattern = sPattern + '|' + 'Uptobox.+?rel="nofollow" href="(.+?)"'
    sPattern = sPattern + '|' + 'Openload.co.+?rel="nofollow" href="(.+?)"'
    sPattern = sPattern + '|' + '1fichier.+?rel="nofollow" href="(.+?)"'
    sPattern = sPattern + '|' + 'Streamin.+?rel="nofollow" href="(.+?)"'
    sPattern = sPattern + '|' + 'Flashx.tv.+?rel="nofollow" href="(.+?)"'
    sPattern = sPattern + '|' + 'Turbobit.+?rel="nofollow" href="(.+?)"'
    sPattern = sPattern + '|' + 'Watchers.+?rel="nofollow" href="(.+?)"'
    sPattern = sPattern + '|' + 'vidzi.tv.+?rel="nofollow" href="(.+?)"'
    sPattern = sPattern + '|' + 'Vidto.me.+?rel="nofollow" href="(.+?)"'
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
                Saison = str(aEntry[0]).replace('<b>','').replace('</b>','').replace('<br>','').replace('<br/>','')
                oOutputParameterHandler = cOutputParameterHandler()
                oOutputParameterHandler.addParameter('sMovieTitle', str(sMovieTitle))
                oOutputParameterHandler.addParameter('sThumbnail', str(sThumbnail))
                oGui.addMisc(SITE_IDENTIFIER, 'showLinks', '[COLOR yellow]'+ Saison + '[/COLOR]', 'series.png', sThumbnail, '', oOutputParameterHandler)
            elif aEntry[1]:
                Saison = str(aEntry[1]).replace('<b>','').replace('</b>','').replace('<br>','').replace('<br/>','')
                oOutputParameterHandler = cOutputParameterHandler()
                oOutputParameterHandler.addParameter('sMovieTitle', str(sMovieTitle))
                oOutputParameterHandler.addParameter('sThumbnail', str(sThumbnail))
                oGui.addMisc(SITE_IDENTIFIER, 'showLinks', '[COLOR yellow]'+ Saison + '[/COLOR]', 'series.png', sThumbnail, '', oOutputParameterHandler)
            elif aEntry[2]:
                Saison = str(aEntry[2]).replace('<b>','').replace('</b>','').replace('<br>','').replace('<br/>','')
                oOutputParameterHandler = cOutputParameterHandler()
                oOutputParameterHandler.addParameter('sMovieTitle', str(sMovieTitle))
                oOutputParameterHandler.addParameter('sThumbnail', str(sThumbnail))
                oGui.addMisc(SITE_IDENTIFIER, 'showLinks', '[COLOR yellow]'+ Saison + '[/COLOR]', 'series.png', sThumbnail, '', oOutputParameterHandler)
            elif aEntry[3]:
                sTitle = 'Estream'
                sMovieTitle = sMovieTitle
                sUrl= str(aEntry[3])
                
                oOutputParameterHandler = cOutputParameterHandler()
                oOutputParameterHandler.addParameter('siteUrl', sUrl)
                oOutputParameterHandler.addParameter('sMovieTitle', sMovieTitle)
                oOutputParameterHandler.addParameter('sThumbnail', str(sThumbnail))
                oGui.addTV(SITE_IDENTIFIER, 'showHosters', sTitle, '', sUrl, '', oOutputParameterHandler)
            elif aEntry[4]:
                sTitle = 'uptobox'
                sMovieTitle = sMovieTitle.replace('480p & 720p & 1080p','') 
                sUrl= str(aEntry[4])
                
                oOutputParameterHandler = cOutputParameterHandler()
                oOutputParameterHandler.addParameter('siteUrl', sUrl)
                oOutputParameterHandler.addParameter('sMovieTitle', sMovieTitle)
                oOutputParameterHandler.addParameter('sThumbnail', str(sThumbnail))
                oGui.addTV(SITE_IDENTIFIER, 'showHosters', sTitle, '', sUrl, '', oOutputParameterHandler)
            elif aEntry[5]:
                sTitle = 'Openload.co'
                sMovieTitle = sMovieTitle.replace('480p & 720p & 1080p','') 
                sUrl= str(aEntry[5])
                
                oOutputParameterHandler = cOutputParameterHandler()
                oOutputParameterHandler.addParameter('siteUrl', sUrl)
                oOutputParameterHandler.addParameter('sMovieTitle', sMovieTitle)
                oOutputParameterHandler.addParameter('sThumbnail', str(sThumbnail))
                oGui.addTV(SITE_IDENTIFIER, 'showHosters', sTitle, '', aEntry[0], '', oOutputParameterHandler)
            elif aEntry[6]:
                sTitle = '1fichier'
                sMovieTitle = sMovieTitle.replace('480p & 720p & 1080p','') 
                sUrl= str(aEntry[6])
                
                oOutputParameterHandler = cOutputParameterHandler()
                oOutputParameterHandler.addParameter('siteUrl', sUrl)
                oOutputParameterHandler.addParameter('sMovieTitle', sMovieTitle)
                oOutputParameterHandler.addParameter('sThumbnail', str(sThumbnail))
                oGui.addTV(SITE_IDENTIFIER, 'showHosters', sTitle, '', aEntry[0], '', oOutputParameterHandler)
            elif aEntry[7]:
                sTitle = 'Streamin'
                sMovieTitle = sMovieTitle.replace('480p & 720p & 1080p','') 
                sUrl= str(aEntry[7])
                
                oOutputParameterHandler = cOutputParameterHandler()
                oOutputParameterHandler.addParameter('siteUrl', sUrl)
                oOutputParameterHandler.addParameter('sMovieTitle', sMovieTitle)
                oOutputParameterHandler.addParameter('sThumbnail', str(sThumbnail))
                oGui.addTV(SITE_IDENTIFIER, 'showHosters', sTitle, '', aEntry[0], '', oOutputParameterHandler)
            elif aEntry[8]:
                sTitle = 'flash'
                sMovieTitle = sMovieTitle.replace('480p & 720p & 1080p','') 
                sUrl= str(aEntry[8])
                
                oOutputParameterHandler = cOutputParameterHandler()
                oOutputParameterHandler.addParameter('siteUrl', sUrl)
                oOutputParameterHandler.addParameter('sMovieTitle', sMovieTitle)
                oOutputParameterHandler.addParameter('sThumbnail', str(sThumbnail))
                oGui.addTV(SITE_IDENTIFIER, 'showHosters', sTitle, '', sUrl, '', oOutputParameterHandler)
            elif aEntry[9]:
                sTitle = 'Turbobit'
                sMovieTitle = sMovieTitle.replace('480p & 720p & 1080p','') 
                sUrl= str(aEntry[9])
                
                oOutputParameterHandler = cOutputParameterHandler()
                oOutputParameterHandler.addParameter('siteUrl', sUrl)
                oOutputParameterHandler.addParameter('sMovieTitle', sMovieTitle)
                oOutputParameterHandler.addParameter('sThumbnail', str(sThumbnail))
                oGui.addTV(SITE_IDENTIFIER, 'showHosters', sTitle, '', aEntry[0], '', oOutputParameterHandler)
            elif aEntry[10]:
                sTitle = 'Watchers'
                sMovieTitle = sMovieTitle.replace('480p & 720p & 1080p','') 
                sUrl= str(aEntry[10])
                
                oOutputParameterHandler = cOutputParameterHandler()
                oOutputParameterHandler.addParameter('siteUrl', sUrl)
                oOutputParameterHandler.addParameter('sMovieTitle', sMovieTitle)
                oOutputParameterHandler.addParameter('sThumbnail', str(sThumbnail))
                oGui.addTV(SITE_IDENTIFIER, 'showHosters', sTitle, '', aEntry[0], '', oOutputParameterHandler)
            elif aEntry[11]:
                sTitle = 'vidzi.tv'
                sMovieTitle = sMovieTitle.replace('480p & 720p & 1080p','') 
                sUrl= str(aEntry[11])
                
                oOutputParameterHandler = cOutputParameterHandler()
                oOutputParameterHandler.addParameter('siteUrl', sUrl)
                oOutputParameterHandler.addParameter('sMovieTitle', sMovieTitle)
                oOutputParameterHandler.addParameter('sThumbnail', str(sThumbnail))
                oGui.addTV(SITE_IDENTIFIER, 'showHosters', sTitle, '', aEntry[0], '', oOutputParameterHandler)
            elif aEntry[12]:
                sTitle = 'Vidto.me'
                sMovieTitle = sMovieTitle.replace('480p & 720p & 1080p','') 
                sUrl= str(aEntry[12])
                
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
               
        
    sPattern = 'class="downloadlinkag" href="(.+?)">'
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
    
