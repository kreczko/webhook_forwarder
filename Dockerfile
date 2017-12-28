FROM python:alpine3.6

LABEL maintainer="kreczko@cern.ch"

RUN apk add --no-cache \
            alpine-sdk \
            bash \
            krb5 \
            libffi-dev \
            librdkafka \
            librdkafka-dev \
            libsasl \
            openssl-dev

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
