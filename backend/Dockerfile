FROM python:3.9

WORKDIR /app
RUN pip install gunicorn==20.1.0
COPY requirements.txt .

RUN pip3 install -r requirements.txt --no-cache-dir

COPY foodgram/ .

CMD ["gunicorn", "foodgram.wsgi", "--bind", "0:8000" ]
