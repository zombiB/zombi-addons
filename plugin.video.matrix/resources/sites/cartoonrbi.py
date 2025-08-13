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
from resources.lib import random_ua

UA = random_ua.get_ua()

SITE_IDENTIFIER = 'cartoonrbi'
SITE_NAME = 'ArabToons'
SITE_DESC = 'arabic vod'
 
URL_MAIN = siteManager().getUrlMain(SITE_IDENTIFIER)
 
KID_MOVIES = (f'{URL_MAIN}movies.php', 'showMovies')
KID_CARTOON = (f'{URL_MAIN}cartoon.php', 'showSeries')
 
URL_SEARCH_ANIMS = (f'{URL_MAIN}livesearch.php?q=', 'showSeries')
FUNCTION_SEARCH = 'showSeries'

def load():
    oGui = cGui()
    addons = addon()

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'http://venom/')
    oGui.addDir(SITE_IDENTIFIER, 'showSearch', addons.VSlang(30079), '1/Search.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', KID_MOVIES[0])
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'أفلام كرتون', '1/1/Anime.png', oOutputParameterHandler)
    
    oOutputParameterHandler.addParameter('siteUrl', KID_CARTOON[0])
    oGui.addDir(SITE_IDENTIFIER, 'showSeries', 'مسلسلات كرتون', 'crtoon.png', oOutputParameterHandler)    

    oOutputParameterHandler.addParameter('siteUrl', KID_CARTOON[0])
    oGui.addDir(SITE_IDENTIFIER, 'showPack', 'جميع الكرتون', 'listes.png', oOutputParameterHandler)            
    oGui.setEndOfDirectory()

def showSearch():
    oGui = cGui()

    sSearchText = oGui.showKeyBoard()    
    if sSearchText is not False:
        sUrl = f'{URL_MAIN}livesearch.php?q={sSearchText}'
        showSeries(sUrl)
        oGui.setEndOfDirectory()
        return

def showPack():
    oGui = cGui()
    
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')

    oParser = cParser() 
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    sStart = '<nav aria-label="navigation" class='
    sEnd = '</ul>'
    sHtmlContent = oParser.abParse(sHtmlContent, sStart, sEnd)
    sPattern = r'<a href=\'([^\']+)\'>(.+?)</a>'

    aResult = oParser.parse(sHtmlContent, sPattern)	
    if aResult[0]:
        oOutputParameterHandler = cOutputParameterHandler()
        for aEntry in aResult[1]:
            if '#' in aEntry[0]:
                continue 
            sTitle = aEntry[1]
            siteUrl = f'{URL_MAIN}{aEntry[0]}'

            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl',siteUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)			

            oGui.addTV(SITE_IDENTIFIER, 'showSeries', sTitle, 'crtoon.png', '', '', oOutputParameterHandler)
 
    oGui.setEndOfDirectory()

