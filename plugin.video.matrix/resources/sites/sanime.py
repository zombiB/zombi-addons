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
from resources.lib.multihost import cMegamax
from resources.lib import random_ua

UA = random_ua.get_phone_ua()

SITE_IDENTIFIER = 'sanime'
SITE_NAME = 'Shahid Anime'
SITE_DESC = 'anime vod'
 
URL_MAIN = siteManager().getUrlMain(SITE_IDENTIFIER)

ANIM_MOVIES = (f'{URL_MAIN}anime/', 'showMovies')
ANIM_NEWS = (f'{URL_MAIN}episodes/' , 'showSeries')

URL_SEARCH = (f'{URL_MAIN}?s=', 'showMovies')
URL_SEARCH_ANIMS = (f'{URL_MAIN}?s=', 'showMovies')
FUNCTION_SEARCH = 'showMovies'
 
def load():
    oGui = cGui()
    addons = addon()

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'http://venom/')
    oGui.addDir(SITE_IDENTIFIER, 'showSearch', addons.VSlang(30118), '1/Search.png', oOutputParameterHandler)
 
    oOutputParameterHandler.addParameter('siteUrl', ANIM_NEWS[0])
    oGui.addDir(SITE_IDENTIFIER, 'showSeries', 'أخر الحلقات المضافة', '1/Anime.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', f'{URL_MAIN}seriesDubbed/')
    oGui.addDir(SITE_IDENTIFIER, 'showSeries',  'مسلسلات انمي مدبلجة', '1/Anime.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', f'{URL_MAIN}series/')
    oGui.addDir(SITE_IDENTIFIER, 'showSeries', 'قائمة الانمي', '1/Anime.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', ANIM_MOVIES[0])
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'أفلام انمي', '1/Anime.png', oOutputParameterHandler)
 
    oGui.setEndOfDirectory()
 
