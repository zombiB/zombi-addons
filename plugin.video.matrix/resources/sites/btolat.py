# -*- coding: utf-8 -*-
# zombi https://github.com/zombiB/zombi-addons/

import re
import requests	

from resources.lib.gui.hoster import cHosterGui
from resources.lib.gui.gui import cGui
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.lib.comaddon import siteManager, VSlog, addon
ADDON = addon()
icons = ADDON.getSetting('defaultIcons')

SITE_IDENTIFIER = 'btolat'
SITE_NAME = 'Btolat'
SITE_DESC = 'sport vod'

URL_MAIN = siteManager().getUrlMain(SITE_IDENTIFIER)
SPORT_FOOT = (URL_MAIN + 'video', 'showMovies')
MOVIE_PACK = (URL_MAIN , 'showPack')
SPORT_SPORTS = ('http://', 'load')

def load():
    oGui = cGui() 

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', SPORT_FOOT[0])
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'أهداف و ملخصات ',  icons + '/Sport.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', MOVIE_PACK[0])
    oGui.addDir(SITE_IDENTIFIER, 'showPack', 'فيديوهات الموقع',  icons + '/Sport.png', oOutputParameterHandler)

    oGui.setEndOfDirectory() 

def showPack():
    oGui = cGui()
    
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
 
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    oParser = cParser()
     # (.+?) ([^<]+) .+?
    sStart = '/video">فيديوهات</a>'
    sEnd = 'matches">مباريات</a></li>'
    sHtmlContent = oParser.abParse(sHtmlContent, sStart, sEnd)
    sPattern = 'href="([^<]+)">([^<]+)</a>'

    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
		
    if aResult[0]:
        oOutputParameterHandler = cOutputParameterHandler()
        for aEntry in aResult[1]:
            if '#' in aEntry[0]:
                continue 
            sTitle = aEntry[1]
            siteUrl = aEntry[0].split('"')[0]
            if siteUrl.startswith('/'):
                siteUrl = URL_MAIN + aEntry[0].split('"')[0]

            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl',siteUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
			
            oGui.addMisc(SITE_IDENTIFIER, 'showPackMovies', sTitle, 'sport.png', '', '', oOutputParameterHandler)
 
        sNextPage = __checkForNextPage(sHtmlContent)
        if sNextPage:
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sNextPage)
            oGui.addDir(SITE_IDENTIFIER, 'showPack', '[COLOR teal]Next >>>[/COLOR]', 'next.png', oOutputParameterHandler)
 
    oGui.setEndOfDirectory()

