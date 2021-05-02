 #-*- coding: utf-8 -*-
#zombi.(@geekzombi)


from resources.lib.gui.gui import cGui
from resources.lib.gui.guiElement import cGuiElement
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.comaddon import progress, isMatrix
from resources.lib.parser import cParser


from resources.lib.player import cPlayer
import re

 
SITE_IDENTIFIER = 'shoofvod'
SITE_NAME = 'shoofvod'
SITE_DESC = 'arabic vod'
 
URL_MAIN = 'http://shoofvod.com/'

RAMADAN_SERIES = (URL_MAIN + '/Cat-98-1', 'showSeries')




MOVIE_EN = (URL_MAIN + '/al_751319_1', 'showMovies')
MOVIE_AR = (URL_MAIN + '/Cat-100-1', 'showMovies')
MOVIE_HI = (URL_MAIN + '/Cat-132-1', 'showMovies')
MOVIE_TURK = (URL_MAIN + '/Cat-48-1', 'showMovies')
MOVIE_ANIME = (URL_MAIN + '/Cat-57-1', 'showMovies')



DOC_NEWS = (URL_MAIN + '/Cat-23-1', 'showMovies')

SERIE_DUBBED = (URL_MAIN + '/Cat-129-1', 'showSeries')
SERIE_AR = (URL_MAIN + '/Cat-98-1', 'showSeries')
SERIE_TR = (URL_MAIN + '/Cat-128-1', 'showSeries')
SERIE_TR_AR = (URL_MAIN + '/Cat-129-1', 'showSeries')
SERIE_HEND = (URL_MAIN + '/Cat-130-1', 'showSerie')
SERIE_GENRES = (True, 'showGenres')

REPLAYTV_NEWS = (URL_MAIN + '/Cat-39-1', 'showSeries')
REPLAYTV_PLAY = (URL_MAIN + '/Cat-44-1', 'showEps')


KID_CARTOON = (URL_MAIN + '/Cat-56-1', 'showSeries')

URL_SEARCH = (URL_MAIN + '/Search/', 'showMovies')
URL_SEARCH_SERIES = (URL_MAIN + '/Search/', 'showMovies')


URL_SEARCH_MOVIES = (URL_MAIN + '/Search/', 'showMovies')
FUNCTION_SEARCH = 'showMovies'
 
def load():
    oGui = cGui()

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'http://venom/')
    oGui.addDir(SITE_IDENTIFIER, 'showSearch', 'Search', 'search.png', oOutputParameterHandler)

            
    oGui.setEndOfDirectory()
 
def showSearch():
    oGui = cGui()
 
    sSearchText = oGui.showKeyBoard()
    if (sSearchText != False):
        sUrl = URL_MAIN + '/Search/'+sSearchText

        showMovies(sUrl)
        oGui.setEndOfDirectory()
        return
   

 
