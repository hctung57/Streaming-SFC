FROM ubuntu:22.04
RUN apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
    tzdata && \
    apt install -y libgl1-mesa-glx && \
    apt install -y ffmpeg
    
# Get the library for nginx && wget && unzip
RUN apt-get update && \
    apt-get install -y build-essential libpcre3 libpcre3-dev zlib1g zlib1g-dev libssl-dev libgd-dev libxml2 libxml2-dev uuid-dev nano libxml2-dev libxslt-dev python-dev-is-python3 libgeoip-dev wget unzip -y 

RUN mkdir nginxDL && \
    cd nginxDL &&\
    wget http://nginx.org/download/nginx-1.21.6.tar.gz &&\
    tar -zxvf nginx-1.21.6.tar.gz

RUN cd nginxDL &&\
    wget https://github.com/sergey-dryabzhinsky/nginx-rtmp-module/archive/dev.zip && \
    unzip dev.zip

RUN cd ./nginxDL/nginx-1.21.6 &&\
    ./configure --with-http_ssl_module --add-module=../nginx-rtmp-module-dev &&\
    make &&\
    make install

COPY nginx.conf /usr/local/nginx/conf/nginx.conf

RUN /usr/local/nginx/sbin/nginx

RUN mkdir noisesuppress

COPY noisesuppress.sh /noisesuppress

COPY cb.rnnn /noisesuppress
   
RUN cd noisesuppress && \
    chmod +x noisesuppress.sh

WORKDIR /noisesuppress
EXPOSE 1935
CMD ["sh","./noisesuppress.sh"]
