import argparse
import os
import shutil
import time
from datetime import datetime
from zipfile import ZipFile, BadZipFile

from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry

import requests
from bs4 import BeautifulSoup


def requests_retry_session(
    retries=3, backoff_factor=10, status_forcelist=(500, 502, 504), session=None,
):
    session = session or requests.Session()
    retry = Retry(
        total=retries,
        read=retries,
        connect=retries,
        backoff_factor=backoff_factor,
        status_forcelist=status_forcelist,
    )
    adapter = HTTPAdapter(max_retries=retry)
    session.mount("http://", adapter)
    session.mount("https://", adapter)
    return session


def ensure_exists(path):
    if not os.path.exists(path):
        os.makedirs(path)
    return path


def scrape():
    toc = requests_retry_session().get("https://www.gesetze-im-internet.de/gii-toc.xml")
    with open(TOC_PATH, "wb") as f:
        f.write(toc.content)

    soup = BeautifulSoup(toc.text, "lxml-xml")
    errors = []

    for item in list(soup.find_all("item"))[:11]:
        link = item.link.get_text()
        print("Loading", link)

        link_parts = link.split("/")
        assert link_parts[-1] == "xml.zip"
        item_id = link_parts[-2]

        r = requests_retry_session().get(link)
        zip_path = TEMP_PATH + "temp.zip"
        with open(zip_path, "wb") as f:
            f.write(r.content)
        try:
            with ZipFile(zip_path) as f:
                f.extractall(ITEMS_PATH + item_id)
        except BadZipFile:
            with open(zip_path, "rb") as f:
                contents = f.read()
            if b"<title>404 Not Found</title>" in contents:
                errors.append(item_id)
            else:
                raise
        os.remove(zip_path)
        time.sleep(1)

    with open("data/not_found.txt", "w") as f:
        for e in errors:
            f.write(e + "\n")

    shutil.rmtree(TEMP_PATH)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("data_repo_path", type=str)
    parser.add_argument("datetime", type=str)
    args = parser.parse_args()

    BASE_PATH = os.path.join(args.data_repo_path, "data/")
    LOG_PATH = os.path.join(BASE_PATH, "log.md")
    TOC_PATH = os.path.join(BASE_PATH, "toc.xml")
    NOT_FOUND_PATH = os.path.join(BASE_PATH, "not_found.txt")
    ITEMS_PATH = os.path.join(BASE_PATH, "items/")
    TEMP_PATH = os.path.join(BASE_PATH, "temp/")

    if os.path.exists(TOC_PATH):
        os.remove(TOC_PATH)
    if os.path.exists(NOT_FOUND_PATH):
        os.remove(NOT_FOUND_PATH)
    shutil.rmtree(ITEMS_PATH, ignore_errors=True)
    shutil.rmtree(TEMP_PATH, ignore_errors=True)

    ensure_exists(BASE_PATH)
    ensure_exists(ITEMS_PATH)
    ensure_exists(TEMP_PATH)
    scrape()

    with open(LOG_PATH, "a+") as file:
        file.writelines(f"- {args.datetime}\n")
    print("done")