def showSearch():
    oGui = cGui()
 
    sSearchText = oGui.showKeyBoard()
    if sSearchText:
        sUrl = f'{URL_MAIN}?s={sSearchText}'
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

    oParser = cParser()
    sPattern = '<div class="wrap-poster.+?src="([^"]+)".+?<h2>\s*<a href="([^"]+)">(.+?)</a>'
    aResult = oParser.parse(sHtmlContent, sPattern)		
    if aResult[0]:
        total = len(aResult[1])
        progress_ = progress().VScreate(SITE_NAME)
        oOutputParameterHandler = cOutputParameterHandler()
        for aEntry in aResult[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break
 
            sTitle = (cUtil().CleanMovieName(aEntry[2]))
            siteUrl = aEntry[1]
            if siteUrl.startswith('//'):
                siteUrl = f'http:{siteUrl}'
            sThumb = aEntry[0]
            sDesc = ''
            sYear = ''

            oOutputParameterHandler.addParameter('siteUrl', siteUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oOutputParameterHandler.addParameter('sYear', sYear)
            oOutputParameterHandler.addParameter('sDesc', sDesc)
            if any(s in siteUrl for s in ['/series/', 'seasonsDubbed/', '/seasons/', '/seriesDubbed/']):
                oGui.addAnime(SITE_IDENTIFIER, 'ShowSeasons', sTitle, '', sThumb, sDesc, oOutputParameterHandler)
            elif 'episodes/' in siteUrl:
                oGui.addAnime(SITE_IDENTIFIER, 'ShowEps', sTitle, '', sThumb, sDesc, oOutputParameterHandler)
            else: 		
                oGui.addAnime(SITE_IDENTIFIER, 'showHosters', sTitle, '', sThumb, sDesc, oOutputParameterHandler)

        progress_.VSclose(progress_)
 
    if not sSearch:
        sStart = "<div id='pagination'>"
        sEnd = '</main>'
        sHtmlContent = oParser.abParse(sHtmlContent, sStart, sEnd)

        sPattern = 'href=["\']([^"\']+)["\']\s*class=["\'].*?["\']\s*>(.+?)</a>'
        aResult = oParser.parse(sHtmlContent, sPattern)
        if aResult[0]:
            for aEntry in aResult[1]:

                sTitle = f'[COLOR red]Page: {aEntry[1]}[/COLOR]'
                siteUrl = aEntry[0]

                oOutputParameterHandler = cOutputParameterHandler()
                oOutputParameterHandler.addParameter('siteUrl',siteUrl)
			
                oGui.addDir(SITE_IDENTIFIER, 'showMovies', sTitle, 'next.png', oOutputParameterHandler) 
        oGui.setEndOfDirectory()
			
def showSeries(sSearch = ''):
    oGui = cGui()
    if sSearch:
      sUrl = sSearch
    else:
        oInputParameterHandler = cInputParameterHandler()
        sUrl = oInputParameterHandler.getValue('siteUrl')
 
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    oParser = cParser()
    sPattern = '<div class="wrap-poster.+?src="([^"]+)".+?<h2>\s*<a href="([^"]+)">(.+?)</a>'
    aResult = oParser.parse(sHtmlContent, sPattern)	
    if aResult[0]:
        total = len(aResult[1])
        progress_ = progress().VScreate(SITE_NAME)
        oOutputParameterHandler = cOutputParameterHandler()
        for aEntry in aResult[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break
 
            sTitle = cUtil().CleanSeriesName(aEntry[2])
            siteUrl = aEntry[1]
            sThumb = aEntry[0]
            sDesc = ''
            sYear = ''
            if "الحلقة" in sTitle:
                sTitle = sTitle.split("الحلقة")[0].split('الموسم')[0]
            if "حلقة" in sTitle:
                sTitle = sTitle.split("حلقة")[0].split('الموسم')[0]

            oOutputParameterHandler.addParameter('siteUrl', siteUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oOutputParameterHandler.addParameter('sYear', sYear)
            oOutputParameterHandler.addParameter('sDesc', sDesc)
			
            if any(s in siteUrl for s in ['/series/', 'seasonsDubbed/', '/seasons/', '/seriesDubbed/']):
                oGui.addAnime(SITE_IDENTIFIER, 'ShowSeasons', sTitle, '', sThumb, sDesc, oOutputParameterHandler)
            elif '/anime/' in siteUrl:
                oGui.addAnime(SITE_IDENTIFIER, 'showHosters', sTitle, '', sThumb, sDesc, oOutputParameterHandler)
            else:
                oGui.addAnime(SITE_IDENTIFIER, 'ShowEps', sTitle, '', sThumb, sDesc, oOutputParameterHandler)

        progress_.VSclose(progress_)
 
    if not sSearch:
        sStart = "<div id='pagination'>"
        sEnd = '</main>'
        sHtmlContent = oParser.abParse(sHtmlContent, sStart, sEnd)

        sPattern = 'href=["\']([^"\']+)["\']\s*class=["\'].*?["\']\s*>(.+?)</a>'
        aResult = oParser.parse(sHtmlContent, sPattern)
        if aResult[0]:
            for aEntry in aResult[1]:

                sTitle = f'[COLOR red]Page: {aEntry[1]}[/COLOR]'
                siteUrl = aEntry[0]

                oOutputParameterHandler = cOutputParameterHandler()
                oOutputParameterHandler.addParameter('siteUrl',siteUrl)
			
                oGui.addDir(SITE_IDENTIFIER, 'showSeries', sTitle, 'next.png', oOutputParameterHandler) 

        oGui.setEndOfDirectory()

def ShowSeasons():
    oGui = cGui()   
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')
    sDesc = oInputParameterHandler.getValue('sDesc')

    oParser = cParser()
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request() 

    pattern = r'<script>window.location = "([^"]+)"'
    match = re.search(pattern, sHtmlContent, re.DOTALL)
    if match:
        sUrl = match.group(1)  
        oRequestHandler = cRequestHandler(sUrl)
        sHtmlContent = oRequestHandler.request()

    sPattern = '<div class="wrap-poster.+?src="([^"]+)".+?<h2>\s*<a href="([^"]+)">(.+?)</a>'
    aResult = oParser.parse(sHtmlContent, sPattern)
    if aResult[0]:
        oOutputParameterHandler = cOutputParameterHandler()
        for aEntry in aResult[1]:
 
            sTitle = cUtil().CleanSeriesName(aEntry[2])
            siteUrl = aEntry[1]
            if siteUrl.startswith('//'):
                siteUrl = f'http:{siteUrl}'
            sThumb = aEntry[0]
 
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('siteUrl', siteUrl)
            oOutputParameterHandler.addParameter('sThumb', sThumb)

            oGui.addSeason(SITE_IDENTIFIER, 'ShowEps', sTitle, '', sThumb, sDesc, oOutputParameterHandler) 

    else:
        sStart = '<select id="show-more'
        sEnd = '</div>'
        sHtmlContent1 = oParser.abParse(sHtmlContent, sStart, sEnd)

        sPattern = '<option value="([^"]+)">(.+?)</option>'
        aResult = oParser.parse(sHtmlContent1, sPattern)
        if aResult[0]:
            oOutputParameterHandler = cOutputParameterHandler()
            for aEntry in aResult[1]:
    
                sTitle = cUtil().CleanSeriesName(aEntry[1])
                siteUrl = aEntry[0]
                if siteUrl.startswith('//'):
                    siteUrl = f'http:{siteUrl}'
    
                oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
                oOutputParameterHandler.addParameter('siteUrl', siteUrl)
                oOutputParameterHandler.addParameter('sThumb', sThumb)

                oGui.addSeason(SITE_IDENTIFIER, 'ShowEps', sTitle, '', sThumb, sDesc, oOutputParameterHandler) 

    oGui.setEndOfDirectory()

def ShowEps():
    oGui = cGui()   
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')
    sDesc = oInputParameterHandler.getValue('sDesc')

    oParser = cParser()
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request() 

    pattern = r'<script>window.location = "([^"]+)"'
    match = re.search(pattern, sHtmlContent, re.DOTALL)
    if match:
        sUrl = match.group(1)  
        oRequestHandler = cRequestHandler(sUrl)
        sHtmlContent = oRequestHandler.request()

    sPattern = '<nav class="navbar.+?href="([^"]+)">(.+?)</a>'
    aResult = oParser.parse(sHtmlContent, sPattern)
    if aResult[0]:
        oOutputParameterHandler = cOutputParameterHandler()
        for aEntry in aResult[1]:
 
            siteUrl = aEntry[0]           
            sTitle = cUtil().CleanSeriesName(aEntry[1])
            for pattern in [r"الحلقة (\d+)", r"الحلقه (\d+)"]:
                m = re.search(pattern, aEntry[1])
                if m:
                    sEp = str(m.group(1))
                    sTitle = f'{sTitle} E{sEp}'

            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('siteUrl', siteUrl)
            oOutputParameterHandler.addParameter('sThumb', sThumb)

            oGui.addEpisode(SITE_IDENTIFIER, 'showHosters', sTitle, '', sThumb, sDesc, oOutputParameterHandler) 

    else:
        sStart = '<select id="show-more'
        sEnd = '</div>'
        sHtmlContent1 = oParser.abParse(sHtmlContent, sStart, sEnd)

        sPattern = '<option value="([^"]+)">(.+?)</option>'
        aResult = oParser.parse(sHtmlContent1, sPattern)
        if aResult[0]:
            oOutputParameterHandler = cOutputParameterHandler()
            for aEntry in aResult[1]:
    
                sTitle = cUtil().CleanSeriesName(aEntry[1])
                for pattern in [r"الحلقة (\d+)", r"الحلقه (\d+)"]:
                    m = re.search(pattern, aEntry[1])
                    if m:
                        sEp = str(m.group(1))
                        sTitle = f'{sTitle} E{sEp}'
                    siteUrl = aEntry[0]
                    if siteUrl.startswith('//'):
                        siteUrl = f'http:{siteUrl}'
    
                oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
                oOutputParameterHandler.addParameter('siteUrl', siteUrl)
                oOutputParameterHandler.addParameter('sThumb', sThumb)

                oGui.addEpisode(SITE_IDENTIFIER, 'showHosters', sTitle, '', sThumb, sDesc, oOutputParameterHandler) 

    oGui.setEndOfDirectory()

def showHosters():
    oGui = cGui()
   
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request() 
    
    oParser = cParser()   
    sPattern = 'data-serv=["\']([^"\']+)["\']\s*data-frameserver=["\']([^"\']+)["\']\s*data-post=["\']([^"\']+)["\']>' 
    aResult = oParser.parse(sHtmlContent, sPattern)
    if aResult[0]:
        for aEntry in aResult[1]:

            sServer = f'{URL_MAIN}wp-admin/admin-ajax.php?action=codecanal_ajax_request&post={aEntry[2]}&frameserver={aEntry[1]}&serv={aEntry[0]}'		
            oRequestHandler = cRequestHandler(sServer)
            oRequestHandler.addHeaderEntry('User-Agent', UA)
            oRequestHandler.addHeaderEntry('Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8')
            oRequestHandler.addHeaderEntry('X-Requested-With', 'XMLHttpRequest')
            oRequestHandler.addHeaderEntry('Accept-Language', 'fr,fr-FR;q=0.8,en-US;q=0.5,en;q=0.3')
            sData = oRequestHandler.request()

            sPattern = '<iframe.+?src="([^"]+)' 
            aResult = oParser.parse(sData, sPattern)	
            if aResult[0]:
               oOutputParameterHandler = cOutputParameterHandler()
               for aEntry in aResult[1]:
        
                    url = aEntry
                    if url.startswith('//'):
                      url = f'http:{url}'
                    if 'leech' in url:
                        continue
                    if 'govid' in url:
                      url = url.replace("play","down").replace("embed-","")
								            
                    sHosterUrl = url

                    if bool(re.search(r'mega.*max', sHosterUrl)):
                        data = cMegamax().GetUrls(sHosterUrl)
                        if data is not False:
                            for item in data:
                                sHosterUrl = item.split(',')[0].split('=')[1]
                                sQual = item.split(',')[1].split('=')[1]
                                sLabel = item.split(',')[2].split('=')[1]

                                sDisplayTitle = f'{sMovieTitle} ({sQual}) [COLOR coral]{sLabel}[/COLOR]'  
                                oOutputParameterHandler.addParameter('sHosterUrl', sHosterUrl)
                                oOutputParameterHandler.addParameter('siteUrl', sUrl)
                                oOutputParameterHandler.addParameter('sQual', sQual)
                                oOutputParameterHandler.addParameter('sMovieTitle', sMovieTitle)
                                oOutputParameterHandler.addParameter('sThumb', sThumb)

                                oGui.addLink(SITE_IDENTIFIER, 'showLinks', sDisplayTitle, sThumb, sDisplayTitle, oOutputParameterHandler)

                    if 'nowvid' in sHosterUrl or 'userload' in sHosterUrl:
                       sHosterUrl = f'{sHosterUrl}|Referer={URL_MAIN}'
   
                    oHoster = cHosterGui().checkHoster(sHosterUrl)
                    if oHoster:
                      sDisplayTitle = sMovieTitle
                      oHoster.setDisplayName(sDisplayTitle)
                      oHoster.setFileName(sMovieTitle)
                      cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb)

    sPattern = '<iframe.+?src="([^"]+)' 
    aResult = oParser.parse(sHtmlContent, sPattern)	
    if aResult[0]:
        oOutputParameterHandler = cOutputParameterHandler()
        for aEntry in aResult[1]:

            url = aEntry
            if url.startswith('//'):
                url = f'http:{url}'
            if 'leech' in url:
                continue
            if 'govid' in url:
                url = url.replace("play","down").replace("embed-","")
                                    
            sHosterUrl = url

            if bool(re.search(r'mega.*max', sHosterUrl)):
                data = cMegamax().GetUrls(sHosterUrl)
                if data is not False:
                    for item in data:
                        sHosterUrl = item.split(',')[0].split('=')[1]
                        sQual = item.split(',')[1].split('=')[1]
                        sLabel = item.split(',')[2].split('=')[1]

                        sDisplayTitle = f'{sMovieTitle} ({sQual}) [COLOR coral]{sLabel}[/COLOR]'  
                        oOutputParameterHandler.addParameter('sHosterUrl', sHosterUrl)
                        oOutputParameterHandler.addParameter('siteUrl', sUrl)
                        oOutputParameterHandler.addParameter('sQual', sQual)
                        oOutputParameterHandler.addParameter('sMovieTitle', sMovieTitle)
                        oOutputParameterHandler.addParameter('sThumb', sThumb)

                        oGui.addLink(SITE_IDENTIFIER, 'showLinks', sDisplayTitle, sThumb, sDisplayTitle, oOutputParameterHandler)

            if 'nowvid' in sHosterUrl or 'userload' in sHosterUrl:
                sHosterUrl = f'{sHosterUrl}|Referer={URL_MAIN}'

            oHoster = cHosterGui().checkHoster(sHosterUrl)
            if oHoster:
                sDisplayTitle = sMovieTitle
                oHoster.setDisplayName(sDisplayTitle)
                oHoster.setFileName(sMovieTitle)
                cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb)

    oGui.setEndOfDirectory()

def showLinks():
    oGui = cGui()

    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sHosterUrl = oInputParameterHandler.getValue('sHosterUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')

    oHoster = cHosterGui().checkHoster(sHosterUrl)
    if oHoster:
        oHoster.setDisplayName(sMovieTitle)
        oHoster.setFileName(sMovieTitle)
        cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb)

    oGui.setEndOfDirectory()