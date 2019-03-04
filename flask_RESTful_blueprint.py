from flask import Flask, jsonify, render_template
from blueprint.students_blueprint import students_bl
from blueprint.courses_blueprint import course_bl
from blueprint.events_blueprint import events_bl


app = Flask(__name__)

@app.route('/')
def hpage():
    return render_template("hpage.html")

    

app.register_blueprint(students_bl, url_prefix='/z1/student')

app.register_blueprint(events_bl, url_prefix='/z3/event')

app.register_blueprint(course_bl, url_prefix='/z2/course')