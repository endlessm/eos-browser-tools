AC_PREREQ([2.63])
AC_INIT([eos-google-chrome-helper], [1.0.0], [mario@endlessm.com])
AC_CONFIG_MACRO_DIR([m4])
AC_CONFIG_HEADERS([config.h])

AM_INIT_AUTOMAKE([1.11 -Wno-portability foreign no-define tar-ustar no-dist-gzip dist-xz])
AM_MAINTAINER_MODE([enable])
AM_SILENT_RULES([yes])

PKG_CHECK_MODULES([glib], [glib-2.0])
GLIB_GSETTINGS

AC_CONFIG_FILES([
Makefile
data/Makefile
src/Makefile
])
AC_OUTPUT

echo "
    eos-google-chrome-helper $VERSION
"
