#!/usr/bin/env python
# coding: utf-8

# In[1]:


import os
import pandas as pd
import PyPDF2
#import pikepdf
import time
import nltk
import pdfplumber
import re
import string
from string import digits
import matplotlib.pyplot as plt
from PIL import Image
import numpy as np
from wordcloud import WordCloud, STOPWORDS
import seaborn as sns
from sklearn.feature_extraction.text import CountVectorizer
import operator
# In[ ]:


# Lists all the PDF files in subdirectory
def listFiles(dir):
    # return [os.path.join(r, n) for r, _, f in os.walk(dir) for n in f]
    r = []
    for root, dirs, files in os.walk(dir):
        for name in files:
            if name[-4:] == ".pdf":
                r.append(os.path.join(root, name))
    return r


os.chdir(os.path.dirname(os.path.abspath("__file__")))


def listtxtFiles(dir):
    # return [os.path.join(r, n) for r, _, f in os.walk(dir) for n in f]
    r = []
    for root, dirs, files in os.walk(dir):
        for name in files:
            if name[-4:] == ".txt":
                r.append(os.path.join(root, name))
    return r


def clean_text(text):
    text = re.sub('\[.*?\]', '', text)
    text = re.sub('https?://\S+|www\.\S+', '', text)
    text = re.sub('<.*?>+\\/-', '', text)
    text = re.sub('[%s]' % re.escape(string.punctuation), '', text)
    text = re.sub('\n', '', text)
    text = re.sub('\w*\d\w*', '', text)
    return text


