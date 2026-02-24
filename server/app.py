from flask import Flask
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route("/api/test", methods=["GET"])
def test():
    return jsonify({"message": "Backend running successfully"})


@app.route("/")
def home():
    return "Server is ready to host!"

if __name__ == "__main__":
    app.run(debug=True)
