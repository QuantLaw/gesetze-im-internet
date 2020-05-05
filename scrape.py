import argparse
import os
import shutil
from multiprocessing.pool import Pool
from zipfile import ZipFile, BadZipFile

import requests
from bs4 import BeautifulSoup
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry


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


def handle_links(link):
    error = None
    print("Loading", link)

    link_parts = link.split("/")
    assert link_parts[-1] == "xml.zip"
    item_id = link_parts[-2]

    r = requests_retry_session().get(link)
    zip_path = TEMP_PATH + item_id + ".zip"
    with open(zip_path, "wb") as f:
        f.write(r.content)
    try:
        with ZipFile(zip_path) as f:
            f.extractall(ITEMS_PATH + item_id)
    except BadZipFile:
        with open(zip_path, "rb") as f:
            contents = f.read()
        if b"<title>404 Not Found</title>" in contents:
            error = item_id
        else:
            raise
    os.remove(zip_path)
    return error


def scrape():
    toc = requests_retry_session().get("https://www.gesetze-im-internet.de/gii-toc.xml")
    with open(TOC_PATH, "wb") as f:
        f.write(toc.content)

    soup = BeautifulSoup(toc.text, "lxml-xml")

    links = [item.link.get_text() for item in list(soup.find_all("item"))]

    with Pool(2) as p:
        errors = p.map(handle_links, links)
    errors = [e for e in errors if e is not None]

    with open(NOT_FOUND_PATH, "w") as f:
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
