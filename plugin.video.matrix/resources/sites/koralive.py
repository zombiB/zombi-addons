# -*- coding: utf-8 -*-
# zombi https://github.com/zombiB/zombi-addons/

import re

from resources.lib.gui.hoster import cHosterGui
from resources.lib.gui.gui import cGui
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.comaddon import progress, VSlog, siteManager
from resources.lib.parser import cParser
from resources.lib.util import cUtil
from resources.lib.util import Quote
 
SITE_IDENTIFIER = 'koralive'
SITE_NAME = 'Koralive'
SITE_DESC = 'arabic vod'
 
URL_MAIN = 'https://cool.360kora.live'
try:
    import requests
    url = URL_MAIN
    session = requests.Session()  # so connections are recycled
    resp = session.head(url, allow_redirects=True)
    URL_MAIN = resp.url.split('/')[2]
    URL_MAIN = 'https://' + URL_MAIN
    VSlog(URL_MAIN)
except:
    pass 
SPORT_LIVE = (URL_MAIN, 'showMovies')

 
def load():
    oGui = cGui()

    oOutputParameterHandler = cOutputParameterHandler()    
    oOutputParameterHandler.addParameter('siteUrl', SPORT_LIVE[0])
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'بث مباشر', 'sport.png', oOutputParameterHandler)
   
    oGui.setEndOfDirectory()
	
    
