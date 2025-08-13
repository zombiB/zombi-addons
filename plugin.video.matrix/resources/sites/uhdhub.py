# -*- coding: utf-8 -*-

import re, base64
from urllib.parse import urlparse
from resources.lib.gui.hoster import cHosterGui
from resources.lib.gui.gui import cGui
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.lib.comaddon import progress, VSlog, addon
from resources.lib import random_ua

UA = random_ua.get_phone_ua()

SITE_IDENTIFIER = 'uhdhub'
SITE_NAME = 'UltraHD Hub'
SITE_DESC = ''

URL_MAIN = 'https://4khdhub.fans/'
try:
    oRequestHandler = cRequestHandler("https://raw.githubusercontent.com/phisher98/TVVVV/refs/heads/main/domains.json")
    domains = oRequestHandler.request(jsonDecode=True)
    URL_MAIN = domains.get("4khdhub", URL_MAIN).rstrip('/') + '/'

except Exception as e:
    VSlog(f'Error {e}')
    URL_MAIN = URL_MAIN

EXTRACTORS = {
    "hubdrive.fit": ("Hubdrive", "https://hubdrive.fit"),
    "hubdrive.live": ("Hubdrivelive", "https://hubdrive.live"),
    "hubcloud.bz": ("Hub-Cloud", "https://hubcloud.bz"),
    "hubcloud.one": ("Hub-Cloud", "https://hubcloud.one"),
    "hubdrive.icu": ("Hubdrive", "https://hubdrive.icu"),
}

MOVIE_4K = (f'{URL_MAIN}category/4k-hdr-10776.html', 'showMovies')
MOVIE_EN = (f'{URL_MAIN}category/movies-10810.html', 'showMovies')

SERIE_EN = (f'{URL_MAIN}category/new-series-10811.html', 'showSeries')

URL_SEARCH_MOVIES = (f'{URL_MAIN}/?s=', 'showMovies')
URL_SEARCH_SERIES = (f'{URL_MAIN}/?s=', 'showSeries')
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
        sUrl = f'{URL_MAIN}/?s={sSearchText}'
        showMovies(sUrl)
        oGui.setEndOfDirectory()
        return

