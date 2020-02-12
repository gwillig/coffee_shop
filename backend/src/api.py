from __future__ import absolute_import
import os
from flask import Flask, request, jsonify, abort
from sqlalchemy import exc
import json
import jwt
from flask_cors import CORS


from database.models import db_drop_and_create_all, setup_db, Drink
from auth.auth import AuthError, requires_auth,get_token_auth_header

def create_app():
    app = Flask(__name__)
    db = setup_db(app)
    CORS(app)


    ## ROUTES

    @app.route('/drinks', methods=['GET'])
    def drinks():
        result = db.session.query(Drink).all()
        result_list = [el.short() for el in result]
        print(result_list)
        return jsonify({
            'success': True,
            'drinks': result_list
        })


    @app.route('/drinks-detail',methods=['GET'])
    @requires_auth('get:drinks-detail')
    def drinks_details(payload):
        result = db.session.query(Drink).all()
        result_list = [el.long() for el in result]
        print(result_list)
        return jsonify({
            'success': True,
            'drinks': result_list
        })

    @app.route('/drinks',methods=['POST'])
    @requires_auth('post:drinks')
    def create_drink(payload):
        try:
            body = request.get_json()
            new_drink = Drink(title=body['title'], recipe=json.dumps(body['recipe']))
            db.session.add(new_drink)
            db.session.commit()
        except:
            db.session.rollback()
            db.session.close()
        return jsonify({
        'success': True,
        'drinks': new_drink.long()
        })


    @app.route('/drinks/<int:drink_id>',methods=['Patch'])
    @requires_auth('patch:drinks')
    def patch_drink(payload,drink_id):
        try:
            body = request.get_json()
            drinkObj = db.session.query(Drink).filter_by(id=drink_id).first()
            drinkObj.title=body['title']
            drinkObj.recipe=json.dumps(body['recipe'])
            db.session.add(drinkObj)
            db.session.commit()
        except:
            db.session.rollback()
            db.session.close()
        return jsonify({
        'success': True,
        'drinks': drinkObj.long()
        })

    @app.route('/drinks/<int:drink_id>',methods=['Delete'])
    @requires_auth('delete:drinks')
    def delete_drink(payload,drink_id):
        try:
            drinkObj = db.session.query(Drink).filter_by(id=drink_id).first().delete()
            db.session.commit()
            return jsonify({
                'success': True,
                'drinks': drinkObj.id
            },200)
        except:
            basequey =  db.session.query(Drink).filter_by(id=drink_id)
            db.session.rollback()
            db.session.close()
            if basequey.count() == 0:
                abort(404, {'message': f'Drink with id {drink_id} not found in database.'})

    ## Error Handling

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
                        "success": False,
                        "error": 422,
                        "message": "unprocessable"
                        }), 422


    def custom_error_msg(error,default_text):
        if 'description' in error.keys():
            return error['description']
        else:
            return default_text

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            "success":False,
            "error":404,
            "message":custom_error_msg(error,"not found")

        })

    @app.errorhandler(AuthError)
    def auth_Error(authError):
        return jsonify({
            "success": False,
            "error": authError.status_code,
            "message": custom_error_msg(authError.error, "error occure durcing authentification ")
        }), 401
    return app

if __name__ == '__main__':
    create_app().run(debug=True)