def showMovies(sSearch = ''):
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')

    oParser = cParser() 
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
 
    sPattern = '<div class="movie.+?href="([^"]+)".+?alt="([^"]+)" src="([^"]+)"'
    aResult = oParser.parse(sHtmlContent, sPattern)	
    if aResult[0]:
        total = len(aResult[1])
        progress_ = progress().VScreate(SITE_NAME)
        oOutputParameterHandler = cOutputParameterHandler()  
        for aEntry in aResult[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break
 
            sTitle = aEntry[1]
            siteUrl = f'{URL_MAIN}{aEntry[0]}'
            sThumb = f'{URL_MAIN}{aEntry[2]}'
            sDesc = ""

            oOutputParameterHandler.addParameter('siteUrl',siteUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)

            oGui.addMovie(SITE_IDENTIFIER, 'showLink', sTitle, '', sThumb, sDesc, oOutputParameterHandler)
        
        progress_.VSclose(progress_)
 
    if not sSearch:  
        itemList = []
        sHtmlContent = cUtil().unescape(sHtmlContent)        
        sPattern = r"<li class='page-item'><a href=\"([^\"]+)\">(.+?)</a>"
        aResult = oParser.parse(sHtmlContent, sPattern)	
        if aResult[0]:
            oOutputParameterHandler = cOutputParameterHandler() 
            for aEntry in aResult[1]:
 
                sTitle = f'[COLOR red]Page: {aEntry[1]}[/COLOR]'
                siteUrl = f'{URL_MAIN}{aEntry[0]}'

                if sTitle not in itemList:
                    itemList.append(sTitle)	
                    oOutputParameterHandler.addParameter('siteUrl', siteUrl)
                    oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
			
                    oGui.addDir(SITE_IDENTIFIER, 'showMovies', sTitle, 'next.png', oOutputParameterHandler)

        oGui.setEndOfDirectory()
		
def showSeries(sSearch = ''):
    oGui = cGui()

    oParser = cParser() 
    if sSearch:
        sUrl = sSearch
        oRequestHandler = cRequestHandler(sUrl)
        sHtmlContent = oRequestHandler.request()
        
        sPattern = 'href="([^"]+)">(.+?)<span'
        aResult = oParser.parse(sHtmlContent, sPattern)	
        if aResult[0]:
            oOutputParameterHandler = cOutputParameterHandler()  
            for aEntry in aResult[1]:

                sTitle = cUtil().ConvertSeasons(aEntry[1])
                siteUrl = f'{URL_MAIN}{aEntry[0]}'
                sThumb = ""
                sDesc = ""
                
                oOutputParameterHandler.addParameter('siteUrl',siteUrl)
                oOutputParameterHandler.addParameter('sMovieTitle', sTitle)

                oGui.addTV(SITE_IDENTIFIER, 'showEps', sTitle, '', sThumb, sDesc, oOutputParameterHandler)

    else:
        oInputParameterHandler = cInputParameterHandler()
        sUrl = oInputParameterHandler.getValue('siteUrl')

    oParser = cParser() 
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
    
    sPattern = '<div class="movie.+?href="([^"]+)".+?alt="([^"]+)" src="([^"]+)"'
    aResult = oParser.parse(sHtmlContent, sPattern)	
    if aResult[0]:
        total = len(aResult[1])
        progress_ = progress().VScreate(SITE_NAME)
        oOutputParameterHandler = cOutputParameterHandler()  
        for aEntry in aResult[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break
 
            sTitle = cUtil().ConvertSeasons(aEntry[1])
            siteUrl = f'{URL_MAIN}{aEntry[0]}'
            sThumb = f'{URL_MAIN}{aEntry[2]}'
            sDesc = ""
			
            oOutputParameterHandler.addParameter('siteUrl',siteUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)

            oGui.addTV(SITE_IDENTIFIER, 'showEps', sTitle, '', sThumb, sDesc, oOutputParameterHandler)
        
        progress_.VSclose(progress_)
 
    if not sSearch:      
        itemList = []
        sHtmlContent = cUtil().unescape(sHtmlContent)        
        sPattern = r"<li class='page-item'><a href=\"([^\"]+)\">(.+?)</a>"
        aResult = oParser.parse(sHtmlContent, sPattern)	
        if aResult[0]:
            oOutputParameterHandler = cOutputParameterHandler() 
            for aEntry in aResult[1]:
 
                sTitle = f'[COLOR red]Page: {aEntry[1]}[/COLOR]'
                siteUrl = f'{URL_MAIN}{aEntry[0]}'

                if sTitle not in itemList:
                    itemList.append(sTitle)	
                    oOutputParameterHandler.addParameter('siteUrl', siteUrl)
                    oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
			
                    oGui.addDir(SITE_IDENTIFIER, 'showSeries', sTitle, 'next.png', oOutputParameterHandler)

        oGui.setEndOfDirectory()

def showEps():
    oGui = cGui()
   
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')

    oParser = cParser() 
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    sPattern = '<div class="movie.+?href="([^"]+)".+?src="([^"]+)".+?<span class="text-white">(.+?)<br>'
    aResult = oParser.parse(sHtmlContent, sPattern) 
    if aResult[0]:
        oOutputParameterHandler = cOutputParameterHandler()  
        for aEntry in aResult[1]:

            siteUrl = f'{URL_MAIN}{aEntry[0]}'
            sThumb = f'{URL_MAIN}{aEntry[1]}'
            sEpisode = aEntry[2].replace("الحلقة ","").replace("حلقة ","")
            sTitle = f'{sMovieTitle} E{sEpisode}'

            oOutputParameterHandler.addParameter('siteUrl', siteUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
 
            oGui.addEpisode(SITE_IDENTIFIER, 'showLink', sTitle, '', sThumb, '', oOutputParameterHandler) 
 
    oGui.setEndOfDirectory()
       
def showLink():
    oGui = cGui()
   
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')
    sUrl = sUrl.replace("cartoon","watch-")

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    object_match = re.search(r'const\s+(\w+)\s*=\s*\{([^}]+)\}', sHtmlContent, re.DOTALL)
    if object_match:
        obj_name, obj_body = object_match.groups()

        kv_pairs = dict(re.findall(r'(\w+):\s*"([^"]+)"', obj_body))
        template_match = re.search(
            rf'\$\{{{re.escape(obj_name)}\.(\w+)\}}://\$\{{{re.escape(obj_name)}\.(\w+)\}}/\$\{{{re.escape(obj_name)}\.(\w+)\}}\?\$\{{{re.escape(obj_name)}\.(\w+)\}}',
            sHtmlContent
        )

        if template_match:
            proto_key, host_key, path_key, query_key = template_match.groups()
            sHosterUrl = f"{kv_pairs[proto_key]}://{kv_pairs[host_key]}/{kv_pairs[path_key]}?{kv_pairs[query_key]}"

            sHosterUrl = f'{sHosterUrl}|Referer={URL_MAIN}'

            oHoster = cHosterGui().checkHoster(sHosterUrl)
            if oHoster:
                oHoster.setDisplayName(sMovieTitle)
                oHoster.setFileName(sMovieTitle)
                cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb)

    oGui.setEndOfDirectory()