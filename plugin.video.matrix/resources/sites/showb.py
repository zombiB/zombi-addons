# -*- coding: utf-8 -*-

import json, base64, requests, re
from resources.lib.gui.hoster import cHosterGui
from resources.lib.gui.gui import cGui
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.lib.comaddon import progress, VSlog, siteManager, addon
from resources.lib import random_ua

UA = random_ua.get_phone_ua()

SITE_IDENTIFIER = 'showb'
SITE_NAME = 'SuperShow'
SITE_DESC = ''

URL_MAIN = siteManager().getUrlMain(SITE_IDENTIFIER)

sHost = base64.b64decode(URL_MAIN)
dHost = sHost.decode("utf-8")
URL_MAIN = dHost[::-1]

MOVIE_4K = (f'{URL_MAIN}movie?quality=4K&release_year=all&genre=all&rating=all', 'showMovies')
DOC_NEWS = (f'{URL_MAIN}movie?genre=7&quality=4K', 'showMovies')
KID_MOVIES = (f'{URL_MAIN}movie?quality=all&release_year=all&genre=3&rating=all', 'showMovies')

SERIE_EN = (f'{URL_MAIN}tv?release_year=all&genre=all&rating=all', 'showSeries')
DOC_SERIES = (f'{URL_MAIN}tv?quality=all&release_year=all&genre=7-12-24&rating=all', 'showSeries')

URL_SEARCH_MOVIES = (f'{URL_MAIN}search?keyword=', 'showMovies')
URL_SEARCH_SERIES = (f'{URL_MAIN}search?keyword=', 'showSeries')
FUNCTION_SEARCH = 'showMovies'

def load():
    oGui = cGui()
    addons = addon()

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'http://')
    oGui.addDir(SITE_IDENTIFIER, 'showSearch', addons.VSlang(30078), '1/Search.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', 'http://')
    oGui.addDir(SITE_IDENTIFIER, 'showSeriesSearch', addons.VSlang(30079), '1/Search.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', MOVIE_4K[0])
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', ' 4k أفلام', '4k.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', KID_MOVIES[0])
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'أفلام كرتون', '1/1/Anime.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', DOC_NEWS[0])
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'أفلام وثائقية', '1/Documentary.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', SERIE_EN[0])
    oGui.addDir(SITE_IDENTIFIER, 'showSeries', 'مسلسلات أجنبية', '1/Movies.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', DOC_SERIES[0])
    oGui.addDir(SITE_IDENTIFIER, 'showSeries', 'مسلسلات وثائقية', '1/Documentary.png', oOutputParameterHandler) 

    oGui.setEndOfDirectory()

def showSearch():
    oGui = cGui()
 
    sSearchText = oGui.showKeyBoard()
    if sSearchText:
        sUrl = f'{URL_MAIN}search?keyword={sSearchText}'
        showMovies(sUrl)
        oGui.setEndOfDirectory()
        return
 
def showSeriesSearch():
    oGui = cGui()
 
    sSearchText = oGui.showKeyBoard()
    if sSearchText:
        sUrl = f'{URL_MAIN}search?keyword={sSearchText}'
        showSeries(sUrl)
        oGui.setEndOfDirectory()
        return

