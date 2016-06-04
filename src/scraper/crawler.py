"""Crawls NaMo's website for speech analysis."""

import sys
from time import sleep

import requests as rq
from bs4 import BeautifulSoup

AGENT = """Mozilla/5.0 (Macintosh; Intel Mac OS X 10.11; rv:44.0) """ + \
        """Gecko/20100101 Firefox/44.0"""
NAMO_URL = "http://www.narendramodi.in/speeches/loadspeeche?page={}&language=hi"
DATA_FOLDER = "../../data/"
SLEEP_TIME = 5
STATUS_OK = 200
HTTP_CONTENT_LEN_THRESHOLD = 100


class SpeechScraper:
    """The speech scraper."""

    def __init__(self, url, path):
        """Initialize the seeking alpha URL and output path.

        Args:
        url - NaMo's root URL to scrape
        path - location where speeches are to be stored
        """
        self.url = url
        self.path = path

    def scrape(self):
        """Run the scraper."""
        page = 1
        counter = 1
        while True:
            req_url = self.url.format(page)
            resp = rq.get(req_url, headers={'User-Agent': AGENT})
            if resp.status_code != STATUS_OK:
                print "Error Code : " + str(resp.status_code)
                print "URL : " + self.url
                sys.exit(1)
            soup = BeautifulSoup(resp.content, 'lxml')
            speeches = soup.find_all('a', class_="left_class")
            if resp.headers['Content-Length'] < HTTP_CONTENT_LEN_THRESHOLD:
                break
            for i, speech in enumerate(speeches):
                if i % 2 == 0:
                    speech_url = speech.get('href')
                    speech_title = speech.get_text()
                    speech_resp = rq.get(speech_url,
                                         headers={'User-Agent': AGENT})
                    if speech_resp.status_code != 200:
                        print "Error Code : ", str(resp.status_code)
                        print "Speech URL : ", self.url
                        print "Speech title : ", speech_title
                        continue
                    speech_soup = BeautifulSoup(speech_resp.content, 'lxml')
                    speech_contents = speech_soup.find_all('article',
                                                           class_="articleBody")
                    speech_text = ''
                    for speech_content in speech_contents:
                        for paragraph in speech_content.find_all('p'):
                            speech_text += paragraph.text + '\n'
                    """
                    print 'Writing speech', speech_title
                    print 'Writing speech text', speech_text
                    """
                    self.writeToFile(self.path, str(counter), speech_text)
                    print 'Processed', counter, 'files'
                    counter += 1
            page += 1
            sleep(3)

    def writeToFile(self, path, filename, text):
        """Write scraped speech to a file.

        Args:
        path - location of the file to be put in
        filename - name of file where speech is to be written
        text - content of the speech
        """
        text = text.encode('utf8')
        with open(''.join([path, filename + '.txt']), 'w') as f:
            f.write(text)

if __name__ == '__main__':
    scraper = SpeechScraper(NAMO_URL, DATA_FOLDER)
    scraper.scrape()
