# driver.py
#
# Copyright 2023 Mirko Brombin
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
# SPDX-License-Identifier: GPL-3.0-or-later

from gi.repository import Gtk, Gio, GObject, Adw


@Gtk.Template(resource_path='/org/vanillaos/drivers_utility/gtk/driver.ui')
class DriverRow(Adw.ActionRow):
    __gtype_name__ = 'DriverRow'
    __gsignals__ = {
        'install': (GObject.SignalFlags.RUN_FIRST, None, (str,)),
        'restart': (GObject.SignalFlags.RUN_FIRST, None, ()),
    }
    img_installed = Gtk.Template.Child()
    img_install = Gtk.Template.Child()
    btn_restart = Gtk.Template.Child()

    def __init__(self, driver, items, is_latest_installed, can_install, **kwargs):
        super().__init__(**kwargs)

        self.__driver = driver
        self.__items = items
        self.__is_latest_installed = is_latest_installed
        self.__can_install = can_install

        self.__build_ui()

    def __build_ui(self):
        subtitle = _("Free") if self.__items.get('free', False) else _("Proprietary")
        subtitle += _(", recommended") if self.__items.get('recommended', False) else ""
        subtitle += _(", builtin") if self.__items.get('builtin', False) else ""
        subtitle += _(", installed") if self.__items.get('installed', False) else ""
        subtitle += _(", Waiting for restart") if self.__items.get('waiting', False) else ""
        
        self.set_title(self.__driver)
        self.set_subtitle(subtitle)

        if self.__items.get('installed', False):
            self.img_installed.show()
        elif not self.__is_latest_installed and self.__can_install:
            self.set_activatable(True)
            self.img_install.show()
            self.connect("activated", self.__on_activated)
        elif not self.__can_install:
            self.set_activatable(False)
            self.set_tooltip_text(
                _("It is not possible to install this driver now. Please restart your device and try again.")
            )
        else:
            self.btn_restart.connect("clicked", self.__on_restart_clicked)
            self.btn_restart.show()

    def __on_activated(self, widget):
        self.emit('install', self.__driver)

    def __on_restart_clicked(self, widget):
        self.emit('restart')
