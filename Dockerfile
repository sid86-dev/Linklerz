FROM python:3

WORKDIR /linklerz

ENV FLASK_APP=app.py

COPY . /linklerz

RUN pip install -r requirements.txt

CMD ["python", "app.py"]