from flask import Blueprint, request, jsonify
from flask_restful import Api, Resource
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import Employee
from models import db 

api_bp = Blueprint("api",__name__) #creates a blueprint for the api here
api = Api(api_bp)  #attaches RESTful to the blueprint

class EmployeeResource(Resource):
    @jwt_required ()
    def get(self,emp_id=None):
        if emp_id :
            employee = Employee.query.get(emp_id)

            if employee : 
                return jsonify({"id":employee.id ,"name":employee.name,"salary":str(employee.salary)})
            return jsonify({"error":"Employee not found"}),404
        
        employees = Employee.query.all()
        return jsonify([{"id":emp.id,"name":emp.name,"salary":str(emp.salary)} for emp in employees])
    
    def post(self):
        #create a new employee in the database
        data = request.get_json() #gets json data from request
        new_emp = Employee(name=data["name"],salary=data["salary"]) #create a new employee 
        db.session.add(new_emp)
        db.session.commit()
        return jsonify({"message":"Employee Created"})

    def put(self,emp_id):
        employee = Employee.query.get(emp_id)
        if not employee:
            return jsonify({"error":"employee not found"})
        data = request.get_json()
        employee.name = data.get("name",employee.name) #	If "name" exists in JSON, update employee.name with new value.
        employee.salary = data.get("salary",employee.salary)
        db.session.commit()
        return jsonify({"message":"Employee Updated"})
    
    def delete(self,emp_id):
        employee = Employee.query.get(emp_id)
        if not employee:
            return jsonify({"error": "Employee not found"}), 404
        db.session.delete(employee)  #Delete from database
        db.session.commit()  #Save changes
        return jsonify({"message": "Employee deleted"})
    
@api_bp.route("/github-webhook/", methods=["POST"])
def github_webhook():
    data = request.get_json()
    print("Received GitHub webhook:", data)  # Logs the payload
    return jsonify({"message": "Webhook received"}), 200    

api.add_resource(EmployeeResource, "/employees", "/employees/<int:emp_id>")    






