from flask import Blueprint, render_template
from app.models.db_models import Event

events_bp = Blueprint('events', __name__)

@events_bp.route('/', methods=['GET'])
def index():
    events = Event.get_all()
    return render_template('index.html', events=events)

@events_bp.route('/event/<int:id>', methods=['GET'])
def event_detail(id):
    event = Event.get_by_id(id)
    if not event:
        return "Event not found", 404
    return render_template('event.html', event=event)
