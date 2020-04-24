from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:''@localhost/test'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
ma = Marshmallow(app)


class Jokes(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    firstSentence = db.Column(db.String(256))
    secondSentence = db.Column(db.String(256))

    def __init__(self, firstSentence, secondSentence):
        self.firstSentence = firstSentence
        self.secondSentence = secondSentence


class JokeSchema(ma.Schema):
    class Meta:
        fields = ("id", "firstSentence", "secondSentence")


joke_schema = JokeSchema()
jokes_schema = JokeSchema(many=True)


@app.route('/getAll', methods=['GET'])
def getAll():
    all_jokes = Jokes.query.all()
    return jsonify(jokes_schema.dump(all_jokes))


@app.route('/get/<id>/', methods=['GET'])
def get(id):
    joke = Jokes.query.get(id)
    return joke_schema.jsonify(joke)


@app.route('/add', methods=['POST'])
def add():
    content = request.get_json(force=True)
    firstSentence = content['firstSentence']
    secondSentence = content['secondSentence']

    new_joke = Jokes(firstSentence, secondSentence)
    db.session.add(new_joke)
    db.session.commit()

    return joke_schema.jsonify(new_joke)


@app.route('/update/<id>/', methods=['PUT'])
def update(id):
    joke = Jokes.query.get(id)
    
    content = request.get_json(force=True)
    joke.firstSentence = content['firstSentence']
    joke.secondSentence = content['secondSentence']
    db.session.commit()

    return joke_schema.jsonify(joke)


@app.route('/delete/<id>/', methods=['DELETE'])
def delete(id):
    joke = Jokes.query.get(id)
    db.session.delete(joke)
    db.session.commit()

    return joke_schema.jsonify(joke)


if __name__ == "__main__":
    app.run(debug=True)

