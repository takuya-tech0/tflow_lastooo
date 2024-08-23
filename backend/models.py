# models.py
from sqlalchemy import Column, Integer, String, ForeignKey, Date  # Date を追加
from sqlalchemy.orm import relationship
from database import Base

class Employee(Base):
    __tablename__ = 'employee'
    employee_id = Column(Integer, primary_key=True)
    name = Column(String)
    password = Column(String)
    birthdate = Column(Date)
    gender = Column(String)
    academic_background = Column(String)
    hire_date = Column(Date)
    recruitment_type = Column(String)
    grades = relationship('EmployeeGrade', back_populates='employee')
    skills = relationship('EmployeeSkill', back_populates='employee')
    spi = relationship('Spi', back_populates='employee', uselist=False)
    evaluations = relationship('EvaluationHistory', back_populates='employee')
    departments = relationship('DepartmentMember', back_populates='employee')
    
    vector = relationship("EmployeeVector", back_populates="employee", uselist=False)
    
    
class EmployeeVector(Base):
    __tablename__ = "employee_vectors"

    id = Column(Integer, primary_key=True, index=True)
    employee_id = Column(Integer, ForeignKey("employee.employee_id"), unique=True)
    vector = Column(String)  # JSON文字列として保存

    employee = relationship("Employee", back_populates="vector")

class EmployeeGrade(Base):
    __tablename__ = 'employee_grade'
    employee_id = Column(Integer, ForeignKey('employee.employee_id'), primary_key=True)
    grade = Column(Integer, ForeignKey('grade.grade_id'))
    employee = relationship('Employee', back_populates='grades')
    grade_info = relationship('Grade', back_populates='employees')

class Grade(Base):
    __tablename__ = 'grade'
    grade_id = Column(Integer, primary_key=True)
    grade_name = Column(String)
    employees = relationship('EmployeeGrade', back_populates='grade_info')

class EmployeeSkill(Base):
    __tablename__ = 'employee_skill'
    employee_skill_id = Column(Integer, primary_key=True)
    employee_id = Column(Integer, ForeignKey('employee.employee_id'))
    skill_id = Column(Integer, ForeignKey('skill_list.skill_id'))
    employee = relationship('Employee', back_populates='skills')
    skill = relationship('SkillList', back_populates='employees')

class SkillList(Base):
    __tablename__ = 'skill_list'
    skill_id = Column(Integer, primary_key=True)
    skill_category = Column(String)
    skill_name = Column(String)
    employees = relationship('EmployeeSkill', back_populates='skill')

class Spi(Base):
    __tablename__ = 'spi'
    spi_id = Column(Integer, primary_key=True)
    employee_id = Column(Integer, ForeignKey('employee.employee_id'))
    extraversion = Column(Integer)
    agreebleness = Column(Integer)
    conscientiousness = Column(Integer)
    neuroticism = Column(Integer)
    openness = Column(Integer)
    employee = relationship('Employee', back_populates='spi')

class EvaluationHistory(Base):
    __tablename__ = 'evaluation_history'
    evaluation_id = Column(Integer, primary_key=True)
    employee_id = Column(Integer, ForeignKey('employee.employee_id'))
    evaluation_year = Column(Integer)
    evaluation = Column(String)
    evaluation_comment = Column(String)
    employee = relationship('Employee', back_populates='evaluations')

class DepartmentMember(Base):
    __tablename__ = 'department_member'
    department_member_id = Column(Integer, primary_key=True)
    department_id = Column(Integer, ForeignKey('department.department_id'))
    employee_id = Column(Integer, ForeignKey('employee.employee_id'))
    employee = relationship('Employee', back_populates='departments')
    department = relationship('Department', back_populates='members')

class Department(Base):
    __tablename__ = 'department'
    department_id = Column(Integer, primary_key=True)
    department_name = Column(String)
    department_detail = Column(String)
    members = relationship('DepartmentMember', back_populates='department')

class JobPost(Base):
    __tablename__ = 'job_post'
    job_post_id = Column(Integer, primary_key=True)
    department_id = Column(Integer, ForeignKey('department.department_id'))
    job_title = Column(String)
    job_detail = Column(String)
    department = relationship('Department')
    
    vector = relationship("JobPostVector", back_populates="job_post", uselist=False)
    
class RequiredSkill(Base):
    __tablename__ = 'required_skill'

    required_id = Column(Integer, primary_key=True, autoincrement=True)
    job_post_id = Column(Integer, ForeignKey('job_post.job_post_id'), nullable=False)
    skill_id = Column(Integer, ForeignKey('skill_list.skill_id'), nullable=False)

class JobPostVector(Base):
    __tablename__ = "job_post_vectors"

    id = Column(Integer, primary_key=True, index=True)
    job_post_id = Column(Integer, ForeignKey("job_post.job_post_id"), unique=True)
    vector = Column(String)  # JSON文字列として保存
    job_post = relationship("JobPost", back_populates="vector")