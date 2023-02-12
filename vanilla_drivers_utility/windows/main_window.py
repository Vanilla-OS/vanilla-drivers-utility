# main_window.py
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

import os
import subprocess
from gi.repository import Gtk, Gdk, Adw

from vanilla_drivers_utility.utils.run_async import RunAsync
from vanilla_drivers_utility.utils.wrapper import DriversUtilityWrapper
from vanilla_drivers_utility.widgets.driver import DriverRow
from vanilla_drivers_utility.windows.installation_window import DriversUtilityWindowInstallation


@Gtk.Template(resource_path='/org/vanillaos/drivers_utility/gtk/window-main.ui')
class DriversUtilityWindow(Adw.ApplicationWindow):
    __gtype_name__ = 'DriversUtilityWindow'
    status_drivers = Gtk.Template.Child()
    status_no_drivers = Gtk.Template.Child()
    page_drivers = Gtk.Template.Child()
    btn_cancel = Gtk.Template.Child()
    toasts = Gtk.Template.Child()
    info_bar = Gtk.Template.Child()

    def __init__(self, embedded, **kwargs):
        super().__init__(**kwargs)

        self.__refs = []
        
        self.__build_ui()
        if embedded:
            self.__set_embedded()

    def __build_ui(self, restart: bool = False):
        if not restart:
            self.btn_cancel.connect("clicked", self.__on_cancel_clicked)

        self.status_drivers.show()
        self.status_no_drivers.hide()

        self.info_bar.set_visible(not self.__can_install)

        for ref in self.__refs:
            ref.get_parent().remove(ref)

        def async_fn():
            return DriversUtilityWrapper().get_drivers()

        def callback_fn(result, error):
            if not result or error:
                self.status_drivers.hide()
                self.status_no_drivers.show()
                return

            self.status_drivers.hide()
            self.status_no_drivers.hide()
            self.page_drivers.show()
            set_drivers(result)

        def set_drivers(drivers):
            for _, items in drivers.items():
                _drivers = items.get('drivers', {})
                _vendor = items.get('vendor', 'Unknown')
                _model = items.get('model', 'Unknown')

                group = Adw.PreferencesGroup(title=f"{_vendor} {_model}")
                self.page_drivers.add(group)
                self.__refs.append(group)

                for driver in _drivers:
                    _row = DriverRow(driver, _drivers[driver], 
                        self.__latest_installed == driver, self.__can_install)
                    group.add(_row)
                    _row.connect("install", self.__on_install_clicked)
                    _row.connect("restart", self.__restart)

        RunAsync(async_fn, callback_fn)

    def __on_install_clicked(self, widget, driver):
        def on_close_fn(res):
            if res:
                self.toast(_("Driver {} installed successfully!".format(driver)))
                self.__build_ui(restart=True)
                self.__write_latest_installed(driver)
                return

            self.toast(_("Driver {} installation failed!".format(driver)))

        cmd = DriversUtilityWrapper().get_install_command(driver)
        window = DriversUtilityWindowInstallation(driver, self, cmd, on_close_fn)
        window.connect("restart", self.__restart)
        window.show()
        
    def __set_embedded(self):
        self.btn_cancel.show()
        self.set_deletable(False)

    def __on_cancel_clicked(self, widget):
        self.destroy()

    def toast(self, message, timeout=2):
        toast = Adw.Toast.new(message)
        toast.props.timeout = timeout
        self.toasts.add_toast(toast)

    def __restart(self, widget):
        subprocess.run(['gnome-session-quit', '--reboot'])

    @property
    def __latest_installed(self):
        if os.path.exists("/tmp/vanilla_drivers_utility.latest"):
            with open("/tmp/vanilla_drivers_utility.latest", "r") as f:
                return f.read().strip()

        return 

    def __write_latest_installed(self, driver):
        with open("/tmp/vanilla_drivers_utility.latest", "w") as f:
            f.write(driver)

    @property
    def __can_install(self):
        return DriversUtilityWrapper().can_install() and not self.__latest_installed
