# -*- coding: utf-8 -*-

from resources.lib.gui.hoster import cHosterGui
from resources.lib.gui.gui import cGui
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.comaddon import progress, VSlog, siteManager, isMatrix
from resources.lib.parser import cParser
 
SITE_IDENTIFIER = 'beinmatch'
SITE_NAME = 'Beinmatch'
SITE_DESC = 'arabic vod'
 
URL_MAIN = siteManager().getUrlMain(SITE_IDENTIFIER)

SPORT_LIVE = (URL_MAIN, 'showMovies')
 
def load():
    oGui = cGui()

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', SPORT_LIVE[0])
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'بث مباشر و أهداف و ملخصات', 'sport.png', oOutputParameterHandler)
  
    oGui.setEndOfDirectory()
   
def showMovies(sSearch = ''):
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
 
    oRequestHandler = cRequestHandler(sUrl)
    oRequestHandler.enableCache(False)
    sHtmlContent = oRequestHandler.request()
 
    oParser = cParser()
    sPattern =  '<link rel="canonical" href="([^"]+)' 
    aResult = oParser.parse(sHtmlContent,sPattern)
    if aResult[0]:
        mSite = aResult[1][0] 

    sPattern = 'onclick="goToMatch\((.+?)\,["\']([^"\']+)["\']\);".+?<span class="matchTime">([^<]+)</span>'
    sPattern += '.+?<img class="imgTeam" src=["\']([^"\']+)["\'].+?class="textMatch">(.+?)</div>' 
    aResult = oParser.parse(sHtmlContent, sPattern)
    if aResult[0]:
        total = len(aResult[1])
        progress_ = progress().VScreate(SITE_NAME)
        oOutputParameterHandler = cOutputParameterHandler()  
        for aEntry in aResult[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break
 
            sTitle =  aEntry[1].replace('_',' ')
            sThumb = ''
            if aEntry[3]:
                sThumb = aEntry[3]
            siteUrl = f'{mSite}bein/live/{aEntry[0]}'
            if siteUrl.startswith('//'):
                siteUrl = f'http:{aEntry[0]}'
            sDesc = aEntry[2]
            if aEntry[4]:
                sDesc = f'{aEntry[2]} \n \nوقت المباراة: {aEntry[4]}'
						
            oOutputParameterHandler.addParameter('siteUrl',siteUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)

            oGui.addMisc(SITE_IDENTIFIER, 'showLive', sTitle, '', sThumb, sDesc, oOutputParameterHandler)
        
        progress_.VSclose(progress_)
 
    oGui.setEndOfDirectory()
  
def showLive():
    oGui = cGui()
   
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    oParser = cParser()
    sPattern =  '<link rel="canonical" href="([^"]+)' 
    aResult = oParser.parse(sHtmlContent,sPattern)
    if aResult[0]:
        mSite = aResult[1][0] 

    sPattern = 'source: "(.+?)",'
    aResult = oParser.parse(sHtmlContent, sPattern)
    if aResult[0]:
        for aEntry in aResult[1]:
            
            url = aEntry
            sHosterUrl = url
            if 'vimeo' in sHosterUrl:
                sHosterUrl = sHosterUrl + "|Referer=" + mSite
            if 'akamaized' in sHosterUrl:
                sHosterUrl = sHosterUrl
            else:
                sHosterUrl = sHosterUrl + '|Referer=' + mSite
            if sHosterUrl.startswith('//'):
                sHosterUrl = 'http:' + sHosterUrl            

            oHoster = cHosterGui().checkHoster(sHosterUrl)
            if oHoster:
                oHoster.setDisplayName(sMovieTitle)
                oHoster.setFileName(sMovieTitle)
                cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb)

    sPattern = '<iframe.+?src="([^"]+)'
    aResult = oParser.parse(sHtmlContent, sPattern)
    if aResult[0]:
        for aEntry in aResult[1]:
            
            url = aEntry
            if '.php' in url:           
                oRequestHandler = cRequestHandler(url)
                sHtmlContent1 = oRequestHandler.request() 
                sPattern =  'src="([^"]+)'
                aResult = oParser.parse(sHtmlContent1,sPattern)
                if aResult[0]:
                     url = aResult[1][0]
 
                     sHosterUrl = url

                     if 'vimeo' in sHosterUrl:
                         sHosterUrl = sHosterUrl + "|Referer=" + mSite                  

                     oHoster = cHosterGui().checkHoster(sHosterUrl)
                     if oHoster:
                               oHoster.setDisplayName(sMovieTitle)
                               oHoster.setFileName(sMovieTitle)
                               cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb)

            elif 'youtube' in url:
                url = url.split('?')[0]     
                sHosterUrl = url

            elif '/embed' in url:
                if url.startswith('//'):
                    url = 'http:' + url     
   
                url = getHosterIframe(url, url) 
                sHosterUrl = url   

            elif 'vimeo' in url:
                sHosterUrl = sHosterUrl + "|Referer=" + mSite

            if sHosterUrl.startswith('//'):
                sHosterUrl = 'http:' + sHosterUrl            

            oHoster = cHosterGui().checkHoster(sHosterUrl)
            if oHoster:
                oHoster.setDisplayName(sMovieTitle)
                oHoster.setFileName(sMovieTitle)
                cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb)

    sPattern = 'onclick="goToLink(.+?), (.+?),'  
    aResult = oParser.parse(sHtmlContent, sPattern)
    if aResult[0]:
        for aEntry in aResult[1]:
            siteUrl = mSite+"bein/live/"+aEntry[0].replace("(","")
            siteUrl = siteUrl+'/'+aEntry[1]
            oRequestHandler = cRequestHandler(siteUrl)
            sHtmlContent0 = oRequestHandler.request()

            sStart = '<div id="contentBody">'
            sEnd = '<div id="leftSide">'
            sHtmlContent0 = oParser.abParse(sHtmlContent0, sStart, sEnd)

            sPattern = '<iframe.+?src="([^"]+)'
            aResult = oParser.parse(sHtmlContent0, sPattern)
            if aResult[0]:
                for aEntry in aResult[1]:
                    url = aEntry
                    sHosterUrl = url
                    sDisplayTitle = sMovieTitle

                    if sHosterUrl.startswith('//'):
                        sHosterUrl = 'http:' + sHosterUrl            
                    sHosterUrl = sHosterUrl + '|Referer=' + mSite
                    oHoster = cHosterGui().checkHoster(sHosterUrl)
                    if oHoster:
                        oHoster.setDisplayName(sDisplayTitle)
                        oHoster.setFileName(sMovieTitle)
                        cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb)


    sPattern = 'href="javascript:goToMatch(.+?), (.+?),.+?>(.+?)</a>'   
    aResult = oParser.parse(sHtmlContent, sPattern)
    if aResult[0]:
        for aEntry in aResult[1]:
            sTitle = aEntry[2]
            siteUrl = mSite+"bein/live/"+aEntry[0].replace("(","")
            siteUrl = siteUrl+'/'+aEntry[1]
            oRequestHandler = cRequestHandler(siteUrl)
            sHtmlContent2 = oRequestHandler.request()

            sPattern = '<iframe.+?src="([^"]+)'
            aResult = oParser.parse(sHtmlContent2, sPattern)
            if aResult[0]:
                for aEntry in aResult[1]:
                    url = aEntry
                    if url.startswith('//'):
                        url = 'http:' + url
                        
                    if 'embed' in url:
                        url = getHosterIframe(url, url) 
                        sHosterUrl = url
                    else:
                        sHosterUrl = url + '|Referer=' + mSite

                    sDisplayTitle = sMovieTitle+' - '+sTitle
          
                    oHoster = cHosterGui().checkHoster(sHosterUrl)
                    if oHoster:
                        oHoster.setDisplayName(sDisplayTitle)
                        oHoster.setFileName(sMovieTitle)
                        cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb)

            sPattern = 'source: "(.+?)",'
            aResult = oParser.parse(sHtmlContent, sPattern)
            if aResult[0]:
                for aEntry in aResult[1]:
            
                    url = aEntry
                    sHosterUrl = url
                    sDisplayTitle = sMovieTitle+' - '+sTitle

                    if sHosterUrl.startswith('//'):
                        sHosterUrl = 'http:' + sHosterUrl            
                    sHosterUrl = sHosterUrl + '|Referer=' + mSite
                    oHoster = cHosterGui().checkHoster(sHosterUrl)
                    if oHoster:
                        oHoster.setDisplayName(sDisplayTitle)
                        oHoster.setFileName(sMovieTitle)
                        cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb)

    else:
        sPattern = 'id="video-container".+?<video.+?src="([^"]+)'
        aResult = oParser.parse(sHtmlContent, sPattern)
        if aResult[0]:
            for aEntry in aResult[1]:
            
                sHosterUrl = aEntry
                if sHosterUrl.startswith('//'):
                    sHosterUrl = 'http:' + sHosterUrl            

                oHoster = cHosterGui().checkHoster(sHosterUrl)
                if oHoster:
                    oHoster.setDisplayName('لم يتم بعد وضع بث لهذه المباراة')
                    oHoster.setFileName(sMovieTitle)
                    cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb)

        sPattern = 'itemprop="embedUrl" content="([^"]+)'
        aResult = oParser.parse(sHtmlContent, sPattern)
        if aResult[0]:
            for aEntry in aResult[1]:
            
                sHosterUrl = aEntry
                if sHosterUrl.startswith('//'):
                    sHosterUrl = 'http:' + sHosterUrl            

                oHoster = cHosterGui().checkHoster(sHosterUrl)
                if oHoster:
                    oHoster.setDisplayName('شاهد الاهداف')
                    oHoster.setFileName(sMovieTitle)
                    cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb)
            
    oGui.setEndOfDirectory() 

