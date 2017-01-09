dist_bin_SCRIPTS = eos-google-chrome

dist_pkglibexec_SCRIPTS = eos-google-chrome-installer

dist_pkgdata_DATA = config.py

config.py: config.py.in Makefile
	$(AM_V_GEN) sed -e "s|\@pkglibexecdir\@|$(pkglibexecdir)|" $<> $@
