FROM python:3

LABEL version="0.0.1-beta"

WORKDIR .
COPY . .

RUN pip install --no-cache-dir -r requirements.txt

VOLUME /data

CMD ./run.sh