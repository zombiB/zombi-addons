# -*- coding: utf-8 -*-

import json
import base64
import requests, os
import urllib.parse
from resources.lib.gui.hoster import cHosterGui
from resources.lib.gui.gui import cGui
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler
from resources.lib.parser import cParser
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.comaddon import progress, addon, isMatrix, VSlog
from resources.lib.tmdb import cTMDb

UA = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36'

SITE_IDENTIFIER = 'tma'
SITE_NAME = 'The Movie Archive'
SITE_DESC = 'english vod'

URL_MAIN = 'https://www.themoviedb.org/'
base_url = base64.b64decode('aHR0cHM6Ly92aWRzcmMucmlw').decode()

addons = addon()
API_Key = addons.getSetting('api_tmdb')

API_VERS = '3'
API_URL = URL_MAIN + API_VERS

tmdb_session = ''
tmdb_account = ''

MOVIE_EN = ('movie/now_playing', 'showMovies')
MOVIE_TOP = ('movie/top_rated', 'showMovies')
MOVIE_POP = ('movie/popular', 'showMovies')
MOVIE_GENRES = ('genre/movie/list', 'showGenreMovie')

URL_SEARCH_MOVIES = ('https://api.themoviedb.org/3/search/movie?include_adult=false&query=', 'showMoviesSearch')
FUNCTION_SEARCH = 'showMovies'
	
