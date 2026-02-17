from flask import Flask, request, jsonify
from flask_cors import CORS
import mysql.connector

app = Flask(__name__)
CORS(app)

# MySQL Connection (XAMPP default settings)
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",  # Default XAMPP password
    database="moviefinder_db"
)

cursor = db.cursor(dictionary=True)

@app.route("/api/test", methods=["GET"])
def test():
    return jsonify({"message": "Backend running successfully"})


# REGISTER API
@app.route("/api/register", methods=["POST"])
def register():
    data = request.get_json()
    email = data.get("email")
    password = data.get("password")

    if not email or not password:
        return jsonify({"message": "Email and password required"}), 400

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

    # Return user object (IMPORTANT for your React context)
    return jsonify({
        "message": "User registered successfully",
        "user": {
            "email": email
        }
    }), 201


# LOGIN API
@app.route("/api/login", methods=["POST"])
def login():
    data = request.get_json()
    email = data.get("email")
    password = data.get("password")

    if not email or not password:
        return jsonify({"message": "Email and password required"}), 400

    cursor.execute(
        "SELECT * FROM users WHERE email = %s AND password = %s",
        (email, password)
    )
    user = cursor.fetchone()

    if not user:
        return jsonify({"message": "Invalid email or password"}), 401

    # Return user in format your frontend expects
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
    data = request.get_json()
    user_id = data.get("user_id")
    movie_id = data.get("movie_id")
    title = data.get("title")
    poster_path = data.get("poster_path")

    if not user_id or not movie_id:
        return jsonify({"message": "Missing data"}), 400

    try:
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
    cursor.execute(
        "SELECT movie_id, title, poster_path FROM favorites WHERE user_id = %s",
        (user_id,)
    )
    favorites = cursor.fetchall()
    return jsonify(favorites), 200


# REMOVE FAVORITE
@app.route("/api/favorites/remove", methods=["POST"])
def remove_favorite():
    data = request.get_json()
    user_id = data.get("user_id")
    movie_id = data.get("movie_id")

    cursor.execute(
        "DELETE FROM favorites WHERE user_id = %s AND movie_id = %s",
        (user_id, movie_id)
    )
    db.commit()

    return jsonify({"message": "Favorite removed"}), 200

if __name__ == "__main__":
    app.run(debug=True)
