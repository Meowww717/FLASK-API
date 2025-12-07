from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Resource, Api, fields, marshal_with, abort
from sqlalchemy.exc import IntegrityError

# Init app, DB, API
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)
api = Api(app)

# User model


class UserModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(80), unique=True, nullable=False)

    def __repr__(self):
        return f"User(name={self.name}, email={self.email})"


# Fields for output
userFields = {
    'id': fields.Integer,
    'name': fields.String,
    'email': fields.String
}

# Resource for all users


class Users(Resource):
    @marshal_with(userFields)
    def get(self):
        return UserModel.query.all()

    @marshal_with(userFields)
    def post(self):
        data = request.get_json()
        user = UserModel(name=data["name"], email=data["email"])
        try:
            db.session.add(user)
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            abort(400, message="Duplicate user")
        return user, 201

# Resource for single user


class User(Resource):
    @marshal_with(userFields)
    def get(self, id):
        user = UserModel.query.filter_by(id=id).first()
        if not user:
            abort(404, message="Not found")
        return user

    @marshal_with(userFields)
    def patch(self, id):
        data = request.get_json()
        user = UserModel.query.filter_by(id=id).first()
        if not user:
            abort(404, message="Not found")
        if "name" in data:
            user.name = data["name"]
        if "email" in data:
            user.email = data["email"]
        db.session.commit()
        return user

    def delete(self, id):
        user = UserModel.query.filter_by(id=id).first()
        if not user:
            abort(404, message="Not found")
        db.session.delete(user)
        db.session.commit()
        return {"message": "Deleted"}, 200


# Register endpoints
api.add_resource(Users, '/api/users/')
api.add_resource(User, '/api/user/<int:id>')

# Home route


@app.route('/')
def home():
    return '<h1>Flask Rest API</h1>'


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
