#!/bin/sh

curl -u alexlopespereira:b206a102b3b038aed0dd217bb4f0c5616bebf229 "https://api.github.com/user/repos?per_page=1000" | grep -e 'svn_url*' | cut -d \" -f 4 | xargs -L1 git clone