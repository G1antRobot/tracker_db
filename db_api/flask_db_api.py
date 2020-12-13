from flask import Flask, request, jsonify, redirect, url_for
from flask_pymongo import PyMongo
import os

#
DB_NAME = 'app.sqlite'
DB_PATH = 'data'
BASE_DIR = os.path.abspath((os.path.dirname(__file__)))

# initialize
app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb://localhost:27017/tracker_db"
app.secret_key = "*******"
#
tracker_mongo = PyMongo(app, uri="mongodb://localhost:27017/tracker_db")
subscriber_mongo = PyMongo(app, uri="mongodb://localhost:27017/subscriber_db")


@app.route("/slot_info", methods=["GET"])
def get_slot_info():
    gym_slots = tracker_mongo.db.gym_slots
    month = request.json['month']
    date_ = request.json['date']
    slot_name = request.json['slot_name']
    record = gym_slots.find_one({'month': month, 'date': date_,
                                'slot_name': slot_name})
    if record:
        return jsonify({"month": record["month"],
                        "date": record["date"],
                        "slot_name": record["slot_name"],
                        "slot_free_count": record["slot_free_count"]
                        }), 200
    else:
        return {"message": f"No data found for {month}:{date_}:{slot_name}"}, 204


@app.route("/update_slot", methods=["POST"])
def update_slot_info():
    """ Updates database with slot info"""
    gym_slots = tracker_mongo.db.gym_slots
    month = request.json['month']
    date_ = request.json['date']
    slot_name = request.json['slot_name']
    slot_free_count = request.json['slot_free_count']
    record = gym_slots.find_one({'month': month, 'date': date_,
                                'slot_name': slot_name})

    if not record:
        # new entry
        _ = gym_slots.insert({
            'month': month, 'date': date_,
            'slot_name': slot_name,
            'slot_free_count': slot_free_count})
        return jsonify({"message": "Record Updated !"}), 201
    else:
        # existing entry
        _ = gym_slots.find_one_and_replace({
                                            'month': month, 'date': date_,
                                            'slot_name': slot_name}, {
                                                'month': month, 'date': date_,
                                                'slot_name': slot_name,
                                                'slot_free_count': slot_free_count})

        return jsonify({"message": "Record Updated !"}), 200


if __name__ == "__main__":
    app.run()