def getHosterIframe(url, referer):
    import re
    from resources.lib.packer import cPacker
    from resources.lib.util import Quote


    oRequestHandler = cRequestHandler(url)
    oRequestHandler.addHeaderEntry('Referer', referer)
    oRequestHandler.enableCache(False)
    sHtmlContent = str(oRequestHandler.request())
    if not sHtmlContent:
        return False

    if 'channel' in url:
         referer = url.split('channel')[0]

    pattern = r"(\s*eval\s*\(\s*function\(p,a,c,k,e(?:.|\s)+?)<\/script>"
    matches = re.finditer(pattern, sHtmlContent)

    second_match = None
    for i, match in enumerate(matches, start=1):
        if i == 2:
            second_match = match
            break

    if second_match:
        sHtmlContent = cPacker().unpack(second_match.group())
    else:
        sPattern = '(\s*eval\s*\(\s*function(?:.|\s)+?{}\)\))'
        aResult = re.findall(sPattern, sHtmlContent)
        if aResult:
            sstr = aResult[0]
            if not sstr.endswith(';'):
                sstr = sstr + ';'
            sHtmlContent = cPacker().unpack(sstr)

        sPattern = '(\s*eval\s*\(\s*function\(p,a,c,k,e(?:.|\s)+?)<\/script>'
        aResult = re.findall(sPattern, sHtmlContent)
        if aResult:
            sstr = aResult[0]
            if not sstr.endswith(';'):
                sstr = sstr + ';'
            sHtmlContent = cPacker().unpack(sstr)

    sPattern = '.atob\("(.+?)"'
    aResult = re.findall(sPattern, sHtmlContent)
    if aResult:
        import base64
        for code in aResult:
            try:
                if isMatrix():
                    code = base64.b64decode(code).decode('ascii')
                else:
                    code = base64.b64decode(code)
                if '.m3u8' in code:
                    return True, code + '|Referer=' + url
            except Exception as e:
                pass

    sPattern = "mimeType: *\"application\/x-mpegURL\",\r\nsource:'([^']+)"
    aResult = re.findall(sPattern, sHtmlContent)
    if aResult:
        oRequestHandler = cRequestHandler(aResult[0])
        oRequestHandler.request()
        sHosterUrl = oRequestHandler.getRealUrl()
        return sHosterUrl + '|referer=' + referer

    sPattern = '<iframe.+?src=["\']([^"\']+)["\']'
    aResult = re.findall(sPattern, sHtmlContent)
    if aResult:
        for url in aResult:
            if url.startswith("./"):
                url = url[1:]
            if not url.startswith("http"):
                if not url.startswith("//"):
                    url = '//'+referer.split('/')[2] + url  
                url = "https:" + url
            referer2 = url.split('embed')[0]
            url = getHosterIframe(url, referer)
            if url:
                return url + "|Referer=" + referer2 

    sPattern = 'src=["\']([^"\']+)["\']'
    aResult = re.findall(sPattern, sHtmlContent)
    if aResult:
        url = aResult[0]
        if '.m3u8' in url:
            return url + '|referer=' + referer

    sPattern = "new Player\(.+?player\",\"([^\"]+)\",{'([^\']+)"
    aResult = re.findall(sPattern, sHtmlContent)
    if aResult:
        site = 'https://' + aResult[0][1]
        url = (site + '/hls/' + aResult[0][0]  + '/live.m3u8') + '|Referer=' + Quote(site)
        return url 

    sPattern = 'player.load\({source: (.+?)\('
    aResult = re.findall(sPattern, sHtmlContent)
    if aResult:
        func = aResult[0]
        sPattern = 'function %s\(\) +{\n + return\(\[([^\]]+)' % func
        aResult = re.findall(sPattern, sHtmlContent)
        if aResult:
            referer = url
            sHosterUrl = aResult[0].replace('"', '').replace(',', '').replace('\\', '').replace('////', '//')
            return True, sHosterUrl + '|referer=' + referer

    sPattern = ';var.+?src=["\']([^"\']+)["\']'
    aResult = re.findall(sPattern, sHtmlContent)
    if aResult:
        sHosterUrl = aResult[0]
        if '.m3u8' in sHosterUrl:
            return True, sHosterUrl 

    sPattern = 'file: *["\'](https.+?\.m3u8)["\']'
    aResult = re.findall(sPattern, sHtmlContent)
    if aResult:
        oRequestHandler = cRequestHandler(aResult[0])
        oRequestHandler.request()
        sHosterUrl = oRequestHandler.getRealUrl()
        return True, sHosterUrl + '|referer=' + referer

    sPattern = '[^/]source.+?["\'](https.+?)["\']'
    aResult = re.findall(sPattern, sHtmlContent)
    if aResult:
        for sHosterUrl in aResult:
            if '.m3u8' in sHosterUrl:
                if 'fls/cdn/' in sHosterUrl:
                    sHosterUrl = sHosterUrl.replace('/playlist.', '/tracks-v1a1/mono.')
                else:
                    oRequestHandler = cRequestHandler(sHosterUrl)
                    oRequestHandler.addHeaderEntry('Referer', referer)
                    oRequestHandler.request()
                    sHosterUrl = oRequestHandler.getRealUrl()
                    return sHosterUrl + '|referer=' + referer

    sPattern = 'source\s*["\'](https.+?\.m3u8)["\']'
    aResult = re.findall(sPattern, sHtmlContent)
    if aResult:
        return aResult[0] + '|referer=' + referer

    return False
	