FROM python:3.11

COPY ./requirements.txt /
RUN mkdir /app && mkdir /config && mkdir /logs && pip3 install --no-cache-dir -r requirements.txt

WORKDIR /app/
COPY ./ha-bt /app/

ENTRYPOINT python ha_bt.py
