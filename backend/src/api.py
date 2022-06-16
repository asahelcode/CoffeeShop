import os
from flask import Flask, request, jsonify, abort
from sqlalchemy import exc
import json
from flask_cors import CORS

from .database.models import db_drop_and_create_all, setup_db, Drink
from .auth.auth import AuthError, requires_auth

app = Flask(__name__)
setup_db(app)
CORS(app)

"""
@TODO uncomment the following line to initialize the datbase
!! NOTE THIS WILL DROP ALL RECORDS AND START YOUR DB FROM SCRATCH
!! NOTE THIS MUST BE UNCOMMENTED ON FIRST RUN
!! Running this funciton will add one
"""
# db_drop_and_create_all()

# ROUTES


@app.route("/drinks", methods=["GET"])
def drink_list():
    # Get all the drinks from db
    """
        @TODO implement endpoint
            GET /drinks
                it should be a public endpoint
                it should contain only the drink.short() data representation
            returns status code 200 and json {"success": True, "drinks": drinks} where drinks is the list of drinks
                or appropriate status code indicating reason for failure
    """
    drinks = Drink.query.all()
    return jsonify({"success": True, "drinks": [d.short() for d in drinks]}), 200


@app.route("/drinks-detail", methods=["GET"])
@requires_auth("get:drinks-detail")
def drink_list_detail(payload):
    """
    @TODO implement endpoint
        GET /drinks-detail
            it should require the 'get:drinks-detail' permission
            it should contain the drink.long() data representation
        returns status code 200 and json {"success": True, "drinks": drinks} where drinks is the list of drinks
            or appropriate status code indicating reason for failure
    """
    # Get all the drinks from db
    drinks = Drink.query.all()
    return jsonify({"success": True, "drinks": [d.long() for d in drinks]}), 200


@app.route("/drinks", methods=["POST"])
@requires_auth("post:drinks")
def drink_create(payload):
    """
    @TODO implement endpoint
        POST /drinks
            it should create a new row in the drinks table
            it should require the 'post:drinks' permission
            it should contain the drink.long() data representation
        returns status code 200 and json {"success": True, "drinks": drink} where drink an array containing only the newly created drink
            or appropriate status code indicating reason for failure
    """
    # Get the body
    body = request.get_json()
    try:
        # Prepare Drink for DB
        drink = Drink(title=body.get("title"), recipe=json.dumps(body.get("recipe")))
        # Commit to DB
        drink.insert()

    except Exception:
        abort(400)

    return jsonify({"success": True, "drinks": [drink.long()]})


@app.route("/drinks/<int:id>", methods=["PATCH"])
@requires_auth("patch:drinks")
def drink_update(payload, id):
    """
    @TODO implement endpoint
        PATCH /drinks/<id>
            where <id> is the existing model id
            it should respond with a 404 error if <id> is not found
            it should update the corresponding row for <id>
            it should require the 'patch:drinks' permission
            it should contain the drink.long() data representation
        returns status code 200 and json {"success": True, "drinks": drink} where drink an array containing only the updated drink
            or appropriate status code indicating reason for failure
    """
    # Get the body
    body = request.get_json()

    # Get the Drink with requested Id
    drink = Drink.query.filter(Drink.id == id).one_or_none()

    # abort, drink not found
    if not drink:
        abort(404)

    try:

        title = body.get("title")
        recipe = body.get("recipe")

        # check if we should update title
        if title:
            drink.title = title

        # check if we should update recipe
        if recipe:
            drink.recipe = json.dumps(body.get("recipe"))

        # update the drink
        drink.update()
    except Exception:
        abort(400)

    return jsonify({"success": True, "drinks": [drink.long()]}), 200


@app.route("/drinks/<int:id>", methods=["DELETE"])
@requires_auth("delete:drinks")
def drink_delete(payload, id):
    """
    @TODO implement endpoint
        DELETE /drinks/<id>
            where <id> is the existing model id
            it should respond with a 404 error if <id> is not found
            it should delete the corresponding row for <id>
            it should require the 'delete:drinks' permission
        returns status code 200 and json {"success": True, "delete": id} where id is the id of the deleted record
            or appropriate status code indicating reason for failure
    """
    # Get the Drink with requested Id
    drink = Drink.query.filter(Drink.id == id).one_or_none()

    # abort when drink not found
    if not drink:
        abort(404)

    try:
        # delete the drink
        drink.delete()
    except Exception:
        abort(400)

    return jsonify({"success": True, "delete": id}), 200


# Error Handling
@app.errorhandler(404)
def not_found_error(error):
    return jsonify({"success": False, "error": 404, "message": "Not Found!!!"}), 404


@app.errorhandler(406)
def not_found_error(error):
    return (
        jsonify({"success": False, "error": 406, "message": "Not Acceptable!!!"}),
        406,
    )


@app.errorhandler(422)
def unprocessable_error(error):
    return (
        jsonify(
            {"success": False, "error": 422, "message": "Request Unprocessable!!!"}
        ),
        422,
    )


@app.errorhandler(400)
def bad_request_error(error):
    return (jsonify({"success": False, "error": 400, "message": "Bad request!!!"}), 400)


@app.errorhandler(500)
def server_error(error):
    return (
        jsonify({"success": False, "error": 500, "message": "Server Error!!!"}),
        500,
    )


@app.errorhandler(AuthError)
def auth_error(error):
    """
    @DONE implement error handler for AuthError
        error handler should conform to general task above
    """
    return (
        jsonify(
            {
                "success": False,
                "error": error.status_code,
                "message": error.error.get("description"),
            }
        ),
        error.status_code,
    )
