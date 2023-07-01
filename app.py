from flask import Flask
from logging.config import dictConfig


dictConfig({
    'version': 1,
    'formatters': {'default': {
        'format': '[%(asctime)s] %(levelname)s in %(module)s: %(message)s',
    }},
    'handlers': {'wsgi': {
        'class': 'logging.StreamHandler',
        'stream': 'ext://flask.logging.wsgi_errors_stream',
        'formatter': 'default'
    }},
    'root': {
        'level': 'INFO',
        'handlers': ['wsgi']
    }
})


app = Flask(__name__)


@app.route('/')
def hello_world():  # put application's code here
    app.logger.info("The site was in process")
    return (
        '<h1>Hello World!</h1>'
    )


@app.route('/about')
def author_info():
    app.logger.info("The information abot the creator was called")
    return (
        '<h1>Danyil Shuba:</h1>'
        '<p>A student in Kyiv`s national university</p>'
    )


@app.route('/json_info')
def author_data():
    app.logger.info("The json format was checked")
    return {
        'name': 'Danyil',
        'surname': 'Shuba',
        'age': 20,
        'natinality': 'Ukraine'
    }


if __name__ == '__main__':
    app.run(debug=True)
