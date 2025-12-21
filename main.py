from flask import Flask, jsonify
from utils import movies, ratings, links, tags

app = Flask(__name__)


@app.route('/', methods=['GET'])
def hello_world():
    return jsonify({'hello': 'world'})


@app.route('/movies', methods=['GET'])
def movies_api():
    return list(map(lambda m: m.__dict__, movies.load_from_file()))


@app.route('/ratings', methods=['GET'])
def ratings_api():
    return list(map(lambda m: m.__dict__, ratings.load_from_file()))


@app.route('/links', methods=['GET'])
def links_api():
    return list(map(lambda m: m.__dict__, links.load_from_file()))


@app.route('/tags', methods=['GET'])
def tags_api():
    return list(map(lambda m: m.__dict__, tags.load_from_file()))


if __name__ == '__main__':
    app.run(debug=True)
