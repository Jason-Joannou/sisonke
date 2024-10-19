from flask import Flask
from flask_cors import CORS  # Import Flask-CORS

from flask_app.routes.whatsapp import whatsapp_bp

app = Flask(__name__)

# Enable CORS for all routes and all origins
CORS(app)  # Add this lines to enable CORS for the entire app

app.register_blueprint(whatsapp_bp)


@app.route("/")
def index() -> str:
    return "Sisonke API"


if __name__ == "__main__":
    app.run(debug=True)
