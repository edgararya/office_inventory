# Office Inventory Management System (Project UAS)

This project is a simple backend API for managing office inventory, created as a Database Final Exam (UAS) assignment. The application is built using Flask (Python) and MongoDB.

## 👥 Group 3 Members (Class SI 3C)

1. **Gede Edgar Arya Saputra** (2415091126)
2. **Made Martha Thalia Sukmawan** (2415091104)
3. **I Gede Radheya Devananda** (2415091105)

🎥 **Demo Video Link:** [https://youtu.be/TH2KTZIeFUM](https://youtu.be/TH2KTZIeFUM)

---

## 🛠️ Prerequisites

Before running the application, ensure you have installed:
- **Python 3.x**: [Download Python](https://www.python.org/downloads/)
- **MongoDB**: Make sure the MongoDB service is running at `localhost:27017`.

## 📦 Installation

1. **Clone this repository** (if using git) or extract the folder zip.

2. **Create a Virtual Environment (Optional but recommended):**
   ```bash
   python -m venv venv
   # Windows
   venv\Scripts\activate
   # Linux/Mac
   source venv/bin/activate
   ```

3. **Install Dependencies:**
   Run the following command in the terminal:
   ```bash
   pip install -r requirements.txt
   ```

## 🚀 Running the Application

1. Ensure MongoDB is running.
2. Run the Flask application:
   ```bash
   python app.py
   ```
   The application will run at `http://0.0.0.0:5000`.

## 📚 API Documentation

Here is the list of available endpoints:

### 1. Server Health Check
- **URL:** `/check`
- **Method:** `GET`
- **Description:** Verifies that the server and database connection are running.

### 2. Get All Items
- **URL:** `/items`
- **Method:** `GET`
- **Query Params:** `category` (optional, e.g., `?category=ATK`)
- **Description:** Retrieves a list of all inventory items.

### 3. Add New Item
- **URL:** `/items`
- **Method:** `POST`
- **Body (JSON):**
  ```json
  {
      "item_name": "Black Marker",
      "category_code": "ATK",
      "stock": 10
  }
  ```
- **Description:** Adds a new item. Note: `category_code` will be validated against the `categories` collection.

### 4. Update Item
- **URL:** `/items/<id>`
- **Method:** `PUT`
- **Body (JSON):** Data to update.
  ```json
  {
      "item_name": "Permanent Black Marker",
      "stock": 15
  }
  ```

### 5. Delete Item
- **URL:** `/items/<id>`
- **Method:** `DELETE`
- **Description:** Deletes an item based on ID.

## 📝 Additional Notes
- The application connects to the `office_inventory` database at `mongodb://localhost:27017/` by default.
- An `office_inventory_api.postman_collection.json` file is included and can be imported into Postman for easier API testing.
