# -*- coding: utf-8 -*-

import re
from resources.lib.util import urlHostName
from resources.lib.gui.hoster import cHosterGui
from resources.lib.gui.gui import cGui
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.lib.comaddon import progress, VSlog, siteManager, addon
from resources.lib import random_ua

UA = random_ua.get_phone_ua()

SITE_IDENTIFIER = 'ultram'
SITE_NAME = 'UltraMovies'
SITE_DESC = ''

URL_MAIN = 'https://uhdmovies.email/'
oRequestHandler = cRequestHandler(f"https://modflix.xyz/?type=uhdmovies")
uhdmoviesAPI = oRequestHandler.request()
meta_start = uhdmoviesAPI.find('<meta http-equiv="refresh"')
if meta_start != -1:
    content_start = uhdmoviesAPI.find('content="', meta_start) + len('content="')
    content_end = uhdmoviesAPI.find('"', content_start)
    URL_MAIN = uhdmoviesAPI[content_start:content_end].split("url=")[-1] + '/'

MOVIE_4K = (f'{URL_MAIN}movies/', 'showMovies')
MOVIE_EN = (f'{URL_MAIN}movies/english-movies/', 'showMovies')

SERIE_EN = (f'{URL_MAIN}web-series/', 'showSeries')

URL_SEARCH_MOVIES = (f'{URL_MAIN}search/', 'showMovies')
URL_SEARCH_SERIES = (f'{URL_MAIN}search/', 'showSeries')
FUNCTION_SEARCH = 'showMovies'

