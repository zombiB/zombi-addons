# -*- coding: utf-8 -*-

import re
import base64
import json
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

SITE_IDENTIFIER = 'witanime'
SITE_NAME = 'WitAnime'
SITE_DESC = 'arabic vod'
 
URL_MAIN = siteManager().getUrlMain(SITE_IDENTIFIER)
if addon().getSetting('Use_alternative') == "true":
    URL_MAIN = siteManager().getUrlMain2(SITE_IDENTIFIER)

ANIM_MOVIES = (f'{URL_MAIN}anime-type/movie/', 'showMovies')
ANIM_NEWS = (f'{URL_MAIN}episode/' , 'showSeries')
ANIM_LIST = (True, 'showAnimesList')

URL_SEARCH = (f'{URL_MAIN}?search_param=animes&s=', 'showMovies')
URL_SEARCH_ANIMS = (f'{URL_MAIN}?search_param=animes&s=', 'showSeries')

FUNCTION_SEARCH = 'showMovies'
 
def load():
    oGui = cGui()
    addons = addon()

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'http://venom/')
    oGui.addDir(SITE_IDENTIFIER, 'showSearch', addons.VSlang(30118), '1/Search.png', oOutputParameterHandler)
 
    oOutputParameterHandler.addParameter('siteUrl', ANIM_NEWS[0])
    oGui.addDir(SITE_IDENTIFIER, 'showSeries', 'مسلسلات انمي', '1/Anime.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', ANIM_MOVIES[0])
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'أفلام انمي', '1/Anime.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', f'{URL_MAIN}anime-status/%d9%8a%d8%b9%d8%b1%d8%b6-%d8%a7%d9%84%d8%a7%d9%86/')
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'يعرض الان', '1/Anime.png', oOutputParameterHandler) 

    oOutputParameterHandler.addParameter('siteUrl', f'{URL_MAIN}anime-season/صيف-2024/')
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'أنميات الموسم', '1/Anime.png', oOutputParameterHandler) 

    oOutputParameterHandler.addParameter('siteUrl', ANIM_LIST[0])
    oGui.addDir(SITE_IDENTIFIER, ANIM_LIST[1], 'قائمة الأنمي', 'az.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()

def showAnimesList():
    oGui = cGui()

    liste = []
    liste.append( ['#', f'{URL_MAIN}/en-anime-letter/228'] )
    liste.append( ['أ', f'{URL_MAIN}/ar-anime-letter/أ'] )
    liste.append( ['ب', f'{URL_MAIN}/ar-anime-letter/ب'] )
    liste.append( ['ت', f'{URL_MAIN}/ar-anime-letter/ت'] )
    liste.append( ['ث', f'{URL_MAIN}/ar-anime-letter/ث'] )
    liste.append( ['ج', f'{URL_MAIN}/ar-anime-letter/ج'] )
    liste.append( ['د', f'{URL_MAIN}/ar-anime-letter/د'] )
    liste.append( ['ر', f'{URL_MAIN}/ar-anime-letter/ر'] )
    liste.append( ['ز', f'{URL_MAIN}/ar-anime-letter/ز'] )
    liste.append( ['س', f'{URL_MAIN}/ar-anime-letter/س'] )
    liste.append( ['ش', f'{URL_MAIN}/ar-anime-letter/ش'] )
    liste.append( ['ط', f'{URL_MAIN}/ar-anime-letter/ط'] )
    liste.append( ['غ', f'{URL_MAIN}/ar-anime-letter/غ'] )
    liste.append( ['ف', f'{URL_MAIN}/ar-anime-letter/ف'] )
    liste.append( ['ك', f'{URL_MAIN}/ar-anime-letter/ك'] )
    liste.append( ['ل', f'{URL_MAIN}/ar-anime-letter/ل'] )
    liste.append( ['م', f'{URL_MAIN}/ar-anime-letter/م'] )
    liste.append( ['ن', f'{URL_MAIN}/ar-anime-letter/ن'] )
    liste.append( ['هـ', f'{URL_MAIN}/ar-anime-letter/ه'] )
    liste.append( ['و', f'{URL_MAIN}/ar-anime-letter/و'] )
    liste.append( ['ي', f'{URL_MAIN}/ar-anime-letter/ي'] )
    liste.append( ['A', f'{URL_MAIN}/en-anime-letter/A'] )
    liste.append( ['B', f'{URL_MAIN}/en-anime-letter/B'] )
    liste.append( ['C', f'{URL_MAIN}/en-anime-letter/C'] )
    liste.append( ['D', f'{URL_MAIN}/en-anime-letter/D'] )
    liste.append( ['E', f'{URL_MAIN}/en-anime-letter/E'] )
    liste.append( ['F', f'{URL_MAIN}/en-anime-letter/F'] )
    liste.append( ['G', f'{URL_MAIN}/en-anime-letter/G'] )
    liste.append( ['H', f'{URL_MAIN}/en-anime-letter/H'] )
    liste.append( ['I', f'{URL_MAIN}/en-anime-letter/I'] )
    liste.append( ['J', f'{URL_MAIN}/en-anime-letter/J'] )
    liste.append( ['K', f'{URL_MAIN}/en-anime-letter/K'] )
    liste.append( ['L', f'{URL_MAIN}/en-anime-letter/L'] )
    liste.append( ['M', f'{URL_MAIN}/en-anime-letter/M'] )
    liste.append( ['N', f'{URL_MAIN}/en-anime-letter/N'] )
    liste.append( ['O', f'{URL_MAIN}/en-anime-letter/O'] )
    liste.append( ['P', f'{URL_MAIN}/en-anime-letter/P'] )
    liste.append( ['Q', f'{URL_MAIN}/en-anime-letter/Q'] )
    liste.append( ['R', f'{URL_MAIN}/en-anime-letter/R'] )
    liste.append( ['S', f'{URL_MAIN}/en-anime-letter/S'] )
    liste.append( ['T', f'{URL_MAIN}/en-anime-letter/T'] )
    liste.append( ['U', f'{URL_MAIN}/en-anime-letter/U'] )
    liste.append( ['V', f'{URL_MAIN}/en-anime-letter/V'] )
    liste.append( ['W', f'{URL_MAIN}/en-anime-letter/W'] )
    liste.append( ['X', f'{URL_MAIN}/en-anime-letter/X'] )
    liste.append( ['Y', f'{URL_MAIN}/en-anime-letter/Y'] )
    liste.append( ['Z', f'{URL_MAIN}/en-anime-letter/Z'] )

    for sTitle, sUrl in liste:

        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', sUrl)
        oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'Letter [COLOR coral]' + sTitle + '[/COLOR]', 'az.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()

def showSearch():
    oGui = cGui()
 
    sSearchText = oGui.showKeyBoard()
    if sSearchText:
        sUrl = f'{URL_MAIN}?search_param=animes&s={sSearchText}'
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
    sPattern = '<img class="img-responsive" src="([^<]+)" alt="([^<]+)" />.+?data-content="([^<]+)".+?<h3><a href="([^<]+)">'
    aResult = oParser.parse(sHtmlContent, sPattern)		
    if aResult[0]:
        total = len(aResult[1])
        progress_ = progress().VScreate(SITE_NAME)
        oOutputParameterHandler = cOutputParameterHandler()
        for aEntry in aResult[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break
 
            sTitle = cUtil().CleanSeriesName(aEntry[1])
            siteUrl = aEntry[3]
            sThumb = re.sub(r'-\d+x\d{0,3}','', aEntry[0])  
            sDesc = aEntry[2]
            sYear = ''

            oOutputParameterHandler.addParameter('siteUrl', siteUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oOutputParameterHandler.addParameter('sYear', sYear)
            oOutputParameterHandler.addParameter('sDesc', sDesc)
            oGui.addAnime(SITE_IDENTIFIER, 'ShowEps', sTitle, '', sThumb, sDesc, oOutputParameterHandler) 

        progress_.VSclose(progress_)
 
        sNextPage = __checkForNextPage(sHtmlContent)
        if sNextPage:
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sNextPage)
            oGui.addDir(SITE_IDENTIFIER, 'showMovies', '[COLOR teal]Next >>>[/COLOR]', 'next.png', oOutputParameterHandler)
 
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

    sPattern = '<img class="img-responsive" src="([^<]+)" alt="([^<]+)" />.+?data-content="([^<]+)".+?<h3><a href="([^<]+)">'
    aResult = oParser.parse(sHtmlContent, sPattern)	
    if aResult[0]:
        total = len(aResult[1])
        progress_ = progress().VScreate(SITE_NAME)
        oOutputParameterHandler = cOutputParameterHandler()
        for aEntry in aResult[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break
 
            sTitle = cUtil().CleanSeriesName(aEntry[1])
            siteUrl = aEntry[3]
            sThumb = re.sub(r'-\d+x\d{0,3}','', aEntry[0])  
            sDesc = aEntry[2]
            sYear = ''

            oOutputParameterHandler.addParameter('siteUrl', siteUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oOutputParameterHandler.addParameter('sYear', sYear)
            oOutputParameterHandler.addParameter('sDesc', sDesc)
			
            oGui.addAnime(SITE_IDENTIFIER, 'ShowEps', sTitle, '', sThumb, sDesc, oOutputParameterHandler)

        progress_.VSclose(progress_)
 
        sNextPage = __checkForNextPage(sHtmlContent)
        if sNextPage:
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sNextPage)
            oGui.addDir(SITE_IDENTIFIER, 'showSeries', '[COLOR teal]Next >>>[/COLOR]', 'next.png', oOutputParameterHandler)
 
    if not sSearch:
        oGui.setEndOfDirectory()
 
def ShowEps():
    oGui = cGui()   
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')
    sDesc = oInputParameterHandler.getValue('sDesc')

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request() 

    oParser = cParser()
    sStart = '<div class="episodes-list-content">'
    sEnd = '<div class="space"></div>'
    sHtmlContent1 = oParser.abParse(sHtmlContent, sStart, sEnd)

    sPattern = '<h3><a href=.+?onclick="(.+?)">([^<]+)</a></h3>.+?src="([^"]+)'
    aResult = oParser.parse(sHtmlContent1, sPattern)   
    if aResult[0]:
        oOutputParameterHandler = cOutputParameterHandler()
        for aEntry in aResult[1]:
 
            sEp = aEntry[1].replace("الحلقة ","").replace("الفلم ","").replace("الخاصة ","")
            sTitle = f'{sMovieTitle} E{sEp}'
            EnCodedUrl = aEntry[0].replace("openEpisode('","").replace("')","")
            siteUrl = base64.b64decode(EnCodedUrl).decode('utf8',errors='ignore')
            sDesc = ''
            sYear = ''
            sThumb = re.sub(r'-\d+x\d{0,3}','', aEntry[2])  
 
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('siteUrl', siteUrl)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oOutputParameterHandler.addParameter('sYear', sYear)
            oOutputParameterHandler.addParameter('sDesc', sDesc)
            oGui.addEpisode(SITE_IDENTIFIER, 'showHosters', sTitle, '', sThumb, sDesc, oOutputParameterHandler) 
    else:
        sPattern = "processedEpisodeData = '([^']+)'"
        aResult = oParser.parse(sHtmlContent, sPattern)
        if aResult[0]:        
            sEps = decode(aResult[1][0])
            oOutputParameterHandler = cOutputParameterHandler()
            for item in sEps:
                sEp = item["number"]
                sTitle = f'{sMovieTitle} E{sEp}'
                siteUrl = item["url"]
                sDesc = ''
                sYear = ''
                sThumb = re.sub(r'-\d+x\d{0,3}','', item["screenshot"])  
    
                oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
                oOutputParameterHandler.addParameter('siteUrl', siteUrl)
                oOutputParameterHandler.addParameter('sThumb', sThumb)
                oOutputParameterHandler.addParameter('sYear', sYear)
                oOutputParameterHandler.addParameter('sDesc', sDesc)
                oGui.addEpisode(SITE_IDENTIFIER, 'showHosters', sTitle, '', sThumb, sDesc, oOutputParameterHandler) 

    oGui.setEndOfDirectory()

def __checkForNextPage(sHtmlContent):
    sPattern = '<link rel="next" href="([^<]+)" />'
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
    if aResult[0]:        
        return aResult[1][0]

    return False

def showHosters():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')
    
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
    oParser = cParser()

    sPattern = '_zH=\s*"([^"]+)"'
    aResult = oParser.parse(sHtmlContent, sPattern)
    if aResult[0]:        
        _zH = aResult[1][0]
        config_settings_list = json.loads(base64.b64decode(_zH).decode('utf-8'))

    sPattern = 'var _zG=\s*"([^"]+)"'
    aResult = oParser.parse(sHtmlContent, sPattern)
    if aResult[0]:        
        _zG = aResult[1][0]
        processed_resource = process_resource_data(_zG)
        decoded_results = []

        matches = re.findall(r'aHR0[A-Za-z0-9+/=]+?(?=aHR0|$)', processed_resource)
        decoded_results = []
        for i, base64_str in enumerate(matches):
            config_settings = config_settings_list[i]
            param_offset = get_parameter_offset(config_settings)
            decoded_resource = base64.b64decode(base64_str).decode("utf-8")[:-param_offset]
            if " " in decoded_resource:
                decoded_results.extend(decoded_resource.split(" "))
            else:
                decoded_results.append(decoded_resource)
                
        for result in decoded_results:
            url = result
            if url.startswith('//'):
                url = 'http:' + url
            if 'yona' in url:
                sPattern = "src='([^']+)' id='ltsm-js'>"
                aResult = oParser.parse(sHtmlContent, sPattern)
                if aResult[0]:        
                    api_key_url = aResult[1][0]

                    oRequestHandler = cRequestHandler(api_key_url)
                    sHtmlContent2 = oRequestHandler.request()
                    
                    pattern = r'var _m1 = "([^"]+)", _m2 = "([^"]+)", _m3 = "([^"]+)", _m4 = "([^"]+)";'
                    match = re.search(pattern, sHtmlContent2)
                    if match:
                        api_key = match.group(1) + match.group(2) + match.group(3) + match.group(4)

                        url = f'{url}&apiKey={api_key}'
                        oRequestHandler = cRequestHandler(url)
                        oRequestHandler.addHeaderEntry('User-Agent', UA)
                        oRequestHandler.addHeaderEntry('Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7')
                        oRequestHandler.addHeaderEntry('Referer', URL_MAIN)
                        sData = oRequestHandler.request()
                        
                        sPattern = 'go_to_player(.+?)".+?<p>([^<]+)'
                        aResult = oParser.parse(sData, sPattern)
                        if aResult[0]:
                            for aEntry in reversed(aResult[1]):  
                                if 'mega' in aEntry[0]:
                                    continue      
                                url = aEntry[0].replace(')','').replace('(','').replace("'","").replace('"','')
                                sQual = aEntry[1].replace('-','').replace(' ','')

                                try:
                                    sHosterUrl = base64.b64decode(f'{url}==').decode('utf8',errors='ignore')
                                except:
                                    sHosterUrl = url
                                if 'soraplay' in sHosterUrl:
                                    sHosterUrl = f'{sHosterUrl}|Referer={URL_MAIN}'

                                oHoster = cHosterGui().checkHoster(sHosterUrl)
                                if oHoster:
                                    sDisplayTitle = f'{sMovieTitle} [COLOR coral] Yonaplay ({sQual})[/COLOR]'
                                    oHoster.setDisplayName(sDisplayTitle)
                                    oHoster.setFileName(sMovieTitle)
                                    cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb)                 

            else:
                sHosterUrl = url
                oHoster = cHosterGui().checkHoster(sHosterUrl)
                if oHoster:
                    sDisplayTitle = f'{sMovieTitle}'
                    oHoster.setDisplayName(sDisplayTitle)
                    oHoster.setFileName(sMovieTitle)
                    cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb)
    try:
        secret_match = re.search(r'_m = {"r":"(.*?)"};', sHtmlContent)
        secret = base64.b64decode(secret_match.group(1)).decode()

        p_vars = re.findall(r"var (_p\d+) = \[(.*?)\];", sHtmlContent)
        encrypted_chunks = []
        for var_name, var_values_str in p_vars:
            values = [v.strip().strip('"') for v in var_values_str.split(',')]
            encrypted_chunks.append(values)

        s_var = re.search(r"var _s = \[(.*?)\];", sHtmlContent)
        sequence_data = []
        if s_var:
            sequence_values_str = s_var.group(1)
            sequence_data = [v.strip().strip('"') for v in sequence_values_str.split(',')]

        encrypted_chunks = [data for data in encrypted_chunks]

        sequences = [json.loads(process(seq_raw.strip('"'), secret)) for seq_raw in sequence_data]
        decrypted_chunks = [[process(chunk, secret) for chunk in group] for group in encrypted_chunks]
        arranged_content = []

        for i in range(len(sequences)):
            arranged = [""] * (max(sequences[i]) + 1)
            for j, pos in enumerate(sequences[i]):
                if pos < len(arranged) and j < len(decrypted_chunks[i]):
                    arranged[pos] = decrypted_chunks[i][j]
            arranged_content.append("".join(arranged))

        for item in arranged_content:

            url = item
            if url.startswith('//'):
                url = 'http:' + url           

            sHosterUrl = url
            oHoster = cHosterGui().checkHoster(sHosterUrl)
            if oHoster:
                sDisplayTitle = f'{sMovieTitle}'
                oHoster.setDisplayName(sDisplayTitle)
                oHoster.setFileName(sMovieTitle)
                cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb)
    except:
        VSlog('Failed to get download links')
	       
    oGui.setEndOfDirectory()


