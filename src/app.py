"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_cors import CORS
from utils import APIException, generate_sitemap
from datastructures import FamilyStructure
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False
CORS(app)

# create the jackson family object
jackson_family = FamilyStructure("Jackson")

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/members', methods=['GET'])
def handle_hello():
    members = jackson_family.get_all_members()
    return jsonify(members), 200

@app.route('/member/<int:member_id>', methods=['GET'])
def get_member(member_id):
    member = jackson_family.get_member(member_id)
    if member:
        return jsonify(member), 200
    else:
        return jsonify({"message": "Member not found"}), 404

@app.route('/member', methods=['POST'])
def add_member():
    request_data = request.get_json()
    member = {
        "first_name": request_data['first_name'],
        "age": request_data['age'],
        "lucky_numbers": request_data['lucky_numbers'],
    }
    member_generated = jackson_family.add_member(member)
    return jsonify(member_generated), 200

@app.route('/member/<int:member_id>', methods=['DELETE'])
def delete_member(member_id):
    result = jackson_family.delete_member(member_id)
    if result:
        return jsonify({"done": True}), 200
    else:
        return jsonify({"message": "Member not found"}), 404

@app.route('/member/<int:member_id>', methods=['PUT'])
def update_member(member_id):
    request_data = request.get_json()
    member = {
        "first_name": request_data.get('first_name'),
        "age": request_data.get('age'),
        "lucky_numbers": request_data.get('lucky_numbers'),
    }
    updated_member = jackson_family.update_member(member_id, member)
    if updated_member:
        return jsonify(updated_member), 200
    else:
        return jsonify({"message": "Member not found"}), 404

# this only runs if $ python src/app.py is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=True)