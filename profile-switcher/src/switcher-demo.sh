#!/bin/sh

usage()
{
    echo "`basename $0` [options]"
    echo "options are:"
    echo "--list <subject>             list available profile(s)"
    echo "--switch <subject> <profile> switch <subject> to use <profile>"
    echo "--status <subject>           print out current profile status"
}

usage
