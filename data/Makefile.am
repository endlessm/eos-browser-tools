appdatadir = $(datadir)/appdata
appdata_DATA = eos-google-chrome-helper.appdata.xml

desktopdir = $(datadir)/applications
desktop_DATA = google-chrome.desktop

icon64dir = $(datadir)/icons/hicolor/64x64/apps
icon64_DATA = eos-google-chrome.png

autostartdir = $(sysconfdir)/xdg/autostart
autostart_in_files = com.endlessm.GoogleChromeInitialSetup.desktop.in
autostart_DATA = $(autostart_in_files:.desktop.in=.desktop)

configdir = $(sysconfdir)/$(PACKAGE)
config_DATA = eos-google-chrome-helper.conf

polkit_policydir = $(datadir)/polkit-1/actions
polkit_policy_in_files = com.endlessm.GoogleChromeHelper.system-helper.policy.in
polkit_policy_DATA = $(polkit_policy_in_files:.policy.in=.policy)

do_edit = sed -e 's|@pkglibexecdir[@]|$(pkglibexecdir)|g'

%.policy: %.policy.in Makefile
	$(AM_V_GEN) $(do_edit) $<> $@

%.desktop: %.desktop.in Makefile
	$(AM_V_GEN) $(do_edit) $<> $@

EXTRA_DIST = \
	$(appdata_DATA) \
	$(desktop_DATA) \
	$(icon64_DATA) \
	$(autostart_in_files) \
	$(polkit_policy_in_files) \
	$(config_DATA) \
	$(NULL)

CLEANFILES = \
	$(autostart_DATA) \
	$(polkit_policy_DATA) \
	$(NULL)
