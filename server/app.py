from flask import Flask, request, make_response, jsonify
from flask_cors import CORS
from flask_migrate import Migrate

from models import db, Message

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

CORS(app)
migrate = Migrate(app, db)

db.init_app(app)

@app.route('/messages', methods=['GET', 'POST'])
def messages():
    if request.method =='GET':
        messages = Message.query.order_by('created_at').all()
        # retrieve all Message objects from the database and order them by created_at field

        response = make_response(
            # create a JSON response containing a list of dictionaries with each Message object's attributes
            jsonify([message.to_dict() for message in messages]),
            200,
            # and set the HTTP status code to 200 (OK)
        )
    elif request.method == 'POST':
        data = request.get_json()
        # retrieve the JSON data from the request body
        message = Message(
            body=data['body'],
            username=data['username']
            # create a new Message object with the body and username attributes from the JSON data
        )

        # add the new Message object to the session and commit changes to the database
        db.session.add(message)
        db.session.commit()

        response = make_response(
            jsonify(message.to_dict()),
            # create a JSON response containing the new Message object's attributes
            201,
            # and set the HTTP status code to 201 (Created)
        )

    # return the response object
    return response



@app.route('/messages/<int:id>', methods=['PATCH', 'DELETE'])
def messages_by_id(id):
    message = Message.query.filter_by(id=id).first()
    # retrieve the Message object with the given id from the database

    if request.method == 'PATCH':
        data = request.get_json()
        # retrieve the JSON data from the request body
        for attr in data:
            setattr(message, attr, data[attr])
        # update the Message object's attributes based on the JSON data

        db.session.add(message)
        db.session.commit()
        # add the updated Message object to the session and commit changes to the database

        response = make_response(
            jsonify(message.to_dict()),
            # create a JSON response containing the updated Message object's attributes
            200,
            # create a JSON response containing the updated Message object's attributes
        )

    elif request.method == 'DELETE':
        db.session.delete(message)
        db.session.commit()
        # delete the Message object from the session and commit changes to the database

        response = make_response(
            jsonify({'deleted': True}),
            # create a JSON response indicating that the Message object was deleted
            200,
            # and set the HTTP status code to 200 (OK)
        )

    return response
    # return the response object

if __name__ == '__main__':
    app.run(port=5555)
