#-*- coding: utf-8 -*-
#zombi.(@geekzombi)
from resources.lib.gui.hoster import cHosterGui
from resources.lib.handler.hosterHandler import cHosterHandler
from resources.lib.gui.gui import cGui
from resources.lib.gui.guiElement import cGuiElement
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.comaddon import progress
from resources.lib.parser import cParser
from resources.lib.util import cUtil
import urllib2,urllib,re
import unicodedata
 
SITE_IDENTIFIER = 'myasianpark'
SITE_NAME = 'myasianpark'
SITE_DESC = 'arabic vod'
 
URL_MAIN = 'http://myasianpark.com/'


SERIE_ASIA = ('http://myasianpark.com/series_online/', 'showMovies')
SERIE_GENRES = (True, 'showGenres')
SERIE_NEWS = ('http://myasianpark.com/%D8%A7%D9%84%D8%AD%D9%84%D9%82%D8%A7%D8%AA-%D8%A7%D9%84%D8%AC%D8%AF%D9%8A%D8%AF%D8%A9/', 'showEps')


URL_SEARCH = ('http://myasianpark.com/?s=', 'showMovies')
FUNCTION_SEARCH = 'showMovies'
 
def load():
    oGui = cGui()

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'http://venom/')
    oGui.addDir(SITE_IDENTIFIER, 'showSearch', 'Recherche', 'search.png', oOutputParameterHandler)

            
    oGui.setEndOfDirectory()
 
def showSearch():
    oGui = cGui()

    sSearchText = oGui.showKeyBoard()
    if (sSearchText != False):
        sUrl = 'http://myasianpark.com/?s='+sSearchText
        showMovies(sUrl)
        oGui.setEndOfDirectory()
        return
   
def showGenres():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
 
    liste = []
    liste.append( ["chinese series","http://myasianpark.com/series_online_cat/%D8%AF%D8%B1%D8%A7%D9%85%D8%A7-%D8%B5%D9%8A%D9%86%D9%8A%D8%A9/"] )
    liste.append( ["korean series","http://myasianpark.com/series_online_cat/%D8%AF%D8%B1%D8%A7%D9%85%D8%A7-%D9%83%D9%88%D8%B1%D9%8A%D8%A9/"] )
    liste.append( ["japanese series","http://myasianpark.com/series_online_cat/%D8%AF%D8%B1%D8%A7%D9%85%D8%A7-%D9%8A%D8%A7%D8%A8%D8%A7%D9%86%D9%8A%D8%A9/"] )
    liste.append( ["Taiwan series","http://myasianpark.com/series_online_cat/%D8%AF%D8%B1%D8%A7%D9%85%D8%A7-%D8%AA%D8%A7%D9%8A%D9%88%D8%A7%D9%86%D9%8A%D8%A9/"] )
    liste.append( ["tailand series","http://myasianpark.com/series_online_cat/%D8%AF%D8%B1%D8%A7%D9%85%D8%A7-%D8%AA%D8%A7%D9%8A%D9%84%D9%86%D8%AF%D9%8A%D8%A9/"] )

    
	            
    for sTitle,sUrl in liste:
        
        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', sUrl)
        oGui.addDir(SITE_IDENTIFIER, 'showMovies', sTitle, 'genres.png', oOutputParameterHandler)
       
    oGui.setEndOfDirectory() 
 
