from bs4 import BeautifulSoup
import requests
from dateutil import parser
import os
from urllib.parse import urlparse


def getArticle(url):
    r = requests.get(url)

    html_doc = r.text

    soup = BeautifulSoup(html_doc, 'html.parser')

    def getByline():
        try:
            byline = soup.find(
                'span', itemprop='author').text.strip().split(',')[0]
            return byline
        except AttributeError:
            pass

    def getPublishDate():
        publishDate = parser.parse(
            soup.find('time', class_='tnt-date')['datetime']).strftime('%Y-%m-%d')
        return publishDate

    def getPhotoCaption():
        try:
            photoCaption = soup.find(
                'span', class_='caption-text').text.strip()
            return photoCaption
        except:
            return None

    def getHeadline():
        headline = soup.find('h1').text.strip()
        return headline

    def getArticleText():
        p_list = []
        t = soup.find('div', itemprop='articleBody')
        for i in t.find_all('p'):
            p_list.append(i)
        return p_list

    def getTags():
        article_tags_list = []
        article_tags = soup.select('.asset-tags a')
        for i in range(0, len(article_tags)):
            article_tags_list.append(article_tags[i].getText())
        return article_tags_list

    def getPhotographerByline():
        try:
            fizz = soup.find(
                'span', class_='tnt-byline').text.strip().split('/')[0]
            return fizz
        except AttributeError:
            pass

    def getPhoto(directory):
        photoSrc = soup.find_all('meta', itemprop='url')[-1]['content']
        photoAlt = soup.select('.image img')[0].get('alt')
        r = requests.get(photoSrc)
        imageFile = open(os.path.join(directory, os.path.basename(
            photoAlt.replace(' ', '-').lower() + '.jpg')), 'wb')
        for chunk in r.iter_content(100000):
            imageFile.write(chunk)
        image_name = photoAlt.replace(' ', '-').lower() + '.jpg'
        return photoSrc, image_name

    def createDir(headline):
        dirName = headline.replace(' ', '-').lower()
        fullDir = 'articles/' + dirName
        foo = dirName + '/image'
        os.makedirs('articles/' + foo, exist_ok=True)
        fizz = 'articles/' + foo
        return fizz, fullDir

    def getCategory():
        parsed_url = urlparse(url).path.split('/')
        category = str(parsed_url[1])
        return category

    headline = getHeadline()
    createDir(headline)
    imageDirectory = createDir(headline)[0]
    image_name = getPhoto(imageDirectory)[1]
    articleDirectory = createDir(headline)[1]
    articleBody = getArticleText()
    tagsList = getTags()
    photographerByline = getPhotographerByline()
    category = getCategory()
    photoCaption = getPhotoCaption()
    publishDate = getPublishDate()
    byline = getByline()

    return headline, byline, publishDate, category, articleBody, photographerByline, photoCaption, tagsList, articleDirectory, image_name
