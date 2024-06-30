import logging
import time
import urllib

from bs4 import BeautifulSoup


def get_webpage(links_url):
    try:
        links_header = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) '
                                      'AppleWebKit/537.36 (KHTML, like Gecko) '
                                      'Chrome/123.0.0.0 Safari/537.36',
                        'Accept': '*/*',  # 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                        'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
                        'Accept-Encoding': 'none',
                        'Accept-Language': 'en-US,en;q=0.9',
                        'Connection': 'keep-alive',
                        }
        links_req = urllib.request.Request(url=links_url, headers=links_header)
        try:
            links_page = urllib.request.urlopen(links_req, timeout=90).read()
            # print(links_page)
        except urllib.error.HTTPError:
            logging.exception(f"Error when getting webpage from {links_url}")
            time.sleep(120)
            logging.info("Retrying......")
            try:
                links_page = urllib.request.urlopen(links_req, timeout=90).read()
            except:
                logging.warning("Retry Failed!!!")
                return
        links_soup = BeautifulSoup(links_page.decode("utf-8", "html.parser"))
        return links_soup
    except:
        logging.exception(f"Error when getting webpage code for {links_url}")