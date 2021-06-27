from flask import Flask, jsonify, abort, request
from flask_pymongo import PyMongo
from bson import ObjectId
from bson.json_util import dumps


app = Flask(__name__)

app.config["MONGO_URI"] = "" #link_"__"
mongo = PyMongo(app)




@app.route('/add_todo', methods=["POST"])
def add_todo():   # why ?(____)
    if not request.json:
        abort(500)

    name = request.json.get("name", None)
    title = request.json.get("title", None)
    desc = request.json.get("desc", None)

    if name is None or title is None or desc is  None:
         return jsonify(message="Invalid Request") , 500 

    tasks = mongo.db.TEST.insert_one({
        "name" : name,
        "title" : title,
        "desc" : desc
    }).inserted_id
    return jsonify(str(tasks)) 

@app.route("/rd_todo/<string:id>", methods=["GET"])
def get_todo(id):
    q = mongo.db.TEST.find({
        "_id" : ObjectId(id)
    })  
    tasks = []
    for x in q:
        x["_id"] = str(x["_id"])
        tasks.append(x)
    return jsonify(str(tasks)) 


@app.route("/up_todo/<string:id>", methods=['PUT'])
def update_todo(id):

    if not request.json:
        abort(500)

    name = request.json.get("name")
    title = request.json.get("title", None)
    desc = request.json.get("desc", "")

    update_json = {}

    if name is not None:
        update_json["name"] = name 

    if title is not None:
        update_json["title"] = title

    if desc is not None:
        update_json["desc"] = desc
    
    tasks = mongo.db.TEST.update({
        "_id": ObjectId(id)
    },{
        "$set": update_json
    }, upsert=False)
    return jsonify(str(tasks)) 

    
    



@app.route("/del_todo/<string:id>", methods=["DELETE"])
def delete_todo(id):

    tasks = mongo.db.TEST.remove({
        "_id" :  ObjectId(id)
    })
    return jsonify(str(tasks)) 



if __name__ == "__main__":
    app.run(debug = True)