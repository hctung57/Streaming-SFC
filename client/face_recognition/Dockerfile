FROM animcogn/face_recognition:cpu

RUN apt-get update && \
    pip install opencv-python-headless==4.5.3.56 && \
    pip install configargparse

RUN mkdir recognition

COPY recognition.py nginx.sh /recognition

RUN cd recognition && \
    chmod +x nginx.sh
WORKDIR /recognition
EXPOSE 1935
CMD ["sh","./nginx.sh"]
