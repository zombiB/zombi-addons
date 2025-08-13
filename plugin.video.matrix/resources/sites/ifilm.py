# -*- coding: utf-8 -*-

import re
from resources.lib.gui.hoster import cHosterGui
from resources.lib.gui.gui import cGui
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.comaddon import progress, VSlog, siteManager
from resources.lib.parser import cParser
from resources.lib.util import Quote
from resources.lib import random_ua

UA = random_ua.get_phone_ua()

SITE_IDENTIFIER = 'ifilm'
SITE_NAME = 'iFilm'
SITE_DESC = 'farsi vod'

URL_MAIN = siteManager().getUrlMain(SITE_IDENTIFIER)

SERIE_IR = (f'{URL_MAIN}Series', 'showSeries')
REPLAYTV_NEWS = (f'{URL_MAIN}Home/PageingItem?category=7&size=150&orderby=1&page=1', 'showPrograms')

def load():
    oGui = cGui()

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', SERIE_IR[0])
    oGui.addDir(SITE_IDENTIFIER, 'showSeries', 'مسلسلات أجنبية', '1/Movies.png', oOutputParameterHandler)
    
    oOutputParameterHandler.addParameter('siteUrl', REPLAYTV_NEWS[0])
    oGui.addDir(SITE_IDENTIFIER, 'showPrograms', 'برامج تلفزيونية', '1/Programs.png', oOutputParameterHandler) 

    oGui.setEndOfDirectory()
	
