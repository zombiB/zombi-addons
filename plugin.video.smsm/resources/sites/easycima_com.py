#-*- coding: utf-8 -*-
#Venom.
#Mod By Zombi.(@geekzombi)

#Cloudflare protection
#https://raw.githubusercontent.com/daniel-lundin/dreamfilm-xbmc/master/cloudflare.py
#https://gist.github.com/Rainbowed/8917670

from resources.lib.gui.hoster import cHosterGui
from resources.lib.handler.hosterHandler import cHosterHandler
from resources.lib.gui.gui import cGui
from resources.lib.gui.guiElement import cGuiElement
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.lib.util import cUtil
from resources.lib.config import cConfig
import re, urllib, urllib2

SITE_IDENTIFIER = 'easycima_com'
SITE_NAME = 'easycima.com'
SITE_DESC = 'vod'

URL_MAIN = 'http://www.easycima.com/'


MOVIE_ANIME = ('http://www.easycima.com/dep/dp/4/', 'showMovies')
MOVIE_HI = ('http://www.easycima.com/dep/dp/3/', 'showMovies')
MOVIE_EN = ('http://www.easycima.com/dep/dp/1/', 'showMovies')
MOVIE_GENRES = (True, 'showGenre')


URL_SEARCH = ('', 'showMovies')
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
        sUrl = URL_SEARCH[0] + sSearchText
        showMovies(sUrl)
        oGui.setEndOfDirectory()
        return  

def showMovies(sSearch = ''):
    oGui = cGui()
    if sSearch:
      sUrl = sSearch
      #correction
      sUrl = sUrl.replace(URL_SEARCH[0],'')
      sUrl = URL_SEARCH[0] + urllib.quote(sUrl)

    else:
        oInputParameterHandler = cInputParameterHandler()
        sUrl = oInputParameterHandler.getValue('siteUrl')
   
    #print sUrl
     
    #oRequestHandler = cRequestHandler(sUrl)
    #sHtmlContent = oRequestHandler.request()

    headers = {'User-Agent' : 'Mozilla 5.10'}
    request = urllib2.Request(sUrl,None,headers)
      
    try: 
        reponse = urllib2.urlopen(request)
    except urllib2.HTTPError, e:
        print e.read()
        print e.reason
      
    sHtmlContent = reponse.read()
    reponse.close()
    
    #fh = open('c:\\test.txt', "w")
    ##fh.write(sHtmlContent)
    #fh.close()
    
    sPattern = '<div class="col-md-3 file_index">.+?<a rel="(.+?)".+?href="(.+?)">.+?<div class="coufi">.+?<div class="imgcounter">.+?<img alt=".+?" src="(.+?)" class="imgres"'
    
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
    
    if (aResult[0] == False):
        oGui.addNone(SITE_IDENTIFIER)

    if (aResult[0] == True):
        total = len(aResult[1])
        dialog = cConfig().createDialog(SITE_NAME)
        for aEntry in aResult[1]:
            cConfig().updateDialog(dialog, total)
            if dialog.iscanceled():
                break
            
            #sTitle = aEntry[2]+' - [COLOR azure]'+aEntry[3]+'[/COLOR]'
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', str(aEntry[1]))
            oOutputParameterHandler.addParameter('sMovieTitle', str(aEntry[0]))
            oOutputParameterHandler.addParameter('sThumbnail', str(aEntry[2]))
			
            oGui.addTV(SITE_IDENTIFIER, 'showSeries', cUtil().DecoTitle(aEntry[0]),'', aEntry[2], '', oOutputParameterHandler)         
    
        cConfig().finishDialog(dialog)

        sNextPage = __checkForNextPage(sHtmlContent)
        if (sNextPage != False):
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sNextPage)
            oGui.addDir(SITE_IDENTIFIER, 'showMovies', '[COLOR teal]Next >>>[/COLOR]', 'next.png', oOutputParameterHandler)

    if not sSearch:
        oGui.setEndOfDirectory()

def showSeries():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumbnail = oInputParameterHandler.getValue('sThumbnail')

        
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
    #sHtmlContent = sHtmlContent.replace('<strong>Téléchargement VOSTFR','').replace('<strong>Téléchargement VF','').replace('<strong>Téléchargement','')
 
    #fh = open('c:\\test.txt', "w")
    #fh.write(sHtmlContent)
    #fh.close()
 
    sPattern = ' <div class="col-md-3"><a href="(.+?)".+?target="_blank" ><div class="btn btn-xs btn-success">.+?</div></a>.+?</div><div class="col-md-3">(.+?)</div></div>'
	
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
    
    #print aResult
    
    if (aResult[0] == True):
        total = len(aResult[1])
        dialog = cConfig().createDialog(SITE_NAME)
        for aEntry in aResult[1]:
            cConfig().updateDialog(dialog, total)
            if dialog.iscanceled():
                break

            sTitle = sMovieTitle+' - '+aEntry[1]
			
            sTitle = cUtil().DecoTitle(sTitle)
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', str(aEntry[0]))
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumbnail', str(sThumbnail))
            oGui.addTV(SITE_IDENTIFIER, 'showHosters', sTitle, '', sThumbnail, '', oOutputParameterHandler)            
    
        cConfig().finishDialog(dialog)

    oGui.setEndOfDirectory()


def __checkForNextPage(sHtmlContent):
    sPattern = '<div class="row"><div class="pagination"><ul><li class="active"><a href="#">.+?</a></li><li><a href="(.+?)"'
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
    if (aResult[0] == True):
        return aResult[1][0]

    return False
    
  
def showLinks():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumbnail = oInputParameterHandler.getValue('sThumbnail')

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
    
    sHtmlContent = sHtmlContent.replace('facebook','<>')
    
    #fh = open('c:\\test.txt', "w")
    #fh.write(sHtmlContent)
    #fh.close()
    
    #Recuperation des liens
    sPattern = '<iframe src="(http[^]+?)" [^<>]+?><\/iframe>'
    oParser = cParser()
    #aResult = oParser.parse(sHtmlContent, sPattern)
    aResult = oParser.parse(sHtmlContent, sPattern)
    
    #print aResult    
    
    if (aResult[0] == True):
        total = len(aResult[1])
        dialog = cConfig().createDialog(SITE_NAME)
        for aEntry in aResult[1]:
            cConfig().updateDialog(dialog, total)
            if dialog.iscanceled():
                break
            
            sHoster = cHosterGui().checkHoster(aEntry[1].lower())
            if (sHoster != False):
                sTitle = sMovieTitle + aEntry[1]
                oOutputParameterHandler = cOutputParameterHandler()
                oOutputParameterHandler.addParameter('siteUrl', str(aEntry[0]))
                oOutputParameterHandler.addParameter('sMovieTitle', str(sMovieTitle))
                oOutputParameterHandler.addParameter('sThumbnail', str(sThumbnail))
                oGui.addMovie(SITE_IDENTIFIER, 'showHosters', sTitle, '', sThumbnail, comm, oOutputParameterHandler)             
    
        cConfig().finishDialog(dialog)

    oGui.setEndOfDirectory()  
#
def showHosters():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumbnail = oInputParameterHandler.getValue('sThumbnail')
    
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request();
    #sHtmlContent = sHtmlContent.replace('<iframe src="//www.facebook.com/plugins/like.php','').replace('<iframe src="http://www.facebook.com/plugins/likebox.php','')
               
        
    sPattern = 'class="col-lg-4"><a href="(.+?)"'
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
