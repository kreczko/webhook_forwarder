import os
import json
import sys
from flask import Flask, abort, request
# from kafka_helper import get_kafka_producer
import confluent_kafka

app = Flask(__name__)
KAFKA_PRODUCER = None

def get_kafka_producer():
    '''
        Get the kafka producer, might differ depending on service
    '''
    global KAFKA_PRODUCER
    conf = {
            'bootstrap.servers': os.environ['CLOUDKARAFKA_BROKERS'],
            'session.timeout.ms': 6000,
            'default.topic.config': {'auto.offset.reset': 'smallest'},
            'security.protocol': 'SASL_SSL',
            'sasl.mechanisms': 'SCRAM-SHA-256',
            'sasl.username': os.environ['CLOUDKARAFKA_USERNAME'],
            'sasl.password': os.environ['CLOUDKARAFKA_PASSWORD'],
    }
    if KAFKA_PRODUCER is not None:
        return KAFKA_PRODUCER
    try:
        KAFKA_PRODUCER = confluent_kafka.Producer(**conf)
        return KAFKA_PRODUCER
    except Exception as e:
        print('Could not create kafka producer', e)

@app.route('/gitlab_forwarder', methods=['POST'])
def forward_gitlab():
    kafka_topic = "{}gitlab".format(os.environ['CLOUDKARAFKA_TOPIC_PREFIX'])

    TOKEN = os.environ.get("GITLAB_TOKEN")
    if TOKEN is None or request.headers.get('X-Gitlab-Token') != TOKEN:
        abort(401)
        return

    content = request.get_json(silent=True)
    js = json.dumps(content)

    producer = get_kafka_producer()
    producer.produce(kafka_topic, js)
    producer.flush()

@app.route('/')
def homepage():

    return """
    <h1>Hello heroku</h1>
    <p>It is currently {time}.</p>

    <img src="http://loremflickr.com/600/400">
    """.format(time="too early")

if __name__ == '__main__':
    app.run(debug=True, use_reloader=True)
