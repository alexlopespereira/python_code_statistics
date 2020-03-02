#!/bin/sh
USER=$1
TOKEN=$2
curl -u $USER:$TOKEN "https://api.github.com/user/repos?per_page=1000" | grep -e 'svn_url*' | cut -d \" -f 4 | xargs -L1 git clone