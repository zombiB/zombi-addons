# -*- coding: utf-8 -*-
# zombi https://github.com/zombiB/zombi-addons/

import re

from resources.lib.gui.hoster import cHosterGui
from resources.lib.gui.gui import cGui
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.comaddon import VSlog, siteManager, addon
from resources.lib.parser import cParser
from resources.lib.packer import cPacker
from resources.lib.util import Quote

ADDON = addon()
icons = ADDON.getSetting('defaultIcons')

SITE_IDENTIFIER = 'koralive'
SITE_NAME = 'Koralive'
SITE_DESC = 'arabic vod'
 
URL_MAIN = siteManager().getUrlMain(SITE_IDENTIFIER)

SPORT_LIVE = (URL_MAIN , 'showMovies')

UA = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:56.0) Gecko/20100101 Firefox/56.0'
 
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
	# (.+?) .+? 
    sPattern = '<div class="match-container"><a href="(.+?)" target="_blank" title=".+?"><div class="right-team"><div class="team-logo"><img alt="(.+?)" src="(.+?)" title=.+?<img alt="(.+?)" src='
    aResult = oParser.parse(sHtmlContent, sPattern)



    if aResult[0]:
        oOutputParameterHandler = cOutputParameterHandler() 
        for aEntry in aResult[1]:
            if "#" in aEntry[0]:
                sCondition = "لا توجد روابط للمباراة \n \n"
            else:
                sCondition = "الروابط متاحة \n \n"
 
            sTitle =  aEntry[1]+'-'+aEntry[3]

            if 'مباراة' in sTitle:
                sTitle = sTitle.split('مباراة')[1]
                if 'كورة' in sTitle:
                    sTitle = sTitle.split('كورة')[0]
            sThumb = aEntry[2]
            siteUrl =  aEntry[0]

            sDesc = sCondition 
			
			

            oOutputParameterHandler.addParameter('siteUrl',siteUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)

            oGui.addMisc(SITE_IDENTIFIER, 'showHosters', sTitle, '', sThumb, sDesc, oOutputParameterHandler)
 
 
    oGui.setEndOfDirectory()
	
def showHosters():
    oGui = cGui()
    import requests
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
        sPattern = '<iframe.+?src=["\']([^"\']+)["\']'
        aResult = oParser.parse(sHtmlContent, sPattern)
        if aResult[0]:
            for aEntry in aResult[1]:
                murl = aEntry

    oRequestHandler = cRequestHandler(murl)
    sHtmlContent = oRequestHandler.request()

    if 'class="albaplayer_name' not in sHtmlContent:
        sPattern = '<iframe src=["\']([^"\']+)["\']'
        aResult = oParser.parse(sHtmlContent, sPattern)
        if aResult[0]:
            for aEntry in aResult[1]:
                murl = aEntry       

                oRequestHandler = cRequestHandler(murl)
                sHtmlContent = oRequestHandler.request()

    oParser = cParser()
    sStart = 'class="albaplayer_name">'
    sEnd = 'class="albaplayer_server-body'
    sHtmlContent0 = oParser.abParse(sHtmlContent, sStart, sEnd)

    oParser = cParser()
    sPattern = 'href="([^"]+)">(.+?)</a>'
    aResult = oParser.parse(sHtmlContent0, sPattern)
    if aResult[0]:
        oOutputParameterHandler = cOutputParameterHandler()
        for aEntry in aResult[1]:
            sTitle = aEntry[1]
            url = aEntry[0]

            oRequestHandler = cRequestHandler(url)
            sHtmlContent = oRequestHandler.request()

            oParser = cParser()
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

            sPattern = "<script>AlbaPlayerControl([^<]+)',"
            aResult = oParser.parse(sHtmlContent, sPattern)
            if aResult[0]: 
               import base64
               for aEntry in aResult[1]:
                   url_tmp = aEntry
                   url = base64.b64decode(url_tmp).decode('utf8',errors='ignore')
                   sTitle = ('%s [COLOR coral](%s)[/COLOR]') % (sMovieTitle, sTitle)
                   sHosterUrl = url+ '|User-Agent=' + "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36" + '&Referer='+ murl

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
                   sHosterUrl = url+ '|User-Agent=' + "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36" +'&Referer='+ murl 
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
                    url = aEntry

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

                    if 'realbitsport' in url:
                            url2 = getHosterIframe(url,url) 
                            url = url2   

                    if 'youtube' in url:
                            url = url  

                    if 'javascript' in url:
                            url = ''
                    if '/albaplayer/ch' in url:
                            import base64
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
        code = aResult[0]
        try:
            if isMatrix():
                code = base64.b64decode(code).decode('ascii')
            else:
                code = base64.b64decode(code)
            return code + '|Referer=' + referer
        except Exception as e:
            pass
    
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

    return False
	
