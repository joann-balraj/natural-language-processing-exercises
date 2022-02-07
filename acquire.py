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


# Create a function to read all articles and create a dictionary containing the title and content of each article from Code Up blogs

def parse_article(article):
    
    #title
    title  = article.select('.entry-title')[0].text
    
    #content
    content = article.select('.et_pb_module.et_pb_post_content.et_pb_post_content_0_tb_body')[0].text.strip()
    
    return {'title': title, 'content': content}



# Create a function to read all articles and create a dictionary containing the title and content of each article

def parse_news_article(article, category):
    
    #title
    title  = article.find('span',itemprop="headline").text
    
    #author
    author = article.find('span', 'author').text
    
    #content
    content = article.find('div',itemprop="articleBody").text.strip()
    
    #category
    category = category
    
    
    
    return {'title': title, 'author':author, 'content': content,'category': category}


# Create a function that takes a list of categories for inshorts website and parses the articles from them and creates a dictionary with 
# title, author, and  content of each article

def get_news_articles(categories):

    filename = "news.csv"

    if os.path.isfile(filename):

       return pd.read_csv(filename)

    else:

        url = 'https://inshorts.com/en/read/'
        
        for category in categories:
            
            if category == categories[0]:
            
                response = requests.get(url+category, headers={'user-agent': 'Codeup DS Germain'})
                soup = BeautifulSoup(response.text)
            
                #Get the articles from the web page
                articles = soup.select('.news-card.z-depth-1')
            
                article = articles[0]
            
                df = pd.DataFrame([parse_news_article(article, category) for article in articles])   
                
            
            else: 
                
                response = requests.get(url+category, headers={'user-agent': 'Codeup DS Germain'})
                soup = BeautifulSoup(response.text)
            
                #Get the articles from the web page
                articles = soup.select('.news-card.z-depth-1')
            
                article = articles[0]  
                
                df = df.append(pd.DataFrame([parse_news_article(article, category) for article in articles]), ignore_index=True)

                df.to_csv(r'news.csv', index=False)
            
        return df