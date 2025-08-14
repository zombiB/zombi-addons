# -*- coding: utf-8 -*-

import base64
from resources.lib.gui.hoster import cHosterGui
from resources.lib.gui.gui import cGui
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.comaddon import progress, VSlog, siteManager, addon
from resources.lib.parser import cParser
 
SITE_IDENTIFIER = 'tvfun'
SITE_NAME = 'Tvfun'
SITE_DESC = 'arabic vod'
 
URL_MAIN = siteManager().getUrlMain(SITE_IDENTIFIER)

RAMADAN_SERIES = (f'{URL_MAIN}ts/mosalsalat-ramadan-2025/', 'showSeries')
SERIE_TR = (f'{URL_MAIN}cat/mosalsalat-torkia/', 'showSeries')
SERIE_DUBBED = (f'{URL_MAIN}ts/mosalsalat-modablaja/', 'showSeries')
SERIE_HEND = (f'{URL_MAIN}cat/mosalsalat-hindia/', 'showSeries')
SERIE_AR = (f'{URL_MAIN}cat/mosalsalat-3arabia/', 'showSeries')
SERIE_ASIA = (f'{URL_MAIN}cat/mosalsalat-korea/', 'showSeries')
SERIE_LATIN = (f'{URL_MAIN}cat/mosalsalat-latinia/', 'showSeries')
REPLAYTV_NEWS = (f'{URL_MAIN}cat/programme-tv/', 'showSeries')

URL_SEARCH = (f'{URL_MAIN}q/', 'showSeries')
FUNCTION_SEARCH = 'showSeries'
 
def load():
    oGui = cGui()
    addons = addon()

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'http://venom/')
    oGui.addDir(SITE_IDENTIFIER, 'showSearch', addons.VSlang(30079), '1/Search.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', SERIE_AR[0])
    oGui.addDir(SITE_IDENTIFIER, 'showSeries', 'مسلسلات عربية', '1/Arabic.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', SERIE_ASIA[0])
    oGui.addDir(SITE_IDENTIFIER, 'showSeries', 'مسلسلات أسيوية', '1/Asian.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', SERIE_TR[0])
    oGui.addDir(SITE_IDENTIFIER, 'showSeries', 'مسلسلات تركية', '1/Turkish.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', SERIE_HEND[0])
    oGui.addDir(SITE_IDENTIFIER, 'showSeries', 'مسلسلات هندية', '1/Hindi.png', oOutputParameterHandler)  

    oOutputParameterHandler.addParameter('siteUrl', SERIE_LATIN [0])
    oGui.addDir(SITE_IDENTIFIER, 'showSeries', 'مسلسلات لاتنية', 'latin.png', oOutputParameterHandler)
    
    oOutputParameterHandler.addParameter('siteUrl', SERIE_DUBBED [0])
    oGui.addDir(SITE_IDENTIFIER, 'showSeries', 'مسلسلات مدبلجة', '1/Dubbed.png', oOutputParameterHandler)
    
    oOutputParameterHandler.addParameter('siteUrl', RAMADAN_SERIES[0])
    oGui.addDir(SITE_IDENTIFIER, 'showSeries', 'مسلسلات رمضان', '1/Ramadan.png', oOutputParameterHandler)
    
    oOutputParameterHandler.addParameter('siteUrl', f'{URL_MAIN}/ts/mosalsalat-motarjama/')
    oGui.addDir(SITE_IDENTIFIER, 'showSeries', 'مسلسلات مترجمة', '1/TVShows.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', f'{URL_MAIN}/ts/zee-alwan/')
    oGui.addDir(SITE_IDENTIFIER, 'showSeries', 'زي الوان', '1/TVShows.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', REPLAYTV_NEWS[0])
    oGui.addDir(SITE_IDENTIFIER, 'showSeries', 'برامج تلفزيونية', '1/Programs.png', oOutputParameterHandler)
    
    oGui.setEndOfDirectory()
 
def showSearch():
    oGui = cGui()
 
    sSearchText = oGui.showKeyBoard()
    if sSearchText:
        sUrl = f'{URL_MAIN}q/{sSearchText}/'
        showSeries(sUrl)
        oGui.setEndOfDirectory()
        return
  
