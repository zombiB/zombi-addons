# -*- coding: utf-8 -*-

import re
import base64
from resources.lib.gui.hoster import cHosterGui
from resources.lib.gui.gui import cGui
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.comaddon import progress, VSlog, isMatrix, siteManager, addon
from resources.lib.parser import cParser
from resources.lib.util import cUtil
from resources.lib import random_ua

UA = random_ua.get_phone_ua()

SITE_IDENTIFIER = 'faselhd'
SITE_NAME = 'Faselhd'
SITE_DESC = 'arabic vod'

sHost = base64.b64decode(siteManager().getUrlMain2(SITE_IDENTIFIER)).decode("utf-8")
sHost = sHost[::-1]

URL_MAIN = siteManager().getUrlMain(SITE_IDENTIFIER)

MOVIE_EN = (f'{URL_MAIN}movies', 'showMovies')
MOVIE_HI = (f'{URL_MAIN}hindi', 'showMovies')
MOVIE_ASIAN = (f'{URL_MAIN}asian-movies', 'showMovies')
KID_MOVIES = (f'{URL_MAIN}dubbed-movies', 'showMovies')
ANIM_MOVIES = (f'{URL_MAIN}anime-movies', 'showMovies')
MOVIE_TOP = (f'{URL_MAIN}movies_top_votes', 'showMovies')
MOVIE_POP = (f'{URL_MAIN}movies_top_views', 'showMovies')
MOVIE_DUBBED = (f'{URL_MAIN}dubbed-movies', 'showMovies')
MOVIE_PACK = (f'{URL_MAIN}movies_collections', 'showMovies')

SERIE_EN = (f'{URL_MAIN}series', 'showSeries')
SERIE_ASIA = (f'{URL_MAIN}asian-series', 'showSeries')
REPLAYTV_NEWS = (f'{URL_MAIN}tvshows', 'showSeries')

ANIM_NEWS = (f'{URL_MAIN}anime', 'showAnimes')
DOC_NEWS = (f'{URL_MAIN}movies-cats/documentary', 'showMovies')
DOC_SERIES = (f'{URL_MAIN}series_genres/documentary', 'showSeries')

URL_SEARCH = (f'{URL_MAIN}?s=', 'showSeries')
URL_SEARCH_MOVIES = (f'{URL_MAIN}?s=%D9%81%D9%8A%D9%84%D9%85+', 'showMovies')
URL_SEARCH_SERIES = (f'{URL_MAIN}?s=%D9%85%D8%B3%D9%84%D8%B3%D9%84+', 'showSeries')
FUNCTION_SEARCH = 'showMovies'
 
def load():
    oGui = cGui()
    addons = addon()

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'http://venom/')
    oGui.addDir(SITE_IDENTIFIER, 'showSearch', addons.VSlang(30078), '1/Search.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', 'http://venom/')
    oGui.addDir(SITE_IDENTIFIER, 'showSeriesSearch', addons.VSlang(30079), '1/Search.png', oOutputParameterHandler)
   
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_EN[0])
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'أفلام أجنبية', '1/Movies.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', MOVIE_DUBBED[0])
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'أفلام مدبلجة', '1/Movies.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', MOVIE_ASIAN[0])
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'أفلام أسيوية', '1/Asian.png', oOutputParameterHandler)
        
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_HI[0])
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'أفلام هندية', '1/Hindi.png', oOutputParameterHandler)
    
    oOutputParameterHandler.addParameter('siteUrl', ANIM_MOVIES[0])
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'أفلام انمي', '1/Anime.png', oOutputParameterHandler)
    
    oOutputParameterHandler.addParameter('siteUrl', KID_MOVIES[0])
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'أفلام انيميشن', '1/1/Anime.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', DOC_NEWS[0])
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'أفلام وثائقية', '1/Documentary.png', oOutputParameterHandler) 

    oOutputParameterHandler.addParameter('siteUrl', MOVIE_PACK[0])
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'سلاسل افلام كاملة', 'pack.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', SERIE_EN[0])
    oGui.addDir(SITE_IDENTIFIER, 'showSeries', 'مسلسلات أجنبية', '1/Movies.png', oOutputParameterHandler)
    
    oOutputParameterHandler.addParameter('siteUrl', SERIE_ASIA[0])
    oGui.addDir(SITE_IDENTIFIER, 'showSeries', 'مسلسلات أسيوية', '1/Asian.png', oOutputParameterHandler)
      
    oOutputParameterHandler.addParameter('siteUrl', DOC_SERIES[0])
    oGui.addDir(SITE_IDENTIFIER, 'showSeries', 'مسلسلات وثائقية', '1/Documentary.png', oOutputParameterHandler) 
        
    oOutputParameterHandler.addParameter('siteUrl', ANIM_NEWS[0])
    oGui.addDir(SITE_IDENTIFIER, 'showAnimes', 'مسلسلات انمي', '1/Anime.png', oOutputParameterHandler)
 
    oOutputParameterHandler.addParameter('siteUrl', REPLAYTV_NEWS[0])
    oGui.addDir(SITE_IDENTIFIER, 'showSeries', 'برامج تلفزيونية', '1/Programs.png', oOutputParameterHandler) 

    oGui.setEndOfDirectory()
	
