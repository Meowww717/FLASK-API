# FLASK-API

This is a simple REST API built with **Flask**, **Flask-RESTful**, and **Flask-SQLAlchemy**.  
It provides basic CRUD operations for a `User` model with `id`, `name`, and `email`.

## Features

- Get all users
- Get a single user by ID
- Create a new user
- Update user data (PATCH)
- Delete a user

## Requirements

- Python 3.x
- Flask
- Flask-RESTful
- Flask-SQLAlchemy

## Run the project

py api.py

The API will be available at: http://127.0.0.1:5000/

## API Endpoints

Users
GET /api/users/ → Get all users

POST /api/users/ → Create a new user (JSON body: { "name": "...", "email": "..." })

User by ID
GET /api/user/<id> → Get user by ID

PATCH /api/user/<id> → Update user (JSON body can include name and/or email)

DELETE /api/user/<id> → Delete user

## Database

The project uses SQLite (database.db). Tables are created automatically when you run the app.
