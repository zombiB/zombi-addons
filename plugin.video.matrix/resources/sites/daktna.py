# -*- coding: utf-8 -*-
# zombi https://github.com/zombiB/zombi-addons/

import re
import requests
from resources.lib.gui.hoster import cHosterGui
from resources.lib.gui.gui import cGui
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.comaddon import VSlog, siteManager, addon
from resources.lib.parser import cParser
import xbmcgui
from resources.lib import random_ua

UA = random_ua.get_ua()

 
ADDON = addon()
icons = ADDON.getSetting('defaultIcons')

SITE_IDENTIFIER = 'daktna'
SITE_NAME = 'daktna'
SITE_DESC = 'arabic vod'
 
URL_MAIN = siteManager().getUrlMain(SITE_IDENTIFIER)
MOVIES = (URL_MAIN + 'list/movies/', 'showMovies')
#RAMADAN_SERIES = (URL_MAIN + '/list/series/', 'showSeries')
SERIE_AR = (URL_MAIN + '/list/series/', 'showSeries')
SERIE_TR = (URL_MAIN + '/list/series-turkish/', 'showSeries')

URL_SEARCH = (URL_MAIN + '/?s=', 'showSearchSeries')

URL_SEARCH_SERIES = (URL_MAIN + '/?s=', 'showSearchSeries')
URL_SEARCH_MOVIES = (URL_MAIN + '/?s=', 'showMovies')

FUNCTION_SEARCH = 'showMovies'

def load():
    oGui = cGui()

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'http://venom/')
    oGui.addDir(SITE_IDENTIFIER, 'showMoviesSearch', 'SEARCH_MOVIES', icons + '/Search.png', oOutputParameterHandler)
    oOutputParameterHandler.addParameter('siteUrl', 'http://venom/')
    oGui.addDir(SITE_IDENTIFIER, 'showSeriesSearch', 'SEARCH_SERIES', icons + '/Search.png', oOutputParameterHandler)
    oOutputParameterHandler.addParameter('siteUrl', MOVIES[0])
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'Movies', icons + '/Movies.png', oOutputParameterHandler)
 #   oOutputParameterHandler.addParameter('siteUrl', RAMADAN_SERIES[0])
#    oGui.addDir(SITE_IDENTIFIER, 'showSeries', 'مسلسلات رمضان', icons + '/Ramadan.png', oOutputParameterHandler)
	
    oOutputParameterHandler.addParameter('siteUrl', SERIE_AR[0])
    oGui.addDir(SITE_IDENTIFIER, 'showSeries', 'مسلسلات عربية', icons + '/Arabic.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', SERIE_TR[0])
    oGui.addDir(SITE_IDENTIFIER, 'showSeries', 'مسلسلات تركية', icons + '/Turkish.png', oOutputParameterHandler)
	
    oGui.setEndOfDirectory()
  #  xbmcgui.Dialog().ok("sHtmlContent",str(URL_MAIN))
def showMoviesSearch():
    oGui = cGui()
 
    sSearchText = oGui.showKeyBoard()
    if sSearchText:
       sUrl = URL_MAIN + '?s='+"فيلم  "+sSearchText 
    #   xbmcgui.Dialog().ok("url",sUrl )

       showMovies(sUrl)
       oGui.setEndOfDirectory()
    return
def showSeriesSearch():
    oGui = cGui()
 
    sSearchText = oGui.showKeyBoard()
    if sSearchText:
        sUrl = URL_MAIN + '?s='+"مسلسل "+sSearchText 
     #   xbmcgui.Dialog().ok("url",sUrl )

        showSearchSeries(sUrl)
        oGui.setEndOfDirectory()
        return
	
