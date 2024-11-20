from flask import Blueprint, render_template, request, redirect, url_for
from app.models import Event, Venue, Schedule
from app.extentions import db
from datetime import datetime

bp = Blueprint('events', __name__, url_prefix='/')



####### Events Page #################

# Defining route to display events
@bp.route('/events', methods=['GET'])
def list_events():
    event = Event.query.all()
    venues = Venue.query.all()    
    return render_template('events.html', events=event, venues=venues)

# Route to handle form submission to add an event
@bp.route('/add_event', methods=['GET', 'POST'])
def add_event():
    if request.method == 'POST':
        # Handle the form submission (POST request)
        name = request.form.get('name')
        date = request.form.get('date')
        venue_id = request.form.get('venue_id')
        
        if not name or not date or not venue_id:
            print("Form data missing")
            return redirect(url_for('events.list_speakers'))  # Or handle with a flash message or error
        
        # Debug print to verify form data
        print(f"Received data - Name: {name}, Date: {date}, Venue ID: {venue_id}")

        # Create a new event instance and save it to the database
        new_event = Event(name=name, date=date, venue_id=venue_id)
        db.session.add(new_event)
        db.session.commit()

        # Automatically create a default schedule (from 8am to 5pm) for the new event
        default_start_time = datetime.strptime("08:00:00", "%H:%M:%S").time()
        default_end_time = datetime.strptime("17:00:00", "%H:%M:%S").time()

        default_schedule = Schedule(start_time=default_start_time, end_time=default_end_time, event_id=new_event.event_id)
        db.session.add(default_schedule)
        db.session.commit()

        # Redirect after adding the event and schedule
        return redirect(url_for('events.list_events'))

    # Render the form with venues list
    return render_template('list_events')



@bp.before_request
def override_method():
    if request.method == 'POST' and '_method' in request.form:
        method = request.form['_method']
        if method.upper() in ['DELETE']:
            request.environ['REQUEST_METHOD'] = method.upper()

@bp.route('/delete_event/<int:event_id>', methods=['POST'])
def delete_event(event_id):
    # Query the speaker by ID
    event_to_delete = Event.query.get_or_404(event_id)

    try:
        # Delete the speaker from the database
        db.session.delete(event_to_delete)
        db.session.commit()
        return redirect(url_for('events.list_events'))
    except Exception as e:
        # Handle any exceptions
        print(f"Error occurred: {e}")
        return redirect(url_for('events.list_events'))

@bp.route('/update_event', methods=['POST'])
def update_event():
    event_id = request.form.get('event_id')
    name = request.form.get('name')
    date = request.form.get('date')
    venue_id = request.form.get('venue_id')

    # Fetch the event to update
    event = Event.query.get_or_404(event_id)
    if event:
        # Update the event details
        event.name = name
        event.date = date
        event.venue_id = venue_id
        db.session.commit()

    return redirect(url_for('events.list_events'))

