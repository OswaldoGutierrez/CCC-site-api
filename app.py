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

    def __init__(self, name, company, email, message):
        self.name = name
        self.company = company
        self.email = email
        self.message = message

class Users(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(100))
    password = db.Column(db.String(20))

    def __init__(self, username, password):
        self.username = username
        self.password = password

class RequestSchema(ma.Schema):
    class Meta:
        fields = ("id", "name", "company", "email", "message")

class UserSchema(ma.Schema):
    class Meta:
        fields = ("id", "username", "password")


request_schema = RequestSchema()
requests_schema = RequestSchema(many=True)
user_schema = UserSchema()
users_schema = UserSchema(many=True)


@app.route("/requests", methods=["GET"])
def get_requests():
    all_requests = Request.query.all()
    result = requests_schema.dump(all_requests)
    return jsonify(result)

@app.route("/users", methods=["GET"])
def get_users():
    all_users = Users.query.all()
    user = users_schema.dump(all_users)
    return jsonify(user)

@app.route("/request", methods=["POST"])
def add_request():
    name = request.json["name"]
    company = request.json["company"]
    email = request.json["email"]
    message = request.json["message"]

    new_request = Request(name, company, email, message)
    db.session.add(new_request)
    db.session.commit()

    created_request = Request.query.get(new_request.id)
    return request_schema.jsonify(created_request)

@app.route("/user", methods=["POST"])
def add_user():
    username = request.json["username"]
    password = request.json["password"]

    new_user = Users(username, password)
    db.session.add(new_user)
    db.session.commit()

    created_user = Users.query.get(new_user.id)
    return user_schema.jsonify(created_user)

@app.route("/request/<id>", methods=["PATCH"])
def update_request(id):
    record = Request.query.get(id)

    record.name = request.json["name"]
    record.company = request.json["company"]
    record.email = request.json["email"]
    record.message = request.json["message"]

    db.session.commit()
    return request_schema.jsonify(record)

@app.route("/request/<id>", methods=["DELETE"])
def delete_request(id):
    request = Request.query.get(id)
    db.session.delete(request)
    db.session.commit()

    return "REQUEST DELETED"

@app.route("/user/<id>", methods=["DELETE"])
def delete_user(id):
    user = Users.query.get(id)
    db.session.delete(user)
    db.session.commit()

    return "USER DELETED"

@app.route("/mailer", methods=["POST"])
def send_email(sent_from):
    sent_from = request.json["sent_from"]


    return requests.post(
	"https://api.mailgun.net/v3/sandboxa406895a820248c3a4d0dea031b4231f.mailgun.org/messages",
	auth=("api", "6dadd9f35f072cf9b428415fc26404e8-f696beb4-caf3df00"),
	data={"from": f"{sent_from}",
		"to": ["oswaldogutierrez218@gmail.com", "sandboxa406895a820248c3a4d0dea031b4231f.mailgun.org"],
		"subject": "Sent From Request",
		"text": "1 New Request"})


if __name__ == "__main__":
    app.debug = True
    app.run()