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
import sys
import urllib

import xbmc
import xbmcgui
import xbmcplugin


def endofdirectory():
	# Sort methods are required in library mode
	xbmcplugin.addSortMethod(int(sys.argv[1]),
								xbmcplugin.SORT_METHOD_NONE)
	# Let xbmc know the script is done adding items to the list
	dontAddToHierarchy = False
	xbmcplugin.endOfDirectory(handle = int(sys.argv[1]),
								updateListing = dontAddToHierarchy)


def add_item(args, info, isFolder=True, total_items=0, queued=False, rex=re.compile(r'(?<=mode=)[^&]*'), mediatype="video"):
	"""Add item to directory listing.
	"""
	# Defaults in dict. Use 'None' instead of None so it is compatible for
	info = set_info_defaults(args,info)
	u = build_url(info)

	# Create list item
	li = xbmcgui.ListItem(label = info['title'],
							iconImage = info['thumb'],
							thumbnailImage = info['thumb'])
	li.setInfo(type		  = mediatype,
			   infoLabels = {"title":   info['title'],
							 "plot":	info['plot'],
							 "year":	info['year'],
							 "episode": info['episode'],
							 "season":	info['season'],
							 "genre":	info['genre']})
	li.setProperty("Fanart_Image", info['fanart_image'])

	# Add item to list
	xbmcplugin.addDirectoryItem(handle	= int(sys.argv[1]),
								url		= u,
								listitem   = li,
								isFolder   = isFolder,
								totalItems = total_items)


def build_url(info):
	# Create params for xbmcplugin module
	s = sys.argv[0]    +\
		'?url='        + urllib.quote_plus(info['url'])          +\
		'&mode='       + urllib.quote_plus(info['mode'])         +\
		'&name='       + urllib.quote_plus(info['title'])        +\
		'&id='         + urllib.quote_plus(info['id'])           +\
		'&count='      + urllib.quote_plus(info['count'])        +\
		'&filterx='    + urllib.quote_plus(info['filterx'])      +\
		'&offset='     + urllib.quote_plus(info['offset'])       +\
		'&icon='       + urllib.quote_plus(info['thumb'])        +\
		'&fanart='     + urllib.quote_plus(info['fanart_image']) +\
		'&season='     + urllib.quote_plus(info['season'])       +\
		'&media_type=' + urllib.quote_plus(info['media_type'])   +\
		'&year='       + urllib.quote_plus(info['year'])         +\
		'&duration='   + urllib.quote_plus(info['duration'])     +\
		'&episode='    + urllib.quote_plus(info['episode'])      +\
		'&genre='	   + urllib.quote_plus(info['genre'])        +\
		'&plot='       + urllib.quote_plus(info['plot'])
	return s


def set_info_defaults(args,info):
	# Defaults in dict. Use 'None' instead of None so it is compatible for
	# quote_plus in parseArgs.
	info.setdefault('url',          'None')
	info.setdefault('thumb',        "DefaultFolder.png")
	info.setdefault('fanart_image',
					xbmc.translatePath(args._addon.getAddonInfo('fanart')))
	info.setdefault('count',        '0')
	info.setdefault('filterx',      'None')
	info.setdefault('id',           'None')
	info.setdefault('offset',       '0')
	info.setdefault('season',       '1')
	info.setdefault('media_type',   'None')
	info.setdefault('title',        'None')
	info.setdefault('year',         '0')
	info.setdefault('duration',     '0')
	info.setdefault('episode',      '0')
	info.setdefault('plot',         'None')
	info.setdefault('ordering',     '0')
	info.setdefault('genre',      'None')
	#And set all None to 'None'
	for key, value in info.items():
		if value == None:
			info[key] = 'None'
	return info
