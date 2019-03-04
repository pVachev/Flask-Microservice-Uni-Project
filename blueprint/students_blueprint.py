from flask import Blueprint, request, render_template
from flask_restful import Resource, reqparse, Api
from flask import Flask

students = []

students_bl = Blueprint('students_bl', __name__, template_folder='templates')


students_blueprint = Flask(__name__)

api = Api(students_blueprint)


@students_bl.route('/student/<int:id>')
class Student(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('name',
                        required=True,
                        help="This field cannot be left blank!"
                        )

    def get(self, id):
        for student in students:
            if student['id'] == id:
                return student
            
        return {'student': None}, 404

    def post(self, id):
        if next(filter(lambda x: x['id'] == id, students), None) is not None:
            return {'message': "A student with id '{}' already exists.".format(id)}
        data_easy = request.get_json()
        data = Student.parser.parse_args()
     
        student = {'id': id, 'name': data['name']}
        students.append(student)
        return student, 201

    def delete(self, id):
        global students
        students = list(filter(lambda x: x['id'] != id, students))
        return {'message': 'Student deleted'}

    def put(self, id):
        data = Student.parser.parse_args()
        student = next(filter(lambda x: x['id'] == id, students), None)
        if student is None:
            student = {'id': id, 'name': data['name']}
            students.append(student)
        else:
            student.update(data)
        return student

@students_bl.route('/allstudents')
class StudentList(Resource):
    def get(self):
        return render_template('students.html', students=students)


api.add_resource(Student, '/student/<int:id>')
api.add_resource(StudentList, '/students')