def showSearchSeries(sSearch = ''):
    oGui = cGui()
    if sSearch:
      sUrl = sSearch
    else:
        oInputParameterHandler = cInputParameterHandler()
        sUrl = oInputParameterHandler.getValue('siteUrl')



    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
    # (.+?) .+? ([^<]+)   
    sPattern = '<div class="thumb"><a href="(.+?)"><img src=.+?alt="(.+?)" data-src="(.+?)" class="'
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
	
    if aResult[0]:
        arrlist=[]
        oOutputParameterHandler = cOutputParameterHandler()
        for aEntry in aResult[1]:
            Title= aEntry[1]
            match = re.search(r'مسلسل\s+(.+?)\s+الحلقة', Title)
         
            series_name = match.group(1).strip()
            series_name_url = series_name

            if str (series_name_url) not in  arrlist:
           
             siteUrl =tag_categories(aEntry[0])
         #    xbmcgui.Dialog().ok("url", siteUrl)
            
           
             #  sTitle = aEntry[1].replace("مشاهدة","").replace("مسلسل","").replace("انمي","").replace("مترجم للعربية","").replace("مترجمة","").replace("مترجم","").replace("مشاهده","").replace("برنامج","").replace("مترجمة","").replace("فيلم","").replace("اون لاين","").replace("WEB-DL","").replace("BRRip","").replace("720p","").replace("HD-TC","").replace("HDRip","").replace("HD-CAM","").replace("DVDRip","").replace("BluRay","").replace("1080p","").replace("WEBRip","").replace("WEB-dl","").replace("مترجم ","").replace("مشاهدة وتحميل","").replace("اون لاين","")
            
             sTitle=str (series_name_url)
             sThumb = aEntry[2]
             sDesc = ''
            #   sTitle = sTitle.replace("الموسم العاشر","S10").replace("الموسم الحادي عشر","S11").replace("الموسم الثاني عشر","S12").replace("الموسم الثالث عشر","S13").replace("الموسم الرابع عشر","S14").replace("الموسم الخامس عشر","S15").replace("الموسم السادس عشر","S16").replace("الموسم السابع عشر","S17").replace("الموسم الثامن عشر","S18").replace("الموسم التاسع عشر","S19").replace("الموسم العشرون","S20").replace("الموسم الحادي و العشرون","S21").replace("الموسم الثاني و العشرون","S22").replace("الموسم الثالث و العشرون","S23").replace("الموسم الرابع والعشرون","S24").replace("الموسم الخامس و العشرون","S25").replace("الموسم السادس والعشرون","S26").replace("الموسم السابع والعشرون","S27").replace("الموسم الثامن والعشرون","S28").replace("الموسم التاسع والعشرون","S29").replace("الموسم الثلاثون","S30").replace("الموسم الحادي و الثلاثون","S31").replace("الموسم الثاني والثلاثون","S32").replace("الموسم الاول","S1").replace("الموسم الثاني","S2").replace("الموسم الثالث","S3").replace("الموسم الثالث","S3").replace("الموسم الرابع","S4").replace("الموسم الخامس","S5").replace("الموسم السادس","S6").replace("الموسم السابع","S7").replace("الموسم الثامن","S8").replace("الموسم التاسع","S9").replace("الموسم","S").replace("موسم","S").replace("S ","S")
             sMovieTitle = sTitle
             
             oOutputParameterHandler.addParameter('siteUrl',siteUrl)
             oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            # oOutputParameterHandler.addParameter('sYear', sYear)
             oOutputParameterHandler.addParameter('sThumb', sThumb)
             oGui.addTV(SITE_IDENTIFIER, 'showSearch_list_ep', sTitle, '', sThumb, sDesc, oOutputParameterHandler)
            
             arrlist.append(str (series_name_url))
  
        
 
        sNextPage = __checkForNextPage(sHtmlContent)
        if sNextPage:
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sNextPage)
            oGui.addDir(SITE_IDENTIFIER, 'showSearchSeries', '[COLOR teal]Next >>>[/COLOR]', icons + '/Next.png', oOutputParameterHandler)

        
  # ([^<]+) .+? (.+?)
 
    if not sSearch:
        oGui.setEndOfDirectory()

       #/////////////////////////////// 

