import random
import time
import requests
import xbmcaddon
from resources.lib.comaddon import VSlog

STRING_TYPES = str

addon = xbmcaddon.Addon()
get_setting = addon.getSetting

def set_setting(id, value):
    addon.setSetting(id, str(value))

def generate_chrome_version():
    return f"Chrome/{random.randint(90, 122)}.0.{random.randint(3221, 4235)}.{random.randint(0, 95)}"

def build_random_ua(os_types, chrome_version):
    return f"Mozilla/5.0 {random.choice(os_types)} (KHTML, like Gecko) {chrome_version} Safari/537.36"

def get_random_ua():
    os_types = [
        '(Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
        '(Windows NT 11.0; Win64; x64) AppleWebKit/537.36',
        '(X11; Ubuntu 22.04; x86_64) AppleWebKit/537.36',
        '(X11; Fedora 37; x86_64) AppleWebKit/537.36',
        '(Macintosh; Intel Mac OS X 10.15; x64) AppleWebKit/537.36',
        '(Macintosh; Intel Mac OS X 11.6; x64) AppleWebKit/537.36',
        '(Linux; U; Android 13; en-us; Pixel 6 Pro Build/TPP1.220621.005) AppleWebKit/537.36',
        '(Linux; U; Android 12; en-us; SM-G998B Build/SP1A.210812.016) AppleWebKit/537.36',
        '(iPad; CPU OS 15_6 like Mac OS X) AppleWebKit/604.1.34',
        '(iPhone; CPU OS 16_3 like Mac OS X) AppleWebKit/605.1.15s',
    ]
    chrome_version = generate_chrome_version()
    return build_random_ua(os_types, chrome_version)

def get_pc_ua():
    os_types = [
        '(Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
        '(Windows NT 11.0; Win64; x64) AppleWebKit/537.36',
        '(X11; Ubuntu 22.04; x86_64) AppleWebKit/537.36',
        '(X11; Fedora 37; x86_64) AppleWebKit/537.36',
        '(Macintosh; Intel Mac OS X 10.15; x64) AppleWebKit/537.36',
        '(Macintosh; Intel Mac OS X 11.6; x64) AppleWebKit/537.36',
    ]
    chrome_version = generate_chrome_version()
    return build_random_ua(os_types, chrome_version)

def get_phone_ua():
    os_types = [
        '(iPhone; CPU OS 16_3 like Mac OS X) AppleWebKit/605.1.15s',
        '(iPad; CPU OS 15_6 like Mac OS X) AppleWebKit/604.1.34',
        '(Linux; U; Android 13; en-us; Pixel 6 Pro Build/TPP1.220621.005)',
        '(Linux; U; Android 12; en-us; SM-G998B Build/SP1A.210812.016)',
        '(Linux; U; Android 10; en-us; Mi 10T Pro Build/QKQ1.190711.002)',
    ]
    chrome_version = generate_chrome_version()
    return build_random_ua(os_types, chrome_version)

def get_ua():
    try:
        last_gen = int(get_setting('last_ua_create'))
    except ValueError:
        last_gen = 0

    if not get_setting('current_ua') or last_gen < time.time() - (7 * 24 * 60 * 60):
        user_agent = get_random_ua()
        set_ua(user_agent)
    else:
        user_agent = get_setting('current_ua')

    return user_agent

def set_ua(ua):
    set_setting('current_ua', ua)
    set_setting('last_ua_create', int(time.time()))

def save_cookies(flarejson):
    set_setting('current_cook', {
        cookie['name']: cookie['value'] for cookie in flarejson
    })

def get_url_with_cache(url, cache_key, expiration_hours):
    try:
        last_gen = int(get_setting(f'last_{cache_key}_create'))
    except ValueError:
        last_gen = 0

    if not get_setting(cache_key) or last_gen < time.time() - (expiration_hours * 3600):
        resolved_url = requests.get(url, allow_redirects=True).url
        set_setting(cache_key, resolved_url)
        set_setting(f'last_{cache_key}_create', int(time.time()))
    else:
        resolved_url = get_setting(cache_key)

    return resolved_url

def get_arabseed_url(url):
    return get_url_with_cache(url, 'seed_url', 24)

def get_wecima_url(url):
    return get_url_with_cache(url, 'wecima_url', 120)