def showSearch():
    oGui = cGui()
 
    sSearchText = oGui.showKeyBoard()
    if sSearchText:
        sUrl = f'{URL_MAIN}?s=%D9%81%D9%8A%D9%84%D9%85+{sSearchText}'
        showMovies(sUrl)
        oGui.setEndOfDirectory()
        return
 
def showSeriesSearch():
    oGui = cGui()
 
    sSearchText = oGui.showKeyBoard()
    if sSearchText:
        sUrl = f'{URL_MAIN}?s=%D9%85%D8%B3%D9%84%D8%B3%D9%84+{sSearchText}'
        showSeries(sUrl)
        oGui.setEndOfDirectory()
        return

def showWeek():
    oGui = cGui()

    oInputParameterHandler = cInputParameterHandler()
    sHtmlContent = oInputParameterHandler.getValue('sHtmlContentX')

    oParser = cParser() 
    sPattern = '<div class="postDiv.+?">.+?<a href="([^"]+)">.+?data-src="([^"]+)".+?alt="([^"]+)'
    aResult = oParser.parse(sHtmlContent, sPattern)
    if aResult[0]:
        oOutputParameterHandler = cOutputParameterHandler()    
        for aEntry in aResult[1]:
            
            sTitle = cUtil().CleanMovieName(aEntry[2])
            siteUrl = aEntry[0]
            sThumb = aEntry[1].replace("(","").replace(")","")
            sDesc = ''
            sYear = ''
            m = re.search('([0-9]{4})', sTitle)
            if m:
                sYear = str(m.group(0))

            oOutputParameterHandler.addParameter('siteUrl', siteUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oOutputParameterHandler.addParameter('sYear', sYear)
            oOutputParameterHandler.addParameter('sDesc', sDesc)
            if 'anime/' in siteUrl:
                oGui.addAnime(SITE_IDENTIFIER, 'showSeasons', sTitle, '', sThumb, sDesc, oOutputParameterHandler)
            elif '/series' in siteUrl or '/season' in siteUrl:
                oGui.addTV(SITE_IDENTIFIER, 'showSeasons', sTitle, '', sThumb, sDesc, oOutputParameterHandler)
            else:
                oGui.addMovie(SITE_IDENTIFIER, 'showLink', sTitle, '', sThumb, sDesc, oOutputParameterHandler)

    oGui.setEndOfDirectory()

def showMovies(sSearch = ''):
    oGui = cGui()
    oOutputParameterHandler = cOutputParameterHandler()
    
    if sSearch:
      sUrl = sSearch
    else:
        oInputParameterHandler = cInputParameterHandler()
        sUrl = oInputParameterHandler.getValue('siteUrl')

    if addon().getSetting('Use_alternative') == "true":
        sUrl = sHost + "/".join(sUrl.split("/")[3:]) if sUrl.startswith("https://") else sUrl

    oParser = cParser() 
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    sStart = '<div class="subHead">'
    sEnd = '<div class="container">'
    sHtmlContentX = oParser.abParse(sHtmlContent, sStart, sEnd)
    oOutputParameterHandler.addParameter('sHtmlContentX', sHtmlContentX)
    if not sSearch:
        oGui.addDir(SITE_IDENTIFIER, 'showWeek', 'الافلام الاكثر مشاهدة هذا الاسبوع', '1/Movies.png', oOutputParameterHandler)
    
    sStart = 'id="postList">'
    sEnd = '</html>'
    sHtmlContent = oParser.abParse(sHtmlContent, sStart, sEnd)

    sPattern = '<div class="postDiv.+?href="([^"]+)">.+?data-src="([^"]+)"'
    if 'collections' in sUrl:
        sPattern += '.+?<div class="h1">(.+?)</div>'
    else:
        sPattern += '.+?alt="([^"]+)'
    aResult = oParser.parse(sHtmlContent, sPattern)	
    if aResult[0]:
        total = len(aResult[1])
        progress_ = progress().VScreate(SITE_NAME)
        for aEntry in aResult[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break
            if 'مواسم' in aEntry[2] or 'موسم' in aEntry[2] or 'حلقة' in aEntry[2]:
                continue
            
            sTitle = cUtil().CleanMovieName(aEntry[2])
            siteUrl = aEntry[0]
            sThumb = aEntry[1].replace("(","").replace(")","")
            sDesc = ''
            sYear = ''
            m = re.findall(r'\b([0-9]{4})\b', aEntry[2])
            if m:
                sYear = m[-1]

            oOutputParameterHandler.addParameter('siteUrl', siteUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oOutputParameterHandler.addParameter('sYear', sYear)
            oOutputParameterHandler.addParameter('sDesc', sDesc)

            if "/serie"  in siteUrl or "/episode"  in siteUrl or "/anime/" in siteUrl:
                oGui.addTV(SITE_IDENTIFIER, 'showEpisodes1', sTitle, '', sThumb, sDesc, oOutputParameterHandler)
            elif 'collections/' in siteUrl:
                oGui.addMovie(SITE_IDENTIFIER, 'showMovies', sTitle, '', sThumb, sDesc, oOutputParameterHandler)
            else:     
                oGui.addMovie(SITE_IDENTIFIER, 'showLink', sTitle, '', sThumb, sDesc, oOutputParameterHandler)

        progress_.VSclose(progress_)

        sNextPage = __checkForNextPage(sHtmlContent)
        if sNextPage:
            oOutputParameterHandler.addParameter('siteUrl', sNextPage)
            oGui.addDir(SITE_IDENTIFIER, 'showMovies', '[COLOR teal]Next >>>[/COLOR]', 'next.png', oOutputParameterHandler)
 
    if not sSearch:
        oGui.setEndOfDirectory()

def showSeries(sSearch = ''):
    oGui = cGui()
    oOutputParameterHandler = cOutputParameterHandler()
    
    if sSearch:
      sUrl = sSearch
    else:
        oInputParameterHandler = cInputParameterHandler()
        sUrl = oInputParameterHandler.getValue('siteUrl')

    oParser = cParser() 
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    sStart = '<div class="subHead">'
    sEnd = '<div class="container">'
    sHtmlContentX = oParser.abParse(sHtmlContent, sStart, sEnd)
    oOutputParameterHandler.addParameter('sHtmlContentX', sHtmlContentX)
    if not sSearch:
        oGui.addDir(SITE_IDENTIFIER, 'showWeek', 'الاكثر مشاهدة هذا الاسبوع', 'history.png', oOutputParameterHandler)
    
    sStart = 'id="postList">'
    sEnd = '</html>'
    sHtmlContent = oParser.abParse(sHtmlContent, sStart, sEnd)

    sPattern = '<div class="postDiv">.+?<a href="([^"]+)".+?data-src="([^"]+)".+?alt="([^"]+)'
    aResult = oParser.parse(sHtmlContent, sPattern)	
    itemList = []
    if aResult[0]:
        total = len(aResult[1])
        progress_ = progress().VScreate(SITE_NAME)
        for aEntry in aResult[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break
            
            sTitle = cUtil().CleanSeriesName(aEntry[2])
            sTitle = re.sub(r"S\d{1,2}", "", sTitle).strip()
            siteUrl = aEntry[0]
            sThumb = aEntry[1].replace("(","").replace(")","")
            sDesc = ''

            if sTitle not in itemList:
                itemList.append(sTitle)	
                oOutputParameterHandler.addParameter('siteUrl', siteUrl)
                oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
                oOutputParameterHandler.addParameter('sThumb', sThumb)
                oOutputParameterHandler.addParameter('sDesc', sDesc)
                
                oGui.addTV(SITE_IDENTIFIER, 'showSeasons', sTitle, '', sThumb, sDesc, oOutputParameterHandler)

        progress_.VSclose(progress_)
 
        sNextPage = __checkForNextPage(sHtmlContent)
        if sNextPage:
            oOutputParameterHandler.addParameter('siteUrl', sNextPage)
            oGui.addDir(SITE_IDENTIFIER, 'showSeries', '[COLOR teal]Next >>>[/COLOR]', 'next.png', oOutputParameterHandler)
 
    if not sSearch:
        oGui.setEndOfDirectory()
		
def showAnimes(sSearch = ''):
    oGui = cGui()
    oOutputParameterHandler = cOutputParameterHandler()

    if sSearch:
      sUrl = sSearch
    else:
        oInputParameterHandler = cInputParameterHandler()
        sUrl = oInputParameterHandler.getValue('siteUrl')

    oParser = cParser() 
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
    if isMatrix(): 
       sHtmlContent = str(sHtmlContent.encode('latin-1',errors='ignore'),'utf-8',errors='ignore')

    sStart = '<div class="subHead">'
    sEnd = '<div class="container">'
    sHtmlContentX = oParser.abParse(sHtmlContent, sStart, sEnd)
    oOutputParameterHandler.addParameter('sHtmlContentX', sHtmlContentX)
    if not sSearch:
        oGui.addDir(SITE_IDENTIFIER, 'showWeek', 'الاكثر مشاهدة هذا الاسبوع', 'history.png', oOutputParameterHandler)
    
    sStart = 'id="postList">'
    sEnd = '</html>'
    sHtmlContent = oParser.abParse(sHtmlContent, sStart, sEnd)

    sPattern = '<div class="postDiv">.+?<a href="([^"]+)".+?data-src="([^"]+)".+?alt="([^"]+)'
    aResult = oParser.parse(sHtmlContent, sPattern)
    if aResult[0]:
        total = len(aResult[1])
        progress_ = progress().VScreate(SITE_NAME)
        for aEntry in aResult[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break
 
            sTitle = cUtil().CleanSeriesName(aEntry[2])
            sTitle = re.sub(r"S\d{1,2}", "", sTitle.replace("Season ","")).strip()
            siteUrl = aEntry[0]
            sThumb = aEntry[1].replace("(","").replace(")","")
            sDesc = ""

            oOutputParameterHandler.addParameter('siteUrl',siteUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oOutputParameterHandler.addParameter('sDesc', sDesc)
			
            oGui.addAnime(SITE_IDENTIFIER, 'showSeasons', sTitle, '', sThumb, sDesc, oOutputParameterHandler)

        progress_.VSclose(progress_)
 
        sNextPage = __checkForNextPage(sHtmlContent)
        if sNextPage:
            oOutputParameterHandler.addParameter('siteUrl', sNextPage)
            oGui.addDir(SITE_IDENTIFIER, 'showAnimes', '[COLOR teal]Next >>>[/COLOR]', 'next.png', oOutputParameterHandler)
 
    if not sSearch:
        oGui.setEndOfDirectory()
  
def showSeasons():
    oGui = cGui()
   
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')

    oParser = cParser() 
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    sPattern = '<div class="seasonDiv.+?window.location.href = ["\']([^"\']+)["\'].+?data-src="([^"]+)".+?alt="([^"]+)".+?<div class="title">(.+?)</div>'
    aResult = oParser.parse(sHtmlContent, sPattern)    
    if (aResult[0]):
        oOutputParameterHandler = cOutputParameterHandler() 
        for aEntry in aResult[1]:
            
            postid = aEntry[0]
            sSeason = aEntry[3].replace("موسم "," S")
            siteUrl = f'{URL_MAIN[:-1]}{postid}'
            sTitle = ("%s %s") % (cUtil().CleanSeriesName(aEntry[2]), sSeason)         
            sThumb = aEntry[1]
            sDesc = ""

            oOutputParameterHandler.addParameter('siteUrl', siteUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('postid', postid)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oGui.addSeason(SITE_IDENTIFIER, 'showEpisodes1', sTitle, '', sThumb, sDesc, oOutputParameterHandler)
    else:
        sNote = ''

        sStart = '<div class="epAll" id="epAll">'
        sEnd = '<div class="postShare">'
        sHtmlContent1 = oParser.abParse(sHtmlContent, sStart, sEnd).replace('class="active">', ">")

        sPattern = '<a href="([^<]+)".+?>([^<]+)</a>'
        aResult = oParser.parse(sHtmlContent1, sPattern)
        if aResult[0]:  
            oOutputParameterHandler = cOutputParameterHandler()                     
            for aEntry in aResult[1]:
    
                sTitle = aEntry[1].strip().replace("الحلقة ","E")
                sTitle = f'{sMovieTitle} {sTitle}'
                siteUrl = aEntry[0]
                sThumb = sThumb
                sDesc = sNote
                
                oOutputParameterHandler.addParameter('siteUrl',siteUrl)
                oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
                oOutputParameterHandler.addParameter('sThumb', sThumb)
                oGui.addEpisode(SITE_IDENTIFIER, 'showLink', sTitle, '', sThumb, sDesc, oOutputParameterHandler)
    
            sNextPage = __checkForNextPage(sHtmlContent)
            if sNextPage:
                oOutputParameterHandler = cOutputParameterHandler()
                oOutputParameterHandler.addParameter('siteUrl', sNextPage)
                oGui.addDir(SITE_IDENTIFIER, 'showEpisodes', '[COLOR teal]Next >>>[/COLOR]', 'next.png', oOutputParameterHandler)      

    oGui.setEndOfDirectory() 
  
def showEpisodes():
    oGui = cGui()
   
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    postid = oInputParameterHandler.getValue('postid')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')

    oParser = cParser() 
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent2 = oRequestHandler.request()

    sStart = '<div class="epAll" id="epAll">'
    sEnd = '<div class="postShare">'
    sHtmlContent2 = oParser.abParse(sHtmlContent2, sStart, sEnd).replace('class="active">', ">")

    oRequestHandler = cRequestHandler(f'{URL_MAIN}/series-ajax/?_action=get_season_list&_post_id={postid}')
    oRequestHandler.addParameters('seasonID', postid)
    oRequestHandler.setRequestType(1)
    sHtmlContent = oRequestHandler.request()

    if sHtmlContent:
       sPattern = r'<a href="([^"]+)"\s*>([^<]+)</a>'
       aResult = oParser.parse(sHtmlContent,sPattern)
       if aResult[0]:
            for aEntry in aResult[1]:
                oOutputParameterHandler = cOutputParameterHandler() 
                if "العضوية" in aEntry[1]:
                    continue
 
                sTitle = aEntry[1].replace("الحلقة ","E")
                sTitle = f'{sMovieTitle} {sTitle}'
                siteUrl = aEntry[0].replace(' class="active"', "").replace('"', "") 
                sThumb = sThumb
                sDesc = ""

                oOutputParameterHandler.addParameter('siteUrl', siteUrl)
                oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
                oOutputParameterHandler.addParameter('sThumb', sThumb)
          
                oGui.addEpisode(SITE_IDENTIFIER, 'showLink', sTitle, '', sThumb, sDesc, oOutputParameterHandler)

    else :
       sPattern = r'<a href="([^"]+)"\s*>([^<]+)</a>'
       aResult = oParser.parse(sHtmlContent2,sPattern)
       if aResult[0]:
            for aEntry in aResult[1]:
                oOutputParameterHandler = cOutputParameterHandler() 
                if "العضوية" in aEntry[1]:
                    continue
 
                sTitle = aEntry[1].strip().replace("الحلقة ","E")
                sTitle = f'{sMovieTitle} {sTitle}'
                siteUrl = aEntry[0]
                sThumb = sThumb
                sDesc = ""

                oOutputParameterHandler.addParameter('siteUrl', siteUrl)
                oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
                oOutputParameterHandler.addParameter('sThumb', sThumb)
           
                oGui.addEpisode(SITE_IDENTIFIER, 'showLink', sTitle, '', sThumb, sDesc, oOutputParameterHandler)
       
    oGui.setEndOfDirectory() 

def showEpisodes1():
    oGui = cGui()
    
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')

    oParser = cParser() 
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    sNote = ''

    sStart = '<div class="epAll" id="epAll">'
    sEnd = '<div class="postShare">'
    sHtmlContent1 = oParser.abParse(sHtmlContent, sStart, sEnd).replace('class="active">', ">")

    sPattern = r'<a href="([^"]+)"\s*>([^<]+)</a>'
    aResult = oParser.parse(sHtmlContent1, sPattern)
    if aResult[0]:  
        oOutputParameterHandler = cOutputParameterHandler()                     
        for aEntry in aResult[1]:
 
            sTitle = aEntry[1].strip().replace("الحلقة ","E")
            sTitle = f'{sMovieTitle} {sTitle}'
            siteUrl = aEntry[0]
            sThumb = sThumb
            sDesc = sNote
			
            oOutputParameterHandler.addParameter('siteUrl',siteUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oGui.addEpisode(SITE_IDENTIFIER, 'showLink', sTitle, '', sThumb, sDesc, oOutputParameterHandler)
 
        sNextPage = __checkForNextPage(sHtmlContent)
        if sNextPage:
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sNextPage)
            oGui.addDir(SITE_IDENTIFIER, 'showEpisodes', '[COLOR teal]Next >>>[/COLOR]', 'next.png', oOutputParameterHandler)
       
    oGui.setEndOfDirectory()
	
def showLink():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')

    if addon().getSetting('Use_alternative') == "true":
        sUrl = sHost + "/".join(sUrl.split("/")[3:]) if sUrl.startswith("https://") else sUrl

    oParser = cParser()    
    oRequestHandler = cRequestHandler(sUrl)
    oRequestHandler.enableCache(False)
    sHtmlContent = oRequestHandler.request()

    sPattern = 'player_iframe.location.href = ["\']([^"\']+)["\'].+?</i>(.+?)</a>'
    aResult = oParser.parse(sHtmlContent, sPattern)	
    if aResult[0]:
        for aEntry in aResult[1]:

            sHosterUrl = aEntry[0]
            sHoster = aEntry[1]
            sTitle = f'{sMovieTitle} ({sHoster})'
            oHoster = cHosterGui().getHoster('faselhd') 
            if oHoster:
                oHoster.setDisplayName(sTitle)
                oHoster.setFileName(sMovieTitle)
                cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb)            

    oGui.setEndOfDirectory()       
  
def __checkForNextPage(sHtmlContent):
    sHtmlContent = sHtmlContent.replace('&rsaquo;','›')
    oParser = cParser()
    sPattern = 'href=["\']([^"\']+)["\']>›</a>'
    aResult = oParser.parse(sHtmlContent, sPattern) 
    if aResult[0]:
        return aResult[1][0]
    else:
        sPattern = 'rel="next" href=["\']([^"\']+)["\']\s*/>'
        aResult = oParser.parse(sHtmlContent, sPattern) 
        if aResult[0]:
            return aResult[1][0]
        
    return False

def decode_page(data):
    t_script = re.findall('var adilbo.*?;.*?\'(.*?);', data, re.S)
    t_int = re.findall('/g.....(.*?)\)', data, re.S)
    if t_script and t_int:
        script = t_script[0].replace("'",'')
        script = script.replace("+",'')
        script = script.replace("\n",'')
        sc = script.split('.')
        page = ''
        for elm in sc:
            try:
                c_elm = base64.b64decode(elm + "==").decode('utf-8')
                t_ch = re.findall(r"(\d+)", c_elm)
                if t_ch:
                    nb = int(t_ch[0]) + int(t_int[0] if t_int[0] != '' else t_int[1])
                    page += chr(nb)
            except Exception:
                continue
        
        return page
    else:
        return ""
