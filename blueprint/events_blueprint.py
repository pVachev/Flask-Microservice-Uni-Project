from flask import Blueprint, request, render_template
from flask_restful import Resource, reqparse, Api
from flask import Flask

events = []

events_bl = Blueprint('events_bl', __name__, template_folder='templates')


events_blueprint = Flask(__name__)

api = Api(events_blueprint)

@events_bl.route('/event/<int:id>')
class Event(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('name',
                        required=True,
                        help="This field cannot be left blank!"
                        )

    def get(self, id):
        for event in events:
            if event['id'] == id:
                return event
            
        return {'event': None}, 404

    def post(self, id):
        if next(filter(lambda x: x['id'] == id, events), None) is not None:
            return {'message': "An event with id '{}' already exists.".format(id)}
        data_easy = request.get_json()
        data = Event.parser.parse_args()
     
        event = {'id': id, 'name': data['name']}
        events.append(event)
        return event, 201

    def delete(self, id):
        global events
        events = list(filter(lambda x: x['id'] != id, events))
        return {'message': 'Event deleted'}

    def put(self, id):
        data = Event.parser.parse_args()
        event = next(filter(lambda x: x['id'] == id, events), None)
        if event is None:
            event = {'id': id, 'name': data['name']}
            events.append(event)
        else:
            event.update(data)
        return event


@events_bl.route('/allevents')
class EventsList(Resource):
    def get(self):
        return render_template('events.html', events=events)

api.add_resource(Event, '/event/<int:id>')
api.add_resource(EventsList, '/events')
