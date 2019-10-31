from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_cors import CORS
from flask_heroku import Heroku

app = Flask(__name__)

heroku = Heroku(app)

app.config["SQLALCHEMY_DATABASE_URI"] = "postgres://mrfrfvimjcbvcb:3000120aebd0c57d75b41e683bfc1ade84f7aaaf2b4d3b8df132243c1b123366@ec2-107-20-243-220.compute-1.amazonaws.com:5432/d6kdqvlr22u5rv"

CORS(app) 

db = SQLAlchemy(app)
ma = Marshmallow(app)

class Request(db.Model):
    __tablename__ = "request"
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(100))
    company = db.Column(db.String(150))
    email = db.Column(db.String(100))
    message = db.Column(db.String(400))
    done = db.Column(db.Boolean)

    def __init__(self, name, company, email, message, done):
        self.name = name
        self.company = company
        self.email = email
        self.message = message
        self.done = done

class RequestSchema(ma.Schema):
    class Meta:
        fields = ("id", "name", "company", "email", "message", "done")


request_schema = RequestSchema()
requests_schema = RequestSchema(many=True)


@app.route("/requests", methods=["GET"])
def get_requests():
    all_requests = Request.query.all()
    result = requests_schema.dump(all_requests)
    return jsonify(result)

@app.route("/request", methods=["POST"])
def add_request():
    name = request.json["name"]
    company = request.json["company"]
    email = request.json["email"]
    message = request.json["message"]
    done = request.json["done"]

    new_request = Request(name, company, email, message, done)
    db.session.add(new_request)
    db.session.commit()

    created_request = Request.query.get(new_request.id)
    return request_schema.jsonify(created_request)

@app.route("/request/<id>", methods=["PATCH"])
def update_request(id):
    record = Request.query.get(id)

    record.name = request.json["name"]
    record.company = request.json["company"]
    record.email = request.json["email"]
    record.message = request.json["message"]
    record.done = request.json["done"]

    db.session.commit()
    return request_schema.jsonify(record)

@app.route("/request/<id>", methods=["DELETE"])
def delete_request(id):
    request = Request.query.get(id)
    db.session.delete(request)
    db.session.commit()

    return "REQUEST DELETED"


if __name__ == "__main__":
    app.debug = True
    app.run()