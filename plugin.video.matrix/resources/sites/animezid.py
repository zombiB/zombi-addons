# -*- coding: utf-8 -*-

import re, base64, json
from resources.lib.gui.hoster import cHosterGui
from resources.lib.gui.gui import cGui
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.comaddon import progress, VSlog, siteManager, addon
from resources.lib.parser import cParser
from resources.lib.util import cUtil
from resources.lib.multihost import cMegamax
from resources.lib import random_ua

UA = random_ua.get_ua()

SITE_IDENTIFIER = 'animezid'
SITE_NAME = 'Animezid'
SITE_DESC = 'arabic vod'
 
URL_MAIN = siteManager().getUrlMain(SITE_IDENTIFIER)

KID_MOVIES = (f'{URL_MAIN}category.php?cat=movies', 'showMovies')
KID_CARTOON = (f'{URL_MAIN}category.php?cat=series', 'showSeries')
ANIM_NEWS = (f'{URL_MAIN}category.php?cat=anime', 'showSeriesLinks')

URL_SEARCH = (f'{URL_MAIN}search.php?keywords=', 'showMovies')
URL_SEARCH_MOVIES = (f'{URL_MAIN}search.php?keywords=', 'showMoviesSearch')
URL_SEARCH_ANIMS = (f'{URL_MAIN}search.php?keywords=', 'showSeriesSearch')
FUNCTION_SEARCH = 'showMovies'
 
