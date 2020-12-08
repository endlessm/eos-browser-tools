# eos-browser-tools

# Description

This package currently contains two main components

  * eos-browser-tools: Endless-specific and browser-related tools
  * eos-google-chrome-helper: Wrapper application to run Google Chrome

## eos-browser-tools

This currently provides a handler for `webapp:<WM_CLASS>@<URI>` URIs,
which is currently deprecated but kept for compability purposes.

## eos-google-chrome-helper

This package provides a system level wrapper application to allow easily
downloading, installing and running Google Chrome on Endless OS.

This wrapper application does mainly two things when you click on the desktop icon:

  * Integrates with the App Center (GNOME Software) so that it gets open on the page
    for Google Chrome when you click on the desktop icon and hasn't been installed yet.

  * If Google Chrome has been previously installed (using flatpak as a delivery mechanism),
    the wrapper script launches chromium with its own sandbox (outside of flatpak), by
    calling a launcher script that is shipped along with the "headless" flatpak app.

This package provides the following elements:
  * `eos-google-chrome`: wrapper to either launch Chrome or the App Center.
  * `eos-google-chrome.png`: icon to integrate with the desktop.
  * `google-chrome.desktop`: application information according to the Desktop Entry
  Specification, to integrate with the shell. Note that we can't name it like the
  icon (i.e. eos-google-chrome.desktop) since that way Google Chrome would not be
  able to recognize itself when running as the default browser, which would end up
  with Chromium asking to set itself as the default each time it was run.

All this files will be installed, exceptionally, as part of the OSTree, so that the
icon and the wrapper app are available on the desktop at any time, either to run
the browser or to install it if not yet available.

## License

eos-browser-tools is Copyright (C) 2016, 2017 Endless Mobile, Inc.
and is licensed under the terms of the GNU General Public License
as published by the Free Software Foundation; either version 2 of
the License, or (at your option) any later version.

See the COPYING file for the full version of the GNU GPLv2 license
