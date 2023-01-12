# eos-browser-tools

# Description

This package currently contains two main components

  * eos-browser-tools: Endless-specific and browser-related tools
  * eos-google-chrome-helper: Wrapper application to run Google Chrome

## eos-browser-tools

This currently provides a handler for `webapp:<WM_CLASS>@<URI>` URIs,
which is currently deprecated but kept for compability purposes.

## eos-google-chrome-helper

This package provides a system level wrapper script and `.desktop` file to run Google Chrome on Endless OS. If Google Chrome has been installed from Endless's Flatpak repository (using Flatpak only as the delivery mechanism), the `.desktop` file is made visible (via `TryExec=`), and the wrapper script launches Chrome with its own sandbox (*outside of Flatpak*), by calling a launcher script that is shipped along with the "headless" flatpak app.

This package provides the following elements:

  * `eos-google-chrome`: wrapper to launch Chrome, if installed
  * `eos-google-chrome.png`: icon to integrate with the desktop
  * `google-chrome.desktop`: application information according to the Desktop Entry
  Specification, to integrate with the shell. Note that we can't name it like the
  icon (i.e. `eos-google-chrome.desktop`) since that way Google Chrome would not be
  able to recognize itself when running as the default browser, which would end up
  with Chrome asking to set itself as the default each time it was run.

These files are installed as part of the OSTree.

Nowadays it is possible to run Chrome within a Flatpak sandbox, and versions of Chrome are published on Flathub that are installed and run in the normal way. However, Endless OS users have not yet been migrated to use this version.

A previous version of the wrapper made the icon always visible, with the script opening the App Center if Chrome was not installed, and would automatically install Chrome in the background on first login. This mechanism was removed in Endless OS 4.

## License

eos-browser-tools is Copyright Endless OS Foundation LLC
and is licensed under the terms of the GNU General Public License
as published by the Free Software Foundation; either version 2 of
the License, or (at your option) any later version.

See the COPYING file for the full version of the GNU GPLv2 license
