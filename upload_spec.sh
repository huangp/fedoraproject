#!/bin/sh

echo will scp $1 to DropBear fedora box

scp $1 cloud-user@10.64.27.27:~/rpmbuild/SPECS


