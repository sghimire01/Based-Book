from flask import Flask, jsonify, request, session, redirect
from passlib.hash import pbkdf2_sha256
from werkzeug.utils import redirect
from app import db
import uuid

class User:

    def start_session(self, user):
        del user['password']
        session['logged_in'] = True
        session['user'] = user
        return jsonify(user), 200

    def signup(self):
        print(request.form)

        #form info for user
        user = {
            "_id": uuid.uuid4().hex,
            "username": request.form.get('username'),
            "name": request.form.get('name'),
            "email": request.form.get('email'),
            "password": request.form.get('password')
        }
        
        #password encryption
        user['password'] = pbkdf2_sha256.encrypt(user['password'])

        #database stuff
        if db.users.find_one({"email": user['email']}):
            return jsonify({ "error": "That email is taken. Try another."}), 400

        if db.users.insert_one(user):
           return self.start_session(user)

        return jsonify({"error": "Signup failed"}), 400


    def signout(self):
        session.clear()
        return redirect('/')

    def signin(self):
        user = db.users.find_one({
            "username": request.form.get('username')
        })

        if user and pbkdf2_sha256.verify(request.form.get('password'), user['password']):
            return self.start_session(user)
        
        return jsonify({"error": "username or password is incorrect"}), 401
