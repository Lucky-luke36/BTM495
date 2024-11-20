from flask import Blueprint, render_template, request, redirect, url_for, g, session,jsonify
from app.models import Admin, db, Speaker, TimeSlot, Event
from datetime import datetime


bp = Blueprint('manager', __name__, url_prefix='/manager')



######### Manager Page ##################



# Route to render the manager page
@bp.route('/manager')
def dashboard():
    speakers = Speaker.query.all()
    events = Event.query.all()
    admins = Admin.query.all() 
    return render_template('manager.html', speakers=speakers, events=events, admins=admins)

@bp.route('/event_details/<int:event_id>')
def event_details(event_id):
    # Fetch the event details based on the selected event_id
    event = Event.query.get_or_404(event_id)
    schedule = event.schedule

    # Get the time slots associated with the schedule
    time_slots = schedule.time_slots if schedule else []

    # Render the event details as a partial HTML snippet
    return render_template('partials/event_details.html', event=event, schedule=schedule, time_slots=time_slots)


@bp.route('/add_time_slot', methods=['POST'])
def add_time_slot():
    speaker_id = request.form['speaker_id']
    event_id = request.form['event_id']
    start_time_str = request.form['start_time']
    end_time_str = request.form['end_time']

    # Convert the time strings to Python time objects
    start_time = datetime.strptime(start_time_str, "%H:%M").time()
    end_time = datetime.strptime(end_time_str, "%H:%M").time()

    event = Event.query.get_or_404(event_id)
    schedule = event.schedule

    # Validation: Check if the time slot is within the schedule's start and end time
    if start_time < schedule.start_time or end_time > schedule.end_time:
        return jsonify(success=False, message="Time slot must be within the schedule timeframe!")
    
    # Validation: Check if the start time is earlier than the end time
    if start_time >= end_time:
        return jsonify(success=False, message="Start time must be earlier than end time!")

    # Create new time slot
    new_time_slot = TimeSlot(start_time=start_time, end_time=end_time, schedule_id=schedule.schedule_id)
    speaker = Speaker.query.get_or_404(speaker_id)
    new_time_slot.speakers.append(speaker)

    db.session.add(new_time_slot)
    db.session.commit()

    return jsonify(success=True)


@bp.route('/delete_time_slot/<int:slot_id>', methods=['POST'])
def delete_time_slot(slot_id):
    # Find the time slot by ID
    time_slot = TimeSlot.query.get_or_404(slot_id)
    
    try:
        # Delete the time slot from the database
        db.session.delete(time_slot)
        db.session.commit()
        
        return jsonify(success=True)
    except Exception as e:
        # If there's an error, return an error message
        return jsonify(success=False, message=str(e))