def  showSearch_list_ep():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')
 
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
    sPattern = r'<ul class="latest-data">(.*?)</ul>'

    oParser = cParser()
    ul_content = oParser.parse(sHtmlContent, sPattern)
    sPattern=  r'<li class="video-grid boxed-grid">.*?<a href="([^"]+)">.*?<img[^>]+alt="([^"]+)"[^>]+data-src="([^"]+)"'
    aResult=oParser.parse(ul_content, sPattern)
    if aResult[0]:
         oOutputParameterHandler = cOutputParameterHandler()
     #    xbmcgui.Dialog().ok("aResult", str ( aResult[1]))
         for aEntry in aResult[1]:
             
             siteUrl = aEntry[0]+"?see=watch"
             sThumb=aEntry[2]
             sTitle = re.sub(r'(الحلقة \d+).*', r'\1', aEntry[1]).replace("مسلسل", "").replace("الحلقة ", "Ep ")
             sDesc = ''
             oOutputParameterHandler.addParameter("siteUrl",siteUrl) 
             oOutputParameterHandler.addParameter("sMovieTitle", sTitle)
             oOutputParameterHandler.addParameter("sThumb", sThumb)
             oGui.addEpisode(SITE_IDENTIFIER, 'showHosters', sTitle, '', sThumb, sDesc, oOutputParameterHandler)
       #      xbmcgui.Dialog().ok("aResult", str (aEntry[1]))
    oGui.setEndOfDirectory()        


             
   

    pass
def tag_categories(sUrl):
    oInputParameterHandler = cInputParameterHandler()
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent =  oRequestHandler.request()
    sPattern =r'<ul class="post-categories">(.*?)</ul>'
    match = re.search(sPattern, sHtmlContent, re.S)
    ui_content= str( match.group(1))
    hrefs = re.findall(r'href="([^"]+)"', ui_content)
 #   xbmcgui.Dialog().ok("",str (hrefs[0]))
    return  str ( hrefs[0])
   
    pass
