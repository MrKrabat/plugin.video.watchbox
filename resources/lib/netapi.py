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

import re
import json
import urllib
import urllib2
from bs4 import BeautifulSoup

import xbmc
import xbmcgui

import list


def genres_show(args):
	"""Show all genres
	"""
	response = urllib2.urlopen('https://www.watchbox.de/genres/')
	html = response.read()

	soup = BeautifulSoup(html, 'html.parser')
	div = soup.find("div", {"class": "grid_genres_b"})

	for item in div.find_all('section'):
		list.add_item(args,
						{'url':			item.a['href'],
						'title':		item.find("div", {"class": "text_browse-teaser-title"}).string.strip().encode('utf-8'),
						'genre':		item.find("div", {"class": "text_browse-teaser-title"}).string.strip().encode('utf-8'),
						'mode':			'genre_list',
						'plot':			item.find("div", {"class": "text_browse-teaser-subtitle"}).string.strip().encode('utf-8')},
						isFolder=True, mediatype="video")


	list.endofdirectory()


def genre_list(args):
	"""List options for gernre
	"""
	list.add_item(args,
			{'title':	args._addon.getLocalizedString(30022),
			'url':		args.url,
			'plot':		args.plot,
			'genre':	args.genre,
			'mode':		'genre_all'})
	list.add_item(args,
			{'title':	args._addon.getLocalizedString(30023),
			'url':		args.url,
			'plot':		args.plot,
			'genre':	args.genre,
			'mode':		'genre_movie'})
	list.add_item(args,
			{'title':	args._addon.getLocalizedString(30024),
			'url':		args.url,
			'plot':		args.plot,
			'genre':	args.genre,
			'mode':		'genre_tvshows'})
	list.endofdirectory()


def genre_view(mode, args):
	"""Show all tv shows / movies
	"""
	url = ''
	if not args.offset == '0':
		url = '?page=' + str(args.offset)

	if mode == 1:
		response = urllib2.urlopen('https://www.watchbox.de' + args.url + 'filme/' + url)
	elif mode == 2:
		response = urllib2.urlopen('https://www.watchbox.de' + args.url + 'serien/' + url)
	elif mode == 3:
		response = urllib2.urlopen('https://www.watchbox.de/beste/' + url)
	elif mode == 4:
		response = urllib2.urlopen('https://www.watchbox.de/neu/' + url)
	else:
		response = urllib2.urlopen('https://www.watchbox.de' + args.url + 'beste/' + url)

	html = response.read()

	soup = BeautifulSoup(html, 'html.parser')
	div = soup.find("div", {"class": "teaser-pagination__page"})

	for item in div.find_all('section'):
		thumb = item.img['src'].replace(" ", "%20")
		if thumb[:4] != "http":
			thumb = "https:" + thumb

		if (mode == 1) or ('.html' in item.a['href']):
			list.add_item(args,
							{'url':			item.a['href'],
							'title':		item.find("div", {"class": "text_teaser-portrait-title"}).string.strip().encode('utf-8'),
							'thumb':		thumb,
							'fanart_image':	thumb,
							'genre':		args.genre,
							'mode':			'videoplay',
							'plot':			item.find("div", {"class": "text_teaser-portrait-description"}).string.strip().encode('utf-8')},
							isFolder=False, mediatype="video")
		else:
			list.add_item(args,
							{'url':			item.a['href'],
							'title':		item.find("div", {"class": "text_teaser-portrait-title"}).string.strip().encode('utf-8'),
							'thumb':		thumb,
							'fanart_image':	thumb,
							'genre':		args.genre,
							'mode':			'season_list',
							'plot':			item.find("div", {"class": "text_teaser-portrait-description"}).string.strip().encode('utf-8')},
							isFolder=True, mediatype="video")


	if '<span>Zeig mir mehr</span>' in html:
		list.add_item(args,
				{'title':	args._addon.getLocalizedString(30025).encode('utf-8'),
				'url':		args.url,
				'plot':		args.plot,
				'genre':	args.genre,
				'offset':	str(int(args.offset) + 1),
				'mode':		args.mode})

	list.endofdirectory()


def season_list(args):
	"""Show all seasons
	"""
	response = urllib2.urlopen('https://www.watchbox.de' + args.url)
	html = response.read()

	soup = BeautifulSoup(html, 'html.parser')
	ul = soup.find("ul", {"class": "season-panel"})
	if not ul:
		list.endofdirectory()
		return

	for item in ul.find_all('li'):
		list.add_item(args,
						{'url':			item.a['href'],
						'title':		item.a.string.strip().encode('utf-8'),
						'thumb':		args.icon,
						'fanart_image':	args.fanart,
						'genre':		args.genre,
						'mode':			'episode_list',
						'plot':			args.plot},
						isFolder=True, mediatype="video")


	list.endofdirectory()


