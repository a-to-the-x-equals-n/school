from flask import request, jsonify
from flask_jwt_extended import jwt_required # get_jwt_identity : useful to get user ID as a search parameter
from config import app


''' POST functions '''

# LOGIN
@app.route('/login', methods = ['POST'])
def login():

    # NOTE: Endpoint to handle login requests. Validates credentials and returns a JWT token for authorized users.

    jwt_token, status = "", ""
    return jsonify(jwt_token), status

# NEW USER
@app.route('/new_user', methods = ['POST'])
def new_user():

    # NOTE: Endpoint to register a new user. Handles POST requests to create a user-specific account.

    response, status = "", ""
    return jsonify(response), status

@app.route('/POST', methods = ['POST'])
@jwt_required
def post():
    # NOTE: Endpoint to handle POST requests

    response, status = "", ""
    return jsonify(response), status


''' GET functions '''

@app.route('/GET', methods = ['GET'])
@jwt_required()
def get():
    # NOTE: Endpoint to handle GET requests
    pass


''' PUT functions '''

@app.route('/PUT', methods = ['PUT'])
@jwt_required()
def put():
    # NOTE: Endpoint to handle PUT requests
    pass


''' DELETE functions '''

@app.route('/DEL', methods = ['DELETE'])
@jwt_required()
def delete():
    # NOTE: Endpoint to handle DELETE requests
    pass


''' PATCH functions '''

@app.route('/PATCH', methods = ['PATCH'])
@jwt_required()
def patch():
    # NOTE: Endpoint to handle PATCH requests
    pass



if __name__ == '__main__':
    app.run(host = "0.0.0.0", port = 5000, debug = True)
    

    