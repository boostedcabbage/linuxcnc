#!/bin/sh -ex
cd src
./autogen.sh
./configure --with-realtime=uspace --disable-check-runtime-deps --enable-build-documentation
make -O -j$(getconf _NPROCESSORS_ONLN) manpages V=1
make -O -j$(getconf _NPROCESSORS_ONLN) translateddocs V=1
make -O -j$(getconf _NPROCESSORS_ONLN) default pycheck V=1
../scripts/rip-environment runtests
