# -*- coding: utf-8 -*-

import re, json
from resources.lib.gui.hoster import cHosterGui
from resources.lib.gui.gui import cGui
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.comaddon import VSlog, siteManager
from resources.lib.parser import cParser
 
SITE_IDENTIFIER = 'asharq'
SITE_NAME = 'Al-Sharq'
SITE_DESC = 'arabic vod'
 
URL_MAIN = siteManager().getUrlMain(SITE_IDENTIFIER)

DOC_NEWS = (f'{URL_MAIN}/doc', 'showMovies')
DOC_SERIES = (f'{URL_MAIN}/doc', 'showMovies')
 
def load():
    oGui = cGui()
    
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', DOC_NEWS[0])
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'أفلام وثائقية', '1/Documentary.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()

def showMovies():
    oGui = cGui()

    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    pattern = r'<script id="__NEXT_DATA__" type="application/json">(.*?)</script>'
    match = re.search(pattern, sHtmlContent, re.DOTALL)
    if match:
        json_data = json.loads(match.group(1))
        sectionsHTML = json_data["props"]["pageProps"]["data"]

        oOutputParameterHandler = cOutputParameterHandler()  
        for aEntry in sectionsHTML["components"]:
            if aEntry["slug"] == '' or aEntry["slug"] is None:
                continue
            sectionURL = f'{URL_MAIN}/components/{aEntry["slug"]}'
            sectionTitle = '[COLOR orange]' + u'\u2193' + aEntry["title"] + '[/COLOR]'
            sectionHTML = aEntry["content"]

            oOutputParameterHandler.addParameter('siteUrl', sectionURL)
            oOutputParameterHandler.addParameter('sMovieTitle', sectionTitle)

            oGui.addMisc(SITE_IDENTIFIER, 'showSection', sectionTitle, '1/Documentary.png', 'https://nowcdn.asharq.com/184x0/14529253851720113239.png', '', oOutputParameterHandler)

            for aEntry in sectionHTML:

                sTitle = aEntry["title"]
                try:
                    sThumb = aEntry["logo"]
                except:
                    sThumb = aEntry["image"]["16-9"]["x-large"]
                if 'movie' in aEntry["type"]:
                    siteUrl = f'{URL_MAIN}/documentary/{aEntry["type"]}s/{aEntry["id"]}/{aEntry["slug"]}'
                else:
                    if aEntry["shortUrl"] is None:
                        siteUrl = f'{URL_MAIN}/documentary/{aEntry["type"]}s/{aEntry["slug"]}'
                    else:
                        siteUrl = aEntry["shortUrl"]
                sDesc = aEntry["description"]["short"]
                
                oOutputParameterHandler.addParameter('siteUrl', siteUrl)
                oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
                oOutputParameterHandler.addParameter('sThumb', sThumb)
                oOutputParameterHandler.addParameter('sDesc', sDesc)

                oGui.addMisc(SITE_IDENTIFIER, 'showHosters', sTitle, '', sThumb, sDesc, oOutputParameterHandler) 

            sNextPage = __checkForNextPage(sHtmlContent)
            if sNextPage:
                oOutputParameterHandler = cOutputParameterHandler()
                oOutputParameterHandler.addParameter('siteUrl', sNextPage)
                oGui.addDir(SITE_IDENTIFIER, 'showMovies', '[COLOR teal]Next >>>[/COLOR]', 'next.png', oOutputParameterHandler)

    oGui.setEndOfDirectory() 
    
