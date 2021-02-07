#!/bin/sh
set -e

rm -rf /data_branch

git clone \
  --branch data \
  --single-branch \
  --depth 1 \
  -q \
  git@github.com:QuantLaw/gesetze-im-internet.git \
  /data_branch

SCRAPE_DATETIME=$(date +'%Y-%m-%dT%T')
SCRAPE_DATE=$(date +'%Y-%m-%d')

git config --global user.email "scraper@github.com"
git config --global user.name "Scraper"

cd /
python scrape.py /data_branch $SCRAPE_DATETIME

cd /data_branch
git add .
git commit -m "scrape $SCRAPE_DATETIME" --date $SCRAPE_DATETIME
git tag $SCRAPE_DATE
git push
git push git@github.com:QuantLaw/gesetze-im-internet.git $SCRAPE_DATE -f
