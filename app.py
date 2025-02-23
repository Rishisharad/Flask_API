from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager, create_access_token, jwt_required
from routes import api_bp
from models import db

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://postgres:admin@localhost:5432/employee_db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False  # To avoid warnings
app.config["JWT_SECRET_KEY"] = "super-secret-key"


db.init_app(app)
#Enable Migrations
migrate = Migrate(app, db)
jwt = JWTManager(app)
from models import Employee
app.register_blueprint(api_bp,url_prefix = "/api")


@app.route("/login",methods = ["POST"])
def login():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")

    if username == "admin" and password == "password":
        acess_token = create_access_token(identity = username)
        return jsonify(acess_token=acess_token)
    
    return jsonify({"message":"Invalid credentials"})

if __name__ == "__main__":
    app.run(debug=True)  # Runs the Flask app on http://127.0.0.1:5000/