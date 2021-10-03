FROM python:3.7.7-stretch

WORKDIR /linklerz

ADD . .

RUN pip install -r requirements.txt

CMD [ "python",".\app.py" ]