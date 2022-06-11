# FROM python:3.8-slim-buster
FROM dhairya137/py3.8sm-poppler20:v1 

ENV PYTHONUNBUFFERED 1

WORKDIR /app

COPY requirements.txt .

RUN pip install fitz
RUN pip install pymupdf
RUN pip install nltk
RUN pip install pdftotext
RUN python -m nltk.downloader punkt  
RUN pip install -r requirements.txt

COPY . .

RUN python manage.py makemigrations
RUN python manage.py migrate
RUN python manage.py collectstatic --no-input

CMD python manage.py runserver 0.0.0.0:80