def showGenres():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
 
    liste = []
	
    liste.append( ['مسلسلات سورية - لبنانية',URL_MAIN + '/Cat-93-1'] )

 
    for sTitle,sUrl in liste:
 
        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', sUrl)
        oGui.addDir(SITE_IDENTIFIER, 'showSeries', sTitle, 'genres.png', oOutputParameterHandler)
 
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
    if isMatrix(): 
       sHtmlContent = str(sHtmlContent.encode('latin-1',errors='ignore'),'utf-8',errors='ignore')
 
     # (.+?) ([^<]+) .+?
    sPattern = '<div class="col-md-3 col-sm-4 col-xs-4 col-xxs-6 item">.+?<a href="([^<]+)">.+?<img src="([^<]+)" class.+?<div class="title"><h4>([^<]+)</h4></div>'

    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
	
	
    if (aResult[0] == True):
        total = len(aResult[1])
        progress_ = progress().VScreate(SITE_NAME)
        for aEntry in aResult[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break
 
            sTitle = aEntry[2].replace("مشاهدة","").replace("مترجمة","").replace("مترجم","").replace("فيلم","").replace("مسلسل","").replace("مدبلج للعربية","مدبلج").replace("مدبلج","[مدبلج]").replace("والأخيرة","").replace("-","").replace("الحلقة "," E").replace("حلقة "," E")


            siteUrl = URL_MAIN+aEntry[0]
            siteUrl = siteUrl.replace('vidpage_','Play/')
            sThumbnail = aEntry[1]
            sInfo = ''
            sYear = ''
            m = re.search('([0-9]{4})', sTitle)
            if m:
                sYear = str(m.group(0))
                sTitle = sTitle.replace(sYear,'')
            sDisplayTitle2 = sTitle.split('مدبلج')[0]
            sDisplayTitle = ('%s (%s)') % (sTitle, sYear)




            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl',siteUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sDisplayTitle2)
            oOutputParameterHandler.addParameter('sThumbnail', sThumbnail)
			
            if 'الحلقة' in aEntry[2]:
                oGui.addTV(SITE_IDENTIFIER, 'showHosters', sDisplayTitle, '', sThumbnail, sInfo, oOutputParameterHandler)
            else:

                oGui.addMovie(SITE_IDENTIFIER, 'showHosters', sDisplayTitle, '', sThumbnail, sInfo, oOutputParameterHandler)
  # ([^<]+) .+?

    sPattern ='class="page" href="([^<]+)">([^<]+)</a>'

    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
	
	
    if (aResult[0] == True):
        total = len(aResult[1])
        progress_ = progress().VScreate(SITE_NAME)
        for aEntry in aResult[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break
 
            sTitle = aEntry[1]
            
            sTitle =  "PAGE " + sTitle
            sTitle =   '[COLOR red]'+sTitle+'[/COLOR]'
            siteUrl = URL_MAIN + str(aEntry[0])


            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl',siteUrl)
			
            oGui.addDir(SITE_IDENTIFIER, 'showMovies', sTitle, '', oOutputParameterHandler)
        
        progress_.VSclose(progress_)
 
        sNextPage = __checkForNextPage(sHtmlContent)
        if (sNextPage != False):
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
 
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
    if isMatrix(): 
       sHtmlContent = str(sHtmlContent.encode('latin-1',errors='ignore'),'utf-8',errors='ignore')
      # (.+?) ([^<]+) .+?
    sPattern = '<div class="col-md-3 col-sm-4 col-xs-4 col-xxs-6 item">.+?<a href="([^<]+)">.+?<img src="([^<]+)" class.+?<div class="title"><h4>([^<]+)</h4></div>'

    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
	
	
    if (aResult[0] == True):
        total = len(aResult[1])
        progress_ = progress().VScreate(SITE_NAME)
        for aEntry in aResult[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break
 
            sTitle = aEntry[2].replace("مشاهدة","").replace("مترجمة","").replace("مترجم","").replace("فيلم","").replace("مسلسل","").replace("مدبلج للعربية","مدبلج").replace("مدبلج","[مدبلج]").replace("والأخيرة","").replace("-","").replace("الحلقة "," E").replace("حلقة "," E")
            siteUrl = URL_MAIN+str(aEntry[0])
            sThumbnail = str(aEntry[1])
            sInfo = ""
            sDisplayTitle2 = sTitle.split('مدبلج')[0]
			


            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl',siteUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sDisplayTitle2)
            oOutputParameterHandler.addParameter('sThumbnail', sThumbnail)

            oGui.addTV(SITE_IDENTIFIER, 'showEps', sTitle, '', sThumbnail, sInfo, oOutputParameterHandler)
        
        progress_.VSclose(progress_)
 
        sNextPage = __checkForNextPage(sHtmlContent)
        if (sNextPage != False):
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sNextPage)
            oGui.addDir(SITE_IDENTIFIER, 'showSeries', '[COLOR teal]Next >>>[/COLOR]', 'next.png', oOutputParameterHandler)
 
    if not sSearch:
        oGui.setEndOfDirectory()
 
 
def __checkForNextPage(sHtmlContent):
    sPattern = '<a href="([^<]+)">التالي</a>'
	
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
 
    if (aResult[0] == True):
        aResult = URL_MAIN+aResult[1][0]
        #print aResult[1][0]
        return aResult

    return False
  
def showEps():
    oGui = cGui()
   
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumbnail = oInputParameterHandler.getValue('sThumbnail')
 
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
    if isMatrix(): 
       sHtmlContent = str(sHtmlContent.encode('latin-1',errors='ignore'),'utf-8',errors='ignore')
     # (.+?) ([^<]+) .+?
    sPattern = '<div class="col-md-3 col-sm-4 col-xs-4 col-xxs-6 item">.+?<a href="([^<]+)">.+?<img src="([^<]+)" class="img-responsive mrg-btm-5">.+?<div class="title"><h4>([^<]+)</h4></div>'

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
 
            sTitle = aEntry[2].replace("مشاهدة","").replace("مترجمة","").replace("مترجم","").replace("فيلم","").replace("مسلسل","").replace("مدبلج للعربية","مدبلج").replace("مدبلج","[مدبلج]").replace("والأخيرة","").replace("-","").replace("الحلقة "," E").replace("حلقة "," E")
            siteUrl = URL_MAIN+str(aEntry[0])
            siteUrl = siteUrl.replace('vidpage_','Play/')
            sThumbnail = str(aEntry[1])
            sInfo = ""

 
            #print sUrl
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', siteUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumbnail', sThumbnail)

            

 
            oGui.addEpisode(SITE_IDENTIFIER, 'showHosters',  sTitle, '', sThumbnail, sInfo, oOutputParameterHandler)
 
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

    oParser = cParser()
            
    sPattern =  'var url = "([^<]+)" +' 
    aResult = oParser.parse(sHtmlContent,sPattern)
    if (aResult[0] == True):
        m3url = aResult[1][0]
        m3url = URL_MAIN + '' + m3url 

			
        oRequest = cRequestHandler(m3url)
        sHtmlContent = oRequest.request()

    oParser = cParser()
         # (.+?) ([^<]+) .+?       
    sPattern =  '<iframe src="(.+?)"' 
    aResult = oParser.parse(sHtmlContent,sPattern)
    if (aResult[0] == True):
        m3url = aResult[1][0]
        m3url = 'http:' + m3url 
			
        oRequest = cRequestHandler(m3url)
        sHtmlContent = oRequest.request()
    #recup du lien mp4
    sPattern = '<source src="(.+?)" type='
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
    
    if (aResult[0] == True):
        
        sUrl = str(aResult[1][0])
        if sUrl.startswith('//'):
           sUrl = 'http:' + sUrl 
                 
        #on lance video directement
        oGuiElement = cGuiElement()
        oGuiElement.setSiteName(SITE_IDENTIFIER)
        oGuiElement.setTitle(sMovieTitle)
        oGuiElement.setMediaUrl(sUrl)
        oGuiElement.setThumbnail(sThumbnail)

        oPlayer = cPlayer()
        oPlayer.clearPlayList()
        oPlayer.addItemToPlaylist(oGuiElement)
        oPlayer.startPlayer()
        return
    
    else:
        return

    oGui.setEndOfDirectory()