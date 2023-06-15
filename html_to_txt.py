from bs4 import BeautifulSoup
import requests

def get_text(url):
    return BeautifulSoup(requests.get(url).text,features="lxml").get_text()