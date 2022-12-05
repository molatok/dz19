import hashlib
import json

from flask import request
from flask_restx import Resource, Namespace
from models.models import User, UserSchema
from setup_db import db

user_ns = Namespace('users')


@user_ns.route('/')
class UsersView(Resource):
    def get(self):
        rs = db.session.query(User).all()
        res = UserSchema(many=True).dump(rs)
        return res, 200
    
    def post(self):
        req_json = request.json
        ent = User(**req_json)
        db.session.add(ent)
        db.session.commit()
        return "", 201
        
    def get_hash(self):
        return hashlib.md5(self.password.encode('utf-8')).hexdigest()
      

@user_ns.route('/<int:uid>')
class UserView(Resource):
    def get(self, uid):
        r = db.session.query(User).get(uid)
        sm_d = UserSchema().dump(r)
        return sm_d, 200
    
    def put(self, bid):
        user = db.session.query(User).get(bid)
        req_json = request.json
        user.username = req_json.get("username")
        user.password = req_json.get("password")
        user.role = req_json.get("role")
        db.session.add(user)
        db.session.commit()
        return "", 204
    
    
    
    
