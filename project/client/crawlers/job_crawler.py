import re
import requests
from lxml import html

import pymongo
client = pymongo.MongoClient("127.0.0.1", 27017)
db = client.jobs


def scrap_jobpages():
    url = 'http://jobsearch.naukri.com/top-skill-jobs'
    response = requests.get(url)
    tree = html.fromstring(response.text)
    joburls = tree.xpath("//div[@class='multiColumn colCount_four']/a")

    for url in joburls:
        db.jobpages.insert({'label': url.attrib['title'], 'url': url.attrib['href']})


if __name__=="__main__":
    # scrap_jobpages()