def showPackMovies(sSearch = ''):
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    nVIdeo = oInputParameterHandler.getValue('nVIdeo')

    oParser = cParser()  
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
	 # .+? ([^<]+) 

    if nVIdeo:
        s = requests.Session() 
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:65.0) Gecko/20100101 Firefox/65.0' }
        data = {'VideoID':nVIdeo}
        r = s.post(URL_MAIN+'video/LoadMore/'+nVIdeo,data=data,headers=headers)
        sHtmlContent = r.content.decode('utf8').replace('\\','').replace('u003c','<').replace('u003e','>').replace('rn','')

    sPattern = '<div class="categoryNewsCard.+?<a href=["\']([^"\']+)["\'].+?data-original="([^"]+)" alt="([^"]+)'
    aResult = oParser.parse(sHtmlContent, sPattern)
    if aResult[0]:
        oOutputParameterHandler = cOutputParameterHandler()  
        for aEntry in aResult[1]:
            sUrl = aEntry[0].replace("'","")
            sUrl = URL_MAIN+sUrl
            sTitle = aEntry[2]
            sDesc = ""
            sThumb = aEntry[1]
            oOutputParameterHandler.addParameter('siteUrl', sUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oGui.addMisc(SITE_IDENTIFIER, 'showHosters', sTitle, 'doc.png', sThumb, sDesc, oOutputParameterHandler)

        sNextPage = __checkForNextPage(sHtmlContent)
        if sNextPage:
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sNextPage)
            if 'LoadMore/' in sNextPage:
                oOutputParameterHandler.addParameter('nVIdeo', sNextPage.split('LoadMore/')[1].replace('&cat=0',''))
            oGui.addDir(SITE_IDENTIFIER, 'showPackMovies', '[COLOR teal]Next >>>[/COLOR]', 'next.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()

def showMovies(sSearch = ''):
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')

    nVIdeo = oInputParameterHandler.getValue('nVIdeo')

    oParser = cParser()  
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
	 # .+? ([^<]+) 

    if nVIdeo:
        s = requests.Session() 
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:65.0) Gecko/20100101 Firefox/65.0' }
        data = {'VideoID':nVIdeo}
        r = s.post(URL_MAIN+'api/video/LoadMore/'+nVIdeo,data=data,headers=headers)
        sHtmlContent = r.content.decode('utf8').replace('\\','').replace('u003c','<').replace('u003e','>').replace('rn','').replace('u0027','"')

    sPattern = '<div class="categoryNewsCard.+?<a href=["\']([^"\']+)["\'].+?data-original="([^"]+)" alt="([^"]+)'
    aResult = oParser.parse(sHtmlContent, sPattern)
    if aResult[0]:
        oOutputParameterHandler = cOutputParameterHandler()  
        for aEntry in aResult[1]:
            sUrl = aEntry[0].replace("'","")
            sUrl = URL_MAIN+sUrl
            VSlog(sUrl)
            sTitle = aEntry[2]
            sDesc = ""
            sThumb = aEntry[1]
            oOutputParameterHandler.addParameter('siteUrl', sUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oGui.addMisc(SITE_IDENTIFIER, 'showHosters', sTitle, 'doc.png', sThumb, sDesc, oOutputParameterHandler)

        sNextPage = __checkForNextPage(sHtmlContent)
        if sNextPage:
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sNextPage)
            if 'LoadMore/' in sNextPage:
                oOutputParameterHandler.addParameter('nVIdeo', sNextPage.split('LoadMore/')[1].replace('&cat=0',''))
            oGui.addDir(SITE_IDENTIFIER, 'showMovies', '[COLOR teal]Next >>>[/COLOR]', 'next.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()

def __checkForNextPage(sHtmlContent):
    oParser = cParser()
    sPattern = 'data-val=["\']([^"\']+)["\']'
    aResult = oParser.parse(sHtmlContent, sPattern)
    if aResult[0]:
        for aEntry in reversed(aResult[1]):
            nPage = int(aEntry)
            nPage = f'{URL_MAIN}video/LoadMore/{nPage}&cat=0'
            return nPage

    sPattern = 'class="next-page"><a href=["\']([^"\']+)["\']'
    aResult = oParser.parse(sHtmlContent, sPattern)  
    if aResult[0]:
        nPage = aResult[1][0]
        return nPage

    return False

def showHosters():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')
    
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
    oParser = cParser()
    sPattern =  '["\']true["\'] src=["\']([^"\']+)["\']'
    aResult = oParser.parse(sHtmlContent,sPattern)
    if aResult[0]:
        m3url = aResult[1][0] 
        oRequest = cRequestHandler(m3url)
        sHtmlContent2 = oRequest.request() 
    
    sPattern = ',src:{hls:["\']([^"\']+)["\']}' 
    aResult = oParser.parse(sHtmlContent2, sPattern)
    if aResult[0]:
        for aEntry in aResult[1]:

            url = aEntry
            if url.startswith('//'):
                url = 'http:' + url
            oRequest = cRequestHandler(url)
            sHtmlContent3 = oRequest.request()           
            sPattern = 'RESOLUTION=(\d+x\d{0,3})(.+?.m3u8)'
            oParser = cParser()
            aResult = oParser.parse(sHtmlContent3, sPattern)
            if aResult[0]:
                for aEntry in aResult[1]:

                    url2 = url.split('0.m3u8')[0]+ aEntry[1]
                    url2 = url2.replace(' ','') 
                    qua = aEntry[1].split('.m3u8')[0]

                    sHosterUrl = url2
                    sTitle = ('%s  [COLOR coral](%s)[/COLOR]') % (sMovieTitle, qua)
                    oHoster = cHosterGui().checkHoster(sHosterUrl)
                    sDisplayTitle = sTitle
                    if oHoster:
                        oHoster.setDisplayName(sDisplayTitle)
                        oHoster.setFileName(sMovieTitle)
                        cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb)

    sPattern = 'source:["\']([^"\']+)["\']'
    aResult = oParser.parse(sHtmlContent2, sPattern)
    if aResult[0]:
        for aEntry in aResult[1]:
            url = aEntry
            if url.startswith('//'):
                url = 'http:' + url
            oRequest = cRequestHandler(url)
            sHtmlContent3 = oRequest.request()           
            sPattern = 'RESOLUTION=(\d+x\d{0,3})(.+?.m3u8)'
            aResult = oParser.parse(sHtmlContent3, sPattern)
            if aResult[0]:
                for aEntry in aResult[1]:
                    url2 = url.split('0.m3u8')[0]+ aEntry[1]
                    url2 = url2.replace(' ','') 
                    qua = aEntry[1].split('.m3u8')[0]
                    sHosterUrl = url2
                    sTitle = ('%s  [COLOR coral](%s)[/COLOR]') % (sMovieTitle, qua)
                    oHoster = cHosterGui().checkHoster(sHosterUrl)
                    sDisplayTitle = sTitle
                    if oHoster:
                        oHoster.setDisplayName(sDisplayTitle)
                        oHoster.setFileName(sMovieTitle)
                        cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb)
                
    sPattern = '<h1>(.+?)</h1>'
    aResult = oParser.parse(sHtmlContent2, sPattern)
    if aResult[0]:
        for aEntry in aResult[1]:
            sDesc = aEntry
            oGui.addText(SITE_IDENTIFIER, f'[COLOR orange] {sDesc} [/COLOR]')
    
    oGui.setEndOfDirectory()    