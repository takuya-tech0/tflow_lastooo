from sqlalchemy.orm import Session
from database import SessionLocal, engine
import models
from utils import get_all_employee_data, vectorize_employee
import json

def update_all_employee_vectors():
    db = SessionLocal()
    try:
        employees = db.query(models.Employee).all()
        for employee in employees:
            employee_data = get_all_employee_data(db, employee)
            if employee_data:
                employee_vector = vectorize_employee(employee_data)
                vector_json = json.dumps(employee_vector)
                
                existing_vector = db.query(models.EmployeeVector).filter(models.EmployeeVector.employee_id == employee.employee_id).first()
                if existing_vector:
                    existing_vector.vector = vector_json
                else:
                    new_vector = models.EmployeeVector(employee_id=employee.employee_id, vector=vector_json)
                    db.add(new_vector)
            
        db.commit()
        print("All employee vectors updated successfully.")
    except Exception as e:
        print(f"Error updating employee vectors: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    update_all_employee_vectors()