def load():
    oGui = cGui()
    addons = addon()

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'http://')
    oGui.addDir(SITE_IDENTIFIER, 'showSearchMovie', addons.VSlang(30330), '1/Search.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', MOVIE_POP[0])
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', addons.VSlang(30425), 'pop.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', MOVIE_EN[0])
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', addons.VSlang(30426), '1/Movies.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', MOVIE_TOP[0])
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', addons.VSlang(30427), 'top.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', MOVIE_GENRES[0])
    oGui.addDir(SITE_IDENTIFIER, 'showGenreMovie', addons.VSlang(30428), 'genres.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()

def showSearchMovie():
    oGui = cGui()

    sSearchText = oGui.showKeyBoard()
    if sSearchText:
        showMovies(sSearchText.replace(' ', '+'))
        return  

def showGenreMovie():
    oGui = cGui()
    grab = cTMDb()

    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')

    result = grab.getUrl(sUrl)
    total = len(result)
    if total > 0:
        oOutputParameterHandler = cOutputParameterHandler()
        for i in result['genres']:
            sId, sTitle = i['id'], i['name']

            if not isMatrix():
                sTitle = sTitle.encode("utf-8")
            sUrl = 'genre/' + str(sId) + '/movies'
            oOutputParameterHandler.addParameter('siteUrl', sUrl)
            oGui.addDir(SITE_IDENTIFIER, 'showMovies', str(sTitle), 'genres.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()

def showFolderList():
    oGui = cGui()

    liste = []
    liste.append(['Top 50 Greatest Movies', '10'])
    liste.append(['Oscar winners', '31670'])
    liste.append(['Fascinating movies ', '43'])
    liste.append(['Science-Fiction', '3945'])
    liste.append(['Adaptations', '9883'])
    liste.append(['Disney Classic', '338'])
    liste.append(['Pixar', '3700'])
    liste.append(['Marvel', '1'])
    liste.append(['DC Comics Universe', '3'])
    liste.append(['Top Manga', '31665'])
    liste.append(['Top Manga 2', '31695'])
    liste.append(['Best Series', '36788'])

    oOutputParameterHandler = cOutputParameterHandler()
    for sTitle, sUrl in liste:
        oOutputParameterHandler.addParameter('siteUrl', sUrl)
        oGui.addDir(SITE_IDENTIFIER, 'showLists', sTitle, 'listes.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()

def showMoviesSearch(sSearch=''):
    oGui = cGui()

    sUrl = sSearch + '&api_key='+API_Key
    simdb_id = ''

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    sPattern = '"id":(.+?),.+?"original_title":"([^"]+)".+?"overview":"([^"]+)".+?"poster_path":(.+?),'

    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
    if aResult[0]:
        total = len(aResult[1])
        progress_ = progress().VScreate(SITE_NAME)
        oOutputParameterHandler = cOutputParameterHandler()    
        for aEntry in aResult[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break
            if 'null' in aEntry[3] or 'none' in aEntry[3]:
                continue
                
            sId = aEntry[0]
            sTitle = aEntry[1]
            sDisplayTitle = sTitle.replace(' ','%2520').replace('%20','%2520')
            siteUrl = base64.b64decode('aHR0cHM6Ly9hcGkuYnJhZmxpeC52aWRlby9mZWJib3gvc291cmNlcy13aXRoLXRpdGxlPw==').decode('utf8',errors='ignore')
            siteUrl = f'{siteUrl}title={sDisplayTitle}&mediaType=movie&episodeId=1&seasonId=1&tmdbId={sId}&imdbId={simdb_id}'
            sThumb = "https://image.tmdb.org/t/p/w500" + aEntry[3].replace('"','')
            sDesc = aEntry[2]

            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', siteUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oOutputParameterHandler.addParameter('sId', sId)
            oGui.addMovie(SITE_IDENTIFIER, 'showHosters', sTitle, '', sThumb, sDesc, oOutputParameterHandler)

            progress_.VSclose(progress_)
    if not sSearch:
        oGui.setEndOfDirectory()


def showMovies(sSearch=''):
    oGui = cGui()
    grab = cTMDb()

    oInputParameterHandler = cInputParameterHandler()

    iPage = 1
    term = ''
    if oInputParameterHandler.exist('page'):
        iPage = oInputParameterHandler.getValue('page')

    if oInputParameterHandler.exist('sSearch'):
        sSearch = oInputParameterHandler.getValue('sSearch')

    if sSearch:
        result = grab.getUrl('search/movie', iPage, 'query=' + sSearch)
        sUrl = ''

    else:
        if oInputParameterHandler.exist('session_id'):
            term += 'session_id=' + oInputParameterHandler.getValue('session_id')

        sUrl = oInputParameterHandler.getValue('siteUrl')
        result = grab.getUrl(sUrl, iPage, term)

    try:
        total = len(result)
        
        if total > 0:
            total = len(result['results'])
            progress_ = progress().VScreate(SITE_NAME)

            for i in result['results']:
                progress_.VSupdate(progress_, total)
                if progress_.iscanceled():
                    break

                if i['original_language'] == 'en':

                    i = grab._format(i, '', "movie")

                    sId, sTitle, simdb_id, sThumb, sDesc, sYear = i['tmdb_id'], i['title'], i['imdb_id'], i['poster_path'], i['plot'], i['year']

                    if not isMatrix():
                        sTitle = sTitle.encode("utf-8")
                    sDisplayTitle = sTitle.replace(' ','%2520').replace('%20','%2520')
                    siteUrl = base64.b64decode('aHR0cHM6Ly9hcGkuYnJhZmxpeC52aWRlby9mZWJib3gvc291cmNlcy13aXRoLXRpdGxlPw==').decode('utf8',errors='ignore')
                    siteUrl = f'{siteUrl}title={sDisplayTitle}&year={sYear}&mediaType=movie&episodeId=1&seasonId=1&tmdbId={sId}&imdbId={simdb_id}'
                    oOutputParameterHandler = cOutputParameterHandler()
                    oOutputParameterHandler.addParameter('siteUrl', siteUrl)
                    oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
                    oOutputParameterHandler.addParameter('sThumb', sThumb)
                    oOutputParameterHandler.addParameter('sId', sId)
                    oGui.addMovie(SITE_IDENTIFIER, 'showHosters', sTitle, '', sThumb, sDesc, oOutputParameterHandler)

                progress_.VSclose(progress_)

            if int(iPage) > 0:
                iNextPage = int(iPage) + 1
                oOutputParameterHandler = cOutputParameterHandler()
                if sSearch:
                    oOutputParameterHandler.addParameter('sSearch', sSearch)

                oOutputParameterHandler.addParameter('siteUrl', sUrl)
                oOutputParameterHandler.addParameter('page', iNextPage)
                oGui.addNext(SITE_IDENTIFIER, 'showMovies', 'Page ' + str(iNextPage), oOutputParameterHandler)

    except TypeError as e:
        oGui.addText(SITE_IDENTIFIER, '[COLOR red]No result n\'was found.[/COLOR]')

    oGui.setEndOfDirectory()

def showHosters():
    oGui = cGui()

    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')
    sId = oInputParameterHandler.getValue('sId')

    simdb_id = sUrl.split('imdbId=')[1]
    if simdb_id == '':
        addons = addon()
        API_Key = addons.getSetting('api_tmdb')
        sApi = f'https://api.themoviedb.org/3/movie/{sId}?api_key={API_Key}'
        oRequestHandler = cRequestHandler(sApi)
        data = oRequestHandler.request(jsonDecode=True)

        simdb_id = data["imdb_id"]
        id = data.get("id")
        original_title = data.get("original_title")
        release_date = data.get("release_date")
        year = None 

        if release_date:
            try:
                year = release_date[:4]  
            except (ValueError, IndexError):
                VSlog("Error parsing year from release date")
                pass

        oOutputParameterHandler = cOutputParameterHandler()
        for sServer in ['WhVx', 'Vidsrc', 'Antol307VVk', 'Rive', 'Torrent']:
            sDisplayTitle = f'{sMovieTitle} [COLOR coral]- {sServer}[/COLOR]'      
            oOutputParameterHandler.addParameter('sId', sId)
            oOutputParameterHandler.addParameter('simdb_id', simdb_id)
            oOutputParameterHandler.addParameter('siteUrl', sUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sMovieTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oOutputParameterHandler.addParameter('sServer', sServer)

            oGui.addLink(SITE_IDENTIFIER, 'showLinks', sDisplayTitle, sThumb, sDisplayTitle, oOutputParameterHandler)

    oGui.setEndOfDirectory()

def showLinks():
    oGui = cGui()

    oInputParameterHandler = cInputParameterHandler()
    sHosterUrl = oInputParameterHandler.getValue('sHosterUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')
    sServer = oInputParameterHandler.getValue('sServer')
    sId = oInputParameterHandler.getValue('sId')
    simdb_id = oInputParameterHandler.getValue('simdb_id')
    
    if sServer == 'WhVx':
        try:
            sHosterUrl = whvx(sId)

            oHoster = cHosterGui().getHoster('streamrapid')
            if oHoster:
                oHoster.setDisplayName(sDisplayTitle)
                oHoster.setFileName(sMovieTitle)
                cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb)

        except:
           VSlog('Failed to connect to api')

    if sServer == 'Rive':
        try:
            data = rive(sId)
            oOutputParameterHandler = cOutputParameterHandler()
            for link in data:
                sUrl = link.get('link')
                sHosterUrl = sUrl

                sDisplayTitle = f'{sMovieTitle} - ({link.get("server")})'  
                oOutputParameterHandler.addParameter('sHosterUrl', sHosterUrl)
                oOutputParameterHandler.addParameter('siteUrl', sUrl)
                oOutputParameterHandler.addParameter('sMovieTitle', sMovieTitle)
                oOutputParameterHandler.addParameter('sThumb', sThumb)

                oGui.addLink(SITE_IDENTIFIER, 'showRiveLinks', sDisplayTitle, sThumb, sDisplayTitle, oOutputParameterHandler)

        except:
            VSlog('Failed to connect to api')

    if sServer == 'Vidsrc':
        try:
            data = vidsrc(sId)
            oOutputParameterHandler = cOutputParameterHandler()
            for link in data:
                sUrl = link.get('link')
                if 'powvideo' in sUrl or 'streamplay' in sUrl:
                    continue
                sHosterUrl = sUrl

                sDisplayTitle = f'{sMovieTitle} - ({link.get("server")})'  
                oOutputParameterHandler.addParameter('sHosterUrl', sHosterUrl)
                oOutputParameterHandler.addParameter('siteUrl', sUrl)
                oOutputParameterHandler.addParameter('sMovieTitle', sMovieTitle)
                oOutputParameterHandler.addParameter('sThumb', sThumb)

                oGui.addLink(SITE_IDENTIFIER, 'showVidsrcLinks', sDisplayTitle, sThumb, sDisplayTitle, oOutputParameterHandler)

        except:
            VSlog('Failed to connect to api')

    if sServer == 'Antol307VVk':
        try:
            import re

            movie_id = simdb_id.replace('tt','')
            subtitles = f'https://rest.opensubtitles.org/search/imdbid-{movie_id}sublanguageid-ara'

            url = f'https://antol307vvk.com/play/{simdb_id}'
            default_domain = "https://antol307vvk.com"
            initial_headers = {
                'Referer': default_domain,
                'User-Agent': 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Mobile Safari/537.36"',
            }

            session = requests.Session()

            qualities= ['144', '240', '360', '480', '720', '1080', '2160']

            initial_response = session.get(url, headers=initial_headers, verify=False).text

            match = re.search(r'"file":"([^"]+)"', initial_response)
            url = match.group(1).replace('\\/', '/')

            match = re.search(r'"key":"([^"]+)"', initial_response)
            key = match.group(1).replace('\\/', '/')

            initial_headers['X-CSRF-TOKEN'] = key

            initial_response = session.post(url, headers=initial_headers, verify=False)

            data = json.loads(initial_response.text)

            hindi_file = next((item['file'] for item in data if item['title'] == 'English'), None)
            cleaned_file = hindi_file.replace('~', '')
            url = f'{default_domain}/playlist/{cleaned_file}.txt'

            initial_response = session.post(url, headers=initial_headers, verify=False)

            initial_response = session.post(initial_response.text, headers=initial_headers, verify=False)
            redirected_url = initial_response.url
            url = redirected_url.rsplit('/', 1)[0]
            for quality in qualities:
                if quality in initial_response.text:
                    sHosterUrl = f"{url}/{quality}/index.m3u8"
                    sQual = f'{quality}p'

                    sHosterUrl = f'{sHosterUrl}|Referer={sHosterUrl}?sub.info={subtitles}'
                    oHoster = cHosterGui().getHoster('vidsrcstream')
                    if oHoster:  
                        oHoster.setDisplayName(f'{sMovieTitle} ({sQual})')
                        oHoster.setFileName(sMovieTitle)
                        cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb)

        except:
            VSlog('Failed to connect to api')

    if sServer == 'Torrent':
        try:
            from resources.lib.scrapers import apibay
            
            sLinks = apibay.get_links('movie', simdb_id, sMovieTitle, '', '')
            for item in sLinks:
                sDisplayTitle = f'Quality: [COLOR orange]{item[3]}[/COLOR] Size: [COLOR gold]{item[2]}GB[/COLOR] File: {item[0].replace("."," ")}'
                sHosterUrl = item[1]
    
                oHoster = cHosterGui().getHoster('torrent')
                if oHoster:  
                    oHoster.setDisplayName(sDisplayTitle)
                    oHoster.setFileName(sMovieTitle)
                    cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb)

        except:
            VSlog('Error')

    oGui.setEndOfDirectory()

def showRiveLinks():
    oGui = cGui()

    oInputParameterHandler = cInputParameterHandler()
    sHosterUrl = oInputParameterHandler.getValue('sHosterUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')

    oHoster = cHosterGui().getHoster('direct_link')  
    if oHoster != False:
        oHoster.setDisplayName(sMovieTitle)
        oHoster.setFileName(sMovieTitle)
        cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb)

    oGui.setEndOfDirectory()

def whvx(id):
    import random, re
    from Cryptodome.Cipher import AES
    from Cryptodome.Util.Padding import pad
    from urllib.parse import urlparse

    base_url = f"https://vidfast.pro/movie/{id}"
    user_agent = "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Mobile Safari/537.36"
    default_domain = '{uri.scheme}://{uri.netloc}/'.format(uri=urlparse(base_url))
    headers = {
        "Accept": "*/*",
        "Referer": default_domain,
        "User-Agent": user_agent,
        "x-session": "",
        "X-Requested-With":"XMLHttpRequest",
        "X-Csrf-Token":"lVx7BVtk9c3SMNbF49PNvUc7GV5zzdem"
    }

    ''' Encodes input using Base64 with custom character mapping. '''
    def custom_encode(input_bytes):
        source_chars = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789-_"
        target_chars = "Ju9Egn27FZNe-kaMUtOBAmf0qp3xDYlTX6PhiL5SRjzQIsHvoVw_WC4dGc1Ky8rb"
        translation_table = str.maketrans(source_chars, target_chars)

        encoded = base64.urlsafe_b64encode(input_bytes).decode().rstrip('=')
        
        return encoded.translate(translation_table)

    session = requests.Session()

    response = session.get(base_url, headers=headers).text

    match = re.search(r'\\"en\\":\\"(.*?)\\"', response)
    if not match:
        exit(print("No data found!"))
    raw_data = match.group(1)

    key_hex = "13346e2c05211f72e46a465e953fd5410826715e28d927f92ea5f4daee985c8b"
    iv_hex = "b83bcd42b90f5364e9b95c398264bca4"
    aes_key = bytes.fromhex(key_hex)
    aes_iv = bytes.fromhex(iv_hex)

    cipher = AES.new(aes_key, AES.MODE_CBC, aes_iv)
    padded_data = pad(raw_data.encode(), AES.block_size)
    aes_encrypted = cipher.encrypt(padded_data)

    xor_key = bytes.fromhex("3fc3e051ddc9dd8a74")
    xor_result = bytes(b ^ xor_key[i % len(xor_key)] for i, b in enumerate(aes_encrypted))

    encoded_final = custom_encode(xor_result)

    static_path = "rebivol/ad/w/2c7998b18129848378021254f87db35df8f562b2/2cf30a7c/APA91nNHHa3xbnvasl8ciswLATkt2fIiVFciF5RLarK4oR7nrTpEDSBjO_kRoBJD730BWfo6bQZIpxCr-PAlSGc8GAAxueegNH5gNzrcqhPDliciuUDv0GTqb_2t1ik9pIAXpVaZ8inm6ey56Qf44wrOOPUfZYlkKuKs18mNKqBluBYTB5lBXWF/775d49bf3b9b4d082f5156cd9f36e21d42014547cd9282b1fe62ccbe3d09f66b/1000094661747536"
    data = {}
    api_servers = f"https://vidfast.pro/{static_path}/k33a7dwPZst1/{encoded_final}"
    response = session.post(api_servers, headers=headers, json=data).json()

    server = random.choice(response)['data']
    api_stream = f"https://vidfast.pro/{static_path}/p6PWA5s/{server}"
    response = requests.post(api_stream, headers=headers).json()

    video_url = response['url']

    return video_url

def rive(tmd_id, episode='1', season='1', stream_type='movie'):
    base_url = 'https://scrapper.rivestream.org'

    headers = {
        "Accept-Language": "en-US,en;q=0.9",
        "Connection": "keep-alive",
        "Origin": "https://rivestream.org",
        "Referer": "https://rivestream.org/",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-site",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36 Edg/132.0.0.0"
    }

    providers_response = requests.get(f"{base_url}/api/providers", headers=headers)
    providers_data = providers_response.json()
       
    servers = providers_data['data']
    cors = f"{os.getenv('CORS_PRXY', '')}?url=" if os.getenv('CORS_PRXY') else ''

    streams = []
    for server in servers:
        route = f"/api/provider?provider={server}&id={tmd_id}&season={season}&episode={episode}" if stream_type == 'series' else f"/api/provider?provider={server}&id={tmd_id}"
        url = cors + (base_url + route)
        try:
            res = requests.get(url + server, headers=headers, timeout=4)
            res.raise_for_status()
            subtitles = []
            if 'captions' in res.json().get('data', {}):
                for sub in res.json()['data']['captions']:
                    subtitles.append({'language': sub.get('label', '')[:2] or 'Und', 'uri': sub.get('file'), 'title': sub.get('label', 'Undefined')})
            for source in res.json().get('data', {}).get('sources', []):
                streams.append({"server": f"{source.get('source')}-{source.get('quality')}", "link": source.get('url'), "stream_type": "m3u8" if source.get('format') == 'hls' else 'mp4', "quality": source.get('quality'), "subtitles": subtitles})
        except:
            pass

    return streams

def get_rive_secret_key(e: int, c: list) -> str:
    if e is not None:
        return c[e % len(c)]
    else:
        return "rive"

def vidsrc(tmd_id, episode='1', season='1', stream_type='movie'):
    base_url = 'https://api.rgshows.me'

    headers = {
        "Host": "api.rgshows.me",
        "Origin": "https://www.vidsrc.wtf",
        "Referer": "https://www.vidsrc.wtf/",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36 Edg/135.0.0.0"
    }

    streams = [] # https://api.rgshows.me/premium_embeds/tv/93405/1/1

    route = f"/premium_embeds/tv/{tmd_id}/{season}/{episode}" if stream_type == 'series' else f"/premium_embeds/movie/{tmd_id}"
    url = (base_url + route)

    try:
        res = requests.get(url, headers=headers, timeout=4)
        res.raise_for_status()
        for source in res.json().get('links', {}):
            streams.append({"server": f"{source.get('host')}", "link": source.get('url')})
    except:
        pass

    return streams

def showVidsrcLinks():
    oGui = cGui()

    oInputParameterHandler = cInputParameterHandler()
    sHosterUrl = oInputParameterHandler.getValue('sHosterUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')

    if '/embed-4' in sHosterUrl:
        url_api = "https://rabbitthunder-eight.vercel.app/api/"
        urlapi = url_api + 'general' 

        idx = sHosterUrl

        ft={'id':idx}
        response = requests.post(urlapi, data=ft, verify=False)
        html = response.content
        html = html.decode(encoding='utf-8', errors='strict')
    
        jsdata = json.loads(html)

        sHosterUrl = jsdata.get('source', None) + "|Referer=" + sHosterUrl.split('embed')[0] 
        tracks = jsdata.get('subtitle', None)
        for track in tracks:
            if 'ara' not in track:
                continue

            sHosterUrl = sHosterUrl + '?sub.info=' + track

    oHoster = cHosterGui().checkHoster(sHosterUrl)
    if oHoster != False:
        oHoster.setDisplayName(sMovieTitle)
        oHoster.setFileName(sMovieTitle)
        cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb)

    oGui.setEndOfDirectory()