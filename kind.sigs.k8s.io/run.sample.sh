#!/usr/bin/env bash

#./deploy.py \
#  --kind-name=ada-oraclu-arm2 \
#  --hostPath=$HOME/github.com/asta-s-eu/teams/scraping-dev/scraping-kleinanzeigen.de/tests/KLEINANZEIGEN_DE_CONFIG_FOLDER \
#  --containerPath=/mnt/github.com/asta-s-eu/teams/scraping-dev/scraping-kleinanzeigen/KLEINANZEIGEN_DE_CONFIG_FOLDER \
#  --apiServerPort=6444


./deploy.py \
  --hostPath=$HOME/github.com/asta-s-eu/teams/scraping-dev/scraping-kleinanzeigen.de/tests/KLEINANZEIGEN_DE_CONFIG_FOLDER \
  --containerPath=/mnt/github.com/asta-s-eu/teams/scraping-dev/scraping-kleinanzeigen/KLEINANZEIGEN_DE_CONFIG_FOLDER \
  --apiServerPort=6443
