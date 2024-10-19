from flask
from flask_cors import CORS  # Import Flask-CORS

app = Flask(__name__)

# Enable CORS for all routes and all origins
CORS(app)  # Add this lines to enable CORS for the entire app

@app.route("/")
def index() -> str:
    return "Sisonke API"


if __name__ == "__main__":
    app.run(debug=True)