def load():
    oGui = cGui()
    addons = addon()

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'http://')
    oGui.addDir(SITE_IDENTIFIER, 'showSearch', addons.VSlang(30078), '1/Search.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', 'http://venom/')
    oGui.addDir(SITE_IDENTIFIER, 'showSeriesSearch', addons.VSlang(30079), '1/Search.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', MOVIE_EN[0])
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'أفلام أجنبية', '1/Movies.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', MOVIE_4K[0])
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', ' 4k أفلام', '4k.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', SERIE_EN[0])
    oGui.addDir(SITE_IDENTIFIER, 'showSeries', 'مسلسلات أجنبية', '1/Movies.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()

def showSearch():
    oGui = cGui()
 
    sSearchText = oGui.showKeyBoard()
    if sSearchText:
        sUrl = f'{URL_MAIN}search/{sSearchText}'
        showMovies(sUrl)
        oGui.setEndOfDirectory()
        return

def showSeriesSearch():
    oGui = cGui()

    sSearchText = oGui.showKeyBoard()
    if sSearchText is not False:
        sUrl = f'{URL_MAIN}search/'+sSearchText
        showSeries(sUrl)
        oGui.setEndOfDirectory()
        return

def showMovies(sSearch = ''):
    oGui = cGui()
    if sSearch:
      sUrl = sSearch.replace(' ','+')
      
    else:
        oInputParameterHandler = cInputParameterHandler()
        sUrl = oInputParameterHandler.getValue('siteUrl')

    oParser = cParser()
    oRequestHandler = cRequestHandler(sUrl)
    oRequestHandler.addHeaderEntry('User-Agent', UA)
    sHtmlContent = oRequestHandler.request()

    sPattern = '<div class="entry-image">.+?href="([^"]+)"\s*title="([^"]+)".+?src="([^"]+)'
    aResult = oParser.parse(sHtmlContent, sPattern)
    if aResult[0]:
        total = len(aResult[1])
        progress_ = progress().VScreate(SITE_NAME)
        oOutputParameterHandler = cOutputParameterHandler()    
        for aEntry in aResult[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break

            if 'season' in aEntry[1].lower():
                continue

            sTitle = aEntry[1]
            sTitle, sDesc = extract_movie_info(sTitle)
            siteUrl = aEntry[0]
            sThumb = aEntry[2]
            sThumb = re.sub(r'-\d*x\d*.','.', sThumb)
            sYear = ''

            oOutputParameterHandler.addParameter('siteUrl', siteUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oOutputParameterHandler.addParameter('sYear', sYear)
            oOutputParameterHandler.addParameter('sDesc', sDesc)
            
            oGui.addMovie(SITE_IDENTIFIER, 'showHosters', sTitle, '', sThumb, sDesc, oOutputParameterHandler)

        progress_.VSclose(progress_)
 
    if not sSearch:
        sPattern = 'class="page-numbers" href="([^"]+)".+?link="internal">([^<]+)</a>'
        aResult = oParser.parse(sHtmlContent, sPattern)
        if aResult[0]:
            oOutputParameterHandler = cOutputParameterHandler()
            for aEntry in aResult[1]:
    
                sTitle = f'[COLOR red]Page: {aEntry[1]}[/COLOR]'
                siteUrl = aEntry[0]

                oOutputParameterHandler.addParameter('siteUrl',siteUrl)
                oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
                
                oGui.addDir(SITE_IDENTIFIER, 'showMovies', sTitle, 'next.png', oOutputParameterHandler)

        oGui.setEndOfDirectory()  

def showSeries(sSearch = ''):
    oGui = cGui()
    if sSearch:
      sUrl = sSearch.replace(' ','+')
      
    else:
        oInputParameterHandler = cInputParameterHandler()
        sUrl = oInputParameterHandler.getValue('siteUrl')

    oParser = cParser()
    oRequestHandler = cRequestHandler(sUrl)
    oRequestHandler.addHeaderEntry('User-Agent', UA)
    sHtmlContent = oRequestHandler.request()

    sPattern = '<div class="entry-image">.+?href="([^"]+)"\s*title="([^"]+)".+?src="([^"]+)'
    aResult = oParser.parse(sHtmlContent, sPattern)
    if aResult[0]:
        total = len(aResult[1])
        progress_ = progress().VScreate(SITE_NAME)
        oOutputParameterHandler = cOutputParameterHandler()    
        for aEntry in aResult[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break

            if 'season' not in aEntry[1].lower():
                continue

            sTitle = aEntry[1]
            sTitle, sDesc = extract_movie_info(sTitle)
            siteUrl = aEntry[0]
            sThumb = aEntry[2]
            sThumb = re.sub(r'-\d*x\d*.','.', sThumb)
            sYear = ''

            oOutputParameterHandler.addParameter('siteUrl', siteUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oOutputParameterHandler.addParameter('sYear', sYear)
            oOutputParameterHandler.addParameter('sDesc', sDesc)
            
            oGui.addMovie(SITE_IDENTIFIER, 'showSeasons', sTitle, '', sThumb, sDesc, oOutputParameterHandler)

        progress_.VSclose(progress_)
 
    if not sSearch:
        sPattern = 'class="page-numbers" href="([^"]+)".+?link="internal">([^<]+)</a>'
        aResult = oParser.parse(sHtmlContent, sPattern)
        if aResult[0]:
            oOutputParameterHandler = cOutputParameterHandler()
            for aEntry in aResult[1]:
    
                sTitle = f'[COLOR red]Page: {aEntry[1]}[/COLOR]'
                siteUrl = aEntry[0]

                oOutputParameterHandler.addParameter('siteUrl',siteUrl)
                oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
                
                oGui.addDir(SITE_IDENTIFIER, 'showSeries', sTitle, 'next.png', oOutputParameterHandler)

        oGui.setEndOfDirectory()  

def showSeasons():
    oGui = cGui()
    oOutputParameterHandler = cOutputParameterHandler() 
   
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')

    oParser = cParser()
 
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    sPattern = '((?:<strong>|<b>)((?:Season|SEASON|season).*?)(?:</strong>|</b>))'
    aResult = oParser.parse(sHtmlContent, sPattern)
    if aResult[0] is True:
        for aEntry in aResult[1]:

            sSeason = aEntry[1]
            sStart = aEntry[0]
            sSeason = sSeason.lower().replace('season','').strip()
            sTitle = f'{sMovieTitle} S{sSeason}'

            oOutputParameterHandler.addParameter('siteUrl', sUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sSeason', sSeason)
            oOutputParameterHandler.addParameter('sStart', sStart)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
 
            oGui.addSeason(SITE_IDENTIFIER, 'showEps', sTitle, '', sThumb, '', oOutputParameterHandler)

    else:
        sSeason = '1'
        if 'season' not in sMovieTitle.lower():
            sTitle = f'{sMovieTitle} S{sSeason}'
        else:
            sTitle = f'{sMovieTitle}'
        sThumb = sThumb
        sDesc = ''

        oOutputParameterHandler.addParameter('siteUrl', sUrl)
        oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
        oOutputParameterHandler.addParameter('sSeason', sSeason)
        oOutputParameterHandler.addParameter('sThumb', sThumb)

        oGui.addSeason(SITE_IDENTIFIER, 'showEps', sTitle, '', sThumb, sDesc, oOutputParameterHandler)
       
    oGui.setEndOfDirectory() 

def showEps():
    oGui = cGui()
   
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sSeason = oInputParameterHandler.getValue('sSeason')
    sStart = oInputParameterHandler.getValue('sStart')
    sThumb = oInputParameterHandler.getValue('sThumb')

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    sDesc = ''
    oParser = cParser()
    sStart = f'{sStart}'
    sEnd = '<p style="text-align: center;"><div class="mks_separator" style="border-bottom: 5px solid;">'
    sHtmlContent1 = oParser.abParse(sHtmlContent, sStart, sEnd)
    
    if sStart in sHtmlContent1:
        if 'Choose Episode Number to Download' not in sHtmlContent1:
            sStart = f'{sStart}<'
            sEnd = '<div class="gridlove-author">'
            sHtmlContent1 = oParser.abParse(sHtmlContent, sStart, sEnd)
    

    sNo = sSeason
    sQual = re.search(r'\b(2160p|1080p|720p|480p|4K|HD|SD)\b', sHtmlContent1, re.IGNORECASE).group(1) if re.search(r'\b(2160p|1080p|720p|480p|4K|HD|SD)\b', sHtmlContent1, re.IGNORECASE) else 'Unknown'
    sDesc = 'Details: \n' + " ".join(re.findall(r'\b(S\d{2}|E\d{2}|2160p|1080p|720p|480p|4K|10bit|HDR|WEB-DL|BluRay|x265|HEVC|DDP5\.1|Atmos|60FPS)\b', sHtmlContent1.replace(".", " "), re.IGNORECASE))
    sSize = (lambda match: match.group(1) if match else sHtmlContent1)(re.search(r'\b([\d.]+\s*(?:GB|MB))\b', sHtmlContent1))
    
    sPattern = 'href="([^"]+)".+?class=\'mb-text\'>(.+?)</span>'
    aResult = oParser.parse(sHtmlContent1, sPattern)  
    if aResult[0]:
        oOutputParameterHandler = cOutputParameterHandler() 
        for aEntry in aResult[1]:
            if 'zip' in aEntry[1].lower():
                continue
            sEp = aEntry[1]
            sHosterUrl = aEntry[0]

            sTitle = f'{sMovieTitle} S{sNo} {sEp} ({sQual} - {sSize})'

            oOutputParameterHandler.addParameter('siteUrl', sUrl)
            oOutputParameterHandler.addParameter('sHosterUrl', sHosterUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
        
            oGui.addEpisode(SITE_IDENTIFIER, 'showLinks', sTitle, '', sThumb, sDesc, oOutputParameterHandler)
    else:
        sPattern = 'title="Choose Episode Number to Download".+?href="([^"]+)".+?class=\'mb-text\'>(.+?)</span>'
        aResult = oParser.parse(sHtmlContent, sPattern)  
        if aResult[0]:
            oOutputParameterHandler = cOutputParameterHandler() 
            for aEntry in aResult[1]:
                if 'zip' in aEntry[1].lower():
                    continue
                sEp = aEntry[1]
                sHosterUrl = aEntry[0]

                sTitle = f'{sMovieTitle} S{sNo} {sEp}'

                oOutputParameterHandler.addParameter('siteUrl', sUrl)
                oOutputParameterHandler.addParameter('sHosterUrl', sHosterUrl)
                oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
                oOutputParameterHandler.addParameter('sThumb', sThumb)
            
                oGui.addEpisode(SITE_IDENTIFIER, 'showLinks', sTitle, '', sThumb, sDesc, oOutputParameterHandler)

    oGui.setEndOfDirectory() 

def showHosters():
    oGui = cGui()
    oParser = cParser()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')

    oParser = cParser()
    oRequestHandler = cRequestHandler(sUrl)
    oRequestHandler.addHeaderEntry('User-Agent', UA)
    sHtmlContent = oRequestHandler.request()

    sPattern = r'<p style="text-align: center;">.*?<span style=\"color: #000000;\">(.*?)</span>.*?href="(.*?)"'
    aResult = oParser.parse(sHtmlContent, sPattern)
    if aResult[0] :
        oOutputParameterHandler = cOutputParameterHandler()     
        for aEntry in aResult[1]:
            sTitle = aEntry[0]
            sHosterUrl = aEntry[1]
            sLabel, sQual = extract_movie_info(sTitle)

            sDisplayTitle = f'{sMovieTitle} [COLOR coral] {sQual}[/COLOR]'      
            oOutputParameterHandler.addParameter('sHosterUrl', sHosterUrl)
            oOutputParameterHandler.addParameter('siteUrl', sUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sMovieTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)

            oGui.addLink(SITE_IDENTIFIER, 'showLinks', sDisplayTitle, sThumb, sDisplayTitle, oOutputParameterHandler)               

    oGui.setEndOfDirectory()

def showLinks():
    oGui = cGui()

    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sHosterUrl = oInputParameterHandler.getValue('sHosterUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')

    oParser = cParser()
    if "driveleech" in sHosterUrl:
        redirect_url = sHosterUrl
        oRequestHandler = cRequestHandler(sHosterUrl)
        oRequestHandler.addHeaderEntry('User-Agent', UA)
        sHtmlContent = oRequestHandler.request()    
        match = re.search(r'window\.location\.replace\(["\'](.*?)["\']\)', sHtmlContent)

        file_id = match.group(1)
        newURL = f'https://{urlHostName(sHosterUrl)}' + file_id

        oRequestHandler = cRequestHandler(newURL)
        oRequestHandler.addHeaderEntry('User-Agent', UA)
        sHtmlContent = oRequestHandler.request()  

        sStart = '<div class="card-body">'
        sEnd = '<script'
        sHtmlContent = oParser.abParse(sHtmlContent, sStart, sEnd)

        sPattern = '<a href="([^"]+)".+?</i>(.+?)</a>'
        aResult = oParser.parse(sHtmlContent, sPattern)
        if aResult[0] :
            oOutputParameterHandler = cOutputParameterHandler()     
            for aEntry in aResult[1]:
                if 'login' in aEntry[1].lower():
                    continue

                sTitle = aEntry[1]
                sHosterUrl = aEntry[0]
                if sHosterUrl.startswith("/"):
                    sHosterUrl = f"https://{urlHostName(redirect_url)}{sHosterUrl}"

                sDisplayTitle = f'{sMovieTitle} [COLOR coral] {sTitle}[/COLOR]'      
                oOutputParameterHandler.addParameter('sHosterUrl', sHosterUrl)
                oOutputParameterHandler.addParameter('siteUrl', sUrl)
                oOutputParameterHandler.addParameter('dTitle', sTitle)
                oOutputParameterHandler.addParameter('sMovieTitle', sMovieTitle)
                oOutputParameterHandler.addParameter('sThumb', sThumb)

                oGui.addLink(SITE_IDENTIFIER, 'showLink', sDisplayTitle, sThumb, sDisplayTitle, oOutputParameterHandler)        


    else:
        oRequestHandler = cRequestHandler(f'https://{urlHostName(sHosterUrl)}/')
        oRequestHandler.addHeaderEntry('Host', urlHostName(sHosterUrl))
        oRequestHandler.addHeaderEntry('sec-fetch-dest', 'document')
        oRequestHandler.addHeaderEntry('sec-fetch-mode', 'navigate')
        oRequestHandler.addHeaderEntry('sec-fetch-site', 'same-origin')
        oRequestHandler.addHeaderEntry('User-Agent', UA)
        oRequestHandler.addParameters('_wp_http', sHosterUrl.split('?sid=')[1])
        oRequestHandler.setRequestType(1)
        sHtmlContent = oRequestHandler.request()

    regex = r'<form.*?action="([^"]*)".*?name="_wp_http2".*?value="([^"]*)".*?name="token".*?value="([^"]*)"'
    match = re.search(regex, sHtmlContent, re.DOTALL)
    if match:
        action = match.group(1)
        wp_http2 = match.group(2)
        token = match.group(3)

        oRequestHandler = cRequestHandler(action)
        oRequestHandler.addHeaderEntry('Origin', f'https://{urlHostName(sHosterUrl)}')
        oRequestHandler.addHeaderEntry('Referer', f'https://{urlHostName(sHosterUrl)}/')
        oRequestHandler.addHeaderEntry('User-Agent', UA)
        oRequestHandler.addParameters('_wp_http2', wp_http2)
        oRequestHandler.addParameters('token', token)
        oRequestHandler.setRequestType(1)
        sHtmlContent = oRequestHandler.request()

        sPattern = r'"([^"]*\?go=[^"]*)"'
        match = re.search(sPattern, sHtmlContent)
        pepe_url = match.group(1) if match else None

        oRequestHandler = cRequestHandler(pepe_url)
        oRequestHandler.addHeaderEntry('Host', urlHostName(sHosterUrl))
        oRequestHandler.addHeaderEntry('Referer', action)
        oRequestHandler.addHeaderEntry('User-Agent', UA)
        if '?go=' in pepe_url:
            key = str(pepe_url.split('?go=')[1])
            oRequestHandler.addCookieEntry(key, wp_http2)
        oRequestHandler.addCookieEntry('__eoi', "ID=6694a1c80224f93f:T=1746700975:RT=1746700975:S=AA-AfjYuMWlptbrRceUcGojMokCC")
        sHtmlContent = oRequestHandler.request()

        sPattern = r'<meta\s+http-equiv="refresh"\s+content="0;url=(.*?)"\s*/?>'
        match = re.search(sPattern, sHtmlContent)
        if match:
            redirect_url = match.group(1)
        
            oRequestHandler = cRequestHandler(redirect_url)
            oRequestHandler.addHeaderEntry('Origin', f'https://{urlHostName(redirect_url)}')
            oRequestHandler.addHeaderEntry('Referer', f'https://{urlHostName(redirect_url)}/')
            oRequestHandler.addHeaderEntry('User-Agent', UA)
            sHtmlContent = oRequestHandler.request()

            sPattern = r'/file/([a-zA-Z0-9]+)'
            matches = re.search(sPattern, sHtmlContent)
            if matches:
                file_id = matches.group(1)

                oRequestHandler = cRequestHandler(f"https://{urlHostName(redirect_url)}/file/{file_id}")
                oRequestHandler.addHeaderEntry('Origin', f'https://{urlHostName(redirect_url)}')
                oRequestHandler.addHeaderEntry('Referer', f'https://{urlHostName(redirect_url)}/')
                oRequestHandler.addHeaderEntry('User-Agent', UA)
                sHtmlContent = oRequestHandler.request()

                sStart = '<div class="card-body">'
                sEnd = '<script'
                sHtmlContent = oParser.abParse(sHtmlContent, sStart, sEnd)

                sPattern = '<a href="([^"]+)".+?</i>(.+?)</a>'
                aResult = oParser.parse(sHtmlContent, sPattern)
                if aResult[0] :
                    oOutputParameterHandler = cOutputParameterHandler()     
                    for aEntry in aResult[1]:
                        if 'login' in aEntry[1].lower():
                            continue

                        sTitle = aEntry[1]
                        sHosterUrl = aEntry[0]
                        if sHosterUrl.startswith("/"):
                                sHosterUrl = f"https://{urlHostName(redirect_url)}{sHosterUrl}"

                        sDisplayTitle = f'{sMovieTitle} [COLOR coral] {sTitle}[/COLOR]'      
                        oOutputParameterHandler.addParameter('sHosterUrl', sHosterUrl)
                        oOutputParameterHandler.addParameter('siteUrl', sUrl)
                        oOutputParameterHandler.addParameter('dTitle', sTitle)
                        oOutputParameterHandler.addParameter('sMovieTitle', sMovieTitle)
                        oOutputParameterHandler.addParameter('sThumb', sThumb)

                        oGui.addLink(SITE_IDENTIFIER, 'showLink', sDisplayTitle, sThumb, sDisplayTitle, oOutputParameterHandler)                

    oGui.setEndOfDirectory()

def showLink():
    oGui = cGui()

    oInputParameterHandler = cInputParameterHandler()
    sHosterUrl = oInputParameterHandler.getValue('sHosterUrl')
    sUrl = oInputParameterHandler.getValue('siteUrl')
    dTitle = oInputParameterHandler.getValue('dTitle')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')

    if 'instant' in dTitle.lower():
        url = "video-leech.pro" if "video-leech" in sHosterUrl else "video-seed.pro"
        token = sHosterUrl.split("url=")[-1]

        oRequestHandler = cRequestHandler(f"https://{url}/api")
        oRequestHandler.addHeaderEntry("x-token", url)
        oRequestHandler.addHeaderEntry('Origin', f'https://{urlHostName(sHosterUrl)}')
        oRequestHandler.addHeaderEntry('Referer', sHosterUrl)
        oRequestHandler.addHeaderEntry('User-Agent', UA)
        oRequestHandler.addParameters('keys', token)
        oRequestHandler.setRequestType(1)
        sHtmlContent = oRequestHandler.request()

        try:
            sHosterUrl = sHtmlContent.split('url":"')[1].split('","name')[0].replace("\\/", "/")
        except:
            sHosterUrl = ''

    elif 'multiup' in dTitle.lower():
        from resources.lib.multihost import cMultiup
        data = cMultiup().GetUrls(sHosterUrl)
        if data is not False:
            for item in data:
                sHosterUrl = item.split(',')[0].split('=')[1]
                sLabel = item.split('label=')[1]
                sMovieTitle = f'{sMovieTitle} [COLOR orange] -{sLabel}[/COLOR]'   

                oHoster = cHosterGui().checkHoster(sHosterUrl)
                if oHoster:
                    oHoster.setDisplayName(sMovieTitle)
                    oHoster.setFileName(sMovieTitle)
                    cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb)

    else:
        from urllib.parse import quote
        oRequestHandler = cRequestHandler(f"{sHosterUrl}?type=1")
        oRequestHandler.addHeaderEntry('Origin', f'https://{urlHostName(sHosterUrl)}')
        oRequestHandler.addHeaderEntry('Referer', f'https://{urlHostName(sHosterUrl)}/')
        oRequestHandler.addHeaderEntry('User-Agent', "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36 Edg/136.0.0.0")
        sHtmlContent = oRequestHandler.request()

        href_link= re.findall(r'<a href="(https?://[^"]+)"\s*target="_blank"\s*class="btn btn-success"', sHtmlContent)
        for link in href_link:
                
            url_safe = quote(link.split('/')[-1], safe='')
            sHosterUrl = link.replace(link.split('/')[-1], url_safe)

        href_link= re.findall(r'<a href="(https?://[^"]+)"\s*type="button"\s*target="_blank"\s*class="btn btn-success"', sHtmlContent)
        for link in href_link:
                
            url_safe = quote(link.split('/')[-1], safe='')
            sHosterUrl = link.replace(link.split('/')[-1], url_safe)

            oHoster = cHosterGui().getHoster('directplay')
            if oHoster != False:
                oHoster.setDisplayName(sMovieTitle)
                oHoster.setFileName(sMovieTitle)
                cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb)

    oHoster = cHosterGui().checkHoster(sHosterUrl)
    if oHoster != False:
        oHoster.setDisplayName(sMovieTitle)
        oHoster.setFileName(sMovieTitle)
        cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb)

    oGui.setEndOfDirectory()

def extract_movie_info(movie_string):
    quality_pattern = r"(?:\b\d{3,4}p\b|\b4k\b|\b10bit\b|\bHDR\b|\bDoVi\b|\bBluray\b|\bBluRay\b|\bBlu-ray\b|\bWEB-DL\b|\bHEVC\b|\bREMUX\b|\bx264\b|\bx265\b|\bDV HDR\b|\bSD\b|\bHD\b|\bSDR\b|\b10Bit\b)"
    
    qualities = list(set(re.findall(quality_pattern, movie_string, re.IGNORECASE)))
    qualities = sorted(qualities, key=str.lower, reverse=True) 
    
    name = re.sub(quality_pattern, "", movie_string, flags=re.IGNORECASE)
    name = re.sub(r"(Download|Dual Audio|Multi Audio|\[.*?\]|\(Season .*?\)|\{.*?\}|Esubs|[\|\-]+)", "", name, flags=re.IGNORECASE).strip()
    name = re.sub(r"\s+", " ", name)
    name = re.sub(r"(\d{4})(\d{4})", r"\1-\2", name)
    name = re.sub(r"\((\d{4}-\d{4})\)", r"\1", name)

    return name, " | ".join(qualities)
