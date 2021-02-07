FROM python:3.7

RUN apt-get update && apt-get -y install cron

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

ADD docker/ssh /root/.ssh/
ADD scrape.py scrape.py

ADD scrape.sh /scrape.sh
RUN chmod +x /scrape.sh

ADD docker/cron.sh /usr/bin/cron.sh
RUN chmod +x /usr/bin/cron.sh

ADD docker/crontab /etc/cron.d/cron-jobs
RUN chmod 0644 /etc/cron.d/cron-jobs

RUN touch /var/log/cron.log

ENTRYPOINT ["/bin/sh", "/usr/bin/cron.sh"]
#ENTRYPOINT ["/bin/sh", "/scrape.sh"]
