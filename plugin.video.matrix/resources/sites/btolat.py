# -*- coding: utf-8 -*-

from resources.lib.gui.hoster import cHosterGui
from resources.lib.gui.gui import cGui
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.lib.comaddon import progress, siteManager, VSlog
from resources.lib import random_ua

UA = random_ua.get_ua()

SITE_IDENTIFIER = 'btolat'
SITE_NAME = 'Btolat'
SITE_DESC = 'sport vod'

URL_MAIN = siteManager().getUrlMain(SITE_IDENTIFIER)
SPORT_FOOT = (f'{URL_MAIN}video', 'showMovies')
SPORT_SPORTS = ('http://', 'load')

def load():
    oGui = cGui() 

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', SPORT_FOOT[0])
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'أهداف و ملخصات ', 'sport.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', URL_MAIN)
    oGui.addDir(SITE_IDENTIFIER, 'showPack', 'فيديوهات الموقع', 'films.png', oOutputParameterHandler)

    oGui.setEndOfDirectory() 

def showPack():
    oGui = cGui()
    
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')

    oParser = cParser() 
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    sStart = '/video">فيديوهات</a>'
    sEnd = 'matches">مباريات</a></li>'
    sHtmlContent = oParser.abParse(sHtmlContent, sStart, sEnd)

    sPattern = 'href="([^<]+)">([^<]+)</a>'
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

def showPackMovies():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    nVIdeo = oInputParameterHandler.getValue('nVIdeo')

    oParser = cParser()   
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    if nVIdeo:
        oRequestHandler = cRequestHandler(f'{URL_MAIN}video/LoadMore/{nVIdeo}')
        oRequestHandler.addHeaderEntry('User-Agent', UA)
        oRequestHandler.addParameters('VideoID', nVIdeo)
        oRequestHandler.setRequestType(1)
        sHtmlContent = oRequestHandler.request().replace('\\','').replace('u003c','<').replace('u003e','>').replace('rn','').replace('u0027','"')

    sPattern = '<div class="categoryNewsCard.+?<a href=["\']([^"\']+)["\'].+?data-original="([^"]+)" alt="([^"]+)'
    aResult = oParser.parse(sHtmlContent, sPattern)
    if aResult[0]:
        total = len(aResult[1])
        progress_ = progress().VScreate(SITE_NAME)
        oOutputParameterHandler = cOutputParameterHandler()  
        for aEntry in aResult[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break
            sUrl = aEntry[0].replace("'","")
            sUrl = f'{URL_MAIN}{sUrl}'
            sTitle = aEntry[2]
            sDesc = ""
            sThumb = aEntry[1]
            oOutputParameterHandler.addParameter('siteUrl', sUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oGui.addMisc(SITE_IDENTIFIER, 'showHosters', sTitle, '1/Documentary.png', sThumb, sDesc, oOutputParameterHandler)

        progress_.VSclose(progress_)

        sNextPage = __checkForNextPage(sHtmlContent)
        if sNextPage:
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sNextPage)
            if 'LoadMore/' in sNextPage:
                oOutputParameterHandler.addParameter('nVIdeo', sNextPage.split('LoadMore/')[1].replace('&cat=0',''))
            oGui.addDir(SITE_IDENTIFIER, 'showPackMovies', '[COLOR teal]Next >>>[/COLOR]', 'next.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()

def showMovies():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    nVIdeo = oInputParameterHandler.getValue('nVIdeo')

    oParser = cParser()    
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    if nVIdeo:
        oRequestHandler = cRequestHandler(f'{URL_MAIN}api/video/LoadMore/{nVIdeo}')
        oRequestHandler.addHeaderEntry('User-Agent', UA)
        oRequestHandler.addParameters('VideoID', nVIdeo)
        oRequestHandler.setRequestType(1)
        sHtmlContent = oRequestHandler.request().replace('\\','').replace('u003c','<').replace('u003e','>').replace('rn','').replace('u0027','"')

    sPattern = '<div class="categoryNewsCard.+?<a href=["\']([^"\']+)["\'].+?data-original="([^"]+)" alt="([^"]+)'
    aResult = oParser.parse(sHtmlContent, sPattern)
    if aResult[0]:
        total = len(aResult[1])
        progress_ = progress().VScreate(SITE_NAME)
        oOutputParameterHandler = cOutputParameterHandler()  
        for aEntry in aResult[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break
            sUrl = aEntry[0].replace("'","")
            sUrl = f'{URL_MAIN}{sUrl}'
            sTitle = aEntry[2]
            sDesc = ""
            sThumb = aEntry[1]
            oOutputParameterHandler.addParameter('siteUrl', sUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oGui.addMisc(SITE_IDENTIFIER, 'showHosters', sTitle, '1/Documentary.png', sThumb, sDesc, oOutputParameterHandler)

        progress_.VSclose(progress_)

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

    oParser = cParser()    
    oRequestHandler = cRequestHandler(sUrl)
    oRequestHandler.enableCache(False)
    sHtmlContent = oRequestHandler.request()

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
                    url = f'http:{url}'

                oRequest = cRequestHandler(url)
                oRequest.addHeaderEntry('Referer', m3url)
                sHtmlContent3 = oRequest.request()
            
                sPattern = 'RESOLUTION=(\d+x\d{0,3})(.+?.m3u8)'
                aResult = oParser.parse(sHtmlContent3, sPattern)
                if aResult[0]:
                    for aEntry in aResult[1]:

                        url2 = url.split('0.m3u8')[0]+ aEntry[1]
                        url2 = url2.replace(' ','') 
                        qua = aEntry[1].split('.m3u8')[0]

                        sHosterUrl = f'{url2}|Referer={m3url}'
                        sTitle = f'{sMovieTitle} [COLOR coral]({qua})[/COLOR]'
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
                        sTitle = f'{sMovieTitle} [COLOR coral]({qua})[/COLOR]'
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

    sPattern = '<iframe.+?src="([^"]+)" title='
    aResult = oParser.parse(sHtmlContent, sPattern)
    if aResult[0]:
        for aEntry in aResult[1]:
            url = aEntry

            sHosterUrl = url
            oHoster = cHosterGui().checkHoster(sHosterUrl)
            if oHoster:
                oHoster.setDisplayName(sMovieTitle)
                oHoster.setFileName(sMovieTitle)
                cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb)
               
    oGui.setEndOfDirectory()    