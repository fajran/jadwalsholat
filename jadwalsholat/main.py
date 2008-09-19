#!/usr/bin/env python

import pygtk
import sys
pygtk.require('2.0')

import gtk
import gtk.glade
import gobject
import gnomeapplet

import time

import itl

class PrayerTimeMenuItem(gtk.MenuItem):

	def __init__(self, label, time):
		gtk.MenuItem.__init__(self, label)

		hb = gtk.HBox()
		hb.set_spacing(60)

		self.label = gtk.Label(label)
		self.time = gtk.Label(time)

		self.label.set_alignment(0, 0.5)
		self.time.set_alignment(1, 0.5)

		hb.add(self.label)
		hb.add(self.time)

		self.remove(self.get_child())
		self.add(hb)


class JadwalSholatApplet:

	def __init__(self, applet):
		self.applet = applet

		self.names = ["Shubuh", "Fajar", "Dzuhur", "Ashar", "Maghrib", "Isya"]

		self.__init_widgets()
		self.itl = itl.PrayerTime(52.3, 4.77, 1)

		self.__init_timer()

		self.today = None

		self.__update_time()


	def __init_widgets(self):

		self.glade = gtk.glade.XML("/home/iang/project/jadwalsholat/dev/master/jadwalsholat.glade")
	
		#
		# Menu structure
		#

		menubar = gtk.MenuBar()
		menubar.connect('button-press-event', self.__on_menubar_pressed)
		self.applet.add(menubar)

		self.menu = gtk.MenuItem("Jadwal Sholat")
		menubar.append(self.menu)

		menu = gtk.Menu()
		self.menu.set_submenu(menu)

		self.menu_prayer_times = []
		for i in self.names:
			m = PrayerTimeMenuItem(i, "00:00")
			self.menu_prayer_times.append(m)
			menu.append(m)

		menu.append(gtk.SeparatorMenuItem())

		self.menu_preferences = gtk.MenuItem("Pengaturan")
		self.menu_preferences.connect("activate", self.__on_preferences_activated)
		menu.append(self.menu_preferences)

		# menu.append(gtk.SeparatorMenuItem())

		# self.menu_about = gtk.MenuItem("Tentang aplikasi")
		# self.menu_about.connect("activate", self.__on_about_activated)
		# menu.append(self.menu_about)

		#
		# Dialogs
		#

		self.dialog_preferences = self.glade.get_widget("dialog_preferences")


	def __init_timer(self):

		gobject.timeout_add(30000, self.__update_time)

	#
	# Signals
	#

	def __on_preferences_activated(self, obj):
		self.dialog_preferences.show()

	def __on_menubar_pressed(self, obj, event):
		if event.button != 1:
			obj.stop_emission('button-press-event')

		return False


	#
	# Time Update
	#

	def __update_prayer_time(self):
		self.prayer_time = self.itl.get_prayer_time()

		for i in range(0, 6):
			widget = self.menu_prayer_times[i]
			widget.time.set_text(self.prayer_time[i])

	def __update_time(self):

		now = time.localtime()
		today = time.strftime("%d-%m-%Y", now)

		if today != self.today:
			self.__update_prayer_time()
			self.today = today

		self.__update_menu(now)

		# return True so gtk.timeout_add won't stop
		return True


	def __update_menu(self, now):

		label = self.menu.get_child()
		today = time.strftime("%d-%m-%Y", now)

		snow = time.mktime(now)

		next = None
		for i in range(0, 6):
			if i == 1:
				continue

			t = self.prayer_time[i]

			sec = time.mktime(time.strptime("%s %s" % (today, t), "%d-%m-%Y %H:%M"))

			if sec > snow:
				next = (i, sec)
				break

		if next:
			i, sec = next

			delta = int(sec - snow)

			next = "%d:%02d" % (int(delta / 3600), ((delta + 60) % 3600) / 60)

			label.set_text("%s -%s" % (self.names[i], next))

		else:
			pass
			# TODO




def factory(applet, iid):

	jsa = JadwalSholatApplet(applet)
	applet.show_all()

	return True

if len(sys.argv) == 2:
	if sys.argv[1] == "--window":
		
		window = gtk.Window(gtk.WINDOW_TOPLEVEL)
		window.set_title("Jadwal Sholat")
		window.connect("destroy", gtk.main_quit)

		applet = gnomeapplet.Applet()
		factory(applet, None)
		applet.reparent(window)

		window.show_all()
		gtk.main()
		sys.exit()

gnomeapplet.bonobo_factory("OAFIID:GNOME_JadwalSholat_Factory",
                                     gnomeapplet.Applet.__gtype__,
                                     "simple remote control", "1.0", factory)

