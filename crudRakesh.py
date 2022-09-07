from flask import Flask, request, Response
from flask_mongoengine import MongoEngine

app = Flask(__name__)

app.config['MONGODB_SETTINGS'] = {
    'db': 'database',
    'host': 'localhost',
    'port': 27017
}

db = MongoEngine()
db.init_app(app)

class Netflix(db.Document):
    meta= {
        "collection": "netflix"
    }
    ID= db.StringField()
    title = db.StringField()
    type = db.StringField()
    description = db.StringField()
    release_year = db.IntField()
    age_certification = db.StringField()
    runtime = db.IntField()
    genres = db.StringField()
    production_countries = db.StringField()
    imdb_score = db.FloatField()


@app.route('/netflix', methods=['GET'])
def get_netflix_items():
    items = Netflix.objects().to_json()
    return Response(items, mimetype="application/json", status=200)

@app.route('/netflix/<title>', methods=['GET'])
def get_netflix_item(title):
    items = Netflix.objects(title=title).to_json()
    return Response(items, mimetype="application/json", status=200)

@app.route('/netflix/<title>', methods=['PATCH'])
def update_item(title):
    ## check the movie avai
    data = request.get_json()
    item=Netflix.objects(title=title).first()
    item.update(**data)
    return  'Updated successfully.', 200

@app.route('/netflix/<title>', methods=['DELETE'])
def delete_netflix_item(title):
    ##check movie available
    Netflix.objects().get(title=title).delete()
    return 'The Item Deleted Successfully.', 200

@app.route('/netflix', methods=['POST'])
def add_item():
    data = request.json
    obj1 = Netflix(**data).save()
    return 'The Item inserted successfully.', 200


if __name__ == "__main__":
    app.run(debug=True, port=8080)