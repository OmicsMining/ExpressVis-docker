FROM python:3.8-buster

ENV PYTHONUNBUFFERED 1

COPY requirements.txt requirements.txt
# change https://mirrors.aliyun.com/pypi/simple/ to you nearest pypi source
RUN python -m pip install -r requirements.txt -i https://mirrors.aliyun.com/pypi/simple/ 

RUN mkdir /code
WORKDIR /code
COPY . /code/

