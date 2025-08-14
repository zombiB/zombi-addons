#-*- coding: utf-8 -*-
# https://github.com/Kodi-vStream/venom-xbmc-addons

import re
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.hosters.hoster import iHoster
from resources.lib.packer import cPacker
from resources.lib.comaddon import VSlog
from resources.lib.GKDecrypter import GKDecrypter

class cHoster(iHoster):

    def __init__(self):
        iHoster.__init__(self, 'vidbull', 'VidBull')

    def _getMediaLinkForGuest(self, autoPlay = False):
        VSlog(self._url)

        url_stream = ''

        oRequest = cRequestHandler(self._url)
        oRequest.enableCache(False)
        sHtmlContent = oRequest.request()

        oParser = cParser()

        sPattern =  "<script type='text\/javascript'>(eval\(function\(p,a,c,k,e,d.+?)<\/script>"
        aResult = oParser.parse(sHtmlContent, sPattern)

        if aResult[0]:
            for i in aResult[1]:
                sHtmlContent = cPacker().unpack(i)
                if '<embed' in sHtmlContent:
                    pass

                else:
                    EncodedLink = re.search('file:"([^"]+)"', sHtmlContent, re.DOTALL)

                    if (EncodedLink):

                        Key = "a949376e37b369" + "f17bc7d3c7a04c5721"
                        x = GKDecrypter(128, 128)
                        sUrl = x.decrypt(EncodedLink.group(1), Key.decode("hex"), "ECB").split('\0')[0]
                        url_stream = sUrl

        if (url_stream):
            return True, url_stream
        else:
            return False, False

        return False, False
