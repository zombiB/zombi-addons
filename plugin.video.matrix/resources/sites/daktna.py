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
RAMADAN_SERIES = (URL_MAIN + '/list/series/', 'showSeries')
SERIE_AR = (URL_MAIN + '/list/series/', 'showSeries')
SERIE_TR = (URL_MAIN + '/list/series-turkish/', 'showSeries')

URL_SEARCH = (URL_MAIN + '/?s=', 'showSearchSeries')
URL_SEARCH_SERIES = (URL_MAIN + '/?s=', 'showSearchSeries')
FUNCTION_SEARCH = 'showSeriesSearch'

def load():
    oGui = cGui()

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'http://venom/')
    
    oGui.addDir(SITE_IDENTIFIER, 'showSeriesSearch', 'SEARCH_SERIES', icons + '/Search.png', oOutputParameterHandler)
    oOutputParameterHandler.addParameter('siteUrl', MOVIES[0])
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'Movies', icons + '/Movies.png', oOutputParameterHandler)
    oOutputParameterHandler.addParameter('siteUrl', RAMADAN_SERIES[0])
    oGui.addDir(SITE_IDENTIFIER, 'showSeries', 'مسلسلات رمضان', icons + '/Ramadan.png', oOutputParameterHandler)
	
    oOutputParameterHandler.addParameter('siteUrl', SERIE_AR[0])
    oGui.addDir(SITE_IDENTIFIER, 'showSeries', 'مسلسلات عربية', icons + '/Arabic.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', SERIE_TR[0])
    oGui.addDir(SITE_IDENTIFIER, 'showSeries', 'مسلسلات تركية', icons + '/Turkish.png', oOutputParameterHandler)
	
    oGui.setEndOfDirectory()
  #  xbmcgui.Dialog().ok("sHtmlContent",str(URL_MAIN))
 
def showSeriesSearch():
    oGui = cGui()
 
    sSearchText = oGui.showKeyBoard()
    if sSearchText:
        sUrl = URL_MAIN + '/?s='+sSearchText
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
        oOutputParameterHandler = cOutputParameterHandler()
        for aEntry in aResult[1]:
 
            siteUrl = aEntry[0]
            
            sTitle = aEntry[1].replace("مشاهدة","").replace("مسلسل","").replace("انمي","").replace("مترجم للعربية","").replace("مترجمة","").replace("مترجم","").replace("مشاهده","").replace("برنامج","").replace("مترجمة","").replace("فيلم","").replace("اون لاين","").replace("WEB-DL","").replace("BRRip","").replace("720p","").replace("HD-TC","").replace("HDRip","").replace("HD-CAM","").replace("DVDRip","").replace("BluRay","").replace("1080p","").replace("WEBRip","").replace("WEB-dl","").replace("مترجم ","").replace("مشاهدة وتحميل","").replace("اون لاين","")
            sThumb = aEntry[2]
            sDesc = ''
            sTitle = sTitle.replace("الموسم العاشر","S10").replace("الموسم الحادي عشر","S11").replace("الموسم الثاني عشر","S12").replace("الموسم الثالث عشر","S13").replace("الموسم الرابع عشر","S14").replace("الموسم الخامس عشر","S15").replace("الموسم السادس عشر","S16").replace("الموسم السابع عشر","S17").replace("الموسم الثامن عشر","S18").replace("الموسم التاسع عشر","S19").replace("الموسم العشرون","S20").replace("الموسم الحادي و العشرون","S21").replace("الموسم الثاني و العشرون","S22").replace("الموسم الثالث و العشرون","S23").replace("الموسم الرابع والعشرون","S24").replace("الموسم الخامس و العشرون","S25").replace("الموسم السادس والعشرون","S26").replace("الموسم السابع والعشرون","S27").replace("الموسم الثامن والعشرون","S28").replace("الموسم التاسع والعشرون","S29").replace("الموسم الثلاثون","S30").replace("الموسم الحادي و الثلاثون","S31").replace("الموسم الثاني والثلاثون","S32").replace("الموسم الاول","S1").replace("الموسم الثاني","S2").replace("الموسم الثالث","S3").replace("الموسم الثالث","S3").replace("الموسم الرابع","S4").replace("الموسم الخامس","S5").replace("الموسم السادس","S6").replace("الموسم السابع","S7").replace("الموسم الثامن","S8").replace("الموسم التاسع","S9").replace("الموسم","S").replace("موسم","S").replace("S ","S")
            sMovieTitle = sTitle.split('الحلقة')[0]
            sEp = sTitle.replace("الحلقة","E")
            sEp = sEp.split('E')[1]
            sEp = sEp.split('ال')[0]
            sYear = ''
            sTitle = 'E'+sEp+sMovieTitle
            sYear = ''
            m = re.search('([0-9]{4})', sTitle)
            if m:
                sYear = str(m.group(0))
                sTitle = sTitle.replace(sYear,'')

			
            oOutputParameterHandler.addParameter('siteUrl',siteUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sYear', sYear)
            oOutputParameterHandler.addParameter('sThumb', sThumb)

            oGui.addEpisode(SITE_IDENTIFIER, 'showHosters', sTitle, '', sThumb, sDesc, oOutputParameterHandler)
        
 
        sNextPage = __checkForNextPage(sHtmlContent)
        if sNextPage:
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sNextPage)
            oGui.addDir(SITE_IDENTIFIER, 'showSearchSeries', '[COLOR teal]Next >>>[/COLOR]', icons + '/Next.png', oOutputParameterHandler)

        
  # ([^<]+) .+? (.+?)
 
    if not sSearch:
        oGui.setEndOfDirectory()		



