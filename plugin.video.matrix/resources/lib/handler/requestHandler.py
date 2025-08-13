# -*- coding: utf-8 -*-
# vStream https://github.com/Kodi-vStream/venom-xbmc-addons

from requests import post, get, Session, Request, RequestException, ConnectionError
from resources.lib.comaddon import addon, dialog, VSlog, VSPath, isMatrix
from resources.lib.util import urlHostName
from resources.lib import random_ua
from requests_cache import CachedSession
import requests.packages.urllib3.util.connection as urllib3_cn
import socket
from datetime import timedelta

UA = random_ua.get_ua()

CACHE = 'special://home/userdata/addon_data/plugin.video.matrix/requests_cache.db'

class cRequestHandler:
    REQUEST_TYPE_GET = 0
    REQUEST_TYPE_POST = 1

    TIME_UNIT = addon().getSetting('cache_expiration_time_unit')
    TIME_VALUE = addon().getSetting('cache_expiration_value')
    ENABLECACHED = addon().getSetting('CachedSession')

    if TIME_UNIT == 'hours':
        CACHE_EXPIRY = timedelta(hours=TIME_VALUE)

    elif TIME_UNIT == 'days':
        CACHE_EXPIRY = timedelta(days=TIME_VALUE)

    elif TIME_UNIT == 'minutes':
        CACHE_EXPIRY = timedelta(minutes=TIME_VALUE)

    else:
        CACHE_EXPIRY = timedelta(hours=24)

    def __init__(self, sUrl):
        self.__sUrl = sUrl
        self.__sRealUrl = ''
        self.__cType = 0
        self.__aParamaters = {}
        self.__aParamatersLine = ''
        self.__aHeaderEntries = {}
        self.__Cookie = {}
        self.removeBreakLines(True)
        self.removeNewLines(True)
        self.__setDefaultHeader()
        self.__timeout = 20
        self.__bRemoveNewLines = False
        self.__bRemoveBreakLines = False
        self.__sResponseHeader = ''
        self.BUG_SSL = False
        self.__enableDNS = False
        self.__enableCache = True
        self.redirects = True
        self.verify = True
        self.json = {}
        self.forceIPV4 = False
        self.oResponse = None

    def statusCode(self):
        return self.oResponse.status_code

    def disableIPV6(self):
        self.forceIPV4 = True

    def allowed_gai_family(self):
        family = socket.AF_INET
        if urllib3_cn.HAS_IPV6:
            family = socket.AF_INET
        return family

    def disableSSL(self):
        self.verify = False

    def disableRedirect(self):
        self.redirects = False

    def enableCache(self, enableCache):
        self.__enableCache = enableCache

    def removeNewLines(self, bRemoveNewLines):
        self.__bRemoveNewLines = bRemoveNewLines

    def removeBreakLines(self, bRemoveBreakLines):
        self.__bRemoveBreakLines = bRemoveBreakLines

    # Define the request type
    # 0: for a GET request
    # 1: for a POST request
    def setRequestType(self, cType):
        self.__cType = cType

    def setTimeout(self, valeur):
        self.__timeout = valeur

    # Add a cookie in the request headers
    def addCookieEntry(self, sHeaderKey, sHeaderValue):
        aHeader = {sHeaderKey: sHeaderValue}
        self.__Cookie.update(aHeader)

    # Add JSON parameters
    def addJSONEntry(self, sHeaderKey, sHeaderValue):
        aHeader = {sHeaderKey: sHeaderValue}
        self.json.update(aHeader)

    def addHeaderEntry(self, sHeaderKey, sHeaderValue):
        for sublist in list(self.__aHeaderEntries):
            if sHeaderKey in sublist:
                self.__aHeaderEntries.pop(sublist)

            if sHeaderKey == "Content-Length":
                sHeaderValue = str(sHeaderValue)

        aHeader = {sHeaderKey: sHeaderValue}
        self.__aHeaderEntries.update(aHeader)

    def addParameters(self, sParameterKey, mParameterValue):
        self.__aParamaters[sParameterKey] = mParameterValue

    def addParametersLine(self, mParameterValue):
        self.__aParamatersLine = mParameterValue

    # egg addMultipartFiled({'sess_id': sId, 'upload_type': 'url', 'srv_tmp_url': sTmp})
    def addMultipartFiled(self, fields):
        mpartdata = MPencode(fields)
        self.__aParamatersLine = mpartdata[1]
        self.addHeaderEntry('Content-Type', mpartdata[0])
        self.addHeaderEntry('Content-Length', len(mpartdata[1]))

    def getResponseHeader(self):
        return self.__sResponseHeader

    # url after redirects
    def getRealUrl(self):
        return self.__sRealUrl

    def request(self, jsonDecode=False):
        return self.__callRequest(jsonDecode)

    # Retrieve cookies from the request
    def GetCookies(self):
        if not self.__sResponseHeader:
            return ''

        if 'Set-Cookie' in self.__sResponseHeader:
            import re

            c = self.__sResponseHeader.get('set-cookie')

            c2 = re.findall('(?:^|,) *([^;,]+?)=([^;,]+?);', c)
            if c2:
                cookies = ''
                for cook in c2:
                    cookies = cookies + cook[0] + '=' + cook[1] + ';'
                cookies = cookies[:-1]
                return cookies
        return ''

    def __setDefaultHeader(self):
        self.addHeaderEntry('User-Agent', UA)
        self.addHeaderEntry('Accept-Language', 'en-US,en;q=0.9,ar;q=0.8,en-GB;q=0.7')
        self.addHeaderEntry('Accept-Charset', 'ISO-8859-1,utf-8;q=0.7,*;q=0.7')

    def __callRequest(self, jsonDecode=False):
        self.s = Session()
        if self.__enableCache and cRequestHandler.ENABLECACHED == "true":
            self.s = CachedSession(VSPath(CACHE), cache_control=True, expire_after=cRequestHandler.CACHE_EXPIRY, stale_if_error=True)
            
        if self.__enableDNS:
            self.save_getaddrinfo = socket.getaddrinfo
            socket.getaddrinfo = self.new_getaddrinfo

        if self.__aParamatersLine:
            sParameters = self.__aParamatersLine
        else:
            sParameters = self.__aParamaters

        if (self.__cType == cRequestHandler.REQUEST_TYPE_GET):
            if (len(sParameters) > 0):
                if (self.__sUrl.find('?') == -1):
                    self.__sUrl = self.__sUrl + '?' + str(sParameters)
                    sParameters = ''
                else:
                    self.__sUrl = self.__sUrl + '&' + str(sParameters)
                    sParameters = ''

        sContent = ''

        if self.BUG_SSL == True:
            self.verify = False

        if self.__cType == cRequestHandler.REQUEST_TYPE_GET:
            method = "GET"
        else:
            method = "POST"

        if self.forceIPV4:
            urllib3_cn.allowed_gai_family = self.allowed_gai_family

        try:
            _request = Request(method, self.__sUrl, headers=self.__aHeaderEntries)
            if method in ['POST']:
                _request.data = sParameters

            if self.__Cookie:
                _request.cookies = self.__Cookie

            if self.json:
                _request.json = self.json

            prepped = _request.prepare()
            self.s.headers.update(self.__aHeaderEntries)
            
            self.oResponse = self.s.send(prepped, timeout=self.__timeout, allow_redirects=self.redirects, verify=self.verify)
            self.__sResponseHeader = self.oResponse.headers
            self.__sRealUrl = self.oResponse.url

            if jsonDecode == True:
                sContent = self.oResponse.json()
            else:
                sContent = self.oResponse.content

                if isMatrix() and 'youtube' not in self.oResponse.url:
                    try:
                        sContent = sContent.decode()
                    except:
                        try:
                            sContent = sContent.decode('unicode-escape')
                        except:
                            pass

        except ConnectionError as e:
            # Error SSL
            if 'CERTIFICATE_VERIFY_FAILED' in str(e) and self.BUG_SSL == False:
                self.BUG_SSL = True
                return self.__callRequest(jsonDecode)
            # Retry with DNS only if addon is present
            elif self.__enableDNS == False and ('getaddrinfo failed' in str(e) or 'Failed to establish a new connection' in str(e)):
                # Retry with DNS only if addon is present
                import xbmcvfs
                if xbmcvfs.exists('special://home/addons/script.module.dnspython/'):
                    self.__enableDNS = True
                    return self.__callRequest()
                else:
                    error_msg = '%s (%s)' % (addon().VSlang(30470), urlHostName(self.__sUrl))
                    dialog().VSerror(error_msg)
                    sContent = ''
            else:
                sContent = ''
                return sContent

        except RequestException as e:
            if 'CERTIFICATE_VERIFY_FAILED' in str(e) and self.BUG_SSL == False:
                self.BUG_SSL = True
                return self.__callRequest()
            elif self.__enableDNS == False and 'getaddrinfo failed' in str(e):
                # Retry with DNS only if addon is present
                import xbmcvfs
                if xbmcvfs.exists('special://home/addons/script.module.dnspython/'):
                    self.__enableDNS = True
                    return self.__callRequest()
                else:
                    error_msg = '%s (%s)' % (addon().VSlang(30470), urlHostName(self.__sUrl))
            else:
                error_msg = "%s (%s),%s" % (addon().VSlang(30205), e, self.__sUrl)

            VSlog(error_msg)
            sContent = ''

        if self.oResponse is not None:
            if self.oResponse.status_code in [503, 403]:
                if "Forbidden" not in sContent:
                    
                    bypass = addon().getSetting('cloudbypass')
                    RapidApi_Key = addon().getSetting('rapidapi')

                    try:
                        import urllib.request                       
                        sHeadersEdit = {key: value for key, value in self.s.headers.items() if key != "Accept-Encoding"}

                        if method == "POST":
                            req = urllib.request.Request(
                                urllib.parse.quote(self.__sUrl, safe="/:?=&"), 
                                data=_request.data, 
                                headers=sHeadersEdit, 
                                method="POST"
                            )
                        else:
                            req = urllib.request.Request(urllib.parse.quote(self.__sUrl, safe="/:?=&"), headers=sHeadersEdit)

                        with urllib.request.urlopen(req) as response:
                            sContent = response.read().decode("utf-8")
                            if sContent:
                                if (self.__bRemoveNewLines == True):
                                    sContent = sContent.replace("\n", "")
                                    sContent = sContent.replace("\r\t", "")

                                if (self.__bRemoveBreakLines == True):
                                    sContent = sContent.replace("&nbsp;", "").replace("&#8217;","'")
                        return sContent
                    except Exception as e:
                        VSlog(f"urllib.request failed: {e}")         

                    # Try by CloudScraper
                    if bypass == '0':
                        try:
                            from cloudscraper2 import CloudScraper
                            scraper = CloudScraper.create_scraper()
                            headers = {
                                    "User-Agent": UA
                                }
                            sContent = scraper.get(self.__sUrl, headers=self.s.headers).text
                                        
                        except:
                            dialog().VSerror("%s (%s)" % ("ScrapeNinja جرب استخدام ، (Cloudflare) الصفحة ربما محمية بواسطة ", urlHostName(self.__sUrl)))

                    # Try by ScrapeNinja (limited)
                    if bypass == '1':
                                            
                        json_response = False
                        try:
                            if method == 'GET':
                                url = "https://scrapeninja.p.rapidapi.com/scrape"

                                querystring = {"url":self.__sUrl,
                                               "headers":[f"{key}: {value}" for key, value in self.s.headers.items()]}

                                headers = {
                                    "x-rapidapi-key": RapidApi_Key,
                                    "x-rapidapi-host": "scrapeninja.p.rapidapi.com"
                                }

                                json_response = get(url, headers=headers, params=querystring)

                            else:
                                url = "https://scrapeninja.p.rapidapi.com/scrape"

                                payload = {
                                    "url": self.__sUrl,
                                    "headers":[f"{key}: {value}" for key, value in self.s.headers.items()],
                                    "method": "POST",
                                    "data": _request.data
                                }
                                headers = {
                                    "x-rapidapi-key": RapidApi_Key,
                                    "x-rapidapi-host": "scrapeninja.p.rapidapi.com",
                                    "Content-Type": "application/json"
                                }

                                response = post(url, json=payload, headers=headers)

                            if json_response:
                                response = json_response.json()
                                if 'body' in response: 
                                    sContent = response['body']
                        except:
                            dialog().VSerror("%s (%s)" % ("Scrappey جرب استخدام ، (Cloudflare) الصفحة ربما محمية بواسطة ", urlHostName(self.__sUrl)))

                    # Try by scrappey (limited)
                    if bypass == '2':
                                            
                        json_response = False
                        if '&img=' in self.__sUrl:
                            self.__sUrl = self.__sUrl.split('&img=')[0]
                        try:

                            url = "https://scrappey-com.p.rapidapi.com/api/v1"

                            if method == 'GET':
                                payload = {
	                                "cmd": "request.get",
	                                "url": convert_url(self.__sUrl),
                                    "headers": [f"{key}: {value}" for key, value in self.s.headers.items()]
                                    }
                            else:
                                payload = {
	                                "cmd": "request.post",
	                                "url": convert_url(self.__sUrl),
                                    "postData": ', '.join([f"{key}={value}" for key, value in _request.data.items()]),
                                    "headers": [f"{key}: {value}" for key, value in self.s.headers.items()]
                                    }
                            headers = {
	                            "content-type": "application/json",
	                            "X-RapidAPI-Key": RapidApi_Key,
	                            "X-RapidAPI-Host": "scrappey-com.p.rapidapi.com"
                                }

                            json_response = post(url, json=payload, headers=headers)  
                            if json_response:
                                response = json_response.json()
                                if 'solution' in response:
                                    sContent = response['solution']['response']
                            else:
                                if json_response.status_code in [429]:
                                    dialog().VSerror("لقد تجاوزت الحصة الشهرية للطلبات ، استخدم رقمك الخاص")
                            
                        except:
                            dialog().VSerror("%s (%s)" % ("فشلت عملية تجاوز الحماية", f'"scrappey" {urlHostName(self.__sUrl)}'))

                    # Try by cloudbypass (limited)
                    if bypass == '3':
                                            
                        json_response = False
                        if '&img=' in self.__sUrl:
                            self.__sUrl = self.__sUrl.split('&img=')[0]
                        try:

                            url = "https://cloudflare-bypass7.p.rapidapi.com/AmrTls.php"

                            if method == 'GET':
                                payload = {
	                                "method": "GET",
	                                "url": convert_url(self.__sUrl),
                                    "headers": { "Content-Type": "application/x-www-form-urlencoded" }
                                    }
                            else:
                                payload = {
	                                "method": "POST",
	                                "url": convert_url(self.__sUrl),
                                    "postData": ', '.join([f"{key}={value}" for key, value in _request.data.items()]),
                                    "headers": { "Content-Type": "application/x-www-form-urlencoded" }
                                    }
                            headers = {
	                            "content-type": "application/json",
	                            "X-RapidAPI-Key": RapidApi_Key,
	                            "X-RapidAPI-Host": "cloudflare-bypass7.p.rapidapi.com"
                                }

                            json_response = post(url, json=payload, headers=headers)  
                            if json_response:
                                response = json_response.json()
                                if 'data' in response:
                                    sContent = response['data']
                            else:
                                if json_response.status_code in [429]:
                                    dialog().VSerror("لقد تجاوزت الحصة الشهرية للطلبات ، استخدم رقمك الخاص")
                            
                        except:
                            dialog().VSerror("%s (%s)" % ("فشلت عملية تجاوز الحماية", f'"cloudbypass" {urlHostName(self.__sUrl)}'))

                    # Try by myE2i (Manual)
                    if bypass == '4':
                        try:
                            import time
                            from resources.lib.mCaptcha.mserver import CaptchaServer

                            captcha_data = {
                                "siteUrl": self.__sUrl,
                                "siteKey": time.time(),
                                "captchaType": "CF"
                            }
                            import json, base64
                            try:
                                expiry_gen = int(addon().getSetting(f'{urlHostName(self.__sUrl)}_create'))
                            except Exception:
                                expiry_gen = 0

                            if not addon().getSetting(f'{urlHostName(self.__sUrl)}_cloudCaptcha') or expiry_gen < (time.time()):
                                server = CaptchaServer(captcha_data)
                                server.start_server()
                            encoded_result = addon().getSetting(f'{urlHostName(self.__sUrl)}_cloudCaptcha')
                            decoded_result = base64.b64decode(encoded_result).decode('utf-8')

                            data = json.loads(decoded_result)

                            user_agent = data['user_agent']
                            cookies = ''
                            cookies = {cookie['name']: cookie['value'] for cookie in data['cookie']}
                            if self.__Cookie:
                                cookies.update(self.__Cookie)
                            headers = {'User-Agent': user_agent}
                            self.s.headers.update(headers)
                            if method == 'POST':
                                sContent = self.s.post(self.__sUrl, data=_request.data, headers=self.s.headers, cookies=cookies)
                                
                            else:
                                sContent = self.s.get(self.__sUrl, headers=self.s.headers, cookies=cookies)
                                
                            if sContent.status_code in [503, 403]:
                                addon().setSetting(f'{urlHostName(self.__sUrl)}_create', str(int(time.time())))
                                dialog().VSinfo('الموقع يطلب اعادة فك الحماية ، أعد المحاولة', 'matrix', 4)
                                sContent = ''
                            else:
                                self.__sResponseHeader = sContent.headers
                                sContent = sContent.text
                        except:
                            sContent = ''

            if self.oResponse is not None and not sContent:
                ignoreStatus = [200, 302]
                if self.oResponse.status_code not in ignoreStatus:
                    VSlog("%s (%d),%s" % (addon().VSlang(30205), self.oResponse.status_code, self.__sUrl))

        if sContent:
            if (self.__bRemoveNewLines == True):
                sContent = sContent.replace("\n", "")
                sContent = sContent.replace("\r\t", "")

            if (self.__bRemoveBreakLines == True):
                sContent = sContent.replace("&nbsp;", "").replace("&#8217;","'")

        if self.__enableDNS:
            socket.getaddrinfo = self.save_getaddrinfo
            self.__enableDNS = False

        return sContent

    def new_getaddrinfo(self, *args):
        try:
            import sys
            import dns.resolver

            if isMatrix():
                path = VSPath('special://home/addons/script.module.dnspython/lib/')
            else:
                path = VSPath('special://home/addons/script.module.dnspython/lib/').decode('utf-8')

            if path not in sys.path:
                sys.path.append(path)
            host = args[0]
            port = args[1]
            # Keep the domain only: http://example.com/foo/bar => example.com
            if "//" in host:
                host = host[host.find("//"):]
            if "/" in host:
                host = host[:host.find("/")]
            resolver = dns.resolver.Resolver(configure=False)

            resolver.nameservers = ['1.1.1.1', '2606:4700:4700::1111', '80.67.169.12', '2001:910:800::12', '80.67.169.40', '2001:910:800::40']
            answer = resolver.query(host, 'a')
            host_found = str(answer[0])
            VSlog("new_getaddrinfo found host %s" % host_found)

            return [(2, 1, 0, '', (host_found, port)), (2, 1, 0, '', (host_found, port))]
        except Exception as e:
            VSlog("new_getaddrinfo ERROR: {0}".format(e))
            return self.save_getaddrinfo(*args)

