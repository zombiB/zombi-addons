# -*- coding: utf-8 -*-
# zombi https://github.com/zombiB/zombi-addons/

import re
import base64
from resources.lib.gui.hoster import cHosterGui
from resources.lib.gui.gui import cGui
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.comaddon import VSlog, siteManager, addon
from resources.lib.parser import cParser
from resources.lib import helpers
from resources.lib.util import Quote
from resources.lib import random_ua

ADDON = addon()
icons = ADDON.getSetting('defaultIcons')

SITE_IDENTIFIER = 'studiotv'
SITE_NAME = 'studio2tv'
SITE_DESC = 'arabic vod'
 
URL_MAIN = siteManager().getUrlMain(SITE_IDENTIFIER)

SPORT_LIVE = (URL_MAIN , 'showMovies')

UA = random_ua.get_pc_ua()
 
def load():
    oGui = cGui()

    oOutputParameterHandler = cOutputParameterHandler()    
    oOutputParameterHandler.addParameter('siteUrl', SPORT_LIVE[0])
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'بث مباشر', icons + '/Sport.png', oOutputParameterHandler)
   
    oGui.setEndOfDirectory()
	
    
def showMovies():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
 
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
    oParser = cParser()
            
	# (.+?) .+? ([^<]+)
    sPattern = '<div class="match-container.+?href="([^"]+)" title="([^"]+)".+?data-img="([^"]+)".+?data-start=["\']([^"\']+)["\']'
    aResult = oParser.parse(sHtmlContent, sPattern)

    if aResult[0]:
        oOutputParameterHandler = cOutputParameterHandler() 
        for aEntry in aResult[1]:
 
            sTitle =  aEntry[1]
            if 'مشاهد' in sTitle:
                sTitle = sTitle.split("مباراة")[1].split("اليوم")[0]
            sThumb = aEntry[2]
            siteUrl =  aEntry[0]
            sDesc = f'وقت المباراة \n {aEntry[3].split("T")[1].split("+")[0]}(GMT+2)'

            oOutputParameterHandler.addParameter('siteUrl',siteUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)

            oGui.addMisc(SITE_IDENTIFIER, 'showHosters', sTitle, '', sThumb, sDesc, oOutputParameterHandler)
 
    oGui.setEndOfDirectory()
	
