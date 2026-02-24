from flask import Flask
from flask_cors import CORS

app = Flask(__name__)
CORS(app, origins="*")

@app.route("/api/test", methods=["GET"])
def test():
    return jsonify({"message": "Backend running successfully"})


@app.route("/")
def home():
    return "Server is ready to host!"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)