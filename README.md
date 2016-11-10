# eos-google-chrome-helper

## Description

This package provides a system level wrapper application to allow easily
downloading, installing and running Google Chrome on Endless OS.

## Detailed description

This wrapper application does mainly three things when you click on the desktop icon:

  * Integrates with the App Center (GNOME Software) so that it gets open on the page
    for Google Chrome when you click on the desktop icon and hasn't been installed yet.

  * If Google Chrome has been previously installed (using flatpak as a delivery mechanism),
    the wrapper script launches chromium with its own sandbox (outside of flatpak.)

  * Finally, the wrapper script keeps and monitors a process running inside the flatpak
    sandbox for Chrome while the browser is running, to prevent uninstalling / updating
    it while running, relying on flatpak's own locking mechanisms.


This package provides the following elements:
  * `eos-google-chrome.py`: launcher script.
  * `eos-google-chrome.desktop` + `eos-google-chrome.png`: icon and application information
     according to the Desktop Entry Specification, to integrate with the shell.

All this files will be installed, exceptionally, as part of the OSTree, so that the
icon and the wrapper app are available on the desktop at any time, either to run
the browser or to install it if not yet available.

## License

eos-google-chrome is Copyright (C) 2016 Endless Mobile, Inc. and
is licensed under the terms of the GNU General Public License as
published by the Free Software Foundation; either version 2 of
the License, or (at your option) any later version.

See the COPYING file for the full version of the GNU GPLv2 license