def showMovies():
    oGui = cGui()
    oOutputParameterHandler = cOutputParameterHandler()
    
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')

    oParser = cParser() 
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
   
    sStart = 'class="row All-Film-body">'
    sEnd = '<ul id="pagination'
    sHtmlContent1 = oParser.abParse(sHtmlContent, sStart, sEnd)

    sPattern = '<a href="([^"]+)".+?src=["\']([^"\']+)["\'].+?<h6>(.+?)</h6'
    aResult = oParser.parse(sHtmlContent1, sPattern)	
    if aResult[0]:
        total = len(aResult[1])
        progress_ = progress().VScreate(SITE_NAME)
        for aEntry in aResult[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break
            if '/Film/' not in aEntry[0]:
                continue

            sTitle = aEntry[2]
            siteUrl = f'{URL_MAIN}{aEntry[0]}'
            sThumb = f'{URL_MAIN}{Quote(aEntry[1].replace("SmallSize/",""))}'
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

            oGui.addMovie(SITE_IDENTIFIER, 'showLink', sTitle, '', sThumb, sDesc, oOutputParameterHandler)

        progress_.VSclose(progress_)

        sNextPage = __checkForNextPage(sHtmlContent)
        if sNextPage:
            oOutputParameterHandler = cOutputParameterHandler()
            if 'page=' in sNextPage:
                sNextPage = re.sub(r'page=(\d+)', lambda m: f'page={int(m.group(1))+1}', sNextPage)
            else:
                sNextPage = f'{sNextPage}&page=2'
            oOutputParameterHandler.addParameter('siteUrl', sNextPage)
            oGui.addDir(SITE_IDENTIFIER, 'showMovies', '[COLOR teal]Next >>>[/COLOR]', 'next.png', oOutputParameterHandler)
 
    oGui.setEndOfDirectory()

def showPrograms():
    oGui = cGui()
    oOutputParameterHandler = cOutputParameterHandler()
    
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request(jsonDecode=True)
   
    for aEntry in sHtmlContent:
        sTitle = aEntry['Title']
        siteUrl = f"{URL_MAIN}Home/PageingAttachmentItem?id={aEntry['Id']}&page="
        sThumb = f'{URL_MAIN}{Quote(aEntry["ImageAddress_S"].replace("SmallSize/",""))}'
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

        oGui.addMovie(SITE_IDENTIFIER, 'showEps', sTitle, '', sThumb, sDesc, oOutputParameterHandler)

    oGui.setEndOfDirectory()

def showSeries():
    oGui = cGui()
    oOutputParameterHandler = cOutputParameterHandler()

    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    oParser = cParser() 
    
    sStart = 'class="row All-Film-body Serial">'
    sEnd = '<ul id="pagination'
    sHtmlContent1 = oParser.abParse(sHtmlContent, sStart, sEnd)

    sPattern = '<a href="([^"]+)".+?src=["\']([^"\']+)["\'].+?<h6>(.+?)</h6'
    aResult = oParser.parse(sHtmlContent1, sPattern)	
    itemList = []
    if aResult[0]:
        total = len(aResult[1])
        progress_ = progress().VScreate(SITE_NAME)
        oOutputParameterHandler = cOutputParameterHandler() 
        for aEntry in aResult[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break
            
            if '/series/' not in aEntry[0]:
                continue

            sTitle = aEntry[2]
            siteUrl = f'{URL_MAIN}{aEntry[0]}'
            sThumb = f'{URL_MAIN}{Quote(aEntry[1].replace("SmallSize/",""))}'
            sDesc = ''
            sYear = ''
            m = re.search('([0-9]{4})', sTitle)
            if m:
                sYear = str(m.group(0))

            if sTitle not in itemList:
                itemList.append(sTitle)	
                oOutputParameterHandler.addParameter('siteUrl', siteUrl)
                oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
                oOutputParameterHandler.addParameter('sThumb', sThumb)
                oOutputParameterHandler.addParameter('sDesc', sDesc)
                
                oGui.addTV(SITE_IDENTIFIER, 'showEpisodes', sTitle, '', sThumb, sDesc, oOutputParameterHandler)

        progress_.VSclose(progress_)
 
        sNextPage = __checkForNextPage(sHtmlContent)
        if sNextPage:
            if 'page=' in sNextPage:
                sNextPage = re.sub(r'page=(\d+)', lambda m: f'page={int(m.group(1))+1}', sNextPage)
            else:
                sNextPage = f'{sNextPage}&page=2'
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sNextPage)
            oGui.addDir(SITE_IDENTIFIER, 'showSeries', '[COLOR teal]Next >>>[/COLOR]', 'next.png', oOutputParameterHandler)
 
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

    try:
        sPattern = r'var langE = ["\']([^"\']+)["\']'
        aResult = oParser.parse(sHtmlContent, sPattern) 
        if aResult[0]:
            sLang = aResult[1][0]

        sPattern = r'var ID_Serial =\s*(\d+);.*var inter_ =\s*(\d+);'
        aResult = oParser.parse(sHtmlContent, sPattern) 
        if aResult[0]:
            for aEntry in aResult[1]:
                sID = aEntry[0]
                sEPcount = aEntry[1]

        sPattern = r'data-video="([^"]+)"'
        aResult = oParser.parse(sHtmlContent, sPattern)
        if aResult[0]:  
            sLink = aResult[1][0].replace(" ", "").replace("'+", "{").replace("+'", "}").replace("+", "}{")
            oOutputParameterHandler = cOutputParameterHandler()
            sEpisode_list = list(range(1, int(sEPcount) + 1))
            for aEntry in sEpisode_list:
    
                sTitle = f'{sMovieTitle} E{aEntry}'
                siteUrl = f"{sLink}"
                siteUrl = siteUrl.format(langE=sLang, ID_Serial=sID, i=aEntry)
                sThumb = sThumb
                sThumb = sThumb
                sDesc = ''
                
                oOutputParameterHandler.addParameter('siteUrl',siteUrl)
                oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
                oOutputParameterHandler.addParameter('sThumb', sThumb)
                oGui.addEpisode(SITE_IDENTIFIER, 'showLink', sTitle, '', sThumb, sDesc, oOutputParameterHandler)
 
    except:
        oGui.addText(SITE_IDENTIFIER, '[COLOR orange] الموقع لم يرفع الحلقات [/COLOR]', 'none.png')

    oGui.setEndOfDirectory()

def showEps():
    oGui = cGui()
    
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')
    total_episodes = oInputParameterHandler.getValue('total_episodes')

    if '&size=50' not in sUrl:
        sUrl = f'{sUrl}1&size=50'
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request(jsonDecode=True)

    oOutputParameterHandler = cOutputParameterHandler()
    for aEntry in sHtmlContent:
    
        sTitle = f'{sMovieTitle} E{aEntry["Episode"]}'
        from six.moves import urllib_parse
        try:
            sVideo = urllib_parse.quote(aEntry["VideoAddress"], '/:')
        except:
            sVideo = aEntry["VideoAddress"]
        siteUrl = f'https://video.ifilmtv.ir/ifilm{sVideo}'
        sThumb = f'{URL_MAIN}{aEntry["ImageAddress_L"]}'
        sDesc = ''
        
        oOutputParameterHandler.addParameter('siteUrl',siteUrl)
        oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
        oOutputParameterHandler.addParameter('sThumb', sThumb)
        oGui.addEpisode(SITE_IDENTIFIER, 'showLink', sTitle, '', sThumb, sDesc, oOutputParameterHandler)

    for aEntry in sHtmlContent:
        total_episodes = aEntry["Episode"]

    oRequestHandler = cRequestHandler(f'{sUrl}1&size=1')
    sHtmlContent = oRequestHandler.request(jsonDecode=True)

    for aEntry in sHtmlContent:
        total_episodes = aEntry["Episode"]

    if 'PageingAttachmentItem' in sUrl:
        links = generate_links(total_episodes, sUrl)
        for aEntry in links:
            pTitle = f'[COLOR red]More Episodes[/COLOR]'
            siteUrl = aEntry
            sThumb = sThumb

            oOutputParameterHandler.addParameter('siteUrl', siteUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sMovieTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oOutputParameterHandler.addParameter('total_episodes', total_episodes)
                
            oGui.addDir(SITE_IDENTIFIER, 'showEps', pTitle, sThumb, oOutputParameterHandler)

    oGui.setEndOfDirectory()

def generate_links(total_episodes, base_link):
    episodes_per_page = 50

    episode_list_url = []
    total_pages = (total_episodes // episodes_per_page) + (1 if total_episodes % episodes_per_page > 0 else 0)
    for page_number in range(1, total_pages + 1):
        episode_list_url.append(base_link + str(page_number) + "&size=" + str(episodes_per_page))

    return episode_list_url

def showLink():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')

    oHoster = cHosterGui().checkHoster(sUrl)
    if oHoster != False:
        oHoster.setDisplayName(sMovieTitle)
        oHoster.setFileName(sMovieTitle)
        cHosterGui().showHoster(oGui, oHoster, sUrl, sThumb)

    oGui.setEndOfDirectory()       
  
def __checkForNextPage(sHtmlContent):
    oParser = cParser()
    if '<a>+</a>' in sHtmlContent:
        sPattern = '<meta name=["\']Uid["\'] content=["\']([^"\']+)["\']/>'
        aResult = oParser.parse(sHtmlContent, sPattern) 
        if aResult[0]:
            return f'{URL_MAIN}Home/PageingAttachmentItem?id={aResult[1][0]}&size=6'
        
    else:
        sPattern = '<meta name=["\']DC.Identifier["\'] content=["\']([^"\']+)["\']/>'
        aResult = oParser.parse(sHtmlContent, sPattern) 
        if aResult[0]:
            if 'page=' in aResult[1][0]:
                return aResult[1][0]
            return f'{aResult[1][0]}/?order=1'
    return False