# In[ ]:
def startPrg(ExcelFileName):
    print("Start Time: " + time.strftime("%H:%M:%S", time.localtime()))
    batchstart = time.time()
    PDFfiles = listFiles(os.getcwd()+"\\input_PDFs")
    list_searchKey = []
    list_count = []
    list_sentences = []
    appended_data = []
    for i in range(len(PDFfiles)):
        pdf = pdfplumber.open(PDFfiles[i], password="")
        with open(PDFfiles[i][:len(PDFfiles[i])-4]+".txt", 'w', encoding='utf-8') as txt_file:
            for j in range(len(pdf.pages)):
                page = pdf.pages[j]
                txt = page.extract_text()
                txt_file.write(str(txt))
            pdf.close()
            txt_file.close()
    print("End Time: " + time.strftime("%H:%M:%S", time.localtime()))
    batchend = time.time()
    batchtime_taken = round(batchend - batchstart)/60
    print('[Info] Batch Completed in ', batchtime_taken, "Minutes")

    txtfiles = listtxtFiles(os.getcwd())

    with open(os.getcwd()+"\\input_PDFs\\"+'output.txt', 'w') as outfile:
        for fname in txtfiles[1:]:
            with open(fname, errors="ignore") as infile:
                outfile.write(infile.read())

    # In[ ]:

    # In[ ]:

    # In[ ]:

    word_list_without_replace_words = []

    df_replace_words = pd.read_excel(os.getcwd(
    )+"\\input_Excel\\"+ExcelFileName, sheet_name="Words that we replace in doc")

    #print (df_replace_words)

    replace_from_list = []
    replace_to_list = []

    for i, j in df_replace_words.iterrows():
        replace_from_list.append(j["Words from transcripts"].strip())
        replace_to_list.append(j["Converted to (in transcripts)"].strip())

    #print (len(replace_from_list),len(replace_to_list))

    with open(os.getcwd()+"\\input_PDFs\\"+"output.txt", 'r') as f:
        for line in f:
            for word in line.split():
                if(word.strip() in replace_from_list):
                    index_of_word_in_replace_from_list = replace_from_list.index(
                        word.strip())
                    #print (word)
                    word = replace_to_list[index_of_word_in_replace_from_list]
                    #print (word)
                    word_list_without_replace_words.append(word)
                else:
                    word_list_without_replace_words.append(word)

    #print (len(word_list_without_replace_words))

    # In[ ]:

    df_stop_words = pd.read_excel(
        os.getcwd()+"\\input_Excel\\"+ExcelFileName, sheet_name="Stop Words")

    # print(df_stop_words)

    stop_word_list = []

    for i, j in df_stop_words.iterrows():
        stop_word_list.append(j["Stop Words"].lower().strip())

    #print (stop_word_list, len(stop_word_list))

    #text = open ("output.txt").read()
    word_list_without_replace_words_and_stop_words = []

    for word in word_list_without_replace_words:
        # print(word)
        word = clean_text(word)
        if (word.lower().strip() not in stop_word_list):
            word_list_without_replace_words_and_stop_words.append(word.strip())

    # print (len(word_list_without_stop_words)

    # In[ ]:

    df_analysis_words = pd.read_excel(
        os.getcwd()+"\\input_Excel\\"+ExcelFileName, sheet_name="Keyword analysis")

    #print (df_analysis_words)

    combined_word_list = []

    for i, j in df_analysis_words.iterrows():
        one_list = []
        keyword = j["Word"].strip()
        one_list.append(keyword)
        for word_index in range(100):
            word_str = "Word " + str(word_index)
            if (str(j[word_str]) != "nan"):
                print(j[word_str])
                word = j[word_str].strip()
                one_list.append(word.lower())
        #print (one_list)
        combined_word_list.append(one_list)

    #print (len(combined_word_list))

    final_word_list = []

    for w in word_list_without_replace_words_and_stop_words:
        isOccured = False
        for each_list in combined_word_list:
            if (w in each_list):
                isOccured = True
                #print (w, each_list[0])
                final_word_list.append(each_list[0])
        if (isOccured == False):
            final_word_list.append(w)

    #print (len(final_word_list))

    # In[ ]:

    final_str = ""

    for f_w in final_word_list:
        final_str += f_w
        final_str += " "

    #clean_list=["fiscal", "million", "quarter", "growth", "highlight", "expect", "strong","Foods","core","Food","Free","Flavor","TYSON","operating income","forward","forward statement","include","year","item","Retail","result","investment","forward statement","looking","share","source","data","Total","Company","Cost","New","performance","Brands","EBITDA","customer","impact","including","portfolio","business","cash","flow","Revenue","Global","Products","Adjusted EBITDA","Consumer","Net","Presentation","CAGNY","GAAP","million","Note","Volume","Investor","Growth","Sale","Sales","Brand","market","product"]
    stopwords = set(STOPWORDS)
    # stopwords.update(clean_list)

    # In[ ]:

    cloud = WordCloud(background_color="white", max_words=20,
                      stopwords=stopwords).generate(final_str)

    # In[ ]:

    # plt.imshow(cloud)
    # plt.axis('off')
    # plt.show()

    # In[ ]:

    cloud.to_file(
        os.getcwd()+"\\Text_Extractor_App\\static\\resultFiles\\unigram.jpg")

    # In[ ]:

    lst = []
    for word in final_word_list:
        if(word not in stopwords):
            lst.append(word)
    unique_words = set(lst)

    freq = []
    for words in unique_words:
        if(len(words) > 1):
            freq.append((words, lst.count(words)))

    df = pd.DataFrame(freq, columns=["word", "frequency"])
    unigram = df.sort_values(by=['frequency'], ascending=False)

    # In[ ]:

    # sort.to_excel("Unigram.xlsx",sheet_name='unigram')

    # In[ ]:

    ax = sns.barplot(x="frequency", y="word",
                     data=unigram.iloc[:10], palette="rainbow")

    # In[ ]:

    bigrams_list = list(nltk.bigrams(final_word_list))
    # print(bigrams_list)
    dictionary2 = [' '.join(tup) for tup in bigrams_list]

    # In[ ]:

    count_vector = CountVectorizer(ngram_range=(2, 2))
    data = count_vector.fit_transform(dictionary2)
    sum_words = data.sum(axis=0)
    words_freq = [(word, sum_words[0, idx])
                  for word, idx in count_vector.vocabulary_.items()]

    # In[ ]:

    words_dict = dict(words_freq)
    wordCloud = WordCloud(background_color="white",
                          max_words=20, stopwords=stopwords)
    wordCloud.generate_from_frequencies(words_dict)
    # plt.imshow(wordCloud)
    # plt.axis("off")
    # plt.show()
    wordCloud.to_file(
        os.getcwd()+"\\Text_Extractor_App\\static\\resultFiles\\bigram.jpg")

    # In[ ]:

    dictionary = dict(
        sorted(words_dict.items(), key=operator.itemgetter(1), reverse=True))
    df1 = pd.DataFrame(dictionary, index=[1])
    #df1 = pd.DataFrame(dictionary)

    # In[ ]:

    # dictionary

    # In[ ]:

    df2 = df1.transpose()
    df2.columns = ['Count']
    df2.loc[(df2['Count'] >= 5)]
    df2.reset_index(level=0, inplace=True)
    print(df2)
    delFiles(os.getcwd()+"\\Input_Excel" + "\\"+ExcelFileName)
    return unigram, df2
    # df2.to_csv("Bigram.csv")


def delFiles(path):
    if path != None:
        if os.path.exists(path):
            os.remove(path)
    PDFfiles = listFiles(os.getcwd()+"\\input_PDFs")
    for fileName in PDFfiles:
        os.remove(fileName)
    txtlst = []
    for root, dirs, files in os.walk(os.getcwd()+"\\input_PDFs"):
        for name in files:
            if name[-4:] == ".txt":
                txtlst.append(os.path.join(root, name))
    for fileName in txtlst:
        os.remove(fileName)
