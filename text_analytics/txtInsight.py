# ! pip install PyMuPDF==1.18.9
import fitz
import os
import re
from io import BytesIO
import pandas as pd
import nltk
from nltk import tokenize
from IPython.display import display, HTML

import circlify
import traceback
import matplotlib

matplotlib.use('agg')
import matplotlib.pyplot as plt, mpld3

# %matplotlib inline
info = {'STATUS': 'Inititated', 'FILE': None}


class TextAnalyst():

    def __init__(self):
        from RIAnalytics.settings import FILES_DIR, OUTPUT_DIR
        self.FILES_DIR = FILES_DIR
        self.OUTPUT_DIR = OUTPUT_DIR
        pass

    def highlight_pdf(self, file_name, search_terms):
        try:
            pdf_doc = fitz.open(f'{os.path.join(self.FILES_DIR, file_name)}')
            output_buffer = BytesIO()

            for pg_num in range(pdf_doc.pageCount):
                page = pdf_doc[pg_num]
                highlight = None

                for term in search_terms:
                    highlight_area = page.search_for(term)
                    highlight = page.add_highlight_annot(highlight_area)

                highlight.update()

            pdf_doc.save(output_buffer)
            pdf_doc.close()
            f = open(f'{os.path.join(self.OUTPUT_DIR, file_name)}', mode='wb')
            f.close()
            with open(f'{os.path.join(self.OUTPUT_DIR, file_name)}', mode='wb') as f:
                f.write(output_buffer.getbuffer())
        except Exception as E:
            print('errors', str(E))
        # with open(f'{file_name}', mode='wb') as f:
        #     f.write(output_buffer.getbuffer())

        return ''

    def extract_text(self, file_name):
        pdf_doc = fitz.open(f'{os.path.join(self.FILES_DIR, file_name)}')
        text = ''

        for pg_num in range(pdf_doc.pageCount):
            page = pdf_doc[pg_num]
            page_text = page.get_text()
            page_text = page_text.replace('\n', ' ')
            text += page_text

        return text

    def highlight_sentences(self, sentences, key_terms):
        html_content = ''
        for sent in sentences:
            sent_lower = sent.lower()
            for term in key_terms:
                if term in sent_lower:
                    start = sent_lower.index(term)
                    end = start + len(term)
                    html = '<p>' + sent[:start] + '<mark>' + sent[start:end] + '</mark>' + sent[end:] + '</p><br><br>'
                    html_content += f'''{HTML(html).data}'''
        return html_content

    def highlight_sentences_by_goal(self, df):
        html_content = ''
        found_goals_df = df[df['No_Of_Occurence'] > 0]
        goals = found_goals_df['Goals'].unique().tolist()

        for goal in goals:
            html_content += f'''
            <div style='text-align:center'>
            {goal}
            </div>
            <br><br>
            '''
            goal_df = found_goals_df[found_goals_df['Goals'] == goal]

            for ind, row in goal_df.iterrows():
                sentences = row['Sentence'].splitlines()

                for sent in sentences:
                    start = sent.lower().index(row['Search_Key'].lower())
                    end = start + len(row['Search_Key'])
                    html = '<p>' + sent[:start] + '<mark>' + sent[start:end] + '</mark>' + sent[end:] + '<b>' + row[
                        'File_Name'] + '</b>' + '</p><br><br>'
                    html_content += f'''{HTML(html).data}'''
        return html_content

    def find_key_sentences(self, sentences, key_term):
        terget_sentences = []
        count = 0

        for sent in sentences:
            sent_lower = sent.lower()
            if key_term in sent_lower:
                ### batch of code to modify the secntences and hightlight key terrm
                start = sent_lower.index(key_term)
                end = start + len(key_term)
                new_sent = '<p>' + sent[:start] + '<mark>' + sent[start:end] + '</mark>' + sent[end:] + '</p>'

                terget_sentences.append(new_sent)
                count += 1

        return count, terget_sentences

    def count_no_of_occurences(self, file_name, sentences, search_key_df):
        list_of_data = []

        for s_key, goal in zip(search_key_df['Key Terms'], search_key_df['Goals']):
            count, key_sentences = self.find_key_sentences(sentences, s_key.lower())

            result_dict = {}
            result_dict['File_Name'] = file_name
            result_dict['Search_Key'] = s_key
            result_dict['No_Of_Occurence'] = count
            result_dict['Goals'] = goal
            result_dict['Sentence'] = ' <br><br>'.join(key_sentences)
            if count > 0:
                list_of_data.append(result_dict)

        return list_of_data

    def make_circles(self):
        goal_freq = self.df.groupby('Goals').sum('No_Of_Occurences')
        goal_freq = goal_freq[goal_freq['No_Of_Occurence'] > 0]

        circles = circlify.circlify(
            goal_freq['No_Of_Occurence'].tolist(),
            show_enclosure=False,
            target_enclosure=circlify.Circle(x=0, y=0, r=1)
        )

        circles = circlify.circlify(
            goal_freq['No_Of_Occurence'].tolist(),
            show_enclosure=False,
            target_enclosure=circlify.Circle(x=0, y=0, r=1)
        )

        fig, ax = plt.subplots(figsize=(10, 10))
        ax.axis('off')

        lim = max(
            max(
                abs(circle.x) + circle.r,
                abs(circle.y) + circle.r,
            )
            for circle in circles
        )
        plt.xlim(-lim, lim)
        plt.ylim(-lim, lim)

        labels = goal_freq.index.to_list()

        for circle, label in zip(circles, labels):
            x, y, r = circle
            font_size = 800 * (r / len(label))
            ax.add_patch(plt.Circle((x, y), r * 0.97, alpha=0.3, linewidth=2))
            plt.annotate(
                label,
                (x, y),
                va='center',
                ha='center',
                fontsize=font_size
            )
        plt_html = mpld3.fig_to_html(fig)
        return plt_html

    def generateHTML(self, reportfile, keywordfile, keywords, report):

        try:
            with open(f"{os.path.join(self.FILES_DIR, report)}.html", 'r') as f:
                print(f">>>>{os.path.join(self.FILES_DIR, report)}.html find")
                repstr = f.read()
                if len(repstr) > 10:
                    return repstr
            html_content = "<div class='col-12 p-4'>"
            self.files = os.listdir(self.FILES_DIR)
            info['FILE'] = os.listdir(self.FILES_DIR)
            pdf_files = sorted([f for f in self.files if f.endswith('.pdf')])
            info['STATUS'] = pdf_files
            for file in self.files:
                if file.endswith('.xlsx'):
                    self.excel_file = os.path.join(self.FILES_DIR, file)
                    break
            search_df = pd.read_excel(self.excel_file)
            search_terms = search_df['Key Terms']
            info['STATUS'] = 'Initial processing Successful'
            # if keywords:
            #     search_terms = pd.concat([search_terms,pd.Series(list(keywords))],axis=0)
            result_list = []
            for file_name in pdf_files:
                html_content += self.highlight_pdf(file_name, search_terms)
                info['STATUS'] = f'Hightlighting Successful for {file_name}'
                info['STATUS'] = f'Extracting text for {file_name}'
                text = self.extract_text(file_name)
                info['STATUS'] = f'Extracted text for {file_name}'
                sentences = tokenize.sent_tokenize(text)
                info['STATUS'] = f'Tokenizing for {file_name}'

                html_content += f'''<h4 style='text-align:center;color:#ff511a;font-weight:500'>
                {file_name}
                </h4>
                <br><br>
                '''
                info['STATUS'] = f'Highlighting sentences for {file_name}'
                html_content += self.highlight_sentences(sentences, search_terms.str.lower())
                info['STATUS'] = f'Stage 2.1: highlighted text for {file_name}'

                info['STATUS'] = f'Making table for {file_name}'
                file_result = self.count_no_of_occurences(file_name, sentences, search_df)
                info['STATUS'] = f'Made table for {file_name}. Cleaning up'
                result_list.extend(file_result)

            self.df = pd.DataFrame(result_list)
            info['STATUS'] = f'Wrapping up {file_name}'
            pivot_table = self.df.groupby(['File_Name', 'Goals']).sum(['No of Occurance']).unstack()
            pivot_table = pivot_table.droplevel(0, axis=1).reset_index()
            self.df.to_excel('Text_Insight.xlsx', index=False)
            pivot_table.to_excel('Pivot Table.xlsx', index=False)
            html_content += self.highlight_sentences_by_goal(self.df)
            html_content += '''<div class="col-sm-12 p-4 "> '''
            html_content += self.df.to_html()
            html_content += "</div>"
            html_content = html_content.replace('''<table border="1" class="dataframe">''',
                                                '''<table class="table small col-12" style="font-size:10px">''').replace(
                '&lt;', '<').replace('&gt;', '>')
            html_content += '''<div class='col-12 d-flex justify-content-center align-items-center'>'''
            html_content += self.make_circles()
            html_content += "</div>"
            html_content += '''<div class="col-sm-12 p-4 "> '''
            html_content += pivot_table.to_html()
            html_content += "</div></div>"
            html_content = html_content.replace('''<table border="1" class="dataframe">''',
                                                '''<table class="table small col-12" style="font-size:10px">''')
            info['STATUS'] = f'Done: {file_name}'
            f = open(f"{os.path.join(self.FILES_DIR, report)}.html", 'w')
            f.write(html_content)
            f.close()
            info['STATUS'] = 'QUIT'
            return html_content

        except Exception as Error:
            info['STATUS'] = f" Exiting with Error {traceback.format_exc()}"