def showSeriesSearch():
    oGui = cGui()

    sSearchText = oGui.showKeyBoard()
    if sSearchText is not False:
        sUrl = f'{URL_MAIN}/?s={sSearchText}'
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

    sPattern = '<a href="([^"]+)"\s*class="movie-card">.+?<img src="([^"]+)"\s*alt="([^"]+)".+?<span class="movie-card-format">(.+?)</div>'
    aResult = oParser.parse(sHtmlContent, sPattern)
    if aResult[0]:
        total = len(aResult[1])
        progress_ = progress().VScreate(SITE_NAME)
        oOutputParameterHandler = cOutputParameterHandler()    
        for aEntry in aResult[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break
            if 'static-' in aEntry[0] or '>serie' in aEntry[3].lower():
                continue
            
            sTitle = aEntry[2]
            siteUrl = f'{URL_MAIN.rstrip("/") if aEntry[0].startswith("/") else URL_MAIN}{aEntry[0]}'
            sThumb = aEntry[1]
            sYear = ''
            sDesc = ''

            oOutputParameterHandler.addParameter('siteUrl', siteUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oOutputParameterHandler.addParameter('sYear', sYear)
            oOutputParameterHandler.addParameter('sDesc', sDesc)
            
            oGui.addMovie(SITE_IDENTIFIER, 'showHosters', sTitle, '', sThumb, sDesc, oOutputParameterHandler)

        progress_.VSclose(progress_)
 
    if not sSearch:
        sPattern = "<a href='([^']+)' class='pagination-item'>(.+?)</a>"
        aResult = oParser.parse(sHtmlContent, sPattern)
        if aResult[0]:
            oOutputParameterHandler = cOutputParameterHandler()
            for aEntry in aResult[1]:
    
                sTitle = f'[COLOR red]Page: {aEntry[1]}[/COLOR]'
                siteUrl = f'{URL_MAIN.rstrip("/") if aEntry[0].startswith("/") else URL_MAIN}{aEntry[0]}'

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

    sPattern = '<a href="([^"]+)"\s*class="movie-card">.+?<img src="([^"]+)"\s*alt="([^"]+)".+?<span class="movie-card-format">(.+?)</div>'
    aResult = oParser.parse(sHtmlContent, sPattern)
    if aResult[0]:
        total = len(aResult[1])
        progress_ = progress().VScreate(SITE_NAME)
        oOutputParameterHandler = cOutputParameterHandler()    
        for aEntry in aResult[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break
            if 'static-' in aEntry[0] or '>movie' in aEntry[3].lower():
                continue

            sTitle = aEntry[2]
            siteUrl = f'{URL_MAIN.rstrip("/") if aEntry[0].startswith("/") else URL_MAIN}{aEntry[0]}'
            sThumb = aEntry[1]
            sYear = ''
            sDesc = ''

            oOutputParameterHandler.addParameter('siteUrl', siteUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oOutputParameterHandler.addParameter('sYear', sYear)
            oOutputParameterHandler.addParameter('sDesc', sDesc)

            oGui.addTV(SITE_IDENTIFIER, 'showSeasons', sTitle, '', sThumb, sDesc, oOutputParameterHandler)

        progress_.VSclose(progress_)
 
    if not sSearch:
        sPattern = "<a href='([^']+)' class='pagination-item'>(.+?)</a>"
        aResult = oParser.parse(sHtmlContent, sPattern)
        if aResult[0]:
            oOutputParameterHandler = cOutputParameterHandler()
            for aEntry in aResult[1]:
    
                sTitle = f'[COLOR red]Page: {aEntry[1]}[/COLOR]'
                siteUrl = f'{URL_MAIN.rstrip("/") if aEntry[0].startswith("/") else URL_MAIN}{aEntry[0]}'

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

    sPattern = '<div class="episode-number">(.+?)</div>.+?<h3 class="episode-title">(.+?)</h3>'
    aResult = oParser.parse(sHtmlContent, sPattern)
    if aResult[0] is True:
        for aEntry in aResult[1]:

            sSeason = aEntry[0]
            sStart = aEntry[1]
            sQual = aEntry[1]
            sSeason = sSeason.lower().replace('s','').strip()
            sTitle = f'{sMovieTitle} S{sSeason} [{sQual}]'

            oOutputParameterHandler.addParameter('siteUrl', sUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sSeason', sSeason)
            oOutputParameterHandler.addParameter('sStart', sStart)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
 
            oGui.addSeason(SITE_IDENTIFIER, 'showEps', sTitle, '', sThumb, '', oOutputParameterHandler)
       
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
    sPattern = f'<h3 class="episode-title">{sStart}</h3>(.+?)</div>\s*</div>\s*</div>\s*</div>\s*</div>'
    aResult = oParser.parse(sHtmlContent, sPattern)
    if aResult[0] is True:
        for aEntry in aResult[1]:
            sHtmlContent1 = aEntry
    
    sPattern = '<span class="badge-psa">(.+?)</span>'
    aResult = oParser.parse(sHtmlContent1, sPattern)  
    if aResult[0]:
        oOutputParameterHandler = cOutputParameterHandler() 
        for aEntry in aResult[1]:

            sEp = aEntry
            eStart = aEntry
            sEp = sEp.lower().replace('episode','').replace('-','').strip()
            sTitle = f'{sMovieTitle} S{sSeason} E{sEp}'

            oOutputParameterHandler.addParameter('siteUrl', sUrl)
            oOutputParameterHandler.addParameter('sStart', sStart)
            oOutputParameterHandler.addParameter('eStart', eStart)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
        
            oGui.addEpisode(SITE_IDENTIFIER, 'showEPLinks', sTitle, '', sThumb, sDesc, oOutputParameterHandler)
 

    oGui.setEndOfDirectory() 

def showEPLinks():
    oGui = cGui()
   
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sStart = oInputParameterHandler.getValue('sStart')
    eStart = oInputParameterHandler.getValue('eStart')
    sThumb = oInputParameterHandler.getValue('sThumb')

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    oParser = cParser()
    sPattern = f'<h3 class="episode-title">{sStart}</h3>.+?<span class="badge-psa">{eStart}</span>(.+?)</div>\s*</div>'
    aResult = oParser.parse(sHtmlContent, sPattern)
    if aResult[0] is True:
        for aEntry in aResult[1]:
            sHtmlContent1 = aEntry
    
    sPattern = r'<span class="badge[^>]*>(.*?)</span>.*?' \
           r'href="([^"]+)"[^>]*\s*class.*?' \
           r'href="([^"]+)"[^>]*\s*class' \

    aResult = oParser.parse(sHtmlContent1, sPattern)
    if aResult[0]:
        oOutputParameterHandler = cOutputParameterHandler()
        for aEntry in aResult[1]:
            sSize = aEntry[0].strip()

            sHubCloudUrl = aEntry[1].strip()
            sHubDriveUrl = aEntry[2].strip()
            sHubCloudUrl = hdhub_get_redirect_links(sHubCloudUrl)
            sHubDriveUrl = hdhub_get_redirect_links(sHubDriveUrl)
            sDisplayTitle = f'[COLOR coral] {sSize}[/COLOR] {eStart} {sStart}'

            oOutputParameterHandler.addParameter('siteUrl', sUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sDisplayTitle)
            oOutputParameterHandler.addParameter('sSize', sSize)
            oOutputParameterHandler.addParameter('sHubCloudUrl', sHubCloudUrl)
            oOutputParameterHandler.addParameter('sHubDriveUrl', sHubDriveUrl)

            oGui.addLink(SITE_IDENTIFIER, 'showLinks', sDisplayTitle, sThumb, sDisplayTitle, oOutputParameterHandler)
 

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

    sPattern = r'<div class="download-item[^>]*>.*?' \
           r'<div class="flex[^>]*>(.*?)<br>.*?' \
           r'<span class="badge[^>]*>(.*?)</span>.*?' \
           r'<a[^>]*href="([^"]+)"[^>]*>(.+?)</span>.*?' \
           r'<a[^>]*href="([^"]+)"[^>]*>(.+?)</span>' \

    aResult = oParser.parse(sHtmlContent, sPattern)
    if aResult[0]:
        oOutputParameterHandler = cOutputParameterHandler()
        for aEntry in aResult[1]:
            sSize = aEntry[1].strip()
            sFileName = re.sub(r'[-_.](?!(\d|p))|(-?(4kHdHub\.Com|4khdhub\.fans|www\.\S+)|\.\S{2,4}$)', ' ', aEntry[0]).strip()
            sHubCloudUrl = aEntry[2].strip()
            sHubDriveUrl = aEntry[4].strip()
            sHubCloudUrl = hdhub_get_redirect_links(sHubCloudUrl)
            sHubDriveUrl = hdhub_get_redirect_links(sHubDriveUrl)
            sDisplayTitle = f'[COLOR coral] {sSize}[/COLOR] {sFileName}'

            oOutputParameterHandler.addParameter('siteUrl', sUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sDisplayTitle)
            oOutputParameterHandler.addParameter('sFileName', sFileName)
            oOutputParameterHandler.addParameter('sSize', sSize)
            oOutputParameterHandler.addParameter('sHubCloudUrl', sHubCloudUrl)
            oOutputParameterHandler.addParameter('sHubDriveUrl', sHubDriveUrl)

            oGui.addLink(SITE_IDENTIFIER, 'showLinks', sDisplayTitle, sThumb, sDisplayTitle, oOutputParameterHandler)
         
    oGui.setEndOfDirectory()

def showLinks():
    oGui = cGui()

    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sHubCloudUrl = oInputParameterHandler.getValue('sHubCloudUrl')
    sHubDriveUrl = oInputParameterHandler.getValue('sHubDriveUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')

    for link in [sHubCloudUrl, sHubDriveUrl]:
        data = extract_links(link)
        if data is not False or data != []:
            oOutputParameterHandler = cOutputParameterHandler()
            for sHosterUrl in data:

                oOutputParameterHandler.addParameter('sHosterUrl', sHosterUrl)
                oOutputParameterHandler.addParameter('sMovieTitle', sMovieTitle)
                oOutputParameterHandler.addParameter('sThumb', sThumb)

                oGui.addLink(SITE_IDENTIFIER, 'showLink', sMovieTitle, sThumb, sMovieTitle, oOutputParameterHandler)              

    oGui.setEndOfDirectory()

def showLink():
    oGui = cGui()

    oInputParameterHandler = cInputParameterHandler()
    sHosterUrl = oInputParameterHandler.getValue('sHosterUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')
    sHosterUrl = sHosterUrl.replace(' ', '||')
    
    oHoster = cHosterGui().getHoster('directplay') 
    if oHoster:
        oHoster.setDisplayName(sMovieTitle)
        oHoster.setFileName(sMovieTitle)
        cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb)

    oGui.setEndOfDirectory()


def base64_decode(s: str) -> str:
    s_padded = s + '=' * (-len(s) % 4)
    try:
        return base64.b64decode(s_padded).decode('utf-8')
    except Exception as e:
        print(f"Error decoding base64 string '{s}': {e}")
        return ""

def hdhubpen(value: str) -> str:
    result = []
    for char in value:
        if 'A' <= char <= 'Z':
            result.append(chr(((ord(char) - ord('A') + 13) % 26) + ord('A')))
        elif 'a' <= char <= 'z':
            result.append(chr(((ord(char) - ord('a') + 13) % 26) + ord('a')))
        else:
            result.append(char)
    return "".join(result)

def hdhubencode(value: str) -> str:
    return base64.b64encode(value.encode('utf-8')).decode('utf-8')

def hdhub_get_redirect_links(url: str) -> str:
    import json
    try:
        oRequestHandler = cRequestHandler(url)
        oRequestHandler.addHeaderEntry('User-Agent', UA)
        doc_content = oRequestHandler.request()

        regex = r"s\('o','([A-Za-z0-9+/=]+)'|ck\('_wp_http_\d+','([^']+)'"
        
        combined_string_parts = []
        for match_result in re.finditer(regex, doc_content):
            extracted_value = match_result.group(1) or match_result.group(2)
            if extracted_value:
                combined_string_parts.append(extracted_value)
        
        combined_string = "".join(combined_string_parts)

        decoded_string_step1 = base64_decode(combined_string)
        decoded_string_step2 = base64_decode(decoded_string_step1)
        decoded_string_step3 = hdhubpen(decoded_string_step2)
        final_decoded_string = base64_decode(decoded_string_step3)

        json_object = json.loads(final_decoded_string)

        encoded_url = base64_decode(json_object.get("o", "")).strip()
        data = hdhubencode(json_object.get("data", "")).strip()
        wphttp1 = json_object.get("blog_url", "").strip()

        direct_link = ""
        if wphttp1 and data:
            try:
                direct_link_url = f"{wphttp1}?re={data}"
                print(f"DEBUG: Attempting direct link fetch from: {direct_link_url}")

                oRequestHandler = cRequestHandler(direct_link_url)
                oRequestHandler.addHeaderEntry('User-Agent', UA)
                direct_link_response = oRequestHandler.request()

                direct_link = direct_link_response.strip()

            except Exception as e:
                print(f"Error processing direct link: {e}")

        return encoded_url if encoded_url else direct_link

    except Exception as e:
        print(f"Error: An unexpected error occurred while processing links for {url}: {e}")
        return ""

def get_extractor_details(url):
    parsed_url = urlparse(url)
    domain = parsed_url.netloc.lower()
    
    for key, (name, base_url) in EXTRACTORS.items():
        if key in domain:
            return name, base_url
    
    return "Unknown", parsed_url.scheme + "://" + parsed_url.netloc

def extract_links(url):
    extractor_name, main_url = get_extractor_details(url)
    new_url = url.replace(main_url, "https://hubcloud.bz") if "hubcloud" in main_url else url

    oRequestHandler = cRequestHandler(url)
    oRequestHandler.addHeaderEntry('User-Agent', UA)
    response = oRequestHandler.request()
    
    links = []

    if "hubdrive" in main_url:
        match = re.search(r'<a[^>]*class="btn btn-primary btn-user btn-success1 m-1"[^>]*href="([^"]+)"', response)
        if match:
            if 'drive' in match.group(1):
                link = match.group(1)
                return extract_links(link)
            else:
                link = match.group(1)

    if "drive" in new_url:
        match = re.search(r"var url = '([^']*)'", response)
        if match:
            link = match.group(1)
    else:
        match = re.search(r'<div class="vd.*?<center>.*?<a[^>]*href="([^"]+)"', response, re.DOTALL)
        if match:
            link = match.group(1)

    try:
        link

        oRequestHandler = cRequestHandler(link)
        oRequestHandler.addHeaderEntry('User-Agent', UA)
        oRequestHandler.addHeaderEntry('Referer', link)
        doc_response = oRequestHandler.request()

        if doc_response:
            for match in re.finditer(r'<a[^>]*href="([^"]+)"[^>]*rel="noreferrer[^"]*"[^>]*>(?:<i[^>]*>.*?</i>\s*)?([^<]+)</a>', doc_response, re.DOTALL):
                dlink, text = match.group(1), match.group(2).strip()

                if "Download [FSL Server]" in text:
                    links.append(dlink)

                elif "Download File" in text:
                    links.append(dlink)

                elif "BuzzServer" in text:
                    oRequestHandler = cRequestHandler(f"{dlink}/download")
                    oRequestHandler.addHeaderEntry('User-Agent', UA)
                    oRequestHandler.addHeaderEntry('Referer', dlink)
                    oRequestHandler.disableRedirect()
                    dlink_response = oRequestHandler.request()

                    buzz_dlink = oRequestHandler.getResponseHeader()['hx-redirect']
                    if buzz_dlink:
                        links.append(f'{get_base_url(dlink)}{buzz_dlink}')

                elif "pixeldra" in dlink:
                    links.append(dlink)

                elif "Download [Server : 10Gbps]" in text:
                    import requests
                    dlink_response = requests.get(dlink, allow_redirects=False)
                    fast_dlink = dlink_response.headers.get("location", "").split("link=")[-1]
                    if 'workers.dev' in fast_dlink:
                        dlink_response = requests.get(fast_dlink)
                        glink_match = re.search(r'id="vd" href=["\']([^"\']+)["\']', dlink_response.text, re.DOTALL)
                        if glink_match:
                            links.append(glink_match.group(1))

                    else:
                        links.append(fast_dlink)
                else:
                    links.append(dlink)
    except NameError:
        from resources.lib.util import urlHostName
        file_id = url.split("/")[-1] if "/file/" in url else None
        url = url.replace("https://hubdrive.live", "https://hubdrive.icu") if "hubdrive" in url else url

        oRequestHandler = cRequestHandler(f'https://{urlHostName(url)}/ajax.php?ajax=direct-download')
        oRequestHandler.addHeaderEntry('Host', urlHostName(url))
        oRequestHandler.addHeaderEntry('Origin', f'https://{urlHostName(url)}')
        oRequestHandler.addHeaderEntry('User-Agent', UA)
        oRequestHandler.addHeaderEntry('X-Requested-With', 'XMLHttpRequest')
        oRequestHandler.addParameters('id', file_id)
        oRequestHandler.setRequestType(1)
        sHtmlContent = oRequestHandler.request(jsonDecode=True)

        links.append(sHtmlContent.get("gd", ""))

    return links

def get_base_url(url):
    parsed_url = urlparse(url)
    return f"{parsed_url.scheme}://{parsed_url.netloc}"