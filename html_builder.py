from jinja2 import Environment, FileSystemLoader
import os


def buildHTML(headline, byline, publishDate, category, articleBody, photographerByline, photoCaption, tagsList, articleDirectory, image_name):

    env = Environment(loader=FileSystemLoader('templates'))
    template = env.get_template('template.html')

    templateOutput = template.render(article_text=articleBody, article_headline=headline, article_date=publishDate, reporter_byline=byline,
                                     article_category=category, article_tags_list=tagsList, image_name=image_name, photographer_byline=photographerByline)

    final_file = open(os.path.join(
        articleDirectory, os.path.basename(headline.replace(' ', '-') + '.html')), 'w')
    final_file.write(templateOutput)
    final_file.close()
