# -*- coding: utf-8 -*-

import re
from resources.lib.gui.hoster import cHosterGui
from resources.lib.gui.gui import cGui
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.comaddon import progress, VSlog, siteManager, addon
from resources.lib.parser import cParser
from resources.lib.util import cUtil
 
SITE_IDENTIFIER = 'asiaarabs'
SITE_NAME = 'Asia4arabs'
SITE_DESC = 'arabic vod'
 
URL_MAIN = siteManager().getUrlMain(SITE_IDENTIFIER)

MOVIE_ASIAN = (f'{URL_MAIN}search/label/%D8%A3%D9%81%D9%84%D8%A7%D9%85', 'showMovies')
SERIE_ASIA = (f'{URL_MAIN}search/label/%D9%85%D8%B3%D9%84%D8%B3%D9%84%D8%A7%D8%AA', 'showSeries')

URL_SEARCH = (f'{URL_MAIN}search?q=', 'showMovies')
URL_SEARCH_SERIES = (f'{URL_MAIN}search?q=', 'showSeries')
URL_SEARCH_MOVIES = (f'{URL_MAIN}search?q=', 'showMovies')
FUNCTION_SEARCH = 'showMovies'
 
def load():
    oGui = cGui()
    addons = addon()

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'http://venom/')
    oGui.addDir(SITE_IDENTIFIER, 'showSearch', addons.VSlang(30078), '1/Search.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', 'http://venom/')
    oGui.addDir(SITE_IDENTIFIER, 'showSearchSeries', addons.VSlang(30079), '1/Search.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', MOVIE_ASIAN[0])
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'أفلام', '1/Asian.png', oOutputParameterHandler)
	
    oOutputParameterHandler.addParameter('siteUrl', SERIE_ASIA[0])
    oGui.addDir(SITE_IDENTIFIER, 'showSeries', 'مسلسلات', '1/Asian.png', oOutputParameterHandler)
    
    oGui.setEndOfDirectory()
 
def showSearch():
    oGui = cGui()
 
    sSearchText = oGui.showKeyBoard()
    if sSearchText:
        sUrl = f'{URL_MAIN}search?q={sSearchText}'
        showMovies(sUrl)
        oGui.setEndOfDirectory()
        return
 
