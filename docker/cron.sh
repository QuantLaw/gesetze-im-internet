#!/usr/bin bash

cp /run/secrets/gii_scraper_github_key /root/.ssh/key
echo '\n' >> /root/.ssh/key
chmod 600 /root/.ssh/key
ssh-agent sh -c 'ssh-add /root/.ssh/key'


printenv | cat - /etc/cron.d/cron-jobs > ~/crontab.tmp \
    && mv ~/crontab.tmp /etc/cron.d/cron-jobs

chmod 644 /etc/cron.d/cron-jobs

tail -f /var/log/cron.log &

cron -f
