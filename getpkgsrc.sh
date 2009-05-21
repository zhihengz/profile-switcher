#!/bin/sh
#
# this script will be called by pkgutils to get package source in
# the way the project specific
#
# input
# $1 - application (package) name
# $2 - application (package) vesion
appname=$1
appver=$2

app=${appname}-${appver}

cd profile-switcher && make clean && cd .. &&
cp -r profile-switcher build/ && cd build && mv profile-switcher $app &&
tar -zcvf $app.tar.gz $app/ && cd ..
