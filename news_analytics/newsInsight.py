# ! apt-get install libpoppler-cpp-dev
# ! pip install pdftotext
# import pdftotext


import os
import re

from IPython.display import display, HTML

import circlify
import pdftotext
import matplotlib
import matplotlib.pyplot as plt, mpld3

matplotlib.use('Agg')

import pandas as pd

info = {'STATUS': 'Inititated', 'FILE': None}


class NewsAnalyst():
    search_df = None
    new_df = None
    pivot_table = None

    def __init__(self):
        from RIAnalytics.settings import FILES_DIR, OUTPUT_DIR
        self.FILES_DIR = FILES_DIR
        self.OUTPUT_DIR = OUTPUT_DIR

    def extract_text(self, file_name):
        with open(f'{os.path.join(self.FILES_DIR, file_name)}', 'rb') as f:
            pdf = pdftotext.PDF(f)

        text = '\n'.join(pdf).split('\n')

        for t in text:
            if t.startswith('Page'):
                text.remove(t)

        return text

    def parse_text(self, text):
        text_list = []
        text_dict = {}
        k = ''
        v = ''

        for t in text:
            if re.match('^[A-Z]+', t):
                try:
                    k, v = t.split(maxsplit=1)
                except ValueError:
                    k, v = t.strip(), ''

                text_dict[k] = v

                if t.startswith('AN'):
                    text_list.append(text_dict)
                    text_dict = {}

            else:
                v = '\n' + t.strip()
                try:
                    text_dict[k] += v
                except KeyError:
                    pass

        return text_list

    def main(self):
        self.files = os.listdir(self.FILES_DIR)
        pdf_files = sorted([f for f in self.files if f.endswith('.pdf')])

        for file in self.files:
            if file.endswith('.xlsx'):
                self.excel_file = os.path.join(self.FILES_DIR, file)
                self.search_df = pd.read_excel(self.excel_file)
                break

        all_data_list = []
        for file_name in pdf_files:
            text = self.extract_text(file_name)
            text_list = self.parse_text(text)
            all_data_list.extend(text_list)
            info['STATUS'] = f'{file_name} processed'

        df = pd.DataFrame(all_data_list)
        df.to_excel('text_extracted.xlsx', index=False)
        info['STATUS'] = 'text_extracted.xlsx saved'
        self.df = df
        return self.df

    def search_terms(self, row):
        s_terms = self.search_df
        try:
            text = str(row['LP']).lower()
        except KeyError:
            text = ""

        for term, goal in zip(s_terms['Key Terms'], s_terms['Goals']):
            cond = (' ' + term.lower() + ' ') in text or (' ' + term.lower() + '.') in text or (
                    '\n' + term.lower() + ' ') in text or (' ' + term.lower() + '\n') in text

            if cond:
                row['Key Terms'] = term
                row['Goals'] = goal
                return row

        row['Key Terms'] = None
        row['Goals'] = None

        return row

    def parse_co(self, row):
        try:
            text = row['CO']
        except KeyError:
            text = ""

        try:
            co_names = text.split('|')
        except AttributeError:
            return row

        for i, name in enumerate(co_names):
            row[f'CO{i + 1}'] = name.split(':')[1].strip()

        return row

    def create_pivot_table(self, df):
        pivot_dict = {}

        for co, goal in zip(df['CO'], df['Goals']):
            if not goal:
                continue

            try:
                co_names = co.split('|')
            except AttributeError:
                continue

            for co_name in co_names:
                co_name = co_name.split(':')[1].strip().replace('\n', ' ')
                co_name = co_name.replace('\r', '')
                co_name = co_name.replace('\t', ' ')

                if co_name not in pivot_dict.keys():
                    pivot_dict[co_name] = {}

                if goal not in pivot_dict[co_name].keys():
                    pivot_dict[co_name][goal] = 0

                pivot_dict[co_name][goal] += 1
                pivot_table = pd.DataFrame(pivot_dict).transpose()

        return pivot_table


    def generatePivotTable(self):
        new_df = self.df.apply(self.search_terms, axis=1)
        old_columns = new_df.columns
        CO_idx = list(old_columns).index('CO')
        print(CO_idx)
        new_df = new_df.apply(self.parse_co, axis=1)
        print(new_df)
        CO_columns = [col for col in new_df.columns if col.startswith('CO')]
        final_columns = list(old_columns[:CO_idx]) + CO_columns + list(old_columns[CO_idx + 1:])
        new_df = new_df[final_columns]
        pivot_table = self.create_pivot_table(new_df)
        self.pivot_table = pivot_table
        self.new_df = new_df
        return pivot_table

    def saveExcel(self):
        writer = pd.ExcelWriter("NewsInsights.xlsx")
        self.new_df.to_excel(writer, sheet_name='new_sheet', index=False)
        self.pivot_table.to_excel(writer, sheet_name='PIVOT', index=True)
        writer.save()

        self.new_df.drop_duplicates(subset=['HD'], inplace=True)
        self.new_df = self.new_df[self.new_df['HD'].notna()]
        self.new_df = self.new_df[self.new_df['Key Terms'].notna()]
        self.new_df = self.new_df[['PD', 'SN', 'HD', 'LP', 'CO1', 'CO2', 'CO3', 'Key Terms', 'Goals']]
        self.new_df.rename(
            columns={'HD': 'Headline', 'PD': 'Publication Date', 'LP': 'Lead Para', 'CO1': 'Tagged Company1',
                     'CO2': 'Tagged Company2', 'CO3': 'Tagged Company3'}, inplace=True)
        self.new_df.to_excel(os.path.join(self.OUTPUT_DIR, "NewsInsights_report.xlsx"), index=False)

        return self.new_df

    def highlight_LP(self):
        html_content = ''
        for ind, row in self.new_df.iterrows():
            lp = row['Lead Para']
            key = row['Key Terms']

            if key:
                start = lp.lower().index(key.lower())
                end = start + len(key)
                html = '<p>' + lp[:start] + '<mark>' + lp[start:end] + '</mark>' + lp[end:] + '</p><br><br>'
                html_content += f'''{HTML(html).data}'''

        return html_content

    def make_circles(self):
        goal_freq = self.new_df['Goals'].value_counts()

        circles = circlify.circlify(
            goal_freq.values.tolist(),
            show_enclosure=False,
            target_enclosure=circlify.Circle(x=0, y=0, r=1)
        )

        fig, ax = plt.subplots(figsize=(10, 10))
        ax.axis('off')

        if len(circles) < 1:
            return ""

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

    def generateHTML(self, filenames, excelfile, namehash):
        self.FILES_DIR = os.path.join(self.FILES_DIR, namehash)
        self.OUTPUT_DIR = os.path.join(self.OUTPUT_DIR, namehash)

        html_content = "<div class='col-12 p-4'>"
        self.main()
        # html_content += self.main().to_html()
        info['STATUS'] = 'Generating pivot table'
        self.generatePivotTable()
        info['STATUS'] = 'Generating Excel Files'
        html_content += '''<div class="col-sm-12 p-4 "> '''
        html_content += self.saveExcel().to_html()
        html_content += "</div></div>"
        info['STATUS'] = 'Generating .xls Files'
        html_content += self.highlight_LP()
        info['STATUS'] = 'Generated Highlights'
        info['STATUS'] = 'Making Chart'
        html_content = html_content.replace('''<table border="1" class="dataframe">''',
                                            '''<table class="table small col-12" style="font-size:10px">''').replace(
            '&lt;', '<').replace('&gt;', '>').replace('\n', '<br>')
        html_content += '''<div class='col-12 d-flex justify-content-center align-items-center'>'''
        html_content += self.make_circles()
        html_content += "</div>"
        info['STATUS'] = 'Chart made successfully'
        html_content += "</div>"
        f = open('html_report.txt', 'w')
        f.write(html_content)
        f.close()
        info['STATUS'] = 'Done'
        info['STATUS'] = 'QUIT'
        return (html_content)
    # except Exception as Error:
    #     print(f" Exiting with Error {str(Error)}")
    #     info['STATUS'] = f" Exiting with Error {str(Error)}"
