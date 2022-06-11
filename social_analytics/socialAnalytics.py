#!/usr/bin/env python
# coding: utf-8

# In[31]:


import pandas as pd
import numpy as np
import seaborn as sns
import tweepy
import datetime
import xlsxwriter
import sys
import json
import re
import nltk
import spacy
import string
import os

info = {'STATUS':''}

class SocialAnalyst():
    def __init__(self):
        from RIAnalytics.settings import FILES_DIR, OUTPUT_DIR
        self.FILES_DIR = FILES_DIR
        self.OUTPUT_DIR = OUTPUT_DIR
        

    # Authentication keys from twitter
    # sending in filename or list
    def generateHtml(self,authKeys, Twitter_Handles_File, tweet_count):
        try:
            html_content = "<div class='col-12 p-4'>"
            consumer_key = authKeys[0]
            consumer_secret = authKeys[1]
            access_token = authKeys[2]
            access_token_secret = authKeys[3]
            info['STATUS'] = 'Credentials Loaded'
            # In[33]:

            # Creating the authentication object
            auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
            info['STATUS'] = 'Auth Loaded'
            # Setting your access token and secret
            auth.set_access_token(access_token, access_token_secret)
            info['STATUS'] = 'Access Token Set'
            # Creating the API object while passing in auth information

            api = tweepy.API(auth)
            info['STATUS'] = 'Api connected successfully'

            if type(Twitter_Handles_File) == list:
                keywordList = pd.DataFrame(Twitter_Handles_File)
                keywordList = keywordList.rename(columns={0: 'Twitter Handles'})
                content = keywordList['Twitter Handles']
            else:
                Isic_data = pd.read_excel(
                    os.path.join(self.FILES_DIR,Twitter_Handles_File), sheet_name='Twitter_Handles')
                content = Isic_data['Twitter Handles']

            info['STATUS'] = 'Obtained Content'

            tweets_competitors = []
            for i in range(0, len(content)):
                tweets_pwc_latest = []
                tmpTweets = tweepy.Cursor(
                    api.user_timeline, id=content[i], tweet_mode='extended').items(int(tweet_count))
                for tweet in tmpTweets:
                    tweets_pwc_latest.append(tweet)
                for each_json_tweet in tweets_pwc_latest:
                    tweets_competitors.append(each_json_tweet._json)

            info['STATUS'] = 'Processing Stage 1'

            tweets_table_competitors = []
            for each_dictionary in tweets_competitors:

                tweet_id = each_dictionary['id']
                tweet_text = each_dictionary['full_text']
                created_at = each_dictionary['created_at']
                company = each_dictionary['user']['name']
                tweets_table_competitors.append({'tweet_id': str(tweet_id),
                                                'tweet_text': str(tweet_text),
                                                'created_at': created_at,
                                                'company': str(company)
                                                })

                # print(tweets_table table)
                tweets_competitors = pd.DataFrame(tweets_table_competitors, columns=['tweet_id', 'tweet_text',
                                                                                    'created_at', 'company'])

            # In[37]:
            info['STATUS'] = 'Processing Stage 2'
            tweets_competitors['link'] = tweets_competitors['tweet_text'].str.extract(
                r'(https?:\/\/(?:www\.)?[-a-zA-Z0-9@:%._+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}[-a-zA-Z0-9()@:%_+.~#?&/=]*)', expand=True)
            tweets_competitors['created_at'] = pd.to_datetime(
                tweets_competitors['created_at']).dt.date
            final_tweets_competitors = tweets_competitors[tweets_competitors['tweet_text'].str.contains(
                "Sustainable|Poverty|Hunger|Health|Well-Being|Education|Gender Equality|Clean Water|Sanitation|Affordable Energy|Sustainability|Clean Energy|Economic Growth|Inequality|climate|Peace|Rural Development|Food Security|Nutrition|population|NSDS|National Sustainable Development Strategies|Women Empowerment|Green Economy|Employment|Human Settlements|Chemicals|Waste|Ocean|Biodiversity|Ecosystem|Forests|Desertification|Land Degradation|Drought|children|Inclusion|Carbon Emissions|Energy Efficiency|Water Scarcity|Pollution|Diversity|labour|Privacy|Community|Compensation|Lobbying|Inequalities|workplace")]
            final_tweets_competitors["keyword"] = final_tweets_competitors["tweet_text"].str.findall(
                "Sustainable|Poverty|Hunger|Health|Well-Being|Education|Gender Equality|Clean Water|Sanitation|Affordable Energy|Sustainability|Clean Energy|Economic Growth|Inequality|climate|Peace|Rural Development|Food Security|Nutrition|population|NSDS|National Sustainable Development Strategies|Women Empowerment|Green Economy|Employment|Human Settlements|Chemicals|Waste|Ocean|Biodiversity|Ecosystem|Forests|Desertification|Land Degradation|Drought|children|Inclusion|Carbon Emissions|Energy Efficiency|Water Scarcity|Pollution|Diversity|labour|Privacy|Community|Compensation|Lobbying|Inequalities|workplace", flags=re.IGNORECASE)
            final_tweets_competitors["Index"] = np.arange(
                start=1, stop=(final_tweets_competitors.shape[0])+1, step=1)
            if type(Twitter_Handles_File) != list:
                info['STATUS'] = 'Deleting Handles'
                try:
                    os.remove(os.path.join(self.FILES_DIR,Twitter_Handles_File))
                    os.remove(os.path.join(self.FILES_DIR,'Search_Terms.xlsx'))
                except:
                    pass
                info['STATUS'] = 'Done with file delete'
            # In[ ]:
            #final_tweets_competitors.to_csv(os.getcwd()+'\\Result_Files'+'Tweets_competitors_taxonomy.csv', index=False)
            html_content += '''<div class="col-sm-12 p-4 "> '''
            html_content += final_tweets_competitors.to_html()
            html_content += "</div>"
            html_content = html_content.replace('''<table border="1" class="dataframe">''', '''<table class="table small col-12" style="font-size:10px">''')
            html_content += "</div>"
            info['STATUS'] = 'QUIT'
            return final_tweets_competitors
        except Exception as Error:
             info['STATUS']= f" Exiting with Error {str(Error)}"  

