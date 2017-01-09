dist_bin_SCRIPTS = eos-google-chrome

dist_pkglibexec_SCRIPTS = eos-google-chrome-installer

nobase_pkgdata_DATA = \
        config.py \
        $(NULL)

config.py: config.py.in Makefile
	$(AM_V_GEN) sed -e "s|\@pkglibexecdir\@|$(pkglibexecdir)|" $<> $@

EXTRA_DIST = \
        config.py.in \
        $(NULL)

CLEANFILES = \
        config.py \
        $(NULL)