def showHosters():
    oGui = cGui()
    
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')
    oParser = cParser()   

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
    if '.mp4' in sUrl:
        oOutputParameterHandler = cOutputParameterHandler()
        sTitle = ' نتيجة مباراة ' + sMovieTitle
        url = sUrl.split('src=')[1]
            
                
        sHosterUrl = url
        oHoster = cHosterGui().checkHoster(sHosterUrl)
        sHosterUrl = sHosterUrl 
        if oHoster:
           oHoster.setDisplayName(sTitle)
           oHoster.setFileName(sTitle)
           cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb, oOutputParameterHandler)

    murl = ''
    sPattern = 'iframe.src = ["\']([^"\']+)["\']'
    aResult = oParser.parse(sHtmlContent, sPattern)
    if aResult[0]:
        for aEntry in aResult[1]:
            murl = aEntry + sUrl.split('src=')[1]
    else:
        murl = []
        sPattern = '<iframe.+?src=["\']([^"\']+)["\']'
        aResult = oParser.parse(sHtmlContent, sPattern)
        if aResult[0]:
            oOutputParameterHandler = cOutputParameterHandler()
            for aEntry in aResult[1]:
                murl.append(str(aEntry))
                
        if '.mp4' in murl or '.m3u8' in murl:
            sHosterUrl = murl
            sTitle = sMovieTitle
            oHoster = cHosterGui().checkHoster(sHosterUrl)
            sHosterUrl = sHosterUrl 
            if oHoster:
                oHoster.setDisplayName(sTitle)
                oHoster.setFileName(sTitle)
                cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb, oOutputParameterHandler)
    for i in murl:
        oRequestHandler = cRequestHandler(i)
        sHtmlContent = oRequestHandler.request()

        sPattern = 'file: ["\']([^"\']+)["\']'
        aResult = re.findall(sPattern, sHtmlContent)
        if aResult:
            oOutputParameterHandler = cOutputParameterHandler()
            sHosterUrl = aResult[0]
            oHoster = cHosterGui().checkHoster(sHosterUrl)
            sHosterUrl = sHosterUrl + '|referer=' + i
            if oHoster:
                oHoster.setDisplayName(sMovieTitle)
                oHoster.setFileName(sMovieTitle)
                cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb, oOutputParameterHandler)

        sPattern = 'source:["\']([^"\']+)["\']'
        aResult = re.findall(sPattern, sHtmlContent)
        if aResult:
            oOutputParameterHandler = cOutputParameterHandler()
            sHosterUrl = aResult[0]
            oHoster = cHosterGui().checkHoster(sHosterUrl)
            sHosterUrl = sHosterUrl + '|referer=' + i
            if oHoster:
                oHoster.setDisplayName(sMovieTitle)
                oHoster.setFileName(sMovieTitle)
                cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb, oOutputParameterHandler)

        sPattern = 'file : ["\']([^"\']+)["\']'
        aResult = re.findall(sPattern, sHtmlContent)
        if aResult:
            oOutputParameterHandler = cOutputParameterHandler()
            sHosterUrl = aResult[0]
            oHoster = cHosterGui().checkHoster(sHosterUrl)
            sHosterUrl = sHosterUrl + '|referer=' + i
            if oHoster:
                oHoster.setDisplayName(sMovieTitle)
                oHoster.setFileName(sMovieTitle)
                cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb, oOutputParameterHandler)

        sPattern = 'url:"(.+?)",mimetype:'
        aResult = re.findall(sPattern, sHtmlContent)
        if aResult:
            oOutputParameterHandler = cOutputParameterHandler()
            sHosterUrl = aResult[0]
            oHoster = cHosterGui().checkHoster(sHosterUrl)
            sHosterUrl = sHosterUrl + '|referer=' + murl
            if oHoster:
                oHoster.setDisplayName(sMovieTitle)
                oHoster.setFileName(sMovieTitle)
                cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb, oOutputParameterHandler)

        if 'class="albaplayer' not in sHtmlContent:
            sPattern = '<iframe.+?id=["\']iframe["\'].+?src=["\']([^"\']+)["\']'
            aResult = oParser.parse(sHtmlContent, sPattern)
            if aResult[0]:
                for aEntry in aResult[1]:
                    murl = aEntry    

                    if '.mp4' in murl or '.m3u8' in murl or 'voodc' in murl or 'youtube' in murl:
                        sHosterUrl = murl
                        sTitle = sMovieTitle
                        oHoster = cHosterGui().checkHoster(sHosterUrl)
                        if oHoster:
                            oHoster.setDisplayName(sTitle)
                            oHoster.setFileName(sTitle)
                            cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb, oOutputParameterHandler)

                    else:
                        oRequestHandler = cRequestHandler(murl)
                        sHtmlContent = oRequestHandler.request()

            sPattern = '<iframe.+?src="([^"]+)" width='
            aResult = oParser.parse(sHtmlContent, sPattern)
            if aResult[0]:
                for aEntry in aResult[1]:
                    murl2 = aEntry    

                    if '.mp4' in murl2 or '.m3u8' in murl2 or 'voodc' in murl2 or 'youtube' in murl2:
                        sHosterUrl = murl2
                        sTitle = sMovieTitle
                        oHoster = cHosterGui().checkHoster(sHosterUrl)
                        if oHoster:
                            oHoster.setDisplayName(sTitle)
                            oHoster.setFileName(sTitle)
                            cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb, oOutputParameterHandler)


        sStart = 'class="albaplayer'
        sEnd = 'class="albaplayer'
        sHtmlContent0 = oParser.abParse(sHtmlContent, sStart, sEnd)

        sPattern = 'href="([^"]+)">(.+?)</a>'
        aResult = oParser.parse(sHtmlContent0, sPattern)
        if aResult[0]:
            oOutputParameterHandler = cOutputParameterHandler()
            for aEntry in aResult[1]:
                sTitle = aEntry[1]
                url = aEntry[0]

                oRequestHandler = cRequestHandler(url)
                sHtmlContent = oRequestHandler.request()

        sPattern = '<iframe.+?src="([^"]+)'
        aResult = oParser.parse(sHtmlContent0, sPattern)
        if aResult[0]:
            for aEntry in aResult[1]:
                if 'http' not in aEntry:
                    continue
                if 'javascript' in aEntry:
                    continue
                url = aEntry
                sTitle = sMovieTitle
                oRequestHandler = cRequestHandler(url)
                sHtmlContent = oRequestHandler.request()

        sPattern = 'source:\s*["\']([^"\']+)["\']'
        aResult = oParser.parse(sHtmlContent, sPattern)
        if aResult[0]:
                    for aEntry in aResult[1]:
                        url = aEntry
                        if 'm3u8' not in url:
                            try:
                                sPatternUrl = "source: 'https:\/\/'\s*\+\s*serv\s*\+\s*'([^']+)'"
                                sPatternPK = 'var servs = .+?,\s*"([^"]+)"'
                                aResultUrl = re.findall(sPatternUrl, sHtmlContent)
                                aResultPK = re.findall(sPatternPK, sHtmlContent)
                                if aResultUrl and aResultPK:
                                    url3 = 'http://'+aResultPK[0]+aResultUrl[0]
                                    url = url3 + "|Referer=" + url
                            except:
                                VSlog('no link detected')

                        sTitle = ('%s [COLOR coral](%s)[/COLOR]') % (sMovieTitle, sTitle)
                        if url.startswith('//'):
                            url = 'https:' + url
            
                        sHosterUrl = url
                        oHoster = cHosterGui().checkHoster(sHosterUrl)
                        sHosterUrl = sHosterUrl + '|AUTH=TLS&verifypeer=false'
                        if oHoster:
                            oHoster.setDisplayName(sTitle)
                            oHoster.setFileName(sTitle)
                            cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb, oOutputParameterHandler)

        sPattern = 'loadSource(.+?);'
        aResult = oParser.parse(sHtmlContent, sPattern)
        if aResult[0]:
                    for aEntry in aResult[1]:
                        url = aEntry.replace("('","").replace("')","")
                        sTitle = ('%s [COLOR coral](%s)[/COLOR]') % (sMovieTitle, sTitle)
                        if url.startswith('//'):
                            url = 'https:' + url
            
                        sHosterUrl = url
                        oHoster = cHosterGui().checkHoster(sHosterUrl)
                        sHosterUrl = sHosterUrl + '|AUTH=TLS&verifypeer=false'
                        if oHoster:
                            oHoster.setDisplayName(sTitle)
                            oHoster.setFileName(sTitle)
                            cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb, oOutputParameterHandler)   	

        sPattern = 'embeds =(.+?)",'
        aResult = oParser.parse(sHtmlContent, sPattern)
        if aResult[0]:
                    for aEntry in aResult[1]:
                        url = aEntry.replace(' ["',"")
                        if 'm3u8' in url:           
                            sHosterUrl = url.split('=')[1]
                        if '.php' in url:
                            oRequestHandler = cRequestHandler(url)
                            sHtmlContent2 = oRequestHandler.request()

                            sPattern =  "src='(.+?)' type="
                            aResult = oParser.parse(sHtmlContent2,sPattern)
                            if aResult[0]:
                                for aEntry in aResult[1]:
                                    url = aEntry
                                    sTitle = ('%s [COLOR coral](%s)[/COLOR]') % (sMovieTitle, sTitle)
                                    if url.startswith('//'):
                                        url = 'https:' + url
                                    sHosterUrl = url
                                    oHoster = cHosterGui().checkHoster(sHosterUrl)
                                    if oHoster:
                                        oHoster.setDisplayName(sTitle)
                                        oHoster.setFileName(sMovieTitle)
                                        cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb, oOutputParameterHandler)

        sPattern = '<iframe src="(.+?)" allowfullscreen'
        aResult = oParser.parse(sHtmlContent, sPattern)
        if aResult[0]:
                    for aEntry in aResult[1]:
                        url = aEntry.replace("('","").replace("')","")
                        sTitle = ('%s [COLOR coral](%s)[/COLOR]') % (sMovieTitle, sTitle)
                        if url.startswith('//'):
                            url = 'https:' + url

                        sHosterUrl = url
                        oHoster = cHosterGui().checkHoster(sHosterUrl)
                        sHosterUrl = sHosterUrl + '|AUTH=TLS&verifypeer=false'
                        if oHoster:
                            oHoster.setDisplayName(sTitle)
                            oHoster.setFileName(sTitle)
                            cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb, oOutputParameterHandler)

        sPattern = 'var file = ["\']([^"\']+)["\']'
        aResult = oParser.parse(sHtmlContent, sPattern)
        if aResult[0]:
                    for aEntry in aResult[1]:
                        url = aEntry
                        sTitle = ('%s [COLOR coral](%s)[/COLOR]') % (sMovieTitle, sTitle)
                        if url.startswith('//'):
                            url = 'https:' + url

                        sHosterUrl = url
                        oHoster = cHosterGui().checkHoster(sHosterUrl)
                        sHosterUrl = sHosterUrl + "|Referer=" + murl
                        if oHoster:
                            oHoster.setDisplayName(sTitle)
                            oHoster.setFileName(sTitle)
                            cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb, oOutputParameterHandler)

        sPattern = "<script>AlbaPlayerControl\((.+?)\,"
        aResult = oParser.parse(sHtmlContent, sPattern)
        if aResult[0]: 
                    for aEntry in aResult[1]:
                        url_tmp = aEntry.replace("'","").replace('"','')
                        url = base64.b64decode(url_tmp).decode('utf8',errors='ignore')
                        sTitle = sMovieTitle
                        sHosterUrl = url+ '|User-Agent=' + UA + '&Referer='+ murl

                        if 'vimeo' in sHosterUrl:
                            sHosterUrl = sHosterUrl + "|Referer=" + sUrl
                        oHoster = cHosterGui().checkHoster(sHosterUrl)
                        if oHoster:
                            oHoster.setDisplayName(sTitle)
                            oHoster.setFileName(sTitle)
                            cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb, oOutputParameterHandler)	

        sPattern = "<source src='(.+?)' type='application/x-mpegURL'"
        aResult = oParser.parse(sHtmlContent, sPattern)
        if aResult[0]:
                    for aEntry in aResult[1]:
                        url = aEntry.replace("('","").replace("')","")
                        sHosterUrl = url+ '|User-Agent=' + UA +'&Referer='+ murl 
                        sMovieTitle = sMovieTitle
                        if 'vimeo' in sHosterUrl:
                            sHosterUrl = sHosterUrl + "|Referer=" + sUrl
                        oHoster = cHosterGui().checkHoster(sHosterUrl)
                        if oHoster:
                            oHoster.setDisplayName(sMovieTitle+' '+sTitle)
                            oHoster.setFileName(sMovieTitle)
                            cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb, oOutputParameterHandler)

        sPattern = '<iframe.+?src="([^"]+)'
        aResult = oParser.parse(sHtmlContent, sPattern)
        if aResult[0]:
                    for aEntry in aResult[1]:
                        if 'http' not in aEntry:
                            continue
                        if 'javascript' in aEntry:
                            continue
                        url = aEntry
                        sTitle = ('%s [COLOR coral](%s)[/COLOR]') % (sMovieTitle, sTitle)

                        if 'sharecast' in url:
                            Referer =  "https://sharecast.ws/"
                            url = Hoster_ShareCast(url, Referer)

                        if 'live7' in url:
                            oRequestHandler = cRequestHandler(url)
                            oRequestHandler.addHeaderEntry('Referer', url)
                            data3 = oRequestHandler.request()

                            sPatternUrl = 'hlsUrl = "https:\/\/" \+ ea \+ "([^"]+)"'
                            sPatternPK = 'var pk = "([^"]+)"'
                            sPatternEA = 'ea = "([^"]+)";'
                            aResultUrl = re.findall(sPatternUrl, data3)
                            aResultEA = re.findall(sPatternEA, data3)
                            aResultPK = re.findall(sPatternPK, data3)
                            if aResultUrl and aResultPK and aResultEA:
                                aResultPK = aResultPK[0][:53] + aResultPK[0][54:] 
                                url3 = aResultEA[0] + aResultUrl[0] + aResultPK
                                url = 'https://' + url3

                        if 'sportsonline' in url:
                            url2 = getHosterIframe(url,url) 
                            url = url2   

                        if 'abolishstand' in url:
                            url2 = getHosterIframe(url,url) 
                            url = url2 + "|Referer=" + url

                        if 'realbitsport' in url:
                            url2 = getHosterIframe(url,url) 
                            url = url2   

                        if 'youtube' in url:
                            url = url  

                        if 'ok.ru' in aEntry:
                            url = aEntry 

                        if 'javascript' in url:
                            url = ''
                        if '/albaplayer/ch' in url:
                            if 'ch2cdn/' in url:
                                url = 'https://ninecdn.online/albaplayer/ch2cdn/'
                            if 'ch3cdn/' in url:
                                url = 'https://ninecdn.online/albaplayer/ch3cdn/'
                            if 'ch4cdn/' in url:
                                url = 'https://ninecdn.online/albaplayer/ch4cdn/'
                            oRequestHandler = cRequestHandler(url)
                            oRequestHandler.addHeaderEntry('Referer', url)
                            data3 = oRequestHandler.request()                        

                            sPattern = "AlbaPlayerControl.+?'([^\']+)"
                            aResult = re.findall(sPattern, data3)
                            if aResult:
                                url = f'{base64.b64decode(aResult[1]).decode("utf8",errors="ignore")}|Referer={url}'
                                sHosterUrl = url
                                oHoster = cHosterGui().checkHoster(sHosterUrl)
                                sHosterUrl = sHosterUrl
                                if oHoster:
                                    oHoster.setDisplayName(sTitle)
                                    oHoster.setFileName(sTitle)
                                    cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb, oInputParameterHandler=oInputParameterHandler)
                        elif '.php' in url or 'stream' in url or 'embed' in url:
                            url2 = getHosterIframe(url,url) 
                            url = url2   

                        sHosterUrl = url
                        oHoster = cHosterGui().checkHoster(sHosterUrl)
                        sHosterUrl = sHosterUrl
                        if oHoster:
                            oHoster.setDisplayName(sTitle)
                            oHoster.setFileName(sTitle)
                            cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb, oInputParameterHandler=oInputParameterHandler)

    oGui.setEndOfDirectory()    