def showSection():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    token = oInputParameterHandler.getValue('token')

    nUrl = sUrl
    if 'page=' not in sUrl:
        nUrl = sUrl.replace('components/','api/dynamic-pages/components/').replace('now.', 'api-now.') + '/?page=1&limit=12'
    
    oRequestHandler = cRequestHandler(nUrl)
    oRequestHandler.addHeaderEntry('Referer', 'https://now.asharq.com/')
    sHtmlContent = oRequestHandler.request(jsonDecode=True)

    if sHtmlContent:
        oOutputParameterHandler = cOutputParameterHandler() 
        for entry in sHtmlContent["data"]["content"]:

            sTitle = entry["title"]
            if 'movie' in entry["type"]:
                siteUrl = f'{URL_MAIN}/documentary/{entry["type"]}s/{entry["id"]}/{entry["slug"]}'
            else:
                if entry["shortUrl"] is None:
                    siteUrl = f'{URL_MAIN}/documentary/{entry["type"]}s/{entry["slug"]}'
                else:
                    siteUrl = entry["shortUrl"]
            try:
                sThumb = entry["logo"]
            except:
                sThumb = entry["image"]["16-9"]["x-large"]

            sDesc = entry["description"]["short"]
          
            oOutputParameterHandler.addParameter('siteUrl', siteUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oOutputParameterHandler.addParameter('sDesc', sDesc)

            oGui.addMisc(SITE_IDENTIFIER, 'showHosters', sTitle, '', sThumb, sDesc, oOutputParameterHandler) 

        sNextPage = __checkForNextjSonPage(nUrl)
        if sNextPage:
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sNextPage)
            oOutputParameterHandler.addParameter('token', token)
            oGui.addDir(SITE_IDENTIFIER, 'showSection', '[COLOR teal]Next >>>[/COLOR]', 'next.png', oOutputParameterHandler)
 
    oGui.setEndOfDirectory()
 
def __checkForNextPage(sHtmlContent):
    oParser = cParser()
    sPattern = '<li >.+?<a href="(.+?)">'
    aResult = oParser.parse(sHtmlContent, sPattern)
    if aResult[0]:    
        return f'{URL_MAIN}/{aResult[1][0]}'

    return False

def __checkForNextjSonPage(sUrl):
    from urllib.parse import urlparse, urlunparse

    parsed_url = urlparse(sUrl)
    query_parts = dict(qc.split("=") for qc in parsed_url.query.split("&"))
    if "page" in query_parts:
        page_number = int(query_parts["page"]) + 1
        query_parts["page"] = str(page_number)
        new_query = "&".join(f"{key}={value}" for key, value in query_parts.items())
        return urlunparse((parsed_url.scheme, parsed_url.netloc, parsed_url.path, parsed_url.params, new_query, parsed_url.fragment))

    return sUrl

def showHosters():
    oGui = cGui()
    
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    pattern = r'<script id="__NEXT_DATA__" type="application/json">(.*?)</script>'
    match = re.search(pattern, sHtmlContent, re.DOTALL)
    if match:
        json_data = json.loads(match.group(1))

        try:
            sectionsHTML = json_data["props"]["pageProps"]["data"]["video"]["sources"]

            for aEntry in sectionsHTML["HLS"]:

                url = aEntry["Link"]
                if url.startswith('//'):
                    url = f'http:{url}'
                sQual = aEntry["Name"]
                sTitle = f'{sMovieTitle} [COLOR coral]{sQual}[/COLOR]'
                    
                sHosterUrl = url			
                oHoster = cHosterGui().checkHoster(sHosterUrl)
                if oHoster:
                    oHoster.setDisplayName(sTitle)
                    oHoster.setFileName(sMovieTitle)
                    cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb)
        except:
            sectionsHTML = json_data["props"]["pageProps"]["episodes"]
            oOutputParameterHandler = cOutputParameterHandler() 
            for aEntry in sectionsHTML:

                sEp = aEntry["episodeNumber"]
                sEpName = aEntry["title"]
                sTitle = f'{sMovieTitle} E{sEp} ({sEpName})'
                siteUrl = aEntry["shortUrl"]
                try:
                    sThumb = aEntry["image"]["16-9"]["x-large"]
                except:
                    sThumb = aEntry["logo"]

                sDesc = aEntry["description"]["short"]

                oOutputParameterHandler.addParameter('siteUrl', siteUrl)
                oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
                oOutputParameterHandler.addParameter('sThumb', sThumb)
                    
                oGui.addEpisode(SITE_IDENTIFIER, 'showHosters', sTitle, '', sThumb, sDesc, oOutputParameterHandler)
               
    oGui.setEndOfDirectory()