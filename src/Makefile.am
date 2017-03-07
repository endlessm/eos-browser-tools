bin_SCRIPTS = eos-google-chrome

chromehelperdir = $(datadir)/$(CHROME_HELPER_NAME)

dist_chromehelper_SCRIPTS = \
	eos-google-chrome.py \
	eos-google-chrome-installer.py \
	eos-google-chrome-system-helper.py \
	$(NULL)

chromehelper_DATA = \
        config.py \
        $(NULL)

do_edit = sed \
	-e "s|\@chromehelpername\@|$(CHROME_HELPER_NAME)|" \
	-e "s|\@datadir\@|$(datadir)|" \
	-e "s|\@localstatedir\@|$(localstatedir)|" \
	-e "s|\@sysconfdir\@|$(sysconfdir)|"

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
