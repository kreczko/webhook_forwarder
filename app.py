import os
import json
import sys
from flask import Flask, abort, request
from kafka_helper import get_kafka_producer

app = Flask(__name__)


@app.route('/gitlab_forwarder', methods=['POST'])
def forward_gitlab():
    kafka_topic = "{}".format(os.environ['KAFKA_TOPIC'])

    TOKEN = os.environ.get("GITLAB_TOKEN")
    if TOKEN is None or request.headers.get('X-Gitlab-Token') != TOKEN:
        abort(401)
        return

    content = request.get_json(silent=True)
    js = json.dumps(content)

    producer = get_kafka_producer()
    producer.produce(kafka_topic, js)
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