def episode_list(args):
	"""Show all episodes
	"""
	response = urllib2.urlopen('https://www.watchbox.de' + args.url)
	html = response.read()

	soup = BeautifulSoup(html, 'html.parser')
	div = soup.find("div", {"class": "swiper-wrapper"})
	if not div:
		list.endofdirectory()
		return
	regex = r"([0-9]{1,3})"

	for item in div.find_all('section'):
		episode = item.find("div", {"class": "teaser__season-info"}).string.strip().encode('utf-8')
		matches = re.findall(regex, episode)

		if not len(matches) == 2:
			list.add_item(args,
							{'url':			item.a['href'],
							'title':		item.find("div", {"class": "text_teaser-landscape-title"}).string.strip().encode('utf-8'),
							'thumb':		args.icon,
							'fanart_image':	args.fanart,
							'genre':		args.genre,
							'mode':			'videoplay',
							'plot':			args.plot},
							isFolder=False, mediatype="video")
		else:
			list.add_item(args,
							{'url':			item.a['href'],
							'title':		matches[1] + ' - ' + item.find("div", {"class": "text_teaser-landscape-title"}).string.strip().encode('utf-8'),
							'thumb':		args.icon,
							'fanart_image':	args.fanart,
							'genre':		args.genre,
							'episode':		matches[1],
							'season':		matches[0],
							'mode':			'videoplay',
							'plot':			args.plot},
							isFolder=False, mediatype="video")


	list.endofdirectory()


def search(args):
	"""Search function
	"""
	d = xbmcgui.Dialog().input(args._addon.getLocalizedString(30021), type=xbmcgui.INPUT_ALPHANUM)
	if not d or len(d) < 2:
		return

	response = urllib2.urlopen('https://api.watchbox.de/v1/search/?page=1&maxPerPage=28&active=true&term=' + urllib.quote_plus(d))
	html = response.read()

	# parse json
	json_obj = json.loads(html)

	for item in json_obj['items']:
		if str(item['type']) == 'film':
			list.add_item(args,
							{'url':			'/serien/test-' + str(item['entityId']) + '/',
							'title':		item['headline'].encode('utf-8'),
							'mode':			'videoplay',
							'thumb':		'https://aiswatchbox-a.akamaihd.net/watchbox/format/' + str(item['entityId']) + '_dvdcover/600x840/test.jpg',
							'fanart_image':	'https://aiswatchbox-a.akamaihd.net/watchbox/format/' + str(item['entityId']) + '_dvdcover/600x840/test.jpg',
							'year':			str(item['productionYear']),
							'plot':			item['description'].encode('utf-8')},
							isFolder=False, mediatype="video")

		else:
			list.add_item(args,
							{'url':			'/serien/test-' + str(item['entityId']) + '/',
							'title':		item['headline'].encode('utf-8'),
							'mode':			'season_list',
							'thumb':		'https://aiswatchbox-a.akamaihd.net/watchbox/format/' + str(item['entityId']) + '_dvdcover/600x840/test.jpg',
							'fanart_image':	'https://aiswatchbox-a.akamaihd.net/watchbox/format/' + str(item['entityId']) + '_dvdcover/600x840/test.jpg',
							'year':			str(item['productionYear']),
							'plot':			item['description'].encode('utf-8')},
							isFolder=True, mediatype="video")


	list.endofdirectory()


def startplayback(args):
	"""Plays a video
	"""
	response = urllib2.urlopen('https://www.watchbox.de' + args.url)
	html = response.read()

	soup = BeautifulSoup(html, 'html.parser')

	regex = r"hls\: '(.*?)',"
	matches = re.search(regex, html).group(1)

	if matches:
		# play stream
		item = xbmcgui.ListItem(args.name, path=matches)
		item.setInfo(type="Video", infoLabels={"Title":       args.name,
												"TVShowTitle": args.name,
												"episode":		args.episode,
												"plot":			args.plot})
		item.setThumbnailImage(args.icon)
		xbmc.Player().play(matches, item)
	else:
		xbmc.log("[PLUGIN] %s: Failed to play stream" % args._addonname, xbmc.LOGERROR)
		xbmcgui.Dialog().ok(args._addonname, args._addon.getLocalizedString(30044))
