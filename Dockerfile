FROM python:3.12

WORKDIR /demo

ADD . /demo

RUN pip install -r requirements.txt

CMD [ "pytest"]