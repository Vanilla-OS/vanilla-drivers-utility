# wrapper.py
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
import logging
import apt
from UbuntuDrivers import detect


logger = logging.getLogger("DriversUtility:Wrapper")


class DriversUtilityWrapper:

    def __init__(self):
        self.__cache = apt.Cache()

    def is_installed(self, package: str):
        """Check if a package is installed."""
        return self.__cache[package].is_installed

    def get_drivers(self):
        """Get drivers list.
        This is just a simple wrapper for UbuntuDrivers.detect.system_device_drivers()
        which adds the "installed" key to each driver and sort drivers by greatest.
        """
        drivers = detect.system_device_drivers()
        tmp_drivers = drivers.copy()

        for group, items in tmp_drivers.items():
            for driver in items.get('drivers', {}):
                items['drivers'][driver]['installed'] = self.is_installed(driver)

            items['drivers'] = {k: v for k, v in sorted(items['drivers'].items(), key=lambda item: item[1]['recommended'], reverse=True)}

        return drivers

    @staticmethod
    def can_install() -> bool:
        return not os.path.exists("/tmp/abroot-transactions.lock")

    def get_install_command(self, driver: str) -> str:
        command = ["pkexec", "abroot", "exec", "-f", "apt", "install", f"linux-headers-$(uname -r)"]

        if "nvidia" in driver:
            command.append("nvidia-prime")

        command.append(driver)
        command.append("-y")

        logger.info(_("Install command: %s"), " ".join(command))
        
        return " ".join(command)
