"""Small apps to demonstrate endpoints with basic feature - CRUD in MongoDB"""
import os
from flask import Flask, request, jsonify
from pymongo import MongoClient
from dotenv import load_dotenv
from bson import ObjectId, json_util

# Load environment variables from the .env file
load_dotenv()
app = Flask(__name__)

# Konfigurasi Koneksi
# Pastikan di file .env isinya: MONGO_URI=mongodb://localhost:27017/
mongodb_connection_addr = os.environ.get("MONGO_URI", "mongodb://localhost:27017/")
db_name = os.environ.get("DB_NAME", "db_inventory_management") # Default ke Inventory

# Connect to MongoDB
print(f'Connecting to MongoDB at {mongodb_connection_addr}...')
try:
    client = MongoClient(mongodb_connection_addr)
    db = client[db_name]    # Menggunakan database 'db_inventory_management'
    collection = db['items'] # Menggunakan collection 'items'
    print(f"--> Berhasil terkoneksi ke Database: {db_name}")
    print(f"--> Menggunakan Collection: items")
except Exception as e:
    print(f"Error connecting to MongoDB: {e}")

# --- ROUTES API ---

# 1. Test API Health
@app.route('/check')
def check_connection():
    """Endpoint untuk cek koneksi database"""
    try:
        client.admin.command('ping')
        return jsonify({
            "status": "success",
            "message": "MongoDB connection is healthy.",
            "database": db_name
        })
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

# 2. Create (Tambah Barang)
@app.route('/create', methods=['POST'])
def create():
    """Endpoint untuk input barang baru"""
    data = request.get_json()

    # Validasi sederhana
    if not data:
        return jsonify({"message": "No data provided"}), 400

    try:
        # Insert data into MongoDB
        result = collection.insert_one(data)
        return jsonify({
            "message": "Barang berhasil ditambahkan", 
            "id": str(result.inserted_id)
        }), 201
    except Exception as e:
        return jsonify({"message": f"Gagal menambah data: {e}"}), 500

# 3. Read (Lihat Semua Barang)
@app.route('/read', methods=['GET'])
def read():
    """Endpoint untuk melihat semua data barang"""
    try:
        # Ambil semua data, urutkan dari yang terbaru (_id desc)
        records = collection.find().sort("_id", -1)
        
        # Bersihkan format data agar _id menjadi string (supaya rapi di Postman)
        data = []
        for doc in records:
            doc['_id'] = str(doc['_id'])
            data.append(doc)

        return jsonify(data), 200
    except Exception as e:
        return jsonify({"message": f"Error fetch data: {e}"}), 500

# 4. Update (Edit Stok/Lokasi/Info)
@app.route('/update/<id>', methods=['PUT'])
def update(id):
    """Endpoint untuk update data berdasarkan ID"""
    data = request.get_json()
    print(f'Updating item _id : {id}')
    
    try:
        # Update data in MongoDB
        # Menggunakan ObjectId(id) untuk mencari dokumen yang tepat
        result = collection.update_one({"_id": ObjectId(id)}, {"$set": data})
        
        if result.matched_count > 0:
            return jsonify({"message": "Data barang berhasil diupdate"}), 200
        else:
            return jsonify({"message": "ID tidak ditemukan"}), 404
    except Exception as e:
        return jsonify({"message": f"Gagal update: {e}"}), 400

# 5. Delete (Hapus Barang)
@app.route('/delete/<id>', methods=['DELETE'])
def delete(id):
    """Endpoint untuk hapus data berdasarkan ID"""
    try:
        result = collection.delete_one({"_id": ObjectId(id)})
        
        if result.deleted_count > 0:
            return jsonify({"message": "Barang berhasil dihapus"}), 200
        else:
            return jsonify({"message": "ID tidak ditemukan"}), 404
    except Exception as e:
        return jsonify({"message": f"Gagal hapus: {e}"}), 400

if __name__ == '__main__':
    # Menjalankan aplikasi di port 5000
    app.run(debug=True, port=5000)