def showMoviesSearch(sSearch=''):
    oGui = cGui()
    addons = addon()
    API_Key = addons.getSetting('api_tmdb')

    sUrl = f'{sSearch}&api_key={API_Key}'      
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request(jsonDecode=True)

    if "results" in sHtmlContent:
        for movie in sHtmlContent["results"]:
                
            sId = movie["id"]
            siteUrl = f'https://api.dmdb.network/v1/gmid/M.{sId}'
            sTitle = movie["original_title"]
            sThumb = f'https://image.tmdb.org/t/p/w500{movie["poster_path"]}'
            sDesc = movie["overview"]

            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', siteUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oGui.addMovie(SITE_IDENTIFIER, 'showLinks', sTitle, '', sThumb, sDesc, oOutputParameterHandler)

    if not sSearch:
        oGui.setEndOfDirectory()

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
    oRequestHandler.disableSSL()
    oRequestHandler.addHeaderEntry('Cookie', "ci=1673a264adc4a4; fe172cc1ecdda95649fbd2e32214dd06=71a2fd70b65e736476ec07ca2fddc240")
    sHtmlContent = oRequestHandler.request()

    sPattern = '<div class="flw-item">.+?quality">(.+?)</div>\s*<img src="([^"]+)".+?alt="([^"]+)".+?<a href="([^"]+)'
    aResult = oParser.parse(sHtmlContent, sPattern)
    if aResult[0]:
        total = len(aResult[1])
        progress_ = progress().VScreate(SITE_NAME)
        oOutputParameterHandler = cOutputParameterHandler()    
        for aEntry in aResult[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break

            if '/tv/' in aEntry[3]:
                continue

            sTitle = aEntry[2]
            sQual = f'[{aEntry[0]}]'
            siteUrl = f'{URL_MAIN[:-1]}{aEntry[3]}'
            sThumb = aEntry[1]
            sDesc = ''
            sYear = ''
            sDisplayTitle = f'{sTitle} {sQual}'

            oOutputParameterHandler.addParameter('siteUrl', siteUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oOutputParameterHandler.addParameter('sYear', sYear)
            oOutputParameterHandler.addParameter('sDesc', sDesc)
            oGui.addMovie(SITE_IDENTIFIER, 'showLinks', sDisplayTitle, '', sThumb, sDesc, oOutputParameterHandler)

        progress_.VSclose(progress_)
 
        sNextPage = __checkForNextPage(sHtmlContent)
        if sNextPage:
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sNextPage)
            oGui.addDir(SITE_IDENTIFIER, 'showMovies', '[COLOR teal]Next >>>[/COLOR]', 'next.png', oOutputParameterHandler)
 
    if not sSearch:
        oGui.setEndOfDirectory()  

def showJsonMovies(sSearch = ''):
    oGui = cGui()
    if sSearch:
      sUrl = sSearch.replace(' ','+')
      
    else:
        oInputParameterHandler = cInputParameterHandler()
        sUrl = oInputParameterHandler.getValue('siteUrl')

    sPage = sUrl.split('page=')[1]
    nPage = int(sPage) + 1
    oRequestHandler = cRequestHandler(sUrl)
    oRequestHandler.addHeaderEntry('User-Agent', UA)
    oRequestHandler.disableSSL()
    sHtmlContent = oRequestHandler.request(jsonDecode=True)

    oOutputParameterHandler = cOutputParameterHandler()  
    for movie in sHtmlContent["data"]["docs"]:
        sTitle = movie["name"]
        sQual = movie["quality_tag"]
        siteUrl = re.search(r'\d+', movie['id']).group()
        sThumb = base64.b64encode(f'{movie["poster"]}|500|74'.encode())
        sThumb = f'https://thumb.chuaxin.com/thumb_{sThumb}.png'
        sDesc = ''
        sYear = ''
        sDisplayTitle = f'{sTitle} [{sQual}]'

        oOutputParameterHandler.addParameter('siteUrl', siteUrl)
        oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
        oOutputParameterHandler.addParameter('sThumb', sThumb)
        oOutputParameterHandler.addParameter('sYear', sYear)
        oOutputParameterHandler.addParameter('sDesc', sDesc)
        oGui.addMovie(SITE_IDENTIFIER, 'showLinks', sDisplayTitle, '', sThumb, sDesc, oOutputParameterHandler)

    sUrl = sUrl.split('page=')[0]
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', f'{sUrl}page={nPage}')
    oGui.addDir(SITE_IDENTIFIER, 'showJsonMovies', f'[COLOR teal]Next (Page:{nPage})>>>[/COLOR]', 'next.png', oOutputParameterHandler)
 
    if not sSearch:
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
    oRequestHandler.disableSSL()
    oRequestHandler.addHeaderEntry('Cookie', "ci=1673a264adc4a4; fe172cc1ecdda95649fbd2e32214dd06=71a2fd70b65e736476ec07ca2fddc240")
    sHtmlContent = oRequestHandler.request()

    sPattern = '<div class="flw-item">.+?quality">(.+?)</div>\s*<img src="([^"]+)".+?alt="([^"]+)".+?<a href="([^"]+)'
    aResult = oParser.parse(sHtmlContent, sPattern)
    if aResult[0]:
        total = len(aResult[1])
        progress_ = progress().VScreate(SITE_NAME)
        oOutputParameterHandler = cOutputParameterHandler()    
        for aEntry in aResult[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break
            if '/movie/' in aEntry[3]:
                continue

            sTitle = aEntry[2]
            sQual = f'[{aEntry[0]}]'
            siteUrl = f'{URL_MAIN[:-1]}{aEntry[3]}'
            sThumb = aEntry[1]
            sDesc = ''
            sYear = ''
            sDisplayTitle = f'{sTitle} {sQual}'

            oOutputParameterHandler.addParameter('siteUrl', siteUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oOutputParameterHandler.addParameter('sYear', sYear)
            oOutputParameterHandler.addParameter('sDesc', sDesc)
            oGui.addTV(SITE_IDENTIFIER, 'showSeasons', sDisplayTitle, '', sThumb, sDesc, oOutputParameterHandler)

        progress_.VSclose(progress_)
 
    if not sSearch:
        sNextPage = __checkForNextPage(sHtmlContent)
        if sNextPage:
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sNextPage)
            oGui.addDir(SITE_IDENTIFIER, 'showSeries', '[COLOR teal]Next >>>[/COLOR]', 'next.png', oOutputParameterHandler)

        oGui.setEndOfDirectory()  


def showSeasons():
    oGui = cGui()
   
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')

    sUrl = showb_function(sUrl, '2') 

    oParser = cParser() 
    session = requests.Session()
    sHtmlContent = session.get(sUrl).text

    sPattern = 'data-id="([^"]+)" data-path="season (.+?)"'
    aResult = oParser.parse(sHtmlContent, sPattern)    
    if (aResult[0]):
        oOutputParameterHandler = cOutputParameterHandler() 
        for aEntry in aResult[1]:
            share_key= sUrl.split("/share/")[1]
            postid = aEntry[0]
            sSeason = aEntry[1]
            siteUrl = f'https://www.febbox.com/file/file_share_list?share_key={share_key}&pwd=&parent_id={postid}&is_html=1'
            sTitle = F'{sMovieTitle} S{sSeason}'         
            sThumb = aEntry[1]
            sDesc = ""

            oOutputParameterHandler.addParameter('siteUrl', siteUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('share_key', share_key)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oGui.addSeason(SITE_IDENTIFIER, 'showEpisodes', sTitle, '', sThumb, sDesc, oOutputParameterHandler)  

    oGui.setEndOfDirectory() 

def showEpisodes():
    oGui = cGui()
   
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    share_key = oInputParameterHandler.getValue('share_key')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')

    oParser = cParser() 
    oRequestHandler = cRequestHandler(sUrl)
    oRequestHandler.addHeaderEntry('User-Agent', UA)
    oRequestHandler.disableSSL()
    sHtmlContent = oRequestHandler.request(jsonDecode=True)
    sHtmlContent = sHtmlContent.get('html')

    sPattern = 'data-id="([^"]+)".+?"file_name">(.+?)<'
    aResult = oParser.parse(sHtmlContent,sPattern)
    if aResult[0]:
        for aEntry in aResult[1]:
            oOutputParameterHandler = cOutputParameterHandler() 

            sTitle = aEntry[1]
            sPattern = r"(?:S|s)(\d{2})(?:E|e)(\d{2})"
            match = re.search(sPattern, sTitle)
            if match:
                season, episode = match.groups()
            sTitle = f'{sMovieTitle} S{season}E{episode}'
            siteUrl = aEntry[0]
            sThumb = sThumb
            sDesc = ""

            oOutputParameterHandler.addParameter('siteUrl', siteUrl)
            oOutputParameterHandler.addParameter('share_key', share_key)
            oOutputParameterHandler.addParameter('file_id', siteUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sSeason', season)
            oOutputParameterHandler.addParameter('sEpisode', episode)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
        
            oGui.addEpisode(SITE_IDENTIFIER, 'showSeriesLinks', sTitle, '', sThumb, sDesc, oOutputParameterHandler)
       
    oGui.setEndOfDirectory() 

def showSeriesLinks():
    oGui = cGui()
    oParser = cParser()
    oInputParameterHandler = cInputParameterHandler()
    share_key = oInputParameterHandler.getValue('share_key')
    file_id = oInputParameterHandler.getValue('file_id')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sSeason = oInputParameterHandler.getValue('sSeason')
    sEpisode = oInputParameterHandler.getValue('sEpisode')
    sThumb = oInputParameterHandler.getValue('sThumb')

    import random
    session = requests.Session()
    ui_tokens = ["eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpYXQiOjE3MzMzNzUwODMsIm5iZiI6MTczMzM3NTA4MywiZXhwIjoxNzY0NDc5MTAzLCJkYXRhIjp7InVpZCI6MjU1Njk4LCJ0b2tlbiI6Ijc1MDQ3MjM4YWJjODg4NmUxZDVlMmYzNGNkZjliNjNkIn19.QMLeSFq_KQZuk1GO0Gd7boSqRSq05g4GKxfHUrU72E8", "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpYXQiOjE3MzM0MjMwNTUsIm5iZiI6MTczMzQyMzA1NSwiZXhwIjoxNzY0NTI3MDc1LCJkYXRhIjp7InVpZCI6NDM0Mjg1LCJ0b2tlbiI6IjM3MjYyNTQ3ZDlkNzk4YmExMTI0NTNjMGFjOTJiYTRiIn19.t_dMkn--gtRzBqWGJuITjiixxwOGP-nVvNRKvjvtsg0"]

    Subtitle = ''
    try:
        api_key = addon().getSetting('api_tmdb')
        base_url = "https://api.themoviedb.org/3/search/tv"
        show_name = re.split(r"S\d+", sMovieTitle)[0]
        url = f"{base_url}?api_key={api_key}&query={show_name.replace(' ','%20')}"
        oRequestHandler = cRequestHandler(url)
        sHtmlContent = oRequestHandler.request()
        data = json.loads(sHtmlContent)

        if data['total_results'] > 0:
            movie_data = data['results'][0]
            tmdb_id = movie_data.get('id')

            surl = f'https://sub-api-two.vercel.app/api/v2/sub/search?tmdbid={tmdb_id}&lang=ar&season={str(int(sSeason))}&episode={str(int(sEpisode))}'
            oRequestHandler = cRequestHandler(surl)
            sHtmlContent = oRequestHandler.request()
            if 'http' in sHtmlContent:
                data = json.loads(sHtmlContent)
                Subtitle = data["file"]["url"]

    except:
        VSlog('Failed to get subs')

    url = "https://www.febbox.com/file/player"
    headers = {
        "Accept": "text/plain, */*; q=0.01",
        "Accept-Language": "en-US,en;q=0.9",
        "Connection": "keep-alive",
        "Content-Length": "31",
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "Cookie": f"ui={ui_tokens[random.randint(0, len(ui_tokens)-1)]}; list_mode=waterfall",
        "Host": "www.febbox.com",
        "Origin": "https://www.febbox.com",
        "Referer": f"https://www.febbox.com/share/{share_key}",
        "sec-ch-ua": "\"Microsoft Edge\";v=\"131\", \"Chromium\";v=\"131\", \"Not_A Brand\";v=\"24\"",
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "\"Windows\"",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-origin",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36 Edg/131.0.0.0",
        "X-Requested-With": "XMLHttpRequest"
    }

    data = f"fid={file_id}&share_key={share_key}"

    initial_response = session.post(url, headers=headers, data=data).text

    sPattern = '<ul id="Arabic">.+?data-url="([^"]+)'
    aResult = oParser.parse(initial_response, sPattern)
    if aResult[0]:  
        for aEntry in aResult[1]:   
            Subtitle = aEntry.replace("\\","")

    itemList = []
    sPattern = '"file":"(.+?)","label":"([^"]+)'
    aResult = oParser.parse(initial_response, sPattern)
    if aResult[0]:
        oOutputParameterHandler = cOutputParameterHandler()     
        for aEntry in aResult[1]:   
            url = aEntry[0].replace("\\","")
            if url.startswith('//'):
                url = 'http:' + url
            sQual = aEntry[1]

            if sQual not in itemList:
                itemList.append(sQual)	
                sDisplayTitle = f'{sMovieTitle} [COLOR coral] ({sQual}) [/COLOR]'
                oOutputParameterHandler.addParameter('siteUrl', url)
                oOutputParameterHandler.addParameter('sQual', sQual)
                oOutputParameterHandler.addParameter('sMovieTitle', sMovieTitle)
                oOutputParameterHandler.addParameter('sThumb', sThumb)
                oOutputParameterHandler.addParameter('Subtitle', Subtitle)

                oGui.addLink(SITE_IDENTIFIER, 'showHosters', sDisplayTitle, sThumb, sDisplayTitle, oOutputParameterHandler)     

    oGui.setEndOfDirectory()

def showLinks():
    oGui = cGui()
    oParser = cParser()
    oInputParameterHandler = cInputParameterHandler()
    sURL = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')

    sUrl = ''
    if 'dmdb' in sURL:
        sResponse = requests.request("GET", sURL, headers=None, data=None)
        data = json.loads(sResponse.text)
        if "superstream" in data["ids"]:
            sUrl = showb_function(data["ids"]["superstream"])

    else:
        sUrl = showb_function(sURL, '1')  

    if 'share/' not in sUrl:
        sTitle = 'No resources Found'
        oGui.addText(SITE_IDENTIFIER, f'[COLOR red]{sTitle}[/COLOR]')
    else:
        ui_tokens = ["eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpYXQiOjE3MzMzNzUwODMsIm5iZiI6MTczMzM3NTA4MywiZXhwIjoxNzY0NDc5MTAzLCJkYXRhIjp7InVpZCI6MjU1Njk4LCJ0b2tlbiI6Ijc1MDQ3MjM4YWJjODg4NmUxZDVlMmYzNGNkZjliNjNkIn19.QMLeSFq_KQZuk1GO0Gd7boSqRSq05g4GKxfHUrU72E8", "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpYXQiOjE3MzM0MjMwNTUsIm5iZiI6MTczMzQyMzA1NSwiZXhwIjoxNzY0NTI3MDc1LCJkYXRhIjp7InVpZCI6NDM0Mjg1LCJ0b2tlbiI6IjM3MjYyNTQ3ZDlkNzk4YmExMTI0NTNjMGFjOTJiYTRiIn19.t_dMkn--gtRzBqWGJuITjiixxwOGP-nVvNRKvjvtsg0"]
        Subtitle = False
        share_key = sUrl.split('share/')[1]

        default_domain = "https://febbox.com/"

        base_url = f'{default_domain}share/{share_key}'
        session = requests.Session()
        initial_response = session.get(base_url).text

        pattern = r'<div\s+class="file\s*"\s+data-id="(.*?)"'
        match = re.search(pattern, initial_response)
        if match:
            file_id = match.group(1)
        else:
            pattern = r'<button\s+class="details"\s+data-id="(.*?)"'
            match = re.search(pattern, initial_response)
            if match:
                file_id = match.group(1)

        import random

        url = "https://www.febbox.com/file/player"

        oRequestHandler = cRequestHandler(url)
        oRequestHandler.setRequestType(1)

        oRequestHandler.addHeaderEntry("Accept", "text/plain, */*; q=0.01")
        oRequestHandler.addHeaderEntry("Accept-Language", "en-US,en;q=0.9")
        oRequestHandler.addHeaderEntry("Connection", "keep-alive")
        oRequestHandler.addHeaderEntry("Content-Type", "application/x-www-form-urlencoded; charset=UTF-8")
        oRequestHandler.addHeaderEntry("Cookie", f"ui={ui_tokens[random.randint(0, len(ui_tokens)-1)]}; list_mode=waterfall")
        oRequestHandler.addHeaderEntry("Host", "www.febbox.com")
        oRequestHandler.addHeaderEntry("Origin", "https://www.febbox.com")
        oRequestHandler.addHeaderEntry("Referer", base_url)
        oRequestHandler.addHeaderEntry("sec-ch-ua", "\"Microsoft Edge\";v=\"131\", \"Chromium\";v=\"131\", \"Not_A Brand\";v=\"24\"")
        oRequestHandler.addHeaderEntry("sec-ch-ua-mobile", "?0")
        oRequestHandler.addHeaderEntry("sec-ch-ua-platform", "\"Windows\"")
        oRequestHandler.addHeaderEntry("Sec-Fetch-Dest", "empty")
        oRequestHandler.addHeaderEntry("Sec-Fetch-Mode", "cors")
        oRequestHandler.addHeaderEntry("Sec-Fetch-Site", "same-origin")
        oRequestHandler.addHeaderEntry("User-Agent", "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36 Edg/131.0.0.0")
        oRequestHandler.addHeaderEntry("X-Requested-With", "XMLHttpRequest")
        oRequestHandler.addParameters('share_key', share_key)
        oRequestHandler.addParameters('fid', file_id)

        # Make the request
        initial_response = oRequestHandler.request()


        sPattern = '<ul id="Arabic">.+?data-url="([^"]+)'
        aResult = oParser.parse(initial_response, sPattern)
        if aResult[0]:  
            for aEntry in aResult[1]:   
                Subtitle = aEntry.replace("\\","")

        else:
            sPatternEnglish = r'<ul id="English">.+?data-url="([^"]+)'
            aResult = oParser.parse(initial_response, sPatternEnglish)
            if aResult[0]:
                for aEntry in aResult[1]:
                    Subtitle = aEntry.replace("\\", "")

        itemList = []
        sPattern = '"file":"(.+?)","label":"([^"]+)'
        aResult = oParser.parse(initial_response, sPattern)
        if aResult[0]:
            oOutputParameterHandler = cOutputParameterHandler()     
            for aEntry in aResult[1]:   
                url = aEntry[0].replace("\\","")
                if url.startswith('//'):
                    url = 'http:' + url
                sQual = aEntry[1]

                if sQual not in itemList:
                    itemList.append(sQual)	
                    sDisplayTitle = f'{sMovieTitle} [COLOR coral] ({sQual}) [/COLOR]'
                    oOutputParameterHandler.addParameter('siteUrl', url)
                    oOutputParameterHandler.addParameter('sQual', sQual)
                    oOutputParameterHandler.addParameter('sMovieTitle', sMovieTitle)
                    oOutputParameterHandler.addParameter('sThumb', sThumb)
                    oOutputParameterHandler.addParameter('Subtitle', Subtitle)

                    oGui.addLink(SITE_IDENTIFIER, 'showHosters', sDisplayTitle, sThumb, sDisplayTitle, oOutputParameterHandler)      

    oGui.setEndOfDirectory()

def showHosters():
    oGui = cGui()

    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sQual = oInputParameterHandler.getValue('sQual')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')
    Subtitle = oInputParameterHandler.getValue('Subtitle')

    sHosterUrl = sUrl + f'|Referer={URL_MAIN}&Origin={URL_MAIN[:-1]}'
    if Subtitle is not False:
        sHosterUrl = sUrl +'?sub.info='+Subtitle

    oHoster = cHosterGui().checkHoster(sHosterUrl)
    sDisplayTitle = ('%s [COLOR coral] (%s) [/COLOR]') % (sMovieTitle, sQual) 
    if oHoster:
        oHoster.setDisplayName(sDisplayTitle)
        oHoster.setFileName(sMovieTitle)
        cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb)

    oGui.setEndOfDirectory()

def __checkForNextPage(sHtmlContent):
    oParser = cParser()
    sPattern = '<li class="page-item active"><a class="page-link">(.+?)</a></li>.+?href="([^"]+)"'
    aResult = oParser.parse(sHtmlContent, sPattern)
    if aResult[0]:
        sNextPage = URL_MAIN[:-1]+aResult[1][0][1]
        return sNextPage

    return False, 'none'

def showb_function(sURL, sType):
    oParser = cParser()

    if 'http' in sURL:
        oRequestHandler = cRequestHandler(sURL)
        sHtmlContent = oRequestHandler.request()

        sPattern = 'class="heading-name"><a href="([^"]+)"'
        aResult = oParser.parse(sHtmlContent, sPattern)
        if aResult[0]:
            show_link = aResult[1][0]
            show_id = show_link.split('/')[3]
    else:
        show_id = sURL
    if sType == '1':
        feb_box_url = f'{URL_MAIN}index/share_link?id={show_id}&type=1'
    else:
        feb_box_url = f'{URL_MAIN}index/share_link?id={show_id}&type=2'

    oRequestHandler = cRequestHandler(feb_box_url)
    oRequestHandler.disableSSL()
    sHtmlContent = oRequestHandler.request()

    sPattern = '"link":\s*"([^"]+)"'
    aResult = oParser.parse(sHtmlContent, sPattern)
    if aResult[0]:
        feb_box_data = aResult[1][0]

    if feb_box_data:
        return feb_box_data.replace('\\','')
        
    return False, False