def Hoster_ShareCast(url, referer):
    oRequestHandler = cRequestHandler(url)
    oRequestHandler.addHeaderEntry('User-Agent', UA)
    oRequestHandler.addHeaderEntry('Referer', referer)
    sHtmlContent = oRequestHandler.request()

    sPattern = "new Player\(.+?player\",\"([^\"]+)\",{'([^\']+)"
    aResult = re.findall(sPattern, sHtmlContent)
    if aResult:
        site = 'https://' + aResult[0][1]
        url = (site + '/hls/' + aResult[0][0]  + '/live.m3u8')
        return True, url  + '|Referer=' + Quote(site)

    return False, False

def getHosterIframe(url, referer):
    oRequestHandler = cRequestHandler(url)
    oRequestHandler.addHeaderEntry('Referer', referer)
    sHtmlContent = str(oRequestHandler.request())
    if not sHtmlContent:
        return False

    referer = url
    if 'channel' in referer:
         referer = referer.split('channel')[0]

    sHtmlContent = helpers.get_packed_data(sHtmlContent)
   
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
        if '.m3u8' in url or '.ts' in url or '.mp4' in url:
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
        if '.m3u8' in sHosterUrl or '.ts' in sHosterUrl or '.mp4' in sHosterUrl:
            return True, sHosterUrl 

    sPattern = '[^/]source.+?["\'](https.+?)["\']'
    aResult = re.findall(sPattern, sHtmlContent)
    if aResult:
        return aResult[0] + '|referer=' + referer

    sPattern = 'file: *["\'](https.+?\.m3u8)["\']'
    aResult = re.findall(sPattern, sHtmlContent)
    if aResult:
        return aResult[0] + '|referer=' + referer

    sPattern = "onload=\"ThePlayerJS\('.+?','([^\']+)"
    aResult = re.findall(sPattern, sHtmlContent)
    if aResult:
        url = 'https://sharecast.ws/player/' + aResult[0]
        b, url = Hoster_ShareCast(url, referer)
        if b:
            return True, url

    sPattern = '[^/]source.+?["\'](https.+?)["\']'
    aResult = re.findall(sPattern, sHtmlContent)
    if aResult:
        return True, aResult[0] + '|referer=' + url

    sPattern = 'source\s*["\'](https.+?\.m3u8)["\']'
    aResult = re.findall(sPattern, sHtmlContent)
    if aResult:
        return aResult[0] + '|referer=' + referer

    sPattern = '.atob\("(.+?)"'
    aResult = re.findall(sPattern, sHtmlContent)
    if aResult:
        import base64
        code = aResult[0]
        try:
            if isMatrix():
                code = base64.b64decode(code).decode('ascii')
            else:
                code = base64.b64decode(code)
            return code + '|Referer=' + referer
        except Exception as e:
            pass

    return False