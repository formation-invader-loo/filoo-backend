FROM python:3

LABEL version="0.0.1-beta"

WORKDIR ../
COPY /requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

VOLUME /data

RUN ./run.sh