def showMovies():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
 
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
    oParser = cParser()
	# (.+?) .+? 
    sPattern = '<a title="(.+?)" id="match-live" href="(.+?)"'
    aResult = oParser.parse(sHtmlContent, sPattern)
	
	
    if aResult[0] is True:
        total = len(aResult[1])
        progress_ = progress().VScreate(SITE_NAME)
        oOutputParameterHandler = cOutputParameterHandler() 
        for aEntry in aResult[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break
 
            sTitle =  aEntry[0]
            sThumb = ""
            siteUrl =  aEntry[1]
            sDesc = ''
			
			

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
    VSlog(sUrl)
      # (.+?) ([^<]+) .+?
    sPattern = 'iframe" src="(.+?)" width'
    aResult = oParser.parse(sHtmlContent, sPattern)

    
    if (aResult[0]):
        sUrl = aResult[1][0]
        oRequestHandler = cRequestHandler(sUrl)
        sHtmlContent = oRequestHandler.request()
    # (.+?) # ([^<]+) .+? 
    sPattern = 'href="(.+?)">(.+?)</a>'
    
    aResult = oParser.parse(sHtmlContent, sPattern)
   

    if aResult[0] is True:
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
            VSlog(aResult)
            if aResult[0] is True: 
               import base64
               for aEntry in aResult[1]:
                   url_tmp = aEntry
                   VSlog(url_tmp)
                   url = base64.b64decode(url_tmp).decode('utf8',errors='ignore')
                   VSlog(url)
                   sHosterUrl = url+ '|User-Agent=' + "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36" + '&Referer='+ siteUrl
                   sMovieTitle = sMovieTitle
                   if 'vimeo' in sHosterUrl:
                       sHosterUrl = sHosterUrl + "|Referer=" + sUrl
                   oHoster = cHosterGui().checkHoster(sHosterUrl)
                   if oHoster != False:
                       oHoster.setDisplayName(sMovieTitle+' '+sTitle)
                       oHoster.setFileName(sMovieTitle)
                       cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb)	


            sPattern = "source: '(.+?)',"
            aResult = oParser.parse(sHtmlContent, sPattern)
            if aResult[0] is True:
               for aEntry in aResult[1]:
                   url = aEntry
                   sHosterUrl = url+ '|User-Agent=' + "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36" + '&Referer=https://hd.360kora.live/' 
                   sMovieTitle = sMovieTitle
                   if 'vimeo' in sHosterUrl:
                       sHosterUrl = sHosterUrl + "|Referer=" + sUrl
                   oHoster = cHosterGui().checkHoster(sHosterUrl)
                   if oHoster != False:
                       oHoster.setDisplayName(sMovieTitle+' '+sTitle)
                       oHoster.setFileName(sMovieTitle)
                       cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb)

            sPattern = "hls.loadSource(.+?);"
            aResult = oParser.parse(sHtmlContent, sPattern)
            if aResult[0] is True:
               for aEntry in aResult[1]:
                   url = aEntry.replace("('","").replace("')","")
                   sHosterUrl = url+ '|User-Agent=' + "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36" + '&Referer=https://hd.360kora.live/' 
                   sMovieTitle = sMovieTitle
                   if 'vimeo' in sHosterUrl:
                       sHosterUrl = sHosterUrl + "|Referer=" + sUrl
                   oHoster = cHosterGui().checkHoster(sHosterUrl)
                   if oHoster != False:
                       oHoster.setDisplayName(sMovieTitle+' '+sTitle)
                       oHoster.setFileName(sMovieTitle)
                       cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb)

            sPattern = "<source src='(.+?)' type='application/x-mpegURL'"
            aResult = oParser.parse(sHtmlContent, sPattern)
            if aResult[0] is True:
               for aEntry in aResult[1]:
                   url = aEntry.replace("('","").replace("')","")
                   sHosterUrl = url+ '|User-Agent=' + "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36" + '&Referer=https://hd.360kora.live/' 
                   sMovieTitle = sMovieTitle
                   if 'vimeo' in sHosterUrl:
                       sHosterUrl = sHosterUrl + "|Referer=" + sUrl
                   oHoster = cHosterGui().checkHoster(sHosterUrl)
                   if oHoster != False:
                       oHoster.setDisplayName(sMovieTitle+' '+sTitle)
                       oHoster.setFileName(sMovieTitle)
                       cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb)
            sPattern = 'source:"(.+?)",'
            aResult = oParser.parse(sHtmlContent, sPattern)
            if aResult[0] is True:
               for aEntry in aResult[1]:
                   url = aEntry
                   sHosterUrl = url+ '|User-Agent=' + "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36" + '&Referer=https://hd.360kora.live/' 
                   sMovieTitle = sMovieTitle
                   if 'vimeo' in sHosterUrl:
                       sHosterUrl = sHosterUrl + "|Referer=" + sUrl
                   oHoster = cHosterGui().checkHoster(sHosterUrl)
                   if oHoster != False:
                       oHoster.setDisplayName(sMovieTitle+' '+sTitle)
                       oHoster.setFileName(sMovieTitle)
                       cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb)

    # (.+?) # ([^<]+) .+? 
            sPattern = 'src="(.+?)"'
            aResult = oParser.parse(sHtmlContent, sPattern)
            if aResult[0] is True:
               for aEntry in aResult[1]:
                   url = aEntry
                   sHosterUrl = url.replace("https://tv.as-goal.site/zurl.html?src=","")
                   sMovieTitle = sMovieTitle
                   if 'vimeo' in sHosterUrl:
                       sHosterUrl = sHosterUrl + "|Referer=" + sUrl
                   oHoster = cHosterGui().checkHoster(sHosterUrl)
                   if oHoster != False:
                       oHoster.setDisplayName(sMovieTitle+' '+sTitle)
                       oHoster.setFileName(sMovieTitle)
                       cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb)
    # (.+?) # ([^<]+) .+? 
            sPattern = 'file:"(.+?)",'
            aResult = oParser.parse(sHtmlContent, sPattern)
            if aResult[0] is True:
               for aEntry in aResult[1]:
                   url = aEntry
                   sHosterUrl = url.replace("https://tv.as-goal.site/zurl.html?src=","")
                   sMovieTitle = sMovieTitle
                   if 'vimeo' in sHosterUrl:
                       sHosterUrl = sHosterUrl + "|Referer=" + sUrl
                   oHoster = cHosterGui().checkHoster(sHosterUrl)
                   if oHoster != False:
                       oHoster.setDisplayName(sMovieTitle+' '+sTitle)
                       oHoster.setFileName(sMovieTitle)
                       cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb)

 # (.+?) # ([^<]+) .+? 

            sPattern = 'onclick="([^<]+)" >.+?>([^<]+)</strong>'
            aResult = oParser.parse(sHtmlContent, sPattern)

            if aResult[0] is True:
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
                      if aResult[0] is True:
                          url = aResult[1][0]
                          sHosterUrl = url.replace("https://tv.as-goal.site/zurl.html?src=","")
                          sMovieTitle = str(aEntry[1])
                          if 'vimeo' in sHosterUrl:
                              sHosterUrl = sHosterUrl + "|Referer=" + sUrl
                          oHoster = cHosterGui().checkHoster(sHosterUrl)
                          if oHoster != False:
                              oHoster.setDisplayName(sMovieTitle+' '+sTitle)
                              oHoster.setFileName(sMovieTitle)
                              cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb)

 # (.+?) # ([^<]+) .+? 

            sPattern = 'src="(.+?)" width="(.+?)"'
            aResult = oParser.parse(sHtmlContent, sPattern)

            if aResult[0] is True:
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
                       if aResult[0] is True:
                           url = aResult[1][0]+ '|User-Agent=' + 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:66.0) Gecko/20100101 Firefox/66.0' +'&Referer=' + "https://memotec.xyz/"
 
                           sHosterUrl = url.replace("https://tv.as-goal.site/zurl.html?src=","") 
                           sMovieTitle = sMovieTitle
                           if 'vimeo' in sHosterUrl:
                               sHosterUrl = sHosterUrl + "|Referer=" + sUrl
            

                           oHoster = cHosterGui().checkHoster(sHosterUrl)
                           if oHoster != False:
                               oHoster.setDisplayName(sMovieTitle+' '+sTitle)
                               oHoster.setFileName(sMovieTitle)
                               cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb)
    
    if 'streamable' in sUrl:
        sHosterUrl = sUrl.split('?src=')[1]
        oHoster = cHosterGui().checkHoster(sHosterUrl)
        if oHoster != False:
           oHoster.setDisplayName(sMovieTitle)
           oHoster.setFileName(sMovieTitle)
           cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb)

                
    oGui.setEndOfDirectory()			
