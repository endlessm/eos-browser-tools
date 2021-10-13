appdatadir = $(datadir)/appdata
appdata_DATA = eos-google-chrome-helper.appdata.xml

desktopdir = $(datadir)/applications
desktop_DATA = \
	eos-browser-appmode.desktop \
	google-chrome.desktop \
	$(NULL)

icon64dir = $(datadir)/icons/hicolor/64x64/apps
dist_icon64_DATA = icons/hicolor/64x64/eos-google-chrome.png

icon128dir = $(datadir)/icons/hicolor/128x128/apps
dist_icon128_DATA = icons/hicolor/128x128/eos-google-chrome.png

icon256dir = $(datadir)/icons/hicolor/256x256/apps
dist_icon256_DATA = icons/hicolor/256x256/eos-google-chrome.png

tmpfilesdir = $(prefix)/lib/tmpfiles.d
tmpfiles_in = eos-google-chrome.conf.in
tmpfiles_DATA = $(tmpfiles_in:.conf.in=.conf)

do_edit = sed \
	-e "s|\@chromehelpername\@|$(CHROME_HELPER_NAME)|" \
	-e "s|\@datadir\@|$(datadir)|" \
	-e "s|\@localstatedir\@|$(localstatedir)|"

%.desktop: %.desktop.in Makefile
	$(AM_V_GEN) $(do_edit) $<> $@

%.conf: %.conf.in Makefile
	$(AM_V_GEN) $(do_edit) $<> $@

EXTRA_DIST = \
	$(appdata_DATA) \
	$(desktop_DATA) \
	$(tmpfiles_in) \
	$(NULL)

CLEANFILES = \
	$(tmpfiles_DATA) \
	$(NULL)
