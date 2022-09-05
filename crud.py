import json
from flask import Flask, request, jsonify, make_response, Response
from flask_mongoengine import MongoEngine

app = Flask(__name__)

app.config['MONGODB_SETTINGS'] = {
    'db': 'database',
    'host': 'localhost',
    'port': 27017
}
db = MongoEngine()
db.init_app(app)

class Movie(db.Document):
    meta = {
        'collection': 'netflix',
    }
    title = db.StringField()
    type = db.StringField()
    description = db.StringField()
    release_year = db.IntField()
    age_certification = db.StringField()
    runtime = db.IntField()
    genres = db.StringField()
    production_countries = db.StringField()
    imdb_score = db.FloatField()

    def to_json(self):
        return {
            "id": self.id
        }

@app.route('/movies', methods=['GET'])
def get_movies():
    movies = Movie.objects().to_json()
    return Response(movies, mimetype="application/json", status=200)

@app.route('/movies', methods=['POST'])
def add_movie():
    body = request.get_json()
    movie =  Movie(**body).save()
    return {'id': str(id)}, 200

@app.route('/movies/<title>', methods=['PATCH'])
def update_movie(title):
    body = request.get_json()
    movie=Movie.objects.get_or_404(title=title)
    movie.update(**body)
    return  'Updated successfully', 200

@app.route('/movies/<title>', methods=['DELETE'])
def delete_movie(title):
    Movie.objects().get(title=title).delete()
    return 'Deleted Successfully', 200

@app.route('/movies/<title>', methods=['GET'])
def get_movie(title):
    movies = Movie.objects(title=title).to_json()
    
    return Response(movies, mimetype="application/json", status=200)
   
if __name__ == "__main__":
    app.run(debug=True, port=80)