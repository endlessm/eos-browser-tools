appdatadir = $(datadir)/appdata
appdata_DATA = eos-google-chrome-helper.appdata.xml

desktopdir = $(datadir)/applications
desktop_DATA = google-chrome.desktop

icon64dir = $(datadir)/icons/hicolor/64x64/apps
icon64_DATA = eos-google-chrome.png

autostartdir = $(sysconfdir)/xdg/autostart
autostart_DATA = com.endlessm.GoogleChromeInitialSetup.desktop

com.endlessm.GoogleChromeInitialSetup.desktop: com.endlessm.GoogleChromeInitialSetup.desktop.in Makefile
	$(AM_V_GEN) sed -e "s|\@pkglibexecdir\@|$(pkglibexecdir)|" $<> $@

gsettings_SCHEMAS = com.endlessm.GoogleChromeInitialSetup.gschema.xml

@GSETTINGS_RULES@

EXTRA_DIST = \
	$(appdata_DATA) \
	$(desktop_DATA) \
	$(icon64_DATA) \
	$(autostart_DATA) \
	$(gsettings_SCHEMAS) \
	$(NULL)
