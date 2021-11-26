FROM debian

WORKDIR /usr/src/app

COPY config.ini backup_manager/* ./

RUN mkdir backup