def showSearchSeries():
    oGui = cGui()
 
    sSearchText = oGui.showKeyBoard()
    if sSearchText:
        sUrl = f'{URL_MAIN}search?q={sSearchText}'
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
    
    oParser = cParser() 
    sUrl = sUrl.replace("+","%2B")
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
 
    sPattern = "<a class='Img-Holder thumb' href='([^<]+)' title='([^<]+)'>.+?class='post-thumb' data-src='([^<]+)' height=.+?<div class='Short_content'>(.+?)</div>"
    aResult = oParser.parse(sHtmlContent, sPattern)
    if aResult[0]:
        total = len(aResult[1])
        progress_ = progress().VScreate(SITE_NAME)
        oOutputParameterHandler = cOutputParameterHandler() 
        for aEntry in aResult[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break
            if "مترجم" not in aEntry[1]:
                continue
            if "مسلسل" in aEntry[1]:
                continue
 
            sTitle = cUtil().CleanMovieName(aEntry[1])
            siteUrl = aEntry[0]
            sThumb = aEntry[2]
            sDesc = cUtil().unescape(aEntry[3])
            sYear = ''
            m = re.search('([0-9]{4})', sTitle)
            if m:
                sYear = str(m.group(0))

            oOutputParameterHandler.addParameter('siteUrl',siteUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oOutputParameterHandler.addParameter('sYear', sYear) 
			
            oGui.addMovie(SITE_IDENTIFIER, 'showHosters', sTitle, '', sThumb, sDesc, oOutputParameterHandler)

        progress_.VSclose(progress_)

        sNextPage = __checkForNextPage(sHtmlContent)
        if sNextPage:
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

    oParser = cParser() 
    sUrl = sUrl.replace("+","%2B")
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
 
    sPattern = "<a class='Img-Holder thumb' href='([^<]+)' title='([^<]+)'>.+?class='post-thumb' data-src='([^<]+)' height=.+?<div class='Short_content'>(.+?)</div>"
    aResult = oParser.parse(sHtmlContent, sPattern)
    if aResult[0]:
        total = len(aResult[1])
        progress_ = progress().VScreate(SITE_NAME)
        oOutputParameterHandler = cOutputParameterHandler() 
        for aEntry in aResult[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break
            if "مترجم" not in aEntry[1]:
                continue
            if "فيلم" in aEntry[1]:
                continue
 
            sTitle = cUtil().CleanSeriesName(aEntry[1])
            siteUrl = aEntry[0]
            sThumb = aEntry[2]
            sDesc = cUtil().unescape(aEntry[3])

            oOutputParameterHandler.addParameter('siteUrl',siteUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
			
            oGui.addTV(SITE_IDENTIFIER, 'showEpisodes', sTitle, '', sThumb, sDesc, oOutputParameterHandler)

        progress_.VSclose(progress_)

        sNextPage = __checkForNextPage(sHtmlContent)
        if sNextPage:
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
    sThumb = oInputParameterHandler.getValue('sThumb')

    oParser = cParser() 
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
 
    sPattern =  '<a href="(https://asia4arabs-fs.+?)"'
    aResult = oParser.parse(sHtmlContent,sPattern)
    if aResult[0]:
        m3url =  aResult[1][0]
        oRequest = cRequestHandler(m3url)
        sHtmlContent = oRequest.request()

    sPattern =  '<a href="(https://www.asia4arabs.co.+?)" target'
    aResult = oParser.parse(sHtmlContent,sPattern)
    if aResult[0]:
        m3url =  aResult[1][0]
        oRequest = cRequestHandler(m3url)
        sHtmlContent = oRequest.request()

    sPattern = '<a class="button" href="([^<]+)" id=".+?">(.+?)</a>'
    aResult = oParser.parse(sHtmlContent, sPattern)
    if aResult[0]:
        for aEntry in aResult[1]:

            url = aEntry[1]
            sTitle = f'{aEntry[0]} {sMovieTitle}'
            if url.startswith('//'):
               url = f'http:{url}'

            sHosterUrl = url
            if "youtube" in sHosterUrl:
                continue
            oHoster = cHosterGui().checkHoster(sHosterUrl)
            if oHoster:
               oHoster.setDisplayName(sTitle)
               oHoster.setFileName(sTitle)
               cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb)

    sPattern = 'iframes([^<]+)=.+?width="100%" height="400" src="(.+?)" frameborder='
    aResult = oParser.parse(sHtmlContent, sPattern)
    if aResult[0]:
        for aEntry in aResult[1]:
            
            url = aEntry[1]
            sTitle = f'E{aEntry[0].replace(" ","").replace("]","").replace("[","").replace(" = {};","").replace(" iframes","").replace("iframes","").replace("={};","")}'
            if url.startswith('//'):
               url = f'http:{url}'
            
            sHosterUrl = url
            if "youtube" in sHosterUrl or "google" in sHosterUrl or "LINK0" in sHosterUrl:
                continue
            if 'userload' in sHosterUrl:
                sHosterUrl = f'{sHosterUrl}|Referer={URL_MAIN}'

            oHoster = cHosterGui().checkHoster(sHosterUrl)
            if oHoster:
               sTitle = f'{sTitle}{sMovieTitle}'
               oHoster.setDisplayName(sTitle)
               oHoster.setFileName(sTitle)
               cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb)

    sPattern = '<a href="([^<]+)" target="_blank">(.+?)</a>'
    aResult = oParser.parse(sHtmlContent, sPattern)
    if aResult[0]:
        for aEntry in aResult[1]:
            
            url = aEntry[0]
            sTitle = aEntry[1].replace("الحلقة "," E")
            if url.startswith('//'):
               url = f'http:{url}'
            
            sHosterUrl = url
            if "youtube" in sHosterUrl or "google" in sHosterUrl or "LINK0" in sHosterUrl:
                continue
            if 'userload' in sHosterUrl:
                sHosterUrl = f'{sHosterUrl}|Referer={URL_MAIN}'

            oHoster = cHosterGui().checkHoster(sHosterUrl)
            if oHoster:
               sTitle = f'{sTitle}{sMovieTitle}'
               oHoster.setDisplayName(sTitle)
               oHoster.setFileName(sTitle)
               cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb)

    sPattern = '<td><a href=["\']([^"\']+)["\']\s*target="iframe_a">(.+?)</a>'
    aResult = oParser.parse(sHtmlContent, sPattern)	
    if aResult[0]:
        for aEntry in aResult[1]:
            
            url = aEntry[0]
            sTitle = aEntry[1].replace("Episode "," E").replace("Episod "," E")
            if url.startswith('//'):
               url = 'http:' + url
            
            sHosterUrl = url
            if "youtube" in sHosterUrl or "google" in sHosterUrl or "LINK0" in sHosterUrl:
                continue
            if 'userload' in sHosterUrl:
                sHosterUrl = f'{sHosterUrl}|Referer={URL_MAIN}'

            oHoster = cHosterGui().checkHoster(sHosterUrl)
            if oHoster:
               sTitle = f'{sTitle}{sMovieTitle}'
               oHoster.setDisplayName(sTitle)
               oHoster.setFileName(sTitle)
               cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb)

    sPattern = '>الحلقة([^<]+)</span></span></h4><iframe allowfullscreen.+?src="(.+?)" width'
    aResult = oParser.parse(sHtmlContent, sPattern)
    if aResult[0]:
        for aEntry in aResult[1]:
            
            url = aEntry[1]
            sTitle = f'E{aEntry[0].replace(" ","").replace("]","").replace("[","").replace(" = {};","").replace(" iframes","").replace("iframes","").replace("={};","")} {sMovieTitle}'
            if url.startswith('//'):
               url = 'http:' + url
            
            sHosterUrl = url
            if "youtube" in sHosterUrl or "google" in sHosterUrl or "LINK0" in sHosterUrl:
                continue
            if 'userload' in sHosterUrl:
                sHosterUrl = f'{sHosterUrl}|Referer={URL_MAIN}'

            oHoster = cHosterGui().checkHoster(sHosterUrl)
            if oHoster:
               oHoster.setDisplayName(sTitle)
               oHoster.setFileName(sTitle)
               cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb)
       
    oGui.setEndOfDirectory()

