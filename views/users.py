from flask import request
from flask_restx import Namespace, Resource

from dao.model.user import UserSchema
from implemented import user_service
from services.decorators import auth_required, admin_required

user_ns = Namespace('users')


@user_ns.route('/')
class UsersView(Resource):
    @auth_required
    def get(self):
        rs = user_service.get_all()
        res = UserSchema(many=True).dump(rs)
        return res, 200

    @auth_required
    @admin_required
    def post(self):
        req_json = request.json
        user = user_service.create(req_json)
        return "", 201, {"location": f"/movies/{user.id}"}


@user_ns.route('/<int:uid>')
class UserView(Resource):
    @auth_required
    def get(self, uid):
        r = user_service.get_one(uid)
        return UserSchema().dump(r), 200

    @auth_required
    @admin_required
    def put(self, uid):
        req_json = request.json
        if "id" not in req_json:
            req_json["id"] = uid
        user_service.update(req_json)
        return "", 204

    @auth_required
    @admin_required
    def delete(self, uid):
        user_service.delete(uid)
        return "", 204
