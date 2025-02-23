
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Employee(db.Model):
    __tablename__ = "employees"

    id = db.Column(db.Integer,primary_key = True)
    name = db.Column(db.String(100),nullable = False)
    salary = db.Column(db.Numeric(10,2),nullable = False)

    def __repr__(self):
        return f"<Employee{self.name}>"
    

class User(db.Model):
    id = db.Column(db.Integer,primary_key = True)
    username = db.Column(db.String(100),unique=True ,nullable = False)
    password_hash = db.Column(db.String(200),nullable = False )

    def set_password(self,password):
        self.password_hash = generate_password_hash(password)

    def check_password(self,password):
        return check_password_hash(self.password_hash,password)    
    


    