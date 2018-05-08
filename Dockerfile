FROM python:alpine3.6

LABEL maintainer="kreczko@cern.ch"

ARG LIBRESSL_VERSION=2.7
ARG LIBRDKAFKA_VERSION=0.11.4-r1

RUN apk update && \
    apk add --no-cache \
            alpine-sdk \
            bash \
            build-base \
            coreutils \
            cyrus-sasl-dev \
            krb5 \
            libffi-dev \
            libsasl \
            openssl \
            openssl-dev \
            zlib-dev

RUN apk add --no-cache \
            libressl${LIBRESSL_VERSION}-libcrypto \
            libressl${LIBRESSL_VERSION}-libssl \
             --repository http://nl.alpinelinux.org/alpine/edge/main && \
    apk add --no-cache \
            librdkafka-dev=${LIBRDKAFKA_VERSION} \
            librdkafka=${LIBRDKAFKA_VERSION} \
            --repository http://nl.alpinelinux.org/alpine/edge/community

# Install dependencies
ADD requirements.txt /tmp/requirements.txt
RUN pip install --no-cache-dir  -r /tmp/requirements.txt

# Add our code
ADD . /app/user
WORKDIR /app/user

# Run the image as a non-root user
RUN adduser -D myuser
USER myuser

# Run the app.  CMD is required to run on Heroku
# $PORT is set by Heroku

CMD gunicorn --bind 0.0.0.0:$PORT wsgi
