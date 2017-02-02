#!/usr/bin/python3
#
# eos-google-chrome-system-helper: system helper to touch / reset the stamp file
#
# Copyright (C) 2017 Endless Mobile, Inc.
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
import config
import logging
import os
import sys

from systemd import journal


def exit_with_error(*args):
    logging.error(*args)
    sys.exit(1)


def touch_file(file):
    with open(file, 'a'):
        os.utime(file, None)


def create_stamp_file(filename):
    dirname = os.path.dirname(filename)

    try:
        os.makedirs(dirname, exist_ok=True)
        touch_file(filename)
        logging.info("Stamp file created at {}".format(filename))
    except OSError as e:
        exit_with_error("Error creating stamp file at {}: {}"
                        .format(filename, str(e)))


def remove_stamp_file(filename):
    try:
        os.unlink(filename)
        logging.info("Stamp file removed from {}".format(filename))
    except OSError as e:
        exit_with_error("Error removing stamp file at {}: {}"
                        .format(filename, str(e)))


if __name__ == '__main__':
    # Send logging messages both to the console and the journal
    logging.basicConfig(level=logging.INFO)
    logging.root.addHandler(journal.JournalHandler())

    parser = argparse.ArgumentParser(description="Marks Google Chrome installation as installed, system-wide")

    parser.add_argument('--debug', help="Show extra messages", action='store_true')
    parser.add_argument('--reset', help="Remove stamp file", action='store_true')

    parsed_args = parser.parse_args()
    if parsed_args.debug:
        logging.root.setLevel(logging.DEBUG)

    if parsed_args.reset:
        remove_stamp_file(config.STAMP_FILE_INITIAL_SETUP_DONE)
    else:
        create_stamp_file(config.STAMP_FILE_INITIAL_SETUP_DONE)

    sys.exit(0)
