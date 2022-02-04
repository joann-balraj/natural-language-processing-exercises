# Data Preparation Exercises



import unicodedata
import re
import json

import nltk
from nltk.tokenize.toktok import ToktokTokenizer
from nltk.corpus import stopwords

import pandas as pd

import acquire


def basic_clean(string):
    
    # This function does basic cleaning and prepping of a string
    
    # Lowercase all text in string
    prepped_string = string.lower()   
    
    # Normalize unicode letters
    prepped_string = unicodedata.normalize('NFKD', prepped_string)\
    .encode('ascii', 'ignore')\
    .decode('utf-8', 'ignore') 
    
    # remove anything that is not a through z, a number, a single quote, or whitespace
    prepped_string = re.sub(r"[^a-z0-9'\s]", '', prepped_string)

    return prepped_string
    

def tokenize(string):
    
    # This function takes in a string and tokenizes all the words in the string
    
    # Create tokenizer
    tokenizer = nltk.tokenize.ToktokTokenizer()
    
    return (tokenizer.tokenize(string, return_str=True))

def stem(text):
    
    # This function accepts some text and returns the text after applying stemming to all the words
    
    # Create the nltk stemmer object, then use it
    ps = nltk.porter.PorterStemmer()
    
    stems = [ps.stem(word) for word in text.split()]
    text_stemmed = ' '.join(stems)
    
    return text_stemmed


def lemmatize(text):
    
    # This function accepts some text and returns the text after applying lemmatization to each word
    
    # Create the nltk lemmatizer object, then use it
    wnl = nltk.stem.WordNetLemmatizer()

    # Use the lemmatizer on each word in the list of words we created
    lemmas = [wnl.lemmatize(word) for word in text.split()]
    text_lemmatized = ' '.join(lemmas)

    return text_lemmatized        

def remove_stopwords(string, extra_words = [], exclude_words = []):
    '''
    This function takes in a string, optional extra_words and exclude_words parameters
    with default empty lists and returns a string.
    '''
    # Create stopword_list
    stopword_list = stopwords.words('english')
    
    # Remove 'exclude_words' from stopword_list to keep these in my text
    stopword_list = set(stopword_list) - set(exclude_words)
    
    # Add in 'extra_words' to stopword_list
    stopword_list = stopword_list.union(set(extra_words))

    # Split words in string
    words = string.split()
    
    # Create a list of words from my string with stopwords removed and assign to variable
    filtered_words = [word for word in words if word not in stopword_list]
    
    # Join words in the list back into strings and assign to a variable
    string_without_stopwords = ' '.join(filtered_words)
    
    return string_without_stopwords

def prep_article_data(df, column, extra_words=[], exclude_words=[]):
    '''
    This function take in a df and the string name for a text column with 
    option to pass lists for extra_words and exclude_words and
    returns a df with the text article title, original text, stemmed text,
    lemmatized text, cleaned, tokenized, & lemmatized text with stopwords removed.
    '''
    df['clean'] = df[column].apply(basic_clean)\
                            .apply(tokenize)\
                            .apply(remove_stopwords, 
                                   extra_words=extra_words, 
                                   exclude_words=exclude_words)
    
    df['stemmed'] = df[column].apply(basic_clean)\
                            .apply(tokenize)\
                            .apply(stem)\
                            .apply(remove_stopwords, 
                                   extra_words=extra_words, 
                                   exclude_words=exclude_words)
    
    df['lemmatized'] = df[column].apply(basic_clean)\
                            .apply(tokenize)\
                            .apply(lemmatize)\
                            .apply(remove_stopwords, 
                                   extra_words=extra_words, 
                                   exclude_words=exclude_words)
    
    return df[['title', column,'clean', 'stemmed', 'lemmatized']]    