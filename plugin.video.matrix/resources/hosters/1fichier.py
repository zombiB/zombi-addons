# -*- coding: utf-8 -*-
# vStream https://github.com/Kodi-vStream/venom-xbmc-addons

import sys
import random
import re
import urllib3

from resources.hosters.hoster import iHoster
from resources.lib.comaddon import dialog, VSlog
from resources.lib.handler.premiumHandler import cPremiumHandler
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser

UA = 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:39.0) Gecko/20100101 Firefox/39.0'


class cHoster(iHoster):
    def __init__(self):
        iHoster.__init__(self, '1fichier', '1FIchier', 'violet')

    def __getIdFromUrl(self, url):
        sId = url.replace('https://', '')
        sId = sId.replace('http://', '')
        sId = sId.replace('1fichier.com/?', '')
        sId = sId.replace('.1fichier.com', '')
        sId = sId.replace('/', '')

        return sId

    def getMediaLink(self ,autoPlay = False):
        self.oPremiumHandler = cPremiumHandler(self.getPluginIdentifier())
        print(self.oPremiumHandler.isPremiumModeAvailable())

        if ('site=cDownload&function' not in sys.argv[2]) and not (self.oPremiumHandler.isPremiumModeAvailable()):
            if not autoPlay:
                oDialog = dialog().VSok("Pas de streaming sans premium.\n" +
                    "Pour voir le film passer par l'option 'Télécharger et Lire' du menu contextuel.")
            return False, False

        if self.oPremiumHandler.isPremiumModeAvailable():
            return self._getMediaLinkByPremiumUser()
        else:
            return self._getMediaLinkForGuest(autoPlay)

    def _getMediaLinkForGuest(self, autoPlay = False):

        api_call = False
        url = 'https://1fichier.com/?' + self.__getIdFromUrl(self._url)

        adcode = random.uniform(000.000000000, 999.999999999)

        oRequestHandler = cRequestHandler(url)
        oRequestHandler.setRequestType(1)
        oRequestHandler.addHeaderEntry('Host', url.split('/')[2])
        oRequestHandler.addHeaderEntry('Referer', url)
        oRequestHandler.addHeaderEntry('Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8')
        oRequestHandler.addHeaderEntry('User-Agent', UA)
        oRequestHandler.addHeaderEntry('Accept-Language', 'fr,fr-FR;q=0.8,en-US;q=0.5,en;q=0.3')
        oRequestHandler.addHeaderEntry('Content-Type', 'application/x-www-form-urlencoded')

        oRequestHandler.addParameters('dl_no_ssl', 'on')
        oRequestHandler.addParameters('adz', adcode)
        sHtmlContent = oRequestHandler.request()

        api_call = self.getMedialinkDL(sHtmlContent)

        if api_call:
            return True, api_call

        return False, False

    def getMedialinkDL(self, sHtmlContent):

        oParser = cParser()
        api_call = False

        sPattern = 'Vous devez attendre encore [0-9]+ minutes'
        aResult = oParser.parse(sHtmlContent, sPattern)
        if aResult[0]:
            dialog().VSinfo('Erreur - Limitation %s' % aResult[1][0])
            return False

        sPattern = '<a href="([^<>"]+?)"  style="float:none;margin:auto;font-weight:bold;padding: 10px;margin: ' + \
            '10px;font-size:\+1\.6em;border:2px solid red" class="ok btn-general btn-orange">'
        aResult = oParser.parse(sHtmlContent, sPattern)

        if aResult[0]:
            api_call = aResult[1][0] + '|User-Agent=' + UA
            return api_call

        return False

    def _getMediaLinkByPremiumUser(self):
        VSlog(self._url)
        api_call = False

        if not self.oPremiumHandler.Authentificate():
            return False, False

        url = 'https://1fichier.com/?' + self.__getIdFromUrl(self._url)

        sHtmlContent = self.oPremiumHandler.GetHtml('%s&e=1' % url)
        if sHtmlContent:
            m = re.search('^(.*);.*;.*;.*$', sHtmlContent)
            if (m):
                url = m.group(1)

            else:
                cookie = self.oPremiumHandler.AddCookies().replace('Cookie=', '', 1)
                data = {
                    'submit': 'download'
                }

                headers = {'User-Agent': UA,
                           'Host': '1fichier.com',
                           'Referer': url,
                           'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                           'Accept-Language': 'fr,fr-FR;q=0.8,en-US;q=0.5,en;q=0.3',
                           'Cookie': cookie,
                           'Content-Length': '15',
                           'Content-Type': 'application/x-www-form-urlencoded'
                           }
                try:
                    http = urllib3.PoolManager()
                    response = http.request(method='POST', url=url, fields=data, headers=headers)
                except urllib3.exceptions.HTTPError as e:
                    VSlog(e.read())
                    VSlog(e.reason)

                url = response.geturl()
                response.release_conn()
        else:
            return False, False

        api_call = url + '|' + self.oPremiumHandler.AddCookies()

        if api_call:
            return True, api_call

        return False, False
