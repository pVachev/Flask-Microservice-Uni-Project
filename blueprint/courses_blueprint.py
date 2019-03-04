from flask import Blueprint, request, render_template
from flask_restful import Resource, reqparse, Api
from flask import Flask


courses = []

course_bl = Blueprint('course_bl', __name__, template_folder='templates')


courses_blueprint = Flask(__name__)

api = Api(courses_blueprint)



@course_bl.route('/course/<int:id>')
class Course(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('name',
                        required=True,
                        help="This field cannot be left blank!"
                        )

    def get(self, id):
        for course in courses:
            if course['id'] == id:
                return course
            
        return {'course': None}, 404

    def post(self, id):
        if next(filter(lambda x: x['id'] == id, courses), None) is not None:
            return {'message': "A course with id '{}' already exists.".format(id)}
        data_easy = request.get_json()
        data = Course.parser.parse_args()
     
        course = {'id': id, 'name': data['name']}
        courses.append(course)
        return course, 201

    def delete(self, id):
        global courses
        courses = list(filter(lambda x: x['id'] != id, courses))
        return {'message': 'Course deleted'}

    def put(self, id):
        data = Course.parser.parse_args()
        course = next(filter(lambda x: x['id'] == id, courses), None)
        if course is None:
            course = {'id': id, 'name': data['name']}
            courses.append(course)
        else:
            course.update(data)
        return course


@course_bl.route('/allcourses')
class CoursesList(Resource):
    def get(self):
        return render_template('courses.html', courses=courses)


api.add_resource(Course, '/course/<int:id>')
api.add_resource(CoursesList, '/courses')