def showMovies(sSearch = ''):
     oGui = cGui()
     if sSearch:
       sUrl = sSearch
  #     xbmcgui.Dialog().ok("",str(sSearch))
     else:
        oInputParameterHandler = cInputParameterHandler()
        sUrl = oInputParameterHandler.getValue('siteUrl')
        pass
       
     oRequestHandler = cRequestHandler(sUrl)
     sHtmlContent =  oRequestHandler.request()
    # (.+?) .+? ([^<]+)   
     sPattern = r'<div class="thumb"><a href="(.*?)"><img src=".*?" alt="(.*?)" data-src="(.*?)"'

     oParser = cParser()
     aResult = oParser.parse(sHtmlContent, sPattern)
     itemList = []
     if aResult[0]:
        oOutputParameterHandler = cOutputParameterHandler()
     #   xbmcgui.Dialog().ok("",str(aResult[1]))
        for aEntry in aResult[1]:
           
 
            siteUrl = aEntry[0]
            
            sTitle = aEntry[1].replace("مشاهدة","").replace("مسلسل","").replace("انمي","").replace("مترجمة","").replace("مترجم للعربية","").replace("مترجم","").replace("مشاهده","").replace("برنامج","").replace("مترجمة","").replace("فيلم","").replace("اون لاين","").replace("WEB-DL","").replace("BRRip","").replace("720p","").replace("HD-TC","").replace("HDRip","").replace("HD-CAM","").replace("DVDRip","").replace("BluRay","").replace("1080p","").replace("WEBRip","").replace("WEB-dl","").replace("مترجم ","").replace("مشاهدة وتحميل","").replace("اون لاين","")
            sThumb = aEntry[2]
            sDesc = ''
            sTitle = sTitle.replace("الموسم العاشر","S10").replace("الموسم الحادي عشر","S11").replace("الموسم الثاني عشر","S12").replace("الموسم الثالث عشر","S13").replace("الموسم الرابع عشر","S14").replace("الموسم الخامس عشر","S15").replace("الموسم السادس عشر","S16").replace("الموسم السابع عشر","S17").replace("الموسم الثامن عشر","S18").replace("الموسم التاسع عشر","S19").replace("الموسم العشرون","S20").replace("الموسم الحادي و العشرون","S21").replace("الموسم الثاني و العشرون","S22").replace("الموسم الثالث و العشرون","S23").replace("الموسم الرابع والعشرون","S24").replace("الموسم الخامس و العشرون","S25").replace("الموسم السادس والعشرون","S26").replace("الموسم السابع والعشرون","S27").replace("الموسم الثامن والعشرون","S28").replace("الموسم التاسع والعشرون","S29").replace("الموسم الثلاثون","S30").replace("الموسم الحادي و الثلاثون","S31").replace("الموسم الثاني والثلاثون","S32").replace("الموسم الاول","S1").replace("الموسم الثاني","S2").replace("الموسم الثالث","S3").replace("الموسم الثالث","S3").replace("الموسم الرابع","S4").replace("الموسم الخامس","S5").replace("الموسم السادس","S6").replace("الموسم السابع","S7").replace("الموسم الثامن","S8").replace("الموسم التاسع","S9").replace("الموسم","S").replace("موسم","S").replace("S ","S").split('الحلقة')[0]
            sYear = ''
            m = re.search('([0-9]{4})', sTitle)
            if m:
                sYear = str(m.group(0))
                sTitle = sTitle.replace(sYear,'')
            
            if sTitle not in itemList:
                itemList.append(sTitle)
                oOutputParameterHandler.addParameter("siteUrl",siteUrl+"?see=watch") 
                oOutputParameterHandler.addParameter("sMovieTitle", sTitle)
                oOutputParameterHandler.addParameter("thumb", sThumb)
                oOutputParameterHandler.addParameter("description", sDesc)
                oGui.addMovie(SITE_IDENTIFIER,'showHosters',   sTitle,'',sThumb,'',oOutputParameterHandler)
                pass
			
              
              
        sNextPage = __checkForNextPage(sHtmlContent)
        if sNextPage:
           oOutputParameterHandler = cOutputParameterHandler()
           oOutputParameterHandler.addParameter('siteUrl', sNextPage)
           oGui.addDir(SITE_IDENTIFIER, 'showMovies', '[COLOR teal]Next >>>[/COLOR]', icons + '/Next.png', oOutputParameterHandler)

        
  # ([^<]+) .+? (.+?)
 
     if not  sSearch:
                 oGui.setEndOfDirectory()

        #/////////////////////////////      oInputParameterHandler              

