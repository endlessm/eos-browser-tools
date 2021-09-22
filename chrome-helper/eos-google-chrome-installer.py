#!/usr/bin/python3
#
# eos-google-chrome-installer: helper script to install Google Chrome
#
# Copyright (C) 2016, 2017 Endless Mobile, Inc.
# Authors:
#  Michal Rostecki <michal@kinvolk.io>
#  Mario Sanchez Prada <mario@endlessm.com>
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.

import argparse
import config
import logging
import os
import subprocess
import sys

import gi
gi.require_version('Flatpak', '1.0')
from gi.repository import Flatpak
from gi.repository import GLib
from systemd import journal


def exit_with_error(*args):
    logging.error(*args)
    sys.exit(1)


class GoogleChromeInstaller:
    def __init__(self):
        try:
            self._installation = Flatpak.Installation.new_system()
        except GLib.Error as e:
            exit_with_error("Couldn't not find current system installation: %r", e)

        if self._check_chrome_flatpak_launcher():
            logging.info("Google Chrome is already installed")
            return

        logging.info("Could not find flatpak launcher for Chrome.")

        self._run_app_center_for_chrome()

    def _check_chrome_flatpak_launcher(self):
        try:
            self._installation.get_current_installed_app(config.FLATPAK_CHROME_APP_ID, None)
        except GLib.Error as e:
            logging.info("Chrome application is not installed")
            return False
        return True

    def _get_unique_id(self):
        chrome_app_center_id = config.FLATPAK_CHROME_APP_ID

        default_branch = None
        try:
            remote = self._installation.get_remote_by_name(config.FLATPAK_REMOTE_EOS_APPS)
        except GLib.Error as e:
            logging.warning("Could not find flatpak remote {}: {}"
                            .format(config.FLATPAK_REMOTE_EOS_APPS, str(e)))

        # Get the default branch now to construct the full unique ID GNOME Software expects.
        default_branch = remote.get_default_branch()
        if default_branch:
            chrome_app_center_id = 'system/flatpak/{}/desktop/{}/{}'.format(config.FLATPAK_REMOTE_EOS_APPS,
                                                                            config.FLATPAK_CHROME_APP_ID,
                                                                            default_branch)
        return chrome_app_center_id

    def _run_app_center_for_chrome(self):
        # FIXME: Ideally, we should be able to pass 'com.google.Chrome' to GNOME Software
        # and it would do the right thing by opening the page for the app's branch matching
        # the default branch for the apps' source remote. Unfortunately, this is not the case
        # at the moment and fixing it is non-trivial, so we'll construct the full unique ID
        # that GNOME Software expects, right from here, based on the remote's metadata.
        unique_id = self._get_unique_id()

        logging.info("Opening App Center...")
        app_center_argv = ['gnome-software', '--details={}'.format(unique_id)]

        try:
            subprocess.Popen(app_center_argv)
        except OSError as e:
            exit_with_error("Could not launch Chrome: {}".format(repr(e)))


def main():
    # Send logging messages both to the console and the journal
    logging.basicConfig(level=logging.INFO)
    logging.root.addHandler(journal.JournalHandler())

    parser = argparse.ArgumentParser()
    parser.add_argument('--debug', dest='debug', action='store_true')

    parsed_args = parser.parse_args()

    if parsed_args.debug:
        logging.root.setLevel(logging.DEBUG)

    app_arch = Flatpak.get_default_arch()
    if app_arch != 'x86_64':
        exit_with_error("Found installation of unsupported architecture: %s", app_arch)

    GoogleChromeInstaller()
    sys.exit(0)


if __name__ == '__main__':
    main()
