import requests
from bs4 import BeautifulSoup
import pandas as pd
import os

def get_links():
    link_list = []
    response = requests.get('https://codeup.com/blog/', headers={'user-agent': 'Codeup DS Hopper'})
    soup = BeautifulSoup(response.text)
    articles = soup.find_all('h2', class_ = 'entry-title')
    for article in articles:
        link = article.a.attrs['href']
        link_list.append(link)
    return link_list



def get_link(article):
    link = article.a.attrs['href']
    return link




def get_blog_articles():
    filename = 'codeup_blog_articles.json'
    if os.path.isfile(filename):
        return pd.read_csv(filename)
    
    else:
        article_list=[]
        response = requests.get('https://codeup.com/blog/', headers={'user-agent': 'Codeup DS Hopper'})
        soup = BeautifulSoup(response.text)
        articles = soup.find_all('h2', class_ = 'entry-title')
        for article in articles:
            title = article.text
            link = get_link(article)
            article_response = requests.get(link, headers={'user-agent': 'Codeup DS Hopper'})
            article_soup = BeautifulSoup(article_response.text)
            article_content = [p.text for p in article_soup.find_all('p')]

            article = {
                'title': title, 'article_content': article_content
            }
            article_list.append(article)
        df = pd.DataFrame(article_list)
        df.to_json('codeup_blog_articles.json')
    return df


# Great, this function is working now