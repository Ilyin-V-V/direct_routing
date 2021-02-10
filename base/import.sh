#!/bin/bash
base="base"
user="postgres"
password=""

if [ -z "$1" ]; then echo "Not parameter table.sql => exit"; fi;
/usr/bin/sudo -u $user /usr/bin/psql -U $user -d $base < ./$1
