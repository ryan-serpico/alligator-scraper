import os
from bs4 import BeautifulSoup
import requests
from get_article import getArticle
from html_builder import buildHTML

# Make a folder for the articles to be stored in.
os.makedirs('articles', exist_ok=True)


# Start page
url = 'https://www.alligator.org/search/?f=html&q=.&sd=desc&l=25&t=article&nsa=eedition'


def getLinksOnPage(url):
    l = []
    fizz = 0
    articleList = soup.find('div', class_='results-container')
    for a in articleList.find_all('a', class_='tnt-asset-link', href=True):
        if fizz == 0:
            l.append('https://alligator.org' + a['href'])
            fizz = + 1
        else:
            fizz = 0
    return l


while True:
    r = requests.get(url)
    html_doc = r.text
    soup = BeautifulSoup(html_doc, 'html.parser')

    links = getLinksOnPage(url)

    for link in links:
        linkContent = list(getArticle(link))
        headline = linkContent[0]
        byline = linkContent[1]
        publishDate = linkContent[2]
        category = linkContent[3]
        articleBody = linkContent[4]
        photographerByline = linkContent[5]
        photoCaption = linkContent[6]
        tagsList = linkContent[7]
        articleDirectory = linkContent[8]
        image_name = linkContent[9]
        buildHTML(headline, byline, publishDate, category, articleBody,
                  photographerByline, photoCaption, tagsList, articleDirectory, image_name)

    prevLink = soup.select('.next a')[0]
    url = 'https://alligator.org' + prevLink.get('href')
