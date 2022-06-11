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
info ={'STATUS':'Initiating Data'}


class WordAnalyst():

    def __init__(self, report_files, input_file):
        # report files return a list of file names
        # input file returns input files
        from RIAnalytics.settings import FILES_DIR, OUTPUT_DIR, IMAGE_ROOT
        self.FILES_DIR = FILES_DIR
        self.OUTPUT_DIR = OUTPUT_DIR
        self.STATIC_DIR = IMAGE_ROOT
        self.report_files = report_files 
        self.ExcelFileName = input_file
        pass
                


    def listFiles(self):
        r = []
        for x in self.report_files:
            r.append(os.path.join(self.FILES_DIR, x))
        return r


    def listtxtFiles(self):
        r = []
        for x in self.report_files:
            r.append(os.path.join(self.FILES_DIR, f'{x[:-4]}.txt'))
        return r


    def clean_text(self, text):
        text = re.sub('\[.*?\]', '', text)
        text = re.sub('https?://\S+|www\.\S+', '', text)
        text = re.sub('<.*?>+\\/-', '', text)
        text = re.sub('[%s]' % re.escape(string.punctuation), '', text)
        text = re.sub('\n', '', text)
        text = re.sub('\w*\d\w*', '', text)
        return text


# In[ ]:
    def generateHTML(self):
        try:
            html_content = "<div class='p-4 col-12 container'>"
            print("Start Time: " + time.strftime("%H:%M:%S", time.localtime()))
            info['STATUS'] = 'Inititated Operations'
            batchstart = time.time()
            PDFfiles = self.listFiles()
            info['STATUS'] = 'Listed Fields'
            list_searchKey = []
            list_count = []
            list_sentences = []
            # appended_data = []
            # for i in range(len(PDFfiles)):
            #     info['STATUS'] = f'No{i}. initiated'
            #     pdf = pdfplumber.open(PDFfiles[i], password="")
            #     with open(PDFfiles[i][:len(PDFfiles[i])-4]+".txt", 'w', encoding='utf-8') as txt_file:
                    
            #         for j in range(len(pdf.pages)):
            #             page = pdf.pages[j]
            #             txt = page.extract_text()
            #             txt_file.write(str(txt))
            #         pdf.close()
            #         txt_file.close()
            info['STATUS'] = 'Text Files Written'
            print("End Time: " + time.strftime("%H:%M:%S", time.localtime()))
            batchend = time.time()
            batchtime_taken = round(batchend - batchstart)/60
            print('[Info] Batch Completed in ', batchtime_taken, "Minutes")

            txtfiles = self.listtxtFiles()

            with open(os.path.join(self.FILES_DIR,'output.txt'), 'w') as outfile:
                for fname in txtfiles[1:]:
                    with open(fname, errors="ignore") as infile:
                        outfile.write(infile.read())



            word_list_without_replace_words = []

            df_replace_words = pd.read_excel(os.path.join(self.FILES_DIR, self.ExcelFileName), sheet_name="Words that we replace in doc")
            info['STATUS'] = 'Getting Replace Words'
            

            replace_from_list = []
            replace_to_list = []

            for i, j in df_replace_words.iterrows():
                replace_from_list.append(j["Words from transcripts"].strip())
                replace_to_list.append(j["Converted to (in transcripts)"].strip())

            
            info['STATUS'] = 'Replaced Words'

            with open(os.path.join(self.FILES_DIR, "output.txt"), 'r') as f:
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

            
            info['STATUS'] = 'Obtained Stipped Words, Now Getting Stop Words'
            # In[ ]:

            df_stop_words = pd.read_excel(
                os.path.join(self.FILES_DIR, self.ExcelFileName), sheet_name="Stop Words")

            info['STATUS'] = 'Obtained Stop Words'
            stop_word_list = []

            for i, j in df_stop_words.iterrows():
                stop_word_list.append(j["Stop Words"].lower().strip())


            word_list_without_replace_words_and_stop_words = []

            for word in word_list_without_replace_words:
                word = self.clean_text(word)
                if (word.lower().strip() not in stop_word_list):
                    word_list_without_replace_words_and_stop_words.append(word.strip())

            

            # In[ ]:
            info['STATUS'] = 'Processed Stop Words'

            df_analysis_words = pd.read_excel(
               os.path.join(self.FILES_DIR, self.ExcelFileName), sheet_name="Keyword analysis")

            # print (df_analysis_words)
            info['STATUS'] = 'Obtained analysis words'
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


            final_word_list = []
            info['STATUS'] = 'Generated Combined words list, now processing Final Words List'
            for w in word_list_without_replace_words_and_stop_words:
                isOccured = False
                for each_list in combined_word_list:
                    if (w in each_list):
                        isOccured = True
                        #print (w, each_list[0])
                        final_word_list.append(each_list[0])
                if (isOccured == False):
                    final_word_list.append(w)



            final_str = ""

            for f_w in final_word_list:
                final_str += f_w
                final_str += " "

 
            stopwords = set(STOPWORDS)
 

            # In[ ]:
            info['STATUS'] = 'Initiating clouds'
            cloud = WordCloud(background_color="white", max_words=20,
                            stopwords=stopwords).generate(final_str)


            cloud.to_file(os.path.join(self.STATIC_DIR, 'resultFiles', "unigram.jpg"))
            info['STATUS'] = 'Saved Unigram Image'
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

            info['STATUS'] = 'Obtained Unigram Image'
            df = pd.DataFrame(freq, columns=["word", "frequency"])

            unigram = df.sort_values(by=['frequency'], ascending=False)
            # uncomment to show unigram table
            # html_content += '''<div class="col-sm-12 p-4 "> <br><h4 class='font-weight-bold text-center text-warning'>Unigram</h4>'''

            # html_content += unigram.to_html()
            # html_content += "</div>"

           

            # sort.to_excel("Unigram.xlsx",sheet_name='unigram')

            # In[ ]:
            info['STATUS'] = 'Obtained Unigram table, Going for bigram'
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

            info['STATUS'] = 'Generating Bigram Image'
            wordCloud.to_file(
                os.path.join(self.STATIC_DIR, 'resultFiles', "bigram.jpg"))

           
            info['STATUS'] = 'Bigram Image Saved'
            dictionary = dict(
                sorted(words_dict.items(), key=operator.itemgetter(1), reverse=True))
            df1 = pd.DataFrame(dictionary, index=[1])

            df2 = df1.transpose()
            df2.columns = ['Count']
            df2.loc[(df2['Count'] >= 5)]
            df2.reset_index(level=0, inplace=True)


            #if you need to show the dataframe  uncommnent this section
            # html_content += '''<div class="col-sm-12 p-4 ">  <br><h4 class='font-weight-bold text-center text-warning'>Bigram</h4>'''
            # html_content += df2.to_html()
            # html_content += "</div>"

            info['STATUS'] = 'QUIT'
            return html_content
        except Exception as Error:
            info['STATUS']= f" Exiting with Error {str(Error)}"

# def delFiles(path):
#     if path != None:
#         if os.path.exists(path):
#             os.remove(path)
#     PDFfiles = listFiles(os.getcwd()+"\\input_PDFs")
#     for fileName in PDFfiles:
#         os.remove(fileName)
#     txtlst = []
#     for root, dirs, files in os.walk(os.getcwd()+"\\input_PDFs"):
#         for name in files:
#             if name[-4:] == ".txt":
#                 txtlst.append(os.path.join(root, name))
#     for fileName in txtlst:
#         os.remove(fileName)