def get_parameter_offset(config_settings):
    """Decodes the key, retrieves the corresponding offset from 'd' list."""
    index_key = int(base64.b64decode(config_settings["k"]).decode("utf-8"), 10)
    return config_settings["d"][index_key]

def decode_base64(encoded_string):
    return base64.b64decode(encoded_string).decode('utf-8')

def process_resource_data(encoded_data):
    decoded_data = decode_base64(encoded_data)
    reversed_data = decoded_data[::-1]
    sanitized_data = ''.join(re.sub(r'[^A-Za-z0-9+/=]', '', reversed_data))

    return sanitized_data

def process(raw, secret):
    data = bytes.fromhex(raw)
    return ''.join(chr(byte ^ ord(secret[i % len(secret)])) for i, byte in enumerate(data))

def decode(data: str):
        parts = data.split(".")
        if len(parts) != 2:
            raise VSlog("Bad data format")

        try:
            decoded_part1 = base64.b64decode(parts[0])
            decoded_part2 = base64.b64decode(parts[1])
        except Exception as err:
            return None, err

        decoded_data = bytearray(len(decoded_part1))
        for i in range(len(decoded_part1)):
            decoded_data[i] = decoded_part1[i] ^ decoded_part2[i % len(decoded_part2)]

        clean_data = decoded_data.decode('utf-8').replace(r'\"', '"')

        try:
            decoded_json = json.loads(clean_data)
        except json.JSONDecodeError as err:
            return None, err

        return decoded_json