def showLive():
    oGui = cGui()
   
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
    oParser = cParser()
    URLMAIN = sUrl.split('/')[2]
    URLMAIN = 'https://' + URLMAIN
    if "?src=" in sUrl:
       slink = sUrl.split('?src=')[1]
       VSlog(slink)
    sHtmlContent2 =""
    sHtmlContent1 =""
    sHtmlContent3 =""
      # (.+?) ([^<]+) .+?
    sPattern = "iframe.src = ([^<]+)+link"
    aResult = oParser.parse(sHtmlContent, sPattern)   
    if (aResult[0]):
        sUrl = aResult[1][0].replace("'","")
        VSlog(sUrl)
        sUrl = sUrl+slink
        VSlog(sUrl)
        oRequestHandler = cRequestHandler(sUrl)
        sHtmlContent3 = oRequestHandler.request()
      # (.+?) ([^<]+) .+?
    sPattern = 'iframe" src="(.+?)" width'
    aResult = oParser.parse(sHtmlContent, sPattern)   
    if (aResult[0]):
        sUrl = aResult[1][0]
        if sUrl.startswith('/'):
           sUrl = URLMAIN + sUrl
        VSlog(sUrl)
        oRequestHandler = cRequestHandler(sUrl)
        sHtmlContent = oRequestHandler.request()
    # (.+?) # ([^<]+) .+? 
    if 'no_mobile_iframe' in sHtmlContent:
       sPattern = 'no_mobile_iframe = "(.+?)";'
       aResult = oParser.parse(sHtmlContent, sPattern)
       if (aResult[0]):
           siteUrl = aResult[1][0]
           if siteUrl.startswith('/'):
               siteUrl = URLMAIN + siteUrl
           import requests    
           oRequestHandler = cRequestHandler(siteUrl)
           hdr = {'User-Agent' : 'Mozilla/5.0 (iPad; CPU OS 13_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) CriOS/87.0.4280.77 Mobile/15E148 Safari/604.1','referer' : URL_MAIN}
           St=requests.Session()
           sHtmlContent2 = St.get(siteUrl,headers=hdr)
           sHtmlContent2 = sHtmlContent2.content.decode('utf-8')
    if 'mobile' in sHtmlContent:
       sPattern = '_iframe = "(.+?)";'
       aResult = oParser.parse(sHtmlContent, sPattern)
       if (aResult[0]):
           siteUrl = aResult[1][0]
           if siteUrl.startswith('/'):
               siteUrl = URL_MAIN + siteUrl
           import requests    
           oRequestHandler = cRequestHandler(siteUrl)
           hdr = {'User-Agent' : 'Mozilla/5.0 (iPad; CPU OS 13_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) CriOS/87.0.4280.77 Mobile/15E148 Safari/604.1','referer' : URL_MAIN}
           St=requests.Session()
           sHtmlContent1 = St.get(siteUrl,headers=hdr)
           sHtmlContent1 = sHtmlContent1.content.decode('utf-8')
    sHtmlContent = sHtmlContent3+sHtmlContent2+sHtmlContent1

    sPattern = 'href="(.+?)">(.+?)</a>'   
    aResult = oParser.parse(sHtmlContent, sPattern) 
   


    if aResult[0]:
        oOutputParameterHandler = cOutputParameterHandler()  
        for aEntry in aResult[1]:
 
            sTitle = aEntry[1]
            siteUrl = aEntry[0].replace("('","").replace("')","")
            if siteUrl.startswith('/'):
               siteUrl = URL_MAIN + siteUrl
            sDesc = ""
            import requests    
            oRequestHandler = cRequestHandler(siteUrl)
            hdr = {'User-Agent' : 'Mozilla/5.0 (iPad; CPU OS 13_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) CriOS/87.0.4280.77 Mobile/15E148 Safari/604.1','referer' : URL_MAIN}
            St=requests.Session()
            sHtmlContent = St.get(siteUrl,headers=hdr)
            sHtmlContent = sHtmlContent.content.decode('utf-8')
            oParser = cParser()
    # (.+?) # ([^<]+) .+? 		


            sPattern = "<script>AlbaPlayerControl([^<]+)',"
            aResult = oParser.parse(sHtmlContent, sPattern)
            if aResult[0]: 
               import base64
               for aEntry in aResult[1]:
                   url_tmp = aEntry
                   url = base64.b64decode(url_tmp).decode('utf8',errors='ignore')
                   sHosterUrl = url+ '|User-Agent=' + "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36" + '&Referer='+ siteUrl
                   sMovieTitle = sMovieTitle
                   sdTitle = ('%s  [COLOR coral]%s[/COLOR]') % (sMovieTitle, sTitle)
                   if 'vimeo' in sHosterUrl:
                       sHosterUrl = sHosterUrl + "|Referer=" + sUrl
                   oHoster = cHosterGui().checkHoster(sHosterUrl)
                   if oHoster:
                       oHoster.setDisplayName(sdTitle)
                       oHoster.setFileName(sMovieTitle)
                       cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb)	


            sPattern = "source: '(.+?)',"
            aResult = oParser.parse(sHtmlContent, sPattern)
            if aResult[0]:
               for aEntry in aResult[1]:
                   url = aEntry
                   sHosterUrl = url+ '|User-Agent=' + "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36"+'&Referer='+ siteUrl
                   sMovieTitle = sMovieTitle
                   sdTitle = ('%s  [COLOR coral]%s[/COLOR]') % (sMovieTitle, sTitle)
                   if 'vimeo' in sHosterUrl:
                       sHosterUrl = sHosterUrl + "|Referer=" + sUrl
                   oHoster = cHosterGui().checkHoster(sHosterUrl)
                   if oHoster:
                       oHoster.setDisplayName(sdTitle)
                       oHoster.setFileName(sMovieTitle)
                       cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb)

            sPattern = "hls.loadSource(.+?);"
            aResult = oParser.parse(sHtmlContent, sPattern)
            if aResult[0]:
               for aEntry in aResult[1]:
                   url = aEntry.replace("('","").replace("')","")
                   sHosterUrl = url+ '|User-Agent=' + "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36" +'&Referer='+ siteUrl
                   sMovieTitle = sMovieTitle
                   sdTitle = ('%s  [COLOR coral]%s[/COLOR]') % (sMovieTitle, sTitle)
                   if 'vimeo' in sHosterUrl:
                       sHosterUrl = sHosterUrl + "|Referer=" + sUrl
                   oHoster = cHosterGui().checkHoster(sHosterUrl)
                   if oHoster:
                       oHoster.setDisplayName(sdTitle)
                       oHoster.setFileName(sMovieTitle)
                       cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb)

            sPattern = "<source src='(.+?)' type='application/x-mpegURL'"
            aResult = oParser.parse(sHtmlContent, sPattern)
            if aResult[0]:
               for aEntry in aResult[1]:
                   url = aEntry.replace("('","").replace("')","")
                   sHosterUrl = url+ '|User-Agent=' + "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36" +'&Referer='+ siteUrl 
                   sMovieTitle = sMovieTitle
                   sdTitle = ('%s  [COLOR coral]%s[/COLOR]') % (sMovieTitle, sTitle)
                   if 'vimeo' in sHosterUrl:
                       sHosterUrl = sHosterUrl + "|Referer=" + sUrl
                   oHoster = cHosterGui().checkHoster(sHosterUrl)
                   if oHoster:
                       oHoster.setDisplayName(sdTitle)
                       oHoster.setFileName(sMovieTitle)
                       cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb)
            sPattern = 'source:"(.+?)",'
            aResult = oParser.parse(sHtmlContent, sPattern)
            if aResult[0]:
               for aEntry in aResult[1]:
                   url = aEntry
                   sHosterUrl = url+ '|User-Agent=' + "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36" +'&Referer='+ siteUrl
                   sMovieTitle = sMovieTitle
                   sdTitle = ('%s  [COLOR coral]%s[/COLOR]') % (sMovieTitle, sTitle)
                   if 'vimeo' in sHosterUrl:
                       sHosterUrl = sHosterUrl + "|Referer=" + sUrl
                   oHoster = cHosterGui().checkHoster(sHosterUrl)
                   if oHoster:
                       oHoster.setDisplayName(sdTitle)
                       oHoster.setFileName(sMovieTitle)
                       cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb)

    # (.+?) # ([^<]+) .+? 
            sPattern = 'src="(.+?)"'
            aResult = oParser.parse(sHtmlContent, sPattern)
            if aResult[0]:
               for aEntry in aResult[1]:
                   url = aEntry
                   sHosterUrl = url.replace("https://tv.as-goal.site/zurl.html?src=","")
                   sMovieTitle = sMovieTitle
                   if 'vimeo' in sHosterUrl:
                       sHosterUrl = sHosterUrl + "|Referer=" + sUrl
                   oHoster = cHosterGui().checkHoster(sHosterUrl)
                   if oHoster:
                       oHoster.setDisplayName(sMovieTitle+' '+sTitle)
                       oHoster.setFileName(sMovieTitle)
                       cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb)
    # (.+?) # ([^<]+) .+? 
            sPattern = 'file:"(.+?)",'
            aResult = oParser.parse(sHtmlContent, sPattern)
            if aResult[0]:
               for aEntry in aResult[1]:
                   url = aEntry
                   sHosterUrl = url.replace("https://tv.as-goal.site/zurl.html?src=","")
                   sMovieTitle = sMovieTitle
                   if 'vimeo' in sHosterUrl:
                       sHosterUrl = sHosterUrl + "|Referer=" + sUrl
                   oHoster = cHosterGui().checkHoster(sHosterUrl)
                   if oHoster:
                       oHoster.setDisplayName(sMovieTitle+' '+sTitle)
                       oHoster.setFileName(sMovieTitle)
                       cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb)

 # (.+?) # ([^<]+) .+? 

            sPattern = 'onclick="([^<]+)" >.+?>([^<]+)</strong>'
            aResult = oParser.parse(sHtmlContent, sPattern)

            if aResult[0]:
               for aEntry in aResult[1]:
                   url = aEntry[0].replace("('",'').replace("')","").replace("update_frame","")
                   url = url.split('?link=', 1)[1]
                   if url.startswith('//'):
                      url = 'http:' + url
                   if '/embed/' in url:
                      oRequestHandler = cRequestHandler(url)
                      oParser = cParser()
                      sPattern =  'src="(.+?)" scrolling="no">'
                      aResult = oParser.parse(url,sPattern)
                      if aResult[0]:
                          url = aResult[1][0]
                          sHosterUrl = url.replace("https://tv.as-goal.site/zurl.html?src=","")
                          sMovieTitle = str(aEntry[1])
                          if 'vimeo' in sHosterUrl:
                              sHosterUrl = sHosterUrl + "|Referer=" + sUrl
                          oHoster = cHosterGui().checkHoster(sHosterUrl)
                          if oHoster:
                              oHoster.setDisplayName(sMovieTitle+' '+sTitle)
                              oHoster.setFileName(sMovieTitle)
                              cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb)

 # (.+?) # ([^<]+) .+? 

            sPattern = 'src="(.+?)" width="(.+?)"'
            aResult = oParser.parse(sHtmlContent, sPattern)

            if aResult[0]:
               for aEntry in aResult[1]:
                   url = aEntry[0]
                   if url.startswith('//'):
                      url = 'http:' + url
                   if 'xyz' in url:
                       oRequestHandler = cRequestHandler(url)
                       oRequestHandler.setRequestType(1)
                       oRequestHandler.addHeaderEntry('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:66.0) Gecko/20100101 Firefox/66.0')
                       oRequestHandler.addHeaderEntry('referer', 'https://msdee.xyz/')
                       data = oRequestHandler.request();
                       sPattern =  '(http[^<]+m3u8)'
                       aResult = oParser.parse(data,sPattern)
                       if aResult[0]:
                           url = aResult[1][0]+ '|User-Agent=' + 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:66.0) Gecko/20100101 Firefox/66.0' +'&Referer=' + "https://memotec.xyz/"
 
                           sHosterUrl = url.replace("https://tv.as-goal.site/zurl.html?src=","") 
                           sMovieTitle = sMovieTitle
                           if 'vimeo' in sHosterUrl:
                               sHosterUrl = sHosterUrl + "|Referer=" + sUrl
            


                           oHoster = cHosterGui().checkHoster(sHosterUrl)
                           if oHoster:
                               oHoster.setDisplayName(sMovieTitle+' '+sTitle)
                               oHoster.setFileName(sMovieTitle)
                               cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb)
    
    if 'streamable' in sUrl:
        sHosterUrl = sUrl.split('?src=')[1]
        oHoster = cHosterGui().checkHoster(sHosterUrl)
        if oHoster:
           oHoster.setDisplayName(sMovieTitle)
           oHoster.setFileName(sMovieTitle)
           cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb)

                
    oGui.setEndOfDirectory()