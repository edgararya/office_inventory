from flask import Flask, request, jsonify, Response
from pymongo import MongoClient
from bson import ObjectId, json_util
import json

app = Flask(__name__)

MONGO_URI = "mongodb://localhost:27017/"
DB_NAME = "office_inventory"
COLLECTION_NAME = "items"

client = MongoClient(MONGO_URI)
db = client[DB_NAME]
collection = db[COLLECTION_NAME]
categories_collection = db['categories']

print(f"Connected to MongoDB: {DB_NAME} -> {COLLECTION_NAME}")

@app.route('/items', methods=['GET'])
def get_items():
    try:
        category = request.args.get('category')
        query = {}
        
        if category:
            query['category_code'] = category

        items = list(collection.find(query).sort("_id", -1))

        return Response(json_util.dumps(items), mimetype='application/json'), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/items', methods=['POST'])
def add_item():
    try:
        data = request.json
        if not data:
            return jsonify({"message": "No data provided"}), 400
        
        if 'item_name' not in data:
            return jsonify({"message": "Field 'item_name' is required"}), 400

        if 'category_code' in data:
            cat = categories_collection.find_one({"code": data['category_code']})
            if cat:
                data['category_id'] = cat['_id']
            else:
                return jsonify({"message": "Invalid category_code not found in DB"}), 400

        result = collection.insert_one(data)
        
        return jsonify({
            "message": "Item added successfully", 
            "id": str(result.inserted_id)
        }), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/items/<id>', methods=['PUT'])
def update_item(id):
    try:
        data = request.json

        result = collection.update_one(
            {"_id": ObjectId(id)}, 
            {"$set": data}
        )
        
        if result.matched_count > 0:
            return jsonify({"message": "Item updated successfully"}), 200
        else:
            return jsonify({"message": "Item not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/items/<id>', methods=['DELETE'])
def delete_item(id):
    try:
        result = collection.delete_one({"_id": ObjectId(id)})
        
        if result.deleted_count > 0:
            return jsonify({"message": "Item deleted successfully"}), 200
        else:
            return jsonify({"message": "Item not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/check')
def health_check():
    return jsonify({"status": "ok", "db": DB_NAME}), 200

if __name__ == '__main__':
    app.run(debug=True, port=5000, host='0.0.0.0')
