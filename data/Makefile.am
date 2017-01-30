appdatadir = $(datadir)/appdata
appdata_DATA = eos-google-chrome-helper.appdata.xml

desktopdir = $(datadir)/applications
desktop_DATA = google-chrome.desktop

icon64dir = $(datadir)/icons/hicolor/64x64/apps
icon64_DATA = eos-google-chrome.png

autostartdir = $(sysconfdir)/xdg/autostart
autostart_DATA = com.endlessm.GoogleChromeInitialSetup.desktop

polkit_policydir = $(datadir)/polkit-1/actions
polkit_policy_in_files = com.endlessm.GoogleChromeHelper.system-helper.policy.in
polkit_policy_DATA = $(polkit_policy_in_files:.policy.in=.policy)

do_edit = sed -e 's|@pkglibexecdir[@]|$(pkglibexecdir)|g'

%.policy: %.policy.in Makefile
	$(AM_V_GEN) $(do_edit) $<> $@

com.endlessm.GoogleChromeInitialSetup.desktop: com.endlessm.GoogleChromeInitialSetup.desktop.in Makefile
	$(AM_V_GEN) $(do_edit) $<> $@

gsettings_SCHEMAS = com.endlessm.GoogleChromeInitialSetup.gschema.xml

@GSETTINGS_RULES@

EXTRA_DIST = \
	$(appdata_DATA) \
	$(desktop_DATA) \
	$(icon64_DATA) \
	$(autostart_DATA) \
	$(gsettings_SCHEMAS) \
	com.endlessm.GoogleChromeInitialSetup.desktop.in \
	$(polkit_policy_in_files) \
	$(NULL)

CLEANFILES = \
	com.endlessm.GoogleChromeInitialSetup.desktop \
	$(polkit_policy_DATA) \
	$(NULL)