def load():
    oGui = cGui()
    addons = addon()

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'http://venom/')
    oGui.addDir(SITE_IDENTIFIER, 'showSearch', addons.VSlang(30078), '1/Search.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', 'http://venom/')
    oGui.addDir(SITE_IDENTIFIER, 'showSearchSeries', addons.VSlang(30079), '1/Search.png', oOutputParameterHandler)
 
    oOutputParameterHandler.addParameter('siteUrl', KID_MOVIES[0])
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'أفلام كرتون', '1/Anime.png', oOutputParameterHandler)
 
    oOutputParameterHandler.addParameter('siteUrl', KID_CARTOON[0])
    oGui.addDir(SITE_IDENTIFIER, 'showSeries', 'مسلسلات كرتون', '1/Anime.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', ANIM_NEWS[0])
    oGui.addDir(SITE_IDENTIFIER, 'showSeriesLinks', 'مسلسلات انمي', '1/Anime.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()
 
def showSearchSeries():
    oGui = cGui()
 
    sSearchText = oGui.showKeyBoard()
    if sSearchText:
        sUrl = f'{URL_MAIN}search.php?keywords={sSearchText}'
        showSeriesSearch(sUrl)
        oGui.setEndOfDirectory()
        return
 
def showSearch():
    oGui = cGui()
 
    sSearchText = oGui.showKeyBoard()
    if sSearchText:
        sUrl = f'{URL_MAIN}search.php?keywords={sSearchText}'
        showMoviesSearch(sUrl)
        oGui.setEndOfDirectory()
        return

def showMoviesSearch(sSearch = ''):
    oGui = cGui()
    if sSearch:
      sUrl = sSearch
    else:
        oInputParameterHandler = cInputParameterHandler()
        sUrl = oInputParameterHandler.getValue('siteUrl')

    oParser = cParser() 
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    sStart = '<div id="movies" class="movies">'
    sEnd = '<div class="clearfix"></div>'
    sHtmlContent = oParser.abParse(sHtmlContent, sStart, sEnd)

    sPattern = 'href="([^"]+)".+?title="([^"]+)".+?data-src="([^"]+)"'
    aResult = oParser.parse(sHtmlContent, sPattern)
    if aResult[0]:
        total = len(aResult[1])
        progress_ = progress().VScreate(SITE_NAME)
        oOutputParameterHandler = cOutputParameterHandler() 
        for aEntry in aResult[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break
 
            if "فيلم" not in aEntry[1]:
                continue
 
            sTitle = cUtil().CleanMovieName(aEntry[1])
            siteUrl = aEntry[0].replace('watch.php?','play.php?')
            sDesc = ''
            sThumb = aEntry[2]
			
            oOutputParameterHandler.addParameter('siteUrl',siteUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oGui.addMisc(SITE_IDENTIFIER, 'showHosters', sTitle, '', sThumb, sDesc, oOutputParameterHandler) 
        
        progress_.VSclose(progress_)
 
    if not sSearch:
        oGui.setEndOfDirectory() 
			
def showSeriesSearch(sSearch = ''):
    oGui = cGui()
    if sSearch:
      sUrl = sSearch
    else:
        oInputParameterHandler = cInputParameterHandler()
        sUrl = oInputParameterHandler.getValue('siteUrl')

    oParser = cParser() 
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    sStart = '<div id="movies" class="movies">'
    sEnd = '<div class="clearfix"></div>'
    sHtmlContent = oParser.abParse(sHtmlContent, sStart, sEnd)

    sPattern = 'href="([^"]+)".+?title="([^"]+)".+?data-src="([^"]+)"'
    aResult = oParser.parse(sHtmlContent, sPattern)	
    if aResult[0]:
        total = len(aResult[1])
        progress_ = progress().VScreate(SITE_NAME)
        oOutputParameterHandler = cOutputParameterHandler() 
        for aEntry in aResult[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break
 
            if "فيلم" in aEntry[1]:
                continue
 
            sTitle = (cUtil().ConvertSeasons(aEntry[1])).replace("الجزء","S").replace("الموسم","S").replace("الحلقة "," E").replace("انمي ","")
            siteUrl = aEntry[0].replace('watch.php?','play.php?')
            sDesc = ''
            sThumb = aEntry[2]

            oOutputParameterHandler.addParameter('siteUrl',siteUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
			
            if 'category.php' in siteUrl:
                oGui.addSeason(SITE_IDENTIFIER, 'showEpisodes', sTitle, '', sThumb, sDesc, oOutputParameterHandler)
            else:
                oGui.addSeason(SITE_IDENTIFIER, 'showHosters', sTitle, '', sThumb, sDesc,  oOutputParameterHandler)
        
        progress_.VSclose(progress_)
 
    if not sSearch:
        oGui.setEndOfDirectory()

def showMovies(sSearch = ''):
    oGui = cGui()
    if sSearch:
      sUrl = sSearch
    else:
        oInputParameterHandler = cInputParameterHandler()
        sUrl = oInputParameterHandler.getValue('siteUrl')

    oParser = cParser() 
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    sStart = '<div id="movies" class="movies">'
    sEnd = '<div class="clearfix"></div>'
    sHtmlContent = oParser.abParse(sHtmlContent, sStart, sEnd)

    sPattern = 'href="([^"]+)".+?title="([^"]+)".+?data-src="([^"]+)"'
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
            siteUrl = aEntry[0]
            sDesc = ''
            sThumb = aEntry[2]
			
            oOutputParameterHandler.addParameter('siteUrl',siteUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oGui.addMisc(SITE_IDENTIFIER, 'showMoviesLinks', sTitle, '', sThumb, sDesc, oOutputParameterHandler) 
        
        progress_.VSclose(progress_)

    if not sSearch:
        oGui.setEndOfDirectory() 

def showMoviesLinks(sSearch = ''):
    
    oGui = cGui()
    
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')

    oParser = cParser() 
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    sStart = '<div id="movies" class="movies">'
    sEnd = '<div class="clearfix"></div>'
    sHtmlContent1 = oParser.abParse(sHtmlContent, sStart, sEnd)

    sPattern = 'href="([^"]+)".+?title="([^"]+)".+?data-src="([^"]+)"'
    aResult = oParser.parse(sHtmlContent1, sPattern)
    if aResult[0]:
        total = len(aResult[1])
        progress_ = progress().VScreate(SITE_NAME)
        oOutputParameterHandler = cOutputParameterHandler() 
        for aEntry in aResult[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break
 
            sTitle = cUtil().CleanMovieName(aEntry[1])
            siteUrl = aEntry[0].replace('watch.php?','play.php?')
            sThumb = aEntry[2]
            sDesc = ''
            sYear = ''
            m = re.search('([0-9]{4})', sTitle)
            if m:
                sYear = str(m.group(0))
                sTitle = sTitle.replace(sYear,'')

            oOutputParameterHandler.addParameter('siteUrl',siteUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oOutputParameterHandler.addParameter('sYear', sYear)
			
            oGui.addMovie(SITE_IDENTIFIER, 'showHosters', sTitle, '', sThumb, sDesc, oOutputParameterHandler)

        progress_.VSclose(progress_)
 
    sStart = '<ul class="pagination'
    sEnd = '<div class='
    sHtmlContent = oParser.abParse(sHtmlContent, sStart, sEnd)
    sPattern = 'href="([^"]+)">([^<]+)</a>'
    aResult = oParser.parse(sHtmlContent, sPattern)
    if aResult[0]:
            for aEntry in aResult[1]:
                sTitle = aEntry[1]
            
                sTitle =  "PAGE " + sTitle
                sTitle =   '[COLOR red]'+sTitle+'[/COLOR]'
                siteUrl = URL_MAIN + aEntry[0]

                oOutputParameterHandler = cOutputParameterHandler()
                oOutputParameterHandler.addParameter('siteUrl',siteUrl)
			
                oGui.addDir(SITE_IDENTIFIER, 'showMoviesLinks', sTitle, '', oOutputParameterHandler)
 
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
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    sStart = '<div id="movies" class="movies">'
    sEnd = '<div class="clearfix"></div>'
    sHtmlContent = oParser.abParse(sHtmlContent, sStart, sEnd)

    sPattern = 'href="([^"]+)".+?title="([^"]+)".+?data-src="([^"]+)"'
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
            siteUrl = aEntry[0]
            sDesc = ''
            sThumb = aEntry[2]

            oOutputParameterHandler.addParameter('siteUrl',siteUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oGui.addMisc(SITE_IDENTIFIER, 'showSeriesLinks', sTitle, '', sThumb, sDesc, oOutputParameterHandler) 
       
        progress_.VSclose(progress_)
 
    if not sSearch:
        oGui.setEndOfDirectory()
 
def showSeriesLinks():
    oGui = cGui()
    
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sThumb = oInputParameterHandler.getValue('sThumb')

    oParser = cParser() 
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    sStart = '<div id="movies" class="movies">'
    sEnd = '<div class="clearfix"></div>'
    sHtmlContent1 = oParser.abParse(sHtmlContent, sStart, sEnd)

    sPattern = 'href="([^"]+)".+?title="([^"]+)".+?data-src="([^"]+)"'
    aResult = oParser.parse(sHtmlContent1, sPattern)	
    if aResult[0]:
        oOutputParameterHandler = cOutputParameterHandler() 
        for aEntry in aResult[1]:
 
            sTitle =  aEntry[1].replace("مسلسل","").replace("انمي","").replace("مترجمة","").replace("مترجم","")
            siteUrl = aEntry[0]
            sThumb = aEntry[2]
            sDesc = ''

            oOutputParameterHandler.addParameter('siteUrl',siteUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oGui.addAnime(SITE_IDENTIFIER, 'showEpisodes', sTitle, '', sThumb, sDesc, oOutputParameterHandler)

    sStart = '<ul class="pagination'
    sEnd = '<div class='
    sHtmlContent = oParser.abParse(sHtmlContent, sStart, sEnd)
    sPattern = 'href="([^"]+)">([^<]+)</a>'
    aResult = oParser.parse(sHtmlContent, sPattern)
    if aResult[0]:
            for aEntry in aResult[1]:       
                sTitle =   f'[COLOR red]Page: {aEntry[1]}[/COLOR]'
                siteUrl = f'{URL_MAIN}{aEntry[0]}'

                oOutputParameterHandler = cOutputParameterHandler()
                oOutputParameterHandler.addParameter('siteUrl',siteUrl)
			
                oGui.addDir(SITE_IDENTIFIER, 'showSeriesLinks', sTitle, 'next.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()
 
def showEpisodes():
    oGui = cGui()
    
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sThumb = oInputParameterHandler.getValue('sThumb')

    oParser = cParser() 
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    sStart = '<div id="movies" class="movies">'
    sEnd = '<div class="clearfix"></div>'
    sHtmlContent = oParser.abParse(sHtmlContent, sStart, sEnd)

    sPattern = 'href="([^"]+)".+?title="([^"]+)".+?data-src="([^"]+)"'
    aResult = oParser.parse(sHtmlContent, sPattern)
    if aResult[0]:
        oOutputParameterHandler = cOutputParameterHandler() 
        for aEntry in aResult[1]:
 
            sTitle = (cUtil().ConvertSeasons(aEntry[1])).replace("الجزء","S").replace("الموسم","S").replace("الحلقة "," E")
            siteUrl = aEntry[0].replace('watch.php?','play.php?')
            sThumb = aEntry[2]
            sDesc = ''
			
            oOutputParameterHandler.addParameter('siteUrl',siteUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
			
            if 'category.php' in siteUrl:
                oGui.addSeason(SITE_IDENTIFIER, 'showEpisodes', sTitle, '', sThumb, sDesc, oOutputParameterHandler)
            else:
                oGui.addEpisode(SITE_IDENTIFIER, 'showHosters', sTitle, '', sThumb, sDesc,  oOutputParameterHandler)

    oGui.setEndOfDirectory()

def showHosters():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')

    oParser = cParser()    
    oRequestHandler = cRequestHandler(sUrl.replace('play.php','watch.php'))
    sHtmlContent = oRequestHandler.request()

    sPattern =  '<a rel="nofollow" href="([^"]+)"\s*class='
    aResult = oParser.parse(sHtmlContent,sPattern)
    if aResult[0]:
        m3url = aResult[1][0]
        if '?url=' in m3url or '?post=' in m3url:
            url_tmp = m3url.split('?url=' if '?url=' in m3url else '?post=')[1].replace('%3D','=')

            hostersData = json.loads(base64.b64decode(url_tmp).decode('utf8',errors='ignore'))
            m3url = hostersData["watchUrl"]
        
        oRequestHandler = cRequestHandler(m3url)
        oRequestHandler.addHeaderEntry('User-Agent', UA)
        oRequestHandler.addHeaderEntry('referer', URL_MAIN)
        sHtmlContent = oRequestHandler.request()

        patterns = ['data-embed=["\']([^"\']+)', 'data-server=.+?iframe src=["\']([^"\']+)']
        for sPattern in patterns:
            aResult = oParser.parse(sHtmlContent, sPattern)
            if aResult[0]:
                oOutputParameterHandler = cOutputParameterHandler()
                for aEntry in aResult[1]:
                    url = aEntry.replace("+", "")
                    if url.startswith('//'):
                        url = f'https:{url}'
                    sHosterUrl = url
                    
                    if bool(re.search(r'mega.*max', sHosterUrl)) or bool(re.search(r'mega.*zid', sHosterUrl)):
                        data = cMegamax().GetUrls(sHosterUrl)
                        if data:
                            for item in data:
                                sHosterUrl, sQual, sLabel = [part.split('=')[1] for part in item.split(',')]
                                sDisplayTitle = f'{sMovieTitle} [COLOR coral] [{sQual}][/COLOR][COLOR orange] - {sLabel}[/COLOR]'
                                oOutputParameterHandler.addParameter('sHosterUrl', sHosterUrl)
                                oOutputParameterHandler.addParameter('siteUrl', sUrl)
                                oOutputParameterHandler.addParameter('sQual', sQual)
                                oOutputParameterHandler.addParameter('sMovieTitle', sMovieTitle)
                                oOutputParameterHandler.addParameter('sThumb', sThumb)
                                oGui.addLink(SITE_IDENTIFIER, 'showLinks', sDisplayTitle, sThumb, sDisplayTitle, oOutputParameterHandler)
                    else:
                        if 'bestx' in sHosterUrl:
                            sHosterUrl = f'{sHosterUrl}|Referer={URL_MAIN}'
                        oHoster = cHosterGui().checkHoster(sHosterUrl)
                        if oHoster:
                            oHoster.setDisplayName(sMovieTitle)
                            oHoster.setFileName(sMovieTitle)
                            cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb)

    sPattern = 'target="_blank" href="(.+?)"><span>(.+?)</span>'
    aResult = oParser.parse(sHtmlContent, sPattern)
    if aResult[0]:
        for aEntry in aResult[1]:
        
            url = aEntry[0].replace("+","")
            if url.startswith('//'):
                url = f'https:{url}'
            sTitle = f'{sMovieTitle} [{aEntry[1]}]'									
            
            sHosterUrl = url 
            if bool(re.search(r'mega.*max', sHosterUrl)) or bool(re.search(r'mega.*zid', sHosterUrl)):
                continue
            oHoster = cHosterGui().checkHoster(sHosterUrl)
            if oHoster:
                oHoster.setDisplayName(sTitle)
                oHoster.setFileName(sTitle)
                cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb)				
                
    oGui.setEndOfDirectory()

def showLinks():
    oGui = cGui()

    oInputParameterHandler = cInputParameterHandler()
    sHosterUrl = oInputParameterHandler.getValue('sHosterUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sQual = oInputParameterHandler.getValue('sQual')
    sThumb = oInputParameterHandler.getValue('sThumb')

    sDisplayTitle = f'{sMovieTitle} [COLOR coral] [{sQual}] [/COLOR]'   
    oHoster = cHosterGui().checkHoster(sHosterUrl)
    if oHoster:
        oHoster.setDisplayName(sDisplayTitle)
        oHoster.setFileName(sMovieTitle)
        cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb)

    oGui.setEndOfDirectory()