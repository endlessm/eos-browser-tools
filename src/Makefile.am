bin_SCRIPTS = eos-google-chrome

dist_pkgdata_SCRIPTS = \
	eos-google-chrome.py \
	eos-google-chrome-installer.py \
	eos-google-chrome-system-helper.py \
	$(NULL)

pkgdata_DATA = \
        config.py \
        $(NULL)

do_edit = sed \
	-e "s|\@localstatedir\@|$(localstatedir)|" \
	-e "s|\@pkgdatadir\@|$(pkgdatadir)|" \
	-e "s|\@PACKAGE\@|$(PACKAGE)|"

eos-google-chrome: eos-google-chrome.in Makefile
	$(AM_V_GEN) $(do_edit) $<> $@

config.py: config.py.in Makefile
	$(AM_V_GEN) $(do_edit) $<> $@

EXTRA_DIST = \
        config.py.in \
        eos-google-chrome.in \
        $(NULL)

CLEANFILES = \
        config.py \
        eos-google-chrome \
        $(NULL)
