FROM python:3.11

USER root

RUN mkdir /code
WORKDIR /code

ADD requirements.txt /code/

RUN python -m pip install --upgrade pip
RUN pip3 install -r requirements.txt

ADD . /code/

CMD ["./start_app.sh"]