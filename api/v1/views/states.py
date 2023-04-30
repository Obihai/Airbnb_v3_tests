from flask import abort, jsonify, make_response, request
from api.v1.views import app_views
from models import storage
from models.state import State


@app_views.route('/states', methods=['GET'], strict_slashes=False)
def get_states():
    """Retrieves the list of all State objects"""
    states = storage.all(State).values()# Convert the list of State objects to a list of dictionaries representing each State object's attributes
    return jsonify([state.to_dict() for state in states])# Return the list of State objects in JSON format


@app_views.route('/states/<state_id>', methods=['GET'], strict_slashes=False)
def get_state(state_id):
    """Retrieves a State object based on its ID"""
    # Using the storage engine to get the State object with the given ID
    state = storage.get(State, state_id)
    # If the state object is not found, return a 404 error message
    if not state:
        abort(404)
    # If the state object is found, return a JSON representation of its dictionary
    return jsonify(state.to_dict())


@app_views.route('/states/<state_id>', methods=['DELETE'], strict_slashes=False)
def delete_state(state_id):
    """Removes a State object from the database"""

    # Retrieve the State object with the given state_id from the database
    state = storage.get(State, state_id)

    # If the State object does not exist, return a 404 error
    if not state:
        abort(404)

    # Delete the State object from the database
    state.delete()

    # Save the changes to the database
    storage.save()

    # Return an empty JSON response with a 200 status code
    return make_response(jsonify({}), 200)


@app_views.route('/states', methods=['POST'], strict_slashes=False)
def create_state():
    """Endpoint to create a new State object"""

    # Check if request data is in JSON format
    if not request.is_json:
        abort(400, "Not a JSON")

    # Get JSON data from the request
    data = request.get_json()

    # Check if the 'name' key is in the JSON data
    if 'name' not in data:
        abort(400, "Missing name")

    # Create a new State object with the data from the request
    state = State(**data)

    # Add the new State object to the storage
    storage.new(state)

    # Save the changes to the storage
    storage.save()

    # Return a JSON response with the new State object and a 201 status code
    return make_response(jsonify(state.to_dict()), 201)


def update_state(state_id):
    """Updates a State object"""
    # get the State object with the given state_id from the storage
    state = storage.get(State, state_id)
    # If the state_id is not found in the storage, we return a 404 Not Found error using Flask's abort function
    if not state:
        abort(404)

    # If the request data is not in JSON format, we return a 400 Bad Request error using Flask's abort function
    if not request.is_json:
        abort(400, "Not a JSON")

    # If the request data is in JSON format, we get the data as a dictionary
    data = request.get_json()

    # update the State object with the new data using the setattr function
    # only update the attributes that are in the request data and not the reserved attributes (id, created_at, updated_at)
    for key, value in data.items():
        if key not in ('id', 'created_at', 'updated_at'):
            setattr(state, key, value)

    # save the updated State object to the storage
    storage.save()

    # return a Flask Response object with the updated State object as a JSON string and a 200 OK status code
    return make_response(jsonify(state.to_dict()), 200)
