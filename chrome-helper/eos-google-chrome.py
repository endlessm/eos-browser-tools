#!/usr/bin/python3
#
# eos-google-chrome: helper script to install/launch Google Chrome
#
# Copyright (C) 2016, 2017 Endless Mobile, Inc.
# Authors:
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
import logging
import os
import subprocess
import sys

import config
import gi
gi.require_version('Flatpak', '1.0')
from gi.repository import Flatpak
from gi.repository import GLib
from systemd import journal


def exit_with_error(message):
    logging.error(message)
    sys.exit(1)


class GoogleChromeLauncher:
    def __init__(self, params):
        self._params = params

        # Remove the old initial-setup stamp file; the system stamp file is
        # removed in a tmpfiles snippet
        legacy_stamp_file = os.path.expanduser(config.LEGACY_USER_CONFIG_STAMP_FILE)
        try:
            os.unlink(legacy_stamp_file)
        except FileNotFoundError:
            pass

        try:
            self._installation = Flatpak.Installation.new_system()
        except GLib.Error as e:
            exit_with_error("Could not find current system installation: {}".format(repr(e)))

        self._start()

    def _start(self):
        chrome_launcher = self._get_chrome_flatpak_launcher()
        if chrome_launcher:
            logging.info("Flatpak launcher for Chrome found. Launching...")
            self._run_chrome_app(chrome_launcher, self._params)
        else:
            logging.info("Could not find flatpak launcher for Chrome. Running installation script...")
            self._install_chrome()

    def _run_chrome_app(self, chrome_launcher, params):
            try:
                launcher_process = subprocess.Popen([chrome_launcher] + params)
                logging.info("Running Google Chrome launcher with PID %d", launcher_process.pid)
            except OSError as e:
                exit_with_error("Could not launch Google Chrome: {}".format(repr(e)))

    def _install_chrome(self):
        try:
            subprocess.Popen([os.path.join(config.PKG_DATADIR, 'eos-google-chrome-installer.py')])
        except OSError as e:
            exit_with_error("Could not launch Chrome: {}".format(repr(e)))

    def _get_chrome_flatpak_launcher(self):
        app = None
        try:
            app = self._installation.get_current_installed_app(config.FLATPAK_CHROME_APP_ID, None)
        except GLib.Error:
            logging.info("Chrome application is not installed")
            return None

        app_path = app.get_deploy_dir()
        if not app_path or not os.path.exists(app_path):
            exit_with_error("Could not find Chrome's application directory")

        app_launcher_path = os.path.join(app_path, 'files', 'bin', 'eos-google-chrome-app')
        if not os.path.exists(app_launcher_path):
            exit_with_error("Could not find flatpak launcher for Google Chrome")

        logging.info("Found flatpak launcher for Google Chrome: %s", repr(app_launcher_path))
        return app_launcher_path


if __name__ == '__main__':
    # Send logging messages both to the console and the journal
    logging.basicConfig(level=logging.INFO)
    logging.root.addHandler(journal.JournalHandler())

    parser = argparse.ArgumentParser()
    parser.add_argument('--debug', dest='debug', action='store_true')
    parser.add_argument('--enable-features', dest='enable_features', default='WebRTCPipeWireCapturer')
    parser.add_argument('--ozone-platform', dest='ozone_platform')
    parser.add_argument('--ozone-platform-hint', dest='ozone_platform_hint', default='auto')

    parsed_args, otherargs = parser.parse_known_args()

    if parsed_args.debug:
        logging.root.setLevel(logging.DEBUG)

    if parsed_args.enable_features:
        features = parsed_args.enable_features.split(',')
        if 'WebRTCPipeWireCapturer' not in features:
            features.append('WebRTCPipeWireCapturer')
        features = ','.join(features)
        otherargs.append(f'--enable-features={features}')

    if parsed_args.ozone_platform:
        otherargs.append(f'--ozone-platform={parsed_args.ozone_platform}')
    elif parsed_args.ozone_platform_hint:
        otherargs.append(f'--ozone-platform-hint={parsed_args.ozone_platform_hint}')

    # Google Chrome is only available for Intel 64-bit
    app_arch = Flatpak.get_default_arch()
    if app_arch != 'x86_64':
        exit_with_error("Found installation of unsupported architecture: {}".format(app_arch))


    GoogleChromeLauncher(otherargs)
    sys.exit(0)
