from flask import Flask, request, jsonify
from flask_cors import CORS
import mysql.connector
from dotenv import load_dotenv
import os
import logging
from mysql.connector import Error

# Load environment variables from .env file
load_dotenv()
app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "*"}})

# MySQL Connection using environment variables
logging.basicConfig(level=logging.DEBUG)

def connect_to_database():
    host = os.getenv("DB_HOST", "").strip()
    port = os.getenv("DB_PORT", "").strip()
    user = os.getenv("DB_USER", "").strip()
    password = os.getenv("DB_PASSWORD", "").strip()
    db_name = os.getenv("DB_NAME", "").strip()
    
    print(f"--- DATABASE CONNECTION ATTEMPT ---")
    print(f"Host: {host}:{port}")
    print(f"User: {user}")
    
    # Try multiple times if it's just a cold-start/network flicker
    max_retries = 2
    for attempt in range(max_retries + 1):
        try:
            db = mysql.connector.connect(
                host=host,
                user=user,
                password=password,
                database=db_name,
                port=int(port) if port else 3306,
                # Aiven specific SSL requirements
                ssl_mode='REQUIRED',
                connection_timeout=15
            )
            logging.info("Database connection successful ✅")
            return db
        except Error as err:
            if attempt < max_retries:
                print(f"⚠️ Attempt {attempt + 1} failed ( {err} ), retrying in 2s...")
                import time
                time.sleep(2)
            else:
                print(f"❌ DATABASE CONNECTION FAILED after {max_retries} retries: {err}")
                import traceback
                logging.error(traceback.format_exc())
                return None

def init_db(db):
    if not db:
        return
    try:
        cursor = db.cursor()
        # Create users table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INT AUTO_INCREMENT PRIMARY KEY,
                email VARCHAR(255) UNIQUE NOT NULL,
                password VARCHAR(255) NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        # Create favorites table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS favorites (
                id INT AUTO_INCREMENT PRIMARY KEY,
                user_id INT NOT NULL,
                movie_id INT NOT NULL,
                title VARCHAR(255) NOT NULL,
                poster_path VARCHAR(255),
                UNIQUE KEY unique_fav (user_id, movie_id),
                FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
            )
        """)
        db.commit()
        logging.info("Database tables initialized successfully")
    except Error as err:
        logging.error(f"Error initializing database tables: {err}")

db = connect_to_database()
if db:
    init_db(db)
    cursor = db.cursor(dictionary=True)
else:
    logging.error("Database connection not established. Tables not initialized.")

@app.route("/api/test", methods=["GET"])
def test():
    return jsonify({"message": "Backend running successfully"})

@app.route("/api/health", methods=["GET"])
def health():
    return jsonify({"status": "ok"}), 200


# REGISTER API
@app.route("/api/register", methods=["POST"])
def register():
    # Ensure cursor exists
    global cursor
    if not db:
        return jsonify({"message": "Database not connected"}), 500
    
    data = request.get_json()
    email = data.get("email")
    password = data.get("password")

    if not email or not password:
        return jsonify({"message": "Email and password required"}), 400

    # Ensure cursor is available
    if not db.is_connected():
        db.reconnect()

    cursor = db.cursor(dictionary=True)
    
    # Check if user already exists
    cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
    existing_user = cursor.fetchone()

    if existing_user:
        return jsonify({"message": "User already exists"}), 400

    # Insert new user
    cursor.execute(
        "INSERT INTO users (email, password) VALUES (%s, %s)",
        (email, password)
    )
    db.commit()

    return jsonify({
        "message": "User registered successfully",
        "user": {
            "email": email
        }
    }), 201


# LOGIN API
@app.route("/api/login", methods=["POST"])
def login():
    global cursor
    if not db:
        return jsonify({"message": "Database not connected"}), 500
        
    data = request.get_json()
    email = data.get("email")
    password = data.get("password")

    if not email or not password:
        return jsonify({"message": "Email and password required"}), 400

    if not db.is_connected():
        db.reconnect()
    
    cursor = db.cursor(dictionary=True)
    cursor.execute(
        "SELECT * FROM users WHERE email = %s AND password = %s",
        (email, password)
    )
    user = cursor.fetchone()

    if not user:
        return jsonify({"message": "Invalid email or password"}), 401

    return jsonify({
        "message": "Login successful",
        "user": {
            "id": user["id"],
            "email": user["email"]
        }
    }), 200

# ADD FAVORITE
@app.route("/api/favorites/add", methods=["POST"])
def add_favorite():
    if not db:
        return jsonify({"message": "Database not connected"}), 500
        
    data = request.get_json()
    user_id = data.get("user_id")
    movie_id = data.get("movie_id")
    title = data.get("title")
    poster_path = data.get("poster_path")

    if not user_id or not movie_id:
        return jsonify({"message": "Missing data"}), 400

    try:
        if not db.is_connected():
            db.reconnect()
        cursor = db.cursor()
        cursor.execute(
            "INSERT INTO favorites (user_id, movie_id, title, poster_path) VALUES (%s, %s, %s, %s)",
            (user_id, movie_id, title, poster_path)
        )
        db.commit()
        return jsonify({"message": "Favorite added successfully"}), 201
    except mysql.connector.Error:
        return jsonify({"message": "Already in favorites"}), 200


# GET USER FAVORITES
@app.route("/api/favorites/<int:user_id>", methods=["GET"])
def get_favorites(user_id):
    if not db:
        return jsonify({"message": "Database not connected"}), 500
        
    if not db.is_connected():
        db.reconnect()
    cursor = db.cursor(dictionary=True)
    cursor.execute(
        "SELECT movie_id, title, poster_path FROM favorites WHERE user_id = %s",
        (user_id,)
    )
    favorites = cursor.fetchall()
    return jsonify(favorites), 200


# REMOVE FAVORITE
@app.route("/api/favorites/remove", methods=["POST"])
def remove_favorite():
    if not db:
        return jsonify({"message": "Database not connected"}), 500
        
    data = request.get_json()
    user_id = data.get("user_id")
    movie_id = data.get("movie_id")

    if not db.is_connected():
        db.reconnect()
    cursor = db.cursor()
    cursor.execute(
        "DELETE FROM favorites WHERE user_id = %s AND movie_id = %s",
        (user_id, movie_id)
    )
    db.commit()

    return jsonify({"message": "Favorite removed"}), 200

@app.route('/test-db')
def test_db():
    try:
        test_db = mysql.connector.connect(
            host=os.getenv("DB_HOST"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            database=os.getenv("DB_NAME"),
            port=int(os.getenv("DB_PORT", 3306)),
            ssl_disabled=False
        )
        if test_db.is_connected():
            test_db.close()
            return "Database connection successful", 200
    except mysql.connector.Error as err:
        return f"Database connection failed: {err}", 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)