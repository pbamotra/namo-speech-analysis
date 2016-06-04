"""Constants used in the code."""

import os

DATA_FOLDER = "./data"
SPEECH_FOLDER = os.path.join(DATA_FOLDER, "speeches")
MISC_FOLDER = os.path.join(DATA_FOLDER, "misc")
ASCII_LIMIT = 128
N_TOP_WORDS = 50
N_SPEECHES = 500
N_TOPICS = 10
AGENT = """Mozilla/5.0 (Macintosh; Intel Mac OS X 10.11; rv:44.0) """ + \
        """Gecko/20100101 Firefox/44.0"""
NAMO_URL = "http://www.narendramodi.in/speeches/loadspeeche?page={}&language=hi"
SLEEP_TIME = 5
STATUS_OK = 200
HTTP_CONTENT_LEN_THRESHOLD = 100
