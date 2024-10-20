from flask import Flask, request
from flask_cors import CORS  # Import Flask-CORS

from flask_app.routes.database import database_bp
from flask_app.routes.insurance import insurance_bp
from flask_app.routes.users import users_bp
from flask_app.routes.validation import validation_bp
from flask_app.routes.whatsapp import whatsapp_bp

app = Flask(__name__)

# Enable CORS for all routes and all origins
CORS(app)  # Add this lines to enable CORS for the entire app

app.register_blueprint(whatsapp_bp)
app.register_blueprint(validation_bp)
app.register_blueprint(insurance_bp)
app.register_blueprint(users_bp)
app.register_blueprint(database_bp)


@app.route("/")
def index() -> str:
    return "Sisonke API"


@app.route("/test_endpoint", methods=["POST"])
def test_endpoint() -> str:

    print(request.json)
    return 200


if __name__ == "__main__":
    app.run(debug=True)
