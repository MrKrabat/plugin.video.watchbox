# -*- coding: utf-8 -*-
# Watchbox
# Copyright (C) 2017 MrKrabat
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import os
try:
    from urllib import urlencode
except ImportError:
    from urllib.parse import urlencode
try:
    from urllib2 import urlopen, build_opener, HTTPCookieProcessor, install_opener
except ImportError:
    from urllib.request import urlopen, build_opener, HTTPCookieProcessor, install_opener
try:
    from cookielib import LWPCookieJar
except ImportError:
    from http.cookiejar import LWPCookieJar

import xbmc


def login(username, password, args):
    """Login and session handler
    """
    login_url = "https://www.watchbox.de/login/"

    # create cookie path
    cookiepath = os.path.join(
        xbmc.translatePath(args._addon.getAddonInfo("profile")),
        "cookies.lwp")

    # create cookiejar
    cj = LWPCookieJar()
    args._cj = cj

    # lets urllib2 handle cookies
    opener = build_opener(HTTPCookieProcessor(cj))
    opener.addheaders = [("User-Agent", "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36")]
    opener.addheaders = [("Accept-Charset", "utf-8")]
    install_opener(opener)

    # check if session exists
    try:
        cj.load(cookiepath, ignore_discard=True)

        # check if session is valid
        response = urlopen("https://www.watchbox.de/profil/")
        html = response.read().decode("utf-8")

        if username in html:
            # session is valid
            return True

    except IOError:
        # cookie file does not exist
        pass

    # build POST data
    post_data = urlencode({"email":    username,
                           "password": password,
                           "lasturl":  "/"})

    # POST to login page
    response = urlopen(login_url, post_data.encode("utf-8"))
    html = response.read().decode("utf-8")

    # check for login string
    response = urlopen("https://www.watchbox.de/profil/")
    html = response.read().decode("utf-8")

    if username in html:
        # save session to disk
        cj.save(cookiepath, ignore_discard=True)
        return True
    else:
        return False


def getCookie(args):
    """Returns all cookies as string and urlencoded
    """
    if not args._login:
        return "|User-Agent=Mozilla%2F5.0%20%28Windows%20NT%2010.0%3B%20Win64%3B%20x64%29%20AppleWebKit%2F537.36%20%28KHTML%2C%20like%20Gecko%29%20Chrome%2F60.0.3112.113%20Safari%2F537.36"

    # create cookie path
    cookiepath = os.path.join(
        xbmc.translatePath(args._addon.getAddonInfo("profile")),
        "cookies.lwp")
    # save session to disk
    args._cj.save(cookiepath, ignore_discard=True)

    ret = ""
    for cookie in args._cj:
        ret += urlencode({cookie.name: cookie.value}) + ";"

    return "|User-Agent=Mozilla%2F5.0%20%28Windows%20NT%2010.0%3B%20Win64%3B%20x64%29%20AppleWebKit%2F537.36%20%28KHTML%2C%20like%20Gecko%29%20Chrome%2F60.0.3112.113%20Safari%2F537.36&Cookie=" + ret[:-1]
