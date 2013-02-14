#!/bin/sh
url=10.64.27.27

echo will scp $1 to DropBear fedora box $url

scp $1 cloud-user@${url}:~/rpmbuild/SPECS