def showMovies(sSearch = ''):
     oGui = cGui()
     if sSearch:
       sUrl = sSearch
     else:
        oInputParameterHandler = cInputParameterHandler()
        sUrl = oInputParameterHandler.getValue('siteUrl')
        pass
       
     oRequestHandler = cRequestHandler(sUrl)
     sHtmlContent =  oRequestHandler.request()
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
                oOutputParameterHandler.addParameter("siteUrl",siteUrl+"?see=watch") 
                oOutputParameterHandler.addParameter("sMovieTitle", sTitle)
                oOutputParameterHandler.addParameter("thumb", sThumb)
            #    oOutputParameterHandler.addParameter("description", sDesc)
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
 
            siteUrl = aEntry[0]
            
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

def xx():
     oGui = cGui()
     oInputParameterHandler = cInputParameterHandler()
     sUrl = oInputParameterHandler.getValue('siteUrl')
     xbmcgui.Dialog().ok("sUrl",sUrl)
     sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
     sThumb = oInputParameterHandler.getValue('sThumb')
'''
def showHosters():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')

    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')


    oRequestHandler = cRequestHandler(sUrl)
   
    sHtmlContent = oRequestHandler.request() 
    xbmcgui.Dialog().ok("sHtmlContent",str (sHtmlContent) )
    if 'class="vp-sources vsn_94902"' in sHtmlContent:
     xbmcgui.Dialog().ok(" Found", 'Exact class string found in HTML')
    else:
     xbmcgui.Dialog().ok(" Not Found", 'class="vp-sources vsn_94902" not found in HTML')
    sPattern = r' <script[^>]*?>(.*?)</script>'
    aResult =  re.search(sPattern, sHtmlContent, re.DOTALL)

    if aResult:
    # Extract data-url attributes from inside the div
     urls = re.findall(r'data-url="([^"]+)"', aResult[0])
     xbmcgui.Dialog().ok("Extracted URLs", (str (aResult[1])))
    else:
     xbmcgui.Dialog().ok("Error", "No matching div found.")

    oParser = cParser()         

    sURL_MAIN= URL_MAIN
   
    # (.+?) ([^<]+)
    sPattern = 'class="logo"><a href="(.+?)">'
    aResult = oParser.parse(sHtmlContent, sPattern)    
    if (aResult[0]):
        sURL_MAIN = aResult[1][0]
            
    sPattern =  'target="_blank" href="(.+?)" rel="nofollow">'
    aResult = re.findall(sPattern,sPattern)
   # xbmcgui.Dialog().ok("sUrl",str(aResult))
    m3url=''
    if aResult[0]:
        m3url = aResult[1][0] 
        if m3url.startswith('//'):
           m3url = 'https:' + m3url
    import requests
    s = requests.Session()            
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:65.0) Gecko/20100101 Firefox/65.0',
							'Referer': sURL_MAIN }
    r = s.get(m3url, headers=headers)
    sHtmlContent = r.content.decode('utf8')

    # ([^<]+) .+? (.+?)
               
    sPattern = 'data-src="([^<]+)">'
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)

	
    if aResult[0]:
        for aEntry in aResult[1]:
            
            sHosterUrl = aEntry
            if sHosterUrl.startswith('//'):
                sHosterUrl = 'http:' + sHosterUrl 
            oHoster = cHosterGui().checkHoster(sHosterUrl)
            if oHoster:
                oHoster.setDisplayName(sMovieTitle)
                oHoster.setFileName(sMovieTitle)
                cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb)
				

                
    oGui.setEndOfDirectory()'''

def showHosters():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')
   # xbmcgui.Dialog().ok("",str("aResult"))

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
        
        if sHosterUrl.startswith('//'):
            pass
        oHoster = cHosterGui().checkHoster(sHosterUrl)
        if oHoster:
      
         oHoster.setDisplayName(sMovieTitle)
         oHoster.setFileName(sMovieTitle)
         cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb)
       #  xbmcgui.Dialog().ok("URL", str(sHosterUrl))


      
    oGui.setEndOfDirectory()



             