def showSeries(sSearch = ''):
    oGui = cGui()
    if sSearch:
      sUrl = sSearch
    else:
        oInputParameterHandler = cInputParameterHandler()
        sUrl = oInputParameterHandler.getValue('siteUrl')

    oParser = cParser() 
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    sPattern = '<div class="thumb.+?href="([^"]+)".+?src="([^"]+)" alt="([^"]+)'
    aResult = oParser.parse(sHtmlContent, sPattern)	
    if aResult[0]:
        total = len(aResult[1])
        progress_ = progress().VScreate(SITE_NAME)
        for aEntry in aResult[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break
            
            sTitle = aEntry[2]
            sTitle = sTitle.replace("مشاهدة وتحميل","").replace("اون لاين","").replace("مترجمة","").replace("مترجم","").replace("مسلسل","").replace("حلقات","")
            if 'الحلقة' in sTitle:
                sTitle = sTitle.split('الحلقة')[0]
            siteUrl = aEntry[0]
            if siteUrl.startswith('//'):
                siteUrl =f'http:{siteUrl}'
            if siteUrl.startswith('/'):
                siteUrl = f'{URL_MAIN}{siteUrl}'

            sThumb = aEntry[1]
            sDesc = ''
            sYear = ''

            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', siteUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oOutputParameterHandler.addParameter('sYear', sYear)
            oOutputParameterHandler.addParameter('sDesc', sDesc)
			
            oGui.addTV(SITE_IDENTIFIER, 'showEpisodes', sTitle, '', sThumb, sDesc, oOutputParameterHandler)

        progress_.VSclose(progress_)

    sPattern = '<ul class="pagination">(.+?)<div id="footer">'  
    aResult = oParser.parse(sHtmlContent, sPattern) 
    if aResult[0]:
        sHtmlContent = aResult[1][0]

    if not sSearch:
        sPattern = '<li><a href="([^<]+)">([^<]+)</a></li>'
        aResult = oParser.parse(sHtmlContent, sPattern)
        if aResult[0]:
            for aEntry in aResult[1]:
                if 'موقع' in aEntry[1] or 'تيفي فان' in aEntry[1]:
                    continue

                sTitle = f'[COLOR red]Page: {aEntry[1]}[/COLOR]'
                siteUrl = aEntry[0]
                if siteUrl.startswith('/'):
                    siteUrl = f'{URL_MAIN}{siteUrl}'
                if siteUrl.startswith('//'):
                    siteUrl = f'http:{siteUrl}'

                oOutputParameterHandler = cOutputParameterHandler()
                oOutputParameterHandler.addParameter('siteUrl',siteUrl)
			
                oGui.addDir(SITE_IDENTIFIER, 'showSeries', sTitle, 'next.png', oOutputParameterHandler)
 
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

    sPattern = '<div class="headline">(.+?)<div id='  
    aResult = oParser.parse(sHtmlContent, sPattern) 
    if aResult[0]:
        sHtmlContent2 = aResult[1][0]

    sPattern = '<div class="thumb.+?href="([^"]+)".+?src="([^"]+)" alt="([^"]+)'
    aResult = oParser.parse(sHtmlContent2, sPattern)
    if aResult[0]:
        total = len(aResult[1])
        progress_ = progress().VScreate(SITE_NAME)
        for aEntry in aResult[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break
 
            sTitle = f'{sMovieTitle} E{aEntry[2].split("الحلقة ")[1]}'
            siteUrl = aEntry[0].replace('video/','watch/')
            if siteUrl.startswith('//'):
                siteUrl = f'http:{siteUrl}'
            if siteUrl.startswith('/'):
                siteUrl = f'{URL_MAIN}{siteUrl}'

            sThumb = aEntry[1]
			
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', siteUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oGui.addEpisode(SITE_IDENTIFIER, 'showHosters', sTitle, '', sThumb, '', oOutputParameterHandler)

        progress_.VSclose(progress_)

    sPattern = 'class="videocontainer">\s*<iframe src="([^<]+)" id="([^<]+)"'
    aResult = oParser.parse(sHtmlContent, sPattern)
    if aResult[0]:
        total = len(aResult[1])
        progress_ = progress().VScreate(SITE_NAME)
        for aEntry in aResult[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break
 
            sTitle = "playlist"
            siteUrl = 'https:'+aEntry[0]
            if siteUrl.startswith('//'):
                siteUrl = 'http:' + siteUrl
            if URL_MAIN not in siteUrl:
                siteUrl = f'{URL_MAIN}{siteUrl}'
            sThumb = sThumb
            sDesc = ""
			
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', siteUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oGui.addEpisode(SITE_IDENTIFIER, 'showHosters', sTitle, '', sThumb, sDesc, oOutputParameterHandler)

        progress_.VSclose(progress_)

    sPattern = '<ul class="pagination">(.+?)div id="footer">'  
    aResult = oParser.parse(sHtmlContent, sPattern) 
    if aResult[0]:
        sHtmlContent3 = aResult[1][0]

        sPattern = '<li><a href="([^<]+)">([^<]+)</a></li>'
        aResult = oParser.parse(sHtmlContent3, sPattern)
        if aResult[0]:
            total = len(aResult[1])
            progress_ = progress().VScreate(SITE_NAME)
            for aEntry in aResult[1]:
                progress_.VSupdate(progress_, total)
                if progress_.iscanceled():
                    break
                if 'موقع' in aEntry[1]:
                    continue

                sTitle = f'[COLOR red]Page: {aEntry[1]}[/COLOR]'
                siteUrl = aEntry[0]
                if siteUrl.startswith('/'):
                    siteUrl = f'{URL_MAIN}{siteUrl}'
                if siteUrl.startswith('//'):
                    siteUrl = f'http:{siteUrl}'

                oOutputParameterHandler = cOutputParameterHandler()
                oOutputParameterHandler.addParameter('siteUrl',siteUrl)
			
                oGui.addDir(SITE_IDENTIFIER, 'showEpisodes', sTitle, 'next.png', oOutputParameterHandler)
        
        progress_.VSclose(progress_)
  
    oGui.setEndOfDirectory()

def showHosters():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')

    oParser = cParser()    
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    sPattern =  'onclick="setVideo(.+?);'
    aResult = oParser.parse(sHtmlContent,sPattern)
    if aResult[0]:
        for aEntry in aResult[1]:
            m3url = aEntry.replace("('","").replace("')","")
            m3url = m3url[2:]

            sHtmlContent2 = base64.b64decode(m3url).decode('ascii',errors='ignore')
   
            sPattern = 'src="(.+?)".+?allowfullscreen'
            aResult = oParser.parse(sHtmlContent2, sPattern)
            if aResult[0]:
               for aEntry in aResult[1]:
        
                   url = aEntry.replace("https://dai.ly/","https://www.dailymotion.com/video/")
                   if url.startswith('//'):
                       url = f'http:{url}'
            
                   sHosterUrl = url 
                   oHoster = cHosterGui().checkHoster(sHosterUrl)
                   if oHoster:
                       oHoster.setDisplayName(sMovieTitle)
                       oHoster.setFileName(sMovieTitle)
                       cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb)
                
    oGui.setEndOfDirectory()