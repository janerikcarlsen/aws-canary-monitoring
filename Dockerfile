FROM python:3.8.2-alpine3.11

RUN pip install --upgrade pip

COPY requirements.txt /requirements.txt
RUN pip install -r requirements.txt

COPY entrypoint.sh /entrypoint.sh
COPY monitor_canary.py /monitor_canary.py
RUN chmod +x /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]