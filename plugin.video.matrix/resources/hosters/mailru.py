# -*- coding: utf-8 -*-
# Adopted from ResolveURL

from resources.hosters.hoster import iHoster
from resources.lib.comaddon import VSlog
from resources.lib import helpers
import requests, re
import json


class cHoster(iHoster):

    def __init__(self):
        iHoster.__init__(self, 'mailru', 'MailRu')

    def _getMediaLinkForGuest(self):
        VSlog(self._url)
        
        media_id = self.get_host_and_id(self._url)

        location, user, media_id = media_id.split('|')
        if user == 'None':
            web_url = 'http://my.mail.ru/+/video/meta/%s' % (media_id)
        else:
            web_url = 'http://my.mail.ru/+/video/meta/%s/%s/%s?ver=0.2.60' % (location, user, media_id)


        s = requests.session()
        response = s.get(web_url)
        html = response.content

        if html:
            js_data = json.loads(html)
            sources = [(video['key'], video['url']) for video in js_data['videos']]
            sorted(sources)
            source = helpers.pick_source(sources)

            if source.startswith("//"):
                source = 'http:%s' % source

            return True, source + helpers.append_headers({'Cookie': response.headers.get('Set-Cookie', '')})

        return False, False

    def get_host_and_id(self, url):
        pattern = r'(?://|\.)(mail\.ru)/(?:\w+/)?(?:videos/embed/)?(inbox|mail|embed|mailua|list|bk|v)/(?:([^/]+)/[^.]+/)?(\d+)'
        r = re.search(pattern, url)
        if r:
            return ('%s|%s|%s' % (r.group(2), r.group(3), r.group(4)))
        else:
            return False