def __checkForNextPage(sHtmlContent):
    oParser = cParser()
    sPattern = "<div class='loadMore'>(.+?) title='NextUrl'></a>"
    aResult = oParser.parse(sHtmlContent, sPattern)
    if aResult[0] :
        return aResult[1][0].split("href='")[1].replace("'","")

    return False

def showHosters():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')

    oParser = cParser() 
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
      
    sPattern = '<iframe.+?src="([^"]+)'
    aResult = oParser.parse(sHtmlContent, sPattern)
    if aResult[0]:
        for aEntry in aResult[1]:
            
            url = str(aEntry)
            sTitle = " " 
            if url.startswith('//'):
               url = 'http:' + url
            
            sHosterUrl = url
            if "youtube" in sHosterUrl:
                sTitle = "-trailer"
             
            if "blogger" in sHosterUrl or ".jpg" in sHosterUrl or ".jpeg" in sHosterUrl or "google" in sHosterUrl:
                continue
            if 'userload' in sHosterUrl:
                sHosterUrl = f'{sHosterUrl}|Referer={URL_MAIN}'
                
            oHoster = cHosterGui().checkHoster(sHosterUrl)
            if oHoster:
               sDisplayTitle = f'{sMovieTitle} {sTitle}'
               oHoster.setDisplayName(sDisplayTitle)
               oHoster.setFileName(sMovieTitle)
               cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb)
               
    sStart = '>روابط التحميل</span>'
    sEnd = '</div>'
    sHtmlContent = oParser.abParse(sHtmlContent, sStart, sEnd)

    sPattern = '<a href="([^<]+)" target="'
    aResult = oParser.parse(sHtmlContent, sPattern)	
    if aResult[0]:
        for aEntry in aResult[1]:
            
            url = str(aEntry)
            sTitle = " " 
            if url.startswith('//'):
               url = 'http:' + url
            
            sHosterUrl = url
            if "youtube" in sHosterUrl:
                sTitle = "-trailer"
             
            if "blogger" in sHosterUrl or ".jpg" in sHosterUrl or ".jpeg" in sHosterUrl or "google" in sHosterUrl:
                continue
            if 'userload' in sHosterUrl:
                sHosterUrl = f'{sHosterUrl}|Referer={URL_MAIN}'
                
            oHoster = cHosterGui().checkHoster(sHosterUrl)
            if oHoster:
               sDisplayTitle = f'{sMovieTitle} {sTitle}'
               oHoster.setDisplayName(sDisplayTitle)
               oHoster.setFileName(sMovieTitle)
               cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb)
                
    oGui.setEndOfDirectory()