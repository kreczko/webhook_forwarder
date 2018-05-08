import os
import json
import sys
from flask import Flask, abort, request
from kafka_helper import get_kafka_producer
import logging

app = Flask(__name__)
app.logger.addHandler(logging.StreamHandler(sys.stdout))
app.logger.setLevel(logging.ERROR)
if os.environ.get('DEBUG', False):
    app.logger.setLevel(logging.DEBUG)


def _delivery_callback(err, msg):
    if err:
        app.logger.error('Message failed delivery: {}'.format(err))
    else:
        app.logger.debug('Message delivered to {}[{}]'.format(
            msg.topic(), msg.partition()))


@app.route('/gitlab_forwarder', methods=['POST'])
def forward_gitlab():
    kafka_topic = "{}".format(os.environ['KAFKA_TOPIC'])
    debug = os.environ.get('DEBUG', False)
    app.logger.debug('received a message ')

    TOKEN = os.environ.get("GITLAB_TOKEN")
    if TOKEN is None or request.headers.get('X-Gitlab-Token') != TOKEN:
        abort(401)
        app.logger.debug('This message is INVALID')
        return

    app.logger.debug('This is a valid message')
    content = request.get_json(silent=True)
    js = json.dumps(content)

    producer = get_kafka_producer()
    producer.produce(kafka_topic, js, callback=_delivery_callback)
    producer.flush()

    return "OK"


@app.route('/')
def homepage():

    return """
    <h1>Hello heroku</h1>
    <p>It is currently {time}.</p>

    <img src="http://loremflickr.com/600/400">
    """.format(time="too early")


if __name__ == '__main__':
    app.run(debug=True, use_reloader=True)