def showSeries(sSearch = ''):
    oGui = cGui()
    if sSearch:
      sUrl = sSearch
      
    else:
        oInputParameterHandler = cInputParameterHandler()
        sUrl = oInputParameterHandler.getValue('siteUrl')



    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
    # (.+?) .+? ([^<]+)   
    sPattern = '<div class="thumb"><a href="(.+?)"><img src=.+?alt="(.+?)" data-src="(.+?)" class="'
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
	
    itemList = []
    if aResult[0]:
        oOutputParameterHandler = cOutputParameterHandler()
        for aEntry in aResult[1]:
 
            siteUrl = aEntry[0]
            
            sTitle = aEntry[1].replace("مشاهدة","").replace("مسلسل","").replace("انمي","").replace("مترجمة","").replace("مترجم للعربية","").replace("مترجم","").replace("مشاهده","").replace("برنامج","").replace("مترجمة","").replace("فيلم","").replace("اون لاين","").replace("WEB-DL","").replace("BRRip","").replace("720p","").replace("HD-TC","").replace("HDRip","").replace("HD-CAM","").replace("DVDRip","").replace("BluRay","").replace("1080p","").replace("WEBRip","").replace("WEB-dl","").replace("مترجم ","").replace("مشاهدة وتحميل","").replace("اون لاين","")
            sThumb = aEntry[2]
            sDesc = ''
            sTitle = sTitle.replace("الموسم العاشر","S10").replace("الموسم الحادي عشر","S11").replace("الموسم الثاني عشر","S12").replace("الموسم الثالث عشر","S13").replace("الموسم الرابع عشر","S14").replace("الموسم الخامس عشر","S15").replace("الموسم السادس عشر","S16").replace("الموسم السابع عشر","S17").replace("الموسم الثامن عشر","S18").replace("الموسم التاسع عشر","S19").replace("الموسم العشرون","S20").replace("الموسم الحادي و العشرون","S21").replace("الموسم الثاني و العشرون","S22").replace("الموسم الثالث و العشرون","S23").replace("الموسم الرابع والعشرون","S24").replace("الموسم الخامس و العشرون","S25").replace("الموسم السادس والعشرون","S26").replace("الموسم السابع والعشرون","S27").replace("الموسم الثامن والعشرون","S28").replace("الموسم التاسع والعشرون","S29").replace("الموسم الثلاثون","S30").replace("الموسم الحادي و الثلاثون","S31").replace("الموسم الثاني والثلاثون","S32").replace("الموسم الاول","S1").replace("الموسم الثاني","S2").replace("الموسم الثالث","S3").replace("الموسم الثالث","S3").replace("الموسم الرابع","S4").replace("الموسم الخامس","S5").replace("الموسم السادس","S6").replace("الموسم السابع","S7").replace("الموسم الثامن","S8").replace("الموسم التاسع","S9").replace("الموسم","S").replace("موسم","S").replace("S ","S").split('الحلقة')[0]
            sYear = ''
            m = re.search('([0-9]{4})', sTitle)
            if m:
                sYear = str(m.group(0))
                sTitle = sTitle.replace(sYear,'')
            
            if sTitle not in itemList:
                itemList.append(sTitle)
			
                oOutputParameterHandler.addParameter('siteUrl',siteUrl)
                oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
                oOutputParameterHandler.addParameter('sYear', sYear)
                oOutputParameterHandler.addParameter('sThumb', sThumb)

                oGui.addTV(SITE_IDENTIFIER, 'showEpisodes', sTitle, '', sThumb, sDesc, oOutputParameterHandler)
        
 
        sNextPage = __checkForNextPage(sHtmlContent)
        if sNextPage:
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sNextPage)
            oGui.addDir(SITE_IDENTIFIER, 'showSeries', '[COLOR teal]Next >>>[/COLOR]', icons + '/Next.png', oOutputParameterHandler)

        
  # ([^<]+) .+? (.+?)
 
    if not sSearch:
        oGui.setEndOfDirectory()

def __checkForNextPage(sHtmlContent):
    sPattern = 'rel="next" href="([^<]+)">'
	 # .+? ([^<]+) (.+?)
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)

 
    if aResult[0]:
        
        return aResult[1][0]


    return False
 
      # (.+?) ([^<]+) .+?
	