def MPencode(fields):
    import mimetypes
    random_boundary = __randy_boundary()
    content_type = "multipart/form-data, boundary=%s" % random_boundary

    form_data = []

    if fields:
        try:
            data = fields.iteritems()
        except:
            data = fields.items()

        for (key, value) in data:
            if not hasattr(value, 'read'):
                itemstr = '--%s\r\nContent-Disposition: form-data; name="%s"\r\n\r\n%s\r\n' % (random_boundary, key, value)
                form_data.append(itemstr)
            elif hasattr(value, 'read'):
                with value:
                    file_mimetype = mimetypes.guess_type(value.name)[0] if mimetypes.guess_type(value.name)[0] else 'application/octet-stream'
                    itemstr = '--%s\r\nContent-Disposition: form-data; name="%s"; filename="%s"\r\nContent-Type: %s\r\n\r\n%s\r\n' % (random_boundary, key, value.name, file_mimetype, value.read())
                form_data.append(itemstr)
            else:
                raise Exception(value, 'Field is neither a file handle or any other decodable type.')
    else:
        pass

    form_data.append('--%s--\r\n' % random_boundary)

    return content_type, ''.join(form_data)

def convert_url(url):
  import urllib.parse
  parsed_url = urllib.parse.urlparse(url)
  path_components = parsed_url.path.split('/')

  encoded_components = []
  for component in path_components:
    encoded_component = urllib.parse.quote(component)
    encoded_components.append(encoded_component)

  encoded_path = '/'.join(encoded_components)

  converted_url = urllib.parse.urlunparse((parsed_url.scheme, parsed_url.netloc, encoded_path, parsed_url.params, parsed_url.query, parsed_url.fragment))
  return converted_url

def __randy_boundary(length=10, reshuffle=False):
    import string
    import random

    if isMatrix():
        character_string = string.ascii_letters + string.digits
    else:
        character_string = string.letters + string.digits

    boundary_string = []
    for i in range(0, length):
        rand_index = random.randint(0, len(character_string) - 1)
        boundary_string.append(character_string[rand_index])
    if reshuffle:
        random.shuffle(boundary_string)
    else:
        pass
    return ''.join(boundary_string)