def showMovies(sSearch = ''):
    oGui = cGui()
    if sSearch:
      sUrl = sSearch
    else:
        oInputParameterHandler = cInputParameterHandler()
        sUrl = oInputParameterHandler.getValue('siteUrl')
 
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
 

    # .+? ([^<]+)
 

    sPattern = '<div class="post-block">
            <a href="([^<]+)">
            	<div class="post-block-a">
					<img width="770" height="1080" src="([^<]+)" class="attachment-anime_list size-anime_list wp-post-image" alt="" srcset="https://myasianpark.net/wp-content/uploads/2020/01/المسلسل-الصيني-ألمع-نجم-في-السماء-The-Brightest-Star-in-The-Sky.jpg 770w, https://myasianpark.net/wp-content/uploads/2020/01/المسلسل-الصيني-ألمع-نجم-في-السماء-The-Brightest-Star-in-The-Sky-257x360.jpg 257w, https://myasianpark.net/wp-content/uploads/2020/01/المسلسل-الصيني-ألمع-نجم-في-السماء-The-Brightest-Star-in-The-Sky-768x1077.jpg 768w, https://myasianpark.net/wp-content/uploads/2020/01/المسلسل-الصيني-ألمع-نجم-في-السماء-The-Brightest-Star-in-The-Sky-525x736.jpg 525w, https://myasianpark.net/wp-content/uploads/2020/01/المسلسل-الصيني-ألمع-نجم-في-السماء-The-Brightest-Star-in-The-Sky-214x300.jpg 214w" sizes="(max-width: 770px) 100vw, 770px" />                </div>
             </a>
             <a href="https://myasianpark.net/series_online/%d8%a7%d9%84%d9%85%d8%b3%d9%84%d8%b3%d9%84-%d8%a7%d9%84%d8%b5%d9%8a%d9%86%d9%8a-%d8%a3%d9%84%d9%85%d8%b9-%d9%86%d8%ac%d9%85-%d9%81%d9%8a-%d8%a7%d9%84%d8%b3%d9%85%d8%a7%d8%a1-the-brightest-star-in-the/#disqus_thread"> <div class="comments-sa"><i class="fa fa-comments-o"></i> <span class="dsq-postid" data-dsqidentifier="24507 https://myasianpark.net/?post_type=series_online&#038;p=24507">0</span></div></a>
               <a href="https://myasianpark.net/series_online/%d8%a7%d9%84%d9%85%d8%b3%d9%84%d8%b3%d9%84-%d8%a7%d9%84%d8%b5%d9%8a%d9%86%d9%8a-%d8%a3%d9%84%d9%85%d8%b9-%d9%86%d8%ac%d9%85-%d9%81%d9%8a-%d8%a7%d9%84%d8%b3%d9%85%d8%a7%d8%a1-the-brightest-star-in-the/"> <div class="title">([^<]+)</div></a>
                <div class="terms-es">
					<a href="https://myasianpark.net/series_online_genre/%d8%af%d8%b1%d8%a7%d9%85%d8%a7-%d8%b5%d9%8a%d9%86%d9%8a%d8%a9/">([^<]+)</a></div>
             </div>'

    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
	
	
    if (aResult[0] == True):
        total = len(aResult[1])
        progress_ = progress().VScreate(SITE_NAME)
        for aEntry in aResult[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break
 

            sUrl = aEntry[0]
            sThumbnail = aEntry[1]
            sTitle = str(aEntry[2])

			           

            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl',sUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumbnail', sThumbnail)
            if 'film_online' in sUrl:
                oGui.addMovie(SITE_IDENTIFIER, 'showHosters', sTitle, '', sThumbnail, aEntry[3], oOutputParameterHandler) 
            else:
                oGui.addMovie(SITE_IDENTIFIER, 'showEpisodes', sTitle, '', sThumbnail, aEntry[3], oOutputParameterHandler)
        
        progress_.VSclose(progress_)
 
        sNextPage = __checkForNextPage(sHtmlContent)
        if (sNextPage != False):
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sNextPage)
            oGui.addDir(SITE_IDENTIFIER, 'showMovies', '[COLOR teal]Next >>>[/COLOR]', 'next.png', oOutputParameterHandler)
 
    if not sSearch:
        oGui.setEndOfDirectory()
def showEps(sSearch = ''):
    oGui = cGui()
    if sSearch:
      sUrl = sSearch
    else:
        oInputParameterHandler = cInputParameterHandler()
        sUrl = oInputParameterHandler.getValue('siteUrl')
 
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
 

    #sPattern = 'src="([^<]+)" class=".+?href="([^<]+)">([^<]+)</.+?<div class="movieDesc">([^<]+)</div>'
 

    sPattern = '<div class="online-block">.+?<a href="([^<]+)">.+?<img.+?src="([^<]+)" class=".+?<div class="title-online">([^<]+)</div></a>'

    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
	
	
    if (aResult[0] == True):
        total = len(aResult[1])
        progress_ = progress().VScreate(SITE_NAME)
        for aEntry in aResult[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break

            siteUrl = aEntry[0]
            sThumbnail = aEntry[1]
            sTitle = aEntry[2].replace("&#8217;","'")


            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl',siteUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumbnail', sThumbnail)
			

            oGui.addMovie(SITE_IDENTIFIER, 'showHosters', sTitle, '', sThumbnail, '', oOutputParameterHandler)
        
        progress_.VSclose(progress_)
 
        sNextPage = __checkForNextPage(sHtmlContent)
        if (sNextPage != False):
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sNextPage)
            oGui.addDir(SITE_IDENTIFIER, 'showMovies', '[COLOR teal]Next >>>[/COLOR]', 'next.png', oOutputParameterHandler)
 
    if not sSearch:
        oGui.setEndOfDirectory()		
	
