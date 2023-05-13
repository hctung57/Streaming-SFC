FROM python:3.8-slim-buster
WORKDIR /app

RUN pip3 install opencv-python-headless &&\
    pip3 install configargparse

COPY capture.py run.sh ./

RUN chmod +x run.sh

CMD ["sh","./run.sh"]
