from flask import request
from flask_restx import Resource, Namespace

from forbidden import admin_required, auth_required
from models.models import Director, DirectorSchema
from setup_db import db

director_ns = Namespace('directors')

@director_ns.route('/')
class DirectorsView(Resource):
    @auth_required
    def get(self):
        rs = db.session.query(Director).all()
        res = DirectorSchema(many=True).dump(rs)
        return res, 200
    
    @admin_required
    def post(self):
        req_json = request.json
        ent = Director(**req_json)

        db.session.add(ent)
        db.session.commit()
        return "", 201


@director_ns.route('/<int:did>')
class DirectorView(Resource):
    @auth_required
    def get(self, did):
        r = db.session.query(Director).get(did)
        sm_d = DirectorSchema().dump(r)
        return sm_d, 200
        
    @admin_required
    def put(self, did):
        director = db.session.query(Director).get(did)
        req_json = request.json
        director.name = req_json.get("name")
        db.session.add(director)
        db.session.commit()
        return "", 204
    
    @admin_required
    def delete(self, did):
        director = db.session.query(Director).get(did)

        db.session.delete(director)
        db.session.commit()
        return "", 204
