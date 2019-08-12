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
import configparser
import logging
import os
import subprocess
import sys

import gi
gi.require_version('Flatpak', '1.0')
from gi.repository import Flatpak
from gi.repository import Gio
from gi.repository import GLib
from systemd import journal


def exit_with_error(*args):
    logging.error(*args)
    sys.exit(1)


class GoogleChromeInstaller:
    def __init__(self, initial_setup):
        self._initial_setup = initial_setup

        if self._initial_setup:
            if not self._automatic_install_enabled():
                logging.info("Google Chrome installation is disabled")
                sys.exit(0)

            if self._initial_setup_already_done():
                logging.info("Google Chrome automatic installation already done")
                sys.exit(0)

        try:
            self._installation = Flatpak.Installation.new_system()
        except GLib.Error as e:
            exit_with_error("Couldn't not find current system installation: %r", e)

        if self._check_chrome_flatpak_launcher():
            logging.info("Google Chrome is already installed")
            self._touch_done_file()
            return

        logging.info("Could not find flatpak launcher for Chrome.")

        if self._initial_setup:
            self._wait_for_network_connectivity()

        self._run_app_center_for_chrome()

    def _initial_setup_already_done(self):
        if os.path.exists(config.STAMP_FILE_INITIAL_SETUP_DONE):
            return True

        legacy_stamp_file = os.path.expanduser(config.LEGACY_USER_CONFIG_STAMP_FILE)
        if os.path.exists(legacy_stamp_file):
            # This is a legacy scenario, so we touch the system-wide file to
            # make sure next time that's the only thing that gets checked.
            self._touch_done_file()
            return True

        return False

    def _automatic_install_enabled(self):
        if not os.path.exists(config.CONFIG_FILE):
            logging.warning("Could not find configuration file at {}"
                            .format(config.CONFIG_FILE))
            return False

        is_enabled = False
        with open(config.CONFIG_FILE, 'r') as config_file:
            helper_config = configparser.ConfigParser(allow_no_value=True)
            try:
                helper_config.read_file(config_file)
                logging.info("Read contents from configuration file at {}\n"
                             .format(config.CONFIG_FILE))
            except configparser.ParsingError as e:
                logging.error("Error parsing contents from configuration file at {}: {}"
                             .format(config.CONFIG_FILE, str(e)))
                return False

            try:
                is_enabled = helper_config.getboolean('Initial Setup', 'AutomaticInstallEnabled')
                logging.info("AutomaticInstallEnabled = {}".format(str(is_enabled)))
            except configparser.NoOptionError:
                logging.warning("AutomaticInstallEnabled key not found in {}".format(config.CONFIG_FILE))
                return False

        return is_enabled

    def _check_chrome_flatpak_launcher(self):
        try:
            self._installation.get_current_installed_app(config.FLATPAK_CHROME_APP_ID, None)
        except GLib.Error as e:
            logging.info("Chrome application is not installed")
            return False
        return True

    def _is_connected_state(self):
        monitor = Gio.NetworkMonitor.get_default()
        return monitor.get_connectivity() == Gio.NetworkConnectivity.FULL

    def _wait_for_network_connectivity(self):
        def _network_changed(monitor, available, loop):
            if not available:
                logging.info("No network available")
                return

            if monitor.get_connectivity() != Gio.NetworkConnectivity.FULL:
                logging.info("Network available, but not connected to the Internet")
                return

            logging.info("Connected to the network and the internet")
            loop.quit()

        logging.info("Checking network connectivity...")
        if self._is_connected_state():
            logging.info("Network connected")
            return

        logging.info("Not connected to any network, wait for connection")

        loop = GLib.MainLoop()

        monitor = Gio.NetworkMonitor.get_default()
        monitor.connect('network-changed', _network_changed, loop)
        loop.run()

    def _wait_for_installation(self):
        def _installation_finished(monitor, file_, other_file, event_type):
            if event_type != Gio.FileMonitorEvent.CHANGES_DONE_HINT:
                return

            if self._check_chrome_flatpak_launcher():
                logging.info("{} has been installed".format(config.FLATPAK_CHROME_APP_ID))
                loop.quit()

        loop = GLib.MainLoop()

        monitor = self._installation.create_monitor(None)
        monitor.connect('changed', _installation_finished)

        loop.run()

    def _set_as_default_browser(self):
        mimetypes = ['text/html',
                     'x-scheme-handler/http',
                     'x-scheme-handler/https',
                     'x-scheme-handler/about']
        for mimetype in mimetypes:
            try:
                subprocess.check_call('xdg-mime default google-chrome.desktop {}'.format(mimetype),
                                      shell=True)
            except subprocess.CalledProcessError as e:
                exit_with_error("Couldn't start xdg-mime: {}".format(str(e)))
        try:
            subprocess.check_call('xdg-settings set default-web-browser google-chrome.desktop',
                                  shell=True)
        except subprocess.CalledProcessError as e:
            exit_with_error("Couldn't start xdg-settings: {}".format(str(e)))

    def _touch_done_file(self):
        # The system-wide stamp file touched by this helper makes sure that
        # the automatic installation won't ever be performed for other users.
        system_helper_cmd = os.path.join(config.PKG_DATADIR, 'eos-google-chrome-system-helper.py')
        try:
            subprocess.check_call('pkexec {}'.format(system_helper_cmd), shell=True)
        except subprocess.CalledProcessError as e:
            exit_with_error("Couldn't run {}: {}".format(system_helper_cmd, str(e)))

    def _post_install_chrome(self):
        self._wait_for_installation()

        if not self._check_chrome_flatpak_launcher():
            exit_with_error("Chrome isn't installed - something went wrong in GNOME Software")

        logging.info("Chrome successfully installed")

        self._set_as_default_browser()
        self._touch_done_file()

        logging.info("Post-installation configuration done")


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
        if self._initial_setup:
            app_center_argv = ['gnome-software', '--install', unique_id, '--interaction', 'none']
        else:
            app_center_argv = ['gnome-software', '--details={}'.format(unique_id)]

        try:
            subprocess.Popen(app_center_argv)
        except OSError as e:
            exit_with_error("Could not launch Chrome: {}".format(repr(e)))

        # There's a post-install procedure for automatic installations.
        if self._initial_setup:
            self._post_install_chrome()


def main():
    # Send logging messages both to the console and the journal
    logging.basicConfig(level=logging.INFO)
    logging.root.addHandler(journal.JournalHandler())

    parser = argparse.ArgumentParser()
    parser.add_argument('--debug', dest='debug', action='store_true')
    parser.add_argument('--initial-setup', dest='initial_setup', action='store_true')

    parsed_args = parser.parse_args()

    if parsed_args.debug:
        logging.root.setLevel(logging.DEBUG)

    app_arch = Flatpak.get_default_arch()
    if app_arch != 'x86_64':
        exit_with_error("Found installation of unsupported architecture: %s", app_arch)

    GoogleChromeInstaller(parsed_args.initial_setup)
    sys.exit(0)


if __name__ == '__main__':
    main()
