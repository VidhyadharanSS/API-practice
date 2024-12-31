from fastapi import FastAPI, Path #Define and validate path parameters in routes
from typing import Optional #Defines optional parameters 
from pydantic import BaseModel #Used to create data models with automatic validation

app = FastAPI()

# Create a dictionary of key(id) : value pairs 
students = {
    1:{
        "name" : "John",
        "age" : 17,
        "year" : "year12"
    },
    2:{
        "name" : "Tim",
        "age" : 18,
        "year" : "year14"
    }
}


#Defines the structure of student using pydantic validation
class Student(BaseModel):
    name: str
    age: int
    year: str

class UpdateStudent(BaseModel):
    name: Optional[str] = None
    age: Optional[int] = None
    year: Optional[str] = None

#GET SOMETHING BY INDEX ROUTE
@app.get("/")
def index():
    return {"name" : "First data"}

#GET ALL STUDENTS
@app.get('/get-students')
def get_students():
    return students


#PATH PARAMETERS - Path() : Gives description, gt and lt 
@app.get('/get-student/{student_id}')
def get_student(student_id: int = Path(description= "the ID of the student you want to view", gt=0, lt = 3)):
    return students[student_id]

#QUERY PARAMETERS of name and test (?)
@app.get("/get-by-name/{student_id}")
def get_student(*, student_id: int, name: Optional[str] = None):
    for student_id in students:
        if students[student_id]['name'] == name:
            return students[student_id]
    return {"Data" : "Not found"}

#POST METHOD TO CREATE STUDENTS 
@app.post('/create-student/{student-id}')
def create_student(student_id : int, student : Student):
    if student_id in students:
        return {'Error' : 'Student exists'}

    students[student_id] = student 
    return students[student_id]


#PUT METHOD TO UPDATE STUDENTS 
@app.put('/update-student/{student_id}')
def update_student(student_id : int, student : UpdateStudent):
    if student_id not in students:
        return {'Error' : 'Student not exists'}

    if student.name != None:
            students[student_id].["name"] = student.name
    if student.age != None:
            students[student_id].['age'] = student.age
    if student.year != None:
            students[student_id].['year'] = student.year       
        
    return students[student_id]