def showEpisodes():
    oGui = cGui()
    
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')
 
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
 # ([^<]+) .+? (.+?)

    sPattern = 'class="tags">.+?href="(.+?)" >'

    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
    m3url=''
    if aResult[0]:
        m3url = aResult[1][0] 
        if m3url.startswith('//'):
           m3url = 'https:' + m3url
    oRequestHandler = cRequestHandler(m3url)
    sHtmlContent = oRequestHandler.request()
    # (.+?) .+? ([^<]+)   
    sPattern = '<div class="thumb"><a href="(.+?)"><img src=.+?alt="(.+?)" data-src="(.+?)" class="'
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
	
	
    if aResult[0]:
        oOutputParameterHandler = cOutputParameterHandler()
        for aEntry in aResult[1]:
 
            siteUrl = aEntry[0]+"?see=watch"
            
            sTitle = aEntry[1].replace("مشاهدة","").replace("مسلسل","").replace("انمي","").replace("مترجم للعربية","").replace("مترجمة","").replace("مترجم","").replace("مشاهده","").replace("برنامج","").replace("مترجمة","").replace("فيلم","").replace("اون لاين","").replace("WEB-DL","").replace("BRRip","").replace("720p","").replace("HD-TC","").replace("HDRip","").replace("HD-CAM","").replace("DVDRip","").replace("BluRay","").replace("1080p","").replace("WEBRip","").replace("WEB-dl","").replace("مترجم ","").replace("مشاهدة وتحميل","").replace("اون لاين","")
            sThumb = aEntry[2]
            sTitle = sTitle.replace("الموسم العاشر","S10").replace("الموسم الحادي عشر","S11").replace("الموسم الثاني عشر","S12").replace("الموسم الثالث عشر","S13").replace("الموسم الرابع عشر","S14").replace("الموسم الخامس عشر","S15").replace("الموسم السادس عشر","S16").replace("الموسم السابع عشر","S17").replace("الموسم الثامن عشر","S18").replace("الموسم التاسع عشر","S19").replace("الموسم العشرون","S20").replace("الموسم الحادي و العشرون","S21").replace("الموسم الثاني و العشرون","S22").replace("الموسم الثالث و العشرون","S23").replace("الموسم الرابع والعشرون","S24").replace("الموسم الخامس و العشرون","S25").replace("الموسم السادس والعشرون","S26").replace("الموسم السابع والعشرون","S27").replace("الموسم الثامن والعشرون","S28").replace("الموسم التاسع والعشرون","S29").replace("الموسم الثلاثون","S30").replace("الموسم الحادي و الثلاثون","S31").replace("الموسم الثاني والثلاثون","S32").replace("الموسم الاول","S1").replace("الموسم الثاني","S2").replace("الموسم الثالث","S3").replace("الموسم الثالث","S3").replace("الموسم الرابع","S4").replace("الموسم الخامس","S5").replace("الموسم السادس","S6").replace("الموسم السابع","S7").replace("الموسم الثامن","S8").replace("الموسم التاسع","S9").replace("الموسم","S").replace("موسم","S").replace("S ","S").replace("الحلقة","E")
            sEp = sTitle.split('E')[1]
            sEp = sEp.split('ال')[0]
            sYear = ''
            sTitle = 'E'+sEp+sMovieTitle
            sDesc = ''

			
            oOutputParameterHandler.addParameter('siteUrl',siteUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sYear', sYear)
            oOutputParameterHandler.addParameter('sThumb', sThumb)

            oGui.addEpisode(SITE_IDENTIFIER, 'showHosters', sTitle, '', sThumb, sDesc, oOutputParameterHandler)
    oGui.setEndOfDirectory()


def showHosters():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')
 #   xbmcgui.Dialog().ok("",str(sUrl))
    ext_Url="None"
    oParser = cParser()
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()    

    sURL_MAIN= URL_MAIN

    sPattern = 'class="logo">\s*<a href="(.+?)">'
    aResult = oParser.parse(sHtmlContent, sPattern)    
    if (aResult[0]):
        sURL_MAIN = aResult[1][0]

    sPattern =  'data-vid="([^"]+)'
    aResult = oParser.parse(sHtmlContent,sPattern)
 #   xbmcgui.Dialog().ok("",sUrl)

    if aResult[0]:
        postid = aResult[1][0] 
    #    xbmcgui.Dialog().ok("",str(postid))
        oRequestHandler = cRequestHandler(f'{sURL_MAIN}wp-admin/admin-ajax.php?action=video_info&post_id={postid}')
        oRequestHandler.addHeaderEntry('User-Agent', UA)
        oRequestHandler.addHeaderEntry('Referer', sURL_MAIN)
        oRequestHandler.addParameters('action', 'video_info')
        oRequestHandler.addParameters('post_id', postid)
        sHtmlContent = oRequestHandler.request()
  #      xbmcgui.Dialog().ok("sHtmlContent",str(sHtmlContent))
        sPattern = '"src":"([^"]+)'
        aResult = oParser.parse(sHtmlContent, sPattern)
      
    if aResult[0]:
   
     for aEntry in aResult[1]:
        sHosterUrl = aEntry.replace('\\', '')
      
      
      #   xbmcgui.Dialog().ok("yesL", ("yes i found "))
        if sHosterUrl.startswith('//'):
            pass
        oHoster = cHosterGui().checkHoster(sHosterUrl)
        if oHoster:
      
         oHoster.setDisplayName(sMovieTitle)
         oHoster.setFileName(sMovieTitle)
         cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb)
         pass
       

            
        pass
   
      
       #  xbmcgui.Dialog().ok("URL", str(sHosterUrl))
    if aResult[0]:
     if "w.froozla"in  aResult[1][0]:
       
         sPattern =r'href="(https://w\.froozla\.pro/[^"]+?serv=(\d+))"'
         response = requests.get(  aResult[1][0])
         content = response.text
         aResult = oParser.parse(content, sPattern)
        
       #  xbmcgui.Dialog().ok("x", str(aResult[1]))
         for aEntry in aResult[1] :
          aEntryrUrl=aEntry[0]
          response=requests.get(aEntryrUrl)
          content = response.text
          sPattern =  r'<iframe[^>]+src="([^"]+)"'
          iframe_aResult = oParser.parse(content, sPattern)
        #  xbmcgui.Dialog().ok("aResult", str(iframe_aResult[1]))
          sHosterUrl=str(iframe_aResult[1])
          sHosterUrl = sHosterUrl.split(',')[0].strip().strip("")
          sHosterUrl = sHosterUrl.strip("[]").strip("'").strip('"')
        #  xbmcgui.Dialog().ok("aResult", (sHosterUrl))
          oHoster = cHosterGui().checkHoster(sHosterUrl)
          if oHoster:
      
           oHoster.setDisplayName(sMovieTitle)
           oHoster.setFileName(sMovieTitle)
           cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb)
     if "v.rmd" in  aResult[1][0]: 
     #    xbmcgui.Dialog().ok("v.rmd", "yes")   
         sPattern = r'href="(https://v\.rmd\.quest/albaplayer/[^"]+?serv=\d+)"'
         response = requests.get(  aResult[1][0])
         content = response.text
         aResult = oParser.parse(content, sPattern)
     #    xbmcgui.Dialog().ok("v.rmd", str( aResult))
         if( aResult[0]):
          for aEntry in aResult[1] :
           aEntryrUrl=aEntry
      #    xbmcgui.Dialog().ok("v.rmd", str( aEntryrUrl))
   
           response=requests.get(aEntryrUrl)
           content = response.text
        #  xbmcgui.Dialog().ok("aResult", (str (content))) 
        
        
           sPattern =  r'<iframe[^>]+src="([^"]+)"'
           iframe_aResult = oParser.parse(content, sPattern) 
        

       
   #       xbmcgui.Dialog().ok("aResult", (str (iframe_aResult)))

           sHosterUrl=str(iframe_aResult[1])
           sHosterUrl = sHosterUrl.split(',')[0].strip().strip("")
           sHosterUrl = sHosterUrl.strip("[]").strip("'").strip('"')
    #      xbmcgui.Dialog().ok("aResult", (str (sHosterUrl)))
           oHoster = cHosterGui().checkHoster(sHosterUrl)   
           if oHoster:
      
            oHoster.setDisplayName(sMovieTitle)
            oHoster.setFileName(sMovieTitle)
            cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb)
         
        

   
       

      
    oGui.setEndOfDirectory()



             