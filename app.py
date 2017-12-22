from flask import Flask
import confluent_kafka

app = Flask(__name__)

@app.route('/')
def homepage():

    return """
    <h1>Hello heroku</h1>
    <p>It is currently {time}.</p>

    <img src="http://loremflickr.com/600/400">
    """.format(time="too early")

if __name__ == '__main__':
    app.run(debug=True, use_reloader=True)