def showEpisodes():
    oGui = cGui()
    
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumbnail = oInputParameterHandler.getValue('sThumbnail')
 
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
 
    sPattern = '<h1 class="eps-title">([^<]+)</h1>.+?<div class="eps-act">.+?<a href="([^<]+)" target="_blank">.+?</a>'

    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
	
	
    if (aResult[0] == True):
        total = len(aResult[1])
        progress_ = progress().VScreate(SITE_NAME)
        for aEntry in aResult[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break
 
            sTitle = aEntry[0]
            siteUrl = aEntry[1]
			


            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl',siteUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumbnail', sThumbnail)
            oGui.addMovie(SITE_IDENTIFIER, 'showLinks', sTitle, '', sThumbnail, '', oOutputParameterHandler)
        
        progress_.VSclose(progress_)
       
    oGui.setEndOfDirectory()
	
def __checkForNextPage(sHtmlContent):
    sPattern = 'class="next page-numbers" href="(.+?)"'
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
    if (aResult[0] == True):
        return aResult[1][0]

    return False

def showLinks():
    oGui = cGui()
   
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumbnail = oInputParameterHandler.getValue('sThumbnail')
 
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()



    sPattern = '"postId":"(.+?)"}'
    

    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
   
    if (aResult[0] == True):
        total = len(aResult[1])
        progress_ = progress().VScreate(SITE_NAME)
        for aEntry in aResult[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break
    sPage = aEntry



    sPattern = '<div class="get_it" id="(.+?)">(.+?)<i class="fa fa-play-circle"></i></div>'

    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
    
    #fh = open('c:\\test.txt', "w")
    #fh.write(sHtmlContent.replace('\n',''))
    #fh.close()

    #print aResult
   
    if (aResult[0] == True):
        total = len(aResult[1])
        progress_ = progress().VScreate(SITE_NAME)
        for aEntry in aResult[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break


            #http://cera.online/wp-content/themes/Theme/servers/server.php?q=17185&i=2


            sErver = aEntry[0]
            siteUrl = 'http://myasianpark.com/wp-content/themes/ForestCima/view_online.php?id='+sPage+'&serv='+sErver
            sTitle = 'server '+sErver+':'+aEntry[1]

            #print sUrl
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', siteUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sMovieTitle)
            oOutputParameterHandler.addParameter('sThumbnail', sThumbnail)

            

 
            oGui.addMovie(SITE_IDENTIFIER, 'showHosters', sTitle, '', sThumbnail, '', oOutputParameterHandler)
 
        progress_.VSclose(progress_)
       
    oGui.setEndOfDirectory()
    


def showHosters():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumbnail = oInputParameterHandler.getValue('sThumbnail')
    
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request();
    #sHtmlContent = sHtmlContent.replace('<iframe src="//www.facebook.com/plugins/like.php','').replace('<iframe src="http://www.facebook.com/plugins/likebox.php','([^<]+)')
               
        
    sPattern = '<iframe.+?src="([^<]+)"'
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
	
    if (aResult[0] == True):
        total = len(aResult[1])
        progress_ = progress().VScreate(SITE_NAME)
        for aEntry in aResult[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break
            
            url = str(aEntry)
            if url.startswith('//'):
                url = 'http:' + url
            
            sHosterUrl = url
            oHoster = cHosterGui().checkHoster(sHosterUrl)
            if (oHoster != False):
                oHoster.setDisplayName(sMovieTitle)
                oHoster.setFileName(sMovieTitle)
                cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumbnail)
				

        progress_.VSclose(progress_) 
                
    oGui.setEndOfDirectory()