def showHosters():
    import requests
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')                    
       
    oParser = cParser()


    oRequestHandler = cRequestHandler(sUrl)
    hdr = {'User-Agent' : 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Mobile Safari/537.36','Origin' : 'live.360koralive.com','Referer' : 'https://live.360koralive.com'}
    St=requests.Session()              
    sHtmlContent = St.get(sUrl,headers=hdr).content.decode('utf-8')            

    # (.+?) .+? ([^<]+)
    sPattern = 'href="(.+?)" target="search_iframe">(.+?)</a>'
    aResult = oParser.parse(sHtmlContent, sPattern)
    if aResult[0] is True:
        for aEntry in aResult[1]:
            sTitle = aEntry[1]
            url = aEntry[0]
            if '.m3u8' in url:           
                url = url.split('=')[1] 
            if '.php' in url:           
                oRequestHandler = cRequestHandler(url)
                hdr = {'User-Agent' : 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Mobile Safari/537.36','referer' : 'https://riyadh.himtree.com/'}
                St=requests.Session()
                sHtmlContent = St.get(url,headers=hdr)
                sHtmlContent2 = sHtmlContent.content 
                sPattern =  'src="(.+?)"'
                aResult = oParser.parse(sHtmlContent2,sPattern)
                if aResult[0] is True:
                   url = aResult[1][0]
                sPattern =  '(http[^<]+m3u8)'
                aResult = oParser.parse(sHtmlContent2,sPattern)
                if aResult[0] is True:
                   url = aResult[1][0]
                oParser = cParser()
                sPattern =  'source: "(.+?)",'
                aResult = oParser.parse(sHtmlContent2,sPattern)
                if aResult[0] is True:
                   url = aResult[1][0]
                sPattern =  "source: '(.+?)',"
                aResult = oParser.parse(sHtmlContent2,sPattern)
                if aResult[0] is True:
                   url = aResult[1][0]
            if 'embed' in url:
                oRequestHandler = cRequestHandler(url)
                sHtmlContent2 = St.get(url).content
                oParser = cParser()
                sPattern =  'src="(.+?)" scrolling="no">'
                aResult = oParser.parse(sHtmlContent2,sPattern)
                if aResult[0] is True:
                   url = aResult[1][0]
            if '/dash/' in url:
                oRequestHandler = cRequestHandler(url)
                sHtmlContent4 = St.get(url).content
                regx = '''var s = '(.+?)';.+?url="(.+?)".+?s;'''
                var = re.findall(regx,sHtmlContent4,re.S)
                if var:
                   a = var[0][0]
                   a = a.replace('\\','')
                   b = var[0][1]
                   url = 'https://video-a-sjc.xx.fbcdn.net/hvideo-ash66'+a
            sHosterUrl = url+ '|User-Agent=' + "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36" + '&Referer=' + URL_MAIN
            

            oHoster = cHosterGui().checkHoster(sHosterUrl)
            if oHoster != False:
                oHoster.setDisplayName(sTitle)
                oHoster.setFileName(sMovieTitle)
                cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb)

    sPattern = "'link': u'(.+?)',"
    aResult = oParser.parse(sHtmlContent, sPattern)
    if aResult[0] is True:
        for aEntry in aResult[1]:
            
            url = aEntry
            if '.php?' in url:
                oRequestHandler = cRequestHandler(url)
                sHtmlContent2 = St.get(url).content
                oParser = cParser()
                sPattern =  'source: "(.+?)",'
                aResult = oParser.parse(sHtmlContent2,sPattern)
                if aResult[0] is True:
                   url = aResult[1][0]
            if 'embed' in url:
                oRequestHandler = cRequestHandler(url)
                sHtmlContent2 = St.get(url).content
                oParser = cParser()
                sPattern =  'src="(.+?)" scrolling="no">'
                aResult = oParser.parse(sHtmlContent2,sPattern)
                if aResult[0] is True:
                   url = aResult[1][0]
            if 'multi.html' in url:
                url2 = url.split('=') 
                live = url2[1].replace("&ch","")
                ch = url2[2]
                oRequestHandler = cRequestHandler(url)
                sHtmlContent2 = St.get(url).content
                oParser = cParser()
                sPattern =  "var src = (.+?),"
                aResult = oParser.parse(sHtmlContent2,sPattern)
                if aResult[0] is True:
                    url2 = aResult[1][0].split('hls:')
                    url2 = url2[1].split('+')
                    url2 = url2[0].replace("'","")
                    url = url2+live+'/'+ch+'.m3u8'
            if '/dash/' in url:
                oRequestHandler = cRequestHandler(url)
                sHtmlContent4 = St.get(url).content
                regx = '''var s = '(.+?)';.+?url="(.+?)".+?s;'''
                var = re.findall(regx,sHtmlContent4,re.S)
                if var:
                   a = var[0][0]
                   a = a.replace('\\','')
                   b = var[0][1]
                   url = 'https://video-a-sjc.xx.fbcdn.net/hvideo-ash66'+a
            sHosterUrl = url+ '|User-Agent=' + "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36" + '&Referer=' + URL_MAIN
            sMovieTitle = 'link'
            

            oHoster = cHosterGui().checkHoster(sHosterUrl)
            if oHoster != False:
                oHoster.setDisplayName(sMovieTitle+' '+sTitle)
                oHoster.setFileName(sMovieTitle)
                cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb)


    oGui.setEndOfDirectory()
  	
def showHosters():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')
    
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request();
    oParser = cParser() # (.+?) .+? ([^<]+)
    sPattern = 'frameborder="0" allowfullscreen="" allow="autoplay" src="https.+?link=(.+?)" scrolling="no">' 
    aResult = oParser.parse(sHtmlContent, sPattern)
    if aResult[0] is True:
        for aEntry in aResult[1]:
            
            url = aEntry
            sTitle = sMovieTitle
            if url.startswith('//'):
                url = 'https:' + url
            
                
            sHosterUrl = url
            oHoster = cHosterGui().checkHoster(sHosterUrl)
            if oHoster != False:
                oHoster.setDisplayName(sTitle)
                oHoster.setFileName(sTitle)
                cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb)

                
    oGui.setEndOfDirectory()    
