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

import sys

import xbmc
import xbmcgui
import xbmcplugin

import cmdargs
import netapi
import list


def main():
	"""Main function for the addon
	"""
	args = cmdargs.parse_args()

	xbmcplugin.setContent(int(sys.argv[1]), 'tvshows')
	check_mode(args)


def check_mode(args):
	"""Run mode-specific functions
	"""
	try:
		mode = args.mode
	except:
		# call from other plugin
		mode = 'videoplay'
		args.name = 'Video'
		args.episode, args.rating, args.plot, args.year, args.studio, args.icon = ('None',)*6

		if hasattr(args,'id'):
			args.url = '/de/v2/catalogue/episode/' + id
		elif hasattr(args,'url'):
			args.url = args.url[24:]
		else:
			mode = None

	if mode is None:
		showMainMenue(args)
	elif mode == 'genres':
		netapi.genres_show(args)
	elif mode == 'genre_list':
		netapi.genre_list(args)
	elif mode == 'genre_all':
		netapi.genre_view(0, args)
	elif mode == 'genre_movie':
		netapi.genre_view(1, args)
	elif mode == 'genre_tvshows':
		netapi.genre_view(2, args)
	elif mode == 'season_list':
		netapi.season_list(args)
	elif mode == 'episode_list':
		netapi.episode_list(args)
	elif mode == 'search':
		netapi.search(args)
	elif mode == 'videoplay':
		netapi.startplayback(args)
	else:
		# unkown mode
		xbmc.log("[PLUGIN] %s: Failed in check_mode '%s'" % (args._addonname, str(mode)), xbmc.LOGERROR)
		xbmcgui.Dialog().notification(args._addonname, args._addon.getLocalizedString(30041), xbmcgui.NOTIFICATION_ERROR)
		showMainMenue(args)


def showMainMenue(args):
	"""Show main menu
	"""
	list.add_item(args,
			{'title':	args._addon.getLocalizedString(30020),
			'mode':		'genres'})
	list.add_item(args,
			{'title':	args._addon.getLocalizedString(30021),
			'mode':		'search'})
	list.endofdirectory()
