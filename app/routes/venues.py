from flask import Blueprint, render_template, request, redirect, url_for
from app.models import Venue
from app.extentions import db

bp = Blueprint('venues', __name__, url_prefix='/')



####### Venues Page ################

@bp.route('/venues')
def list_venues():
    venues = Venue.query.all()
    return render_template('venues.html', venues=venues)

# Route to handle form submission to add an event
@bp.route('/add_venue', methods=['POST'])
def add_venue():
    # Print form data for debugging
    print("Form submitted")

    # Check if the form has data
    if 'name' in request.form and 'location' in request.form and 'capacity' in request.form :
        # Get the form data
        name = request.form['name']
        location = request.form['location']
        capacity = request.form['capacity']


        # Debug print to verify form data
        print(f"Received data - Name: {name}")

        # Create a new event instance and save it to the database
        new_venue = Venue(name=name, location=location ,capacity=capacity)
        db.session.add(new_venue)
        db.session.commit()

        # Redirect back to the speakers list
        return redirect(url_for('venues.list_venues'))
    
    else:
        # If form data is missing, print an error message for debugging
        print("Form data missing")
        return redirect(url_for('venues.list_venues'))  # Redirect to speakers list even if something is wrong

@bp.route('/delete_venue/<int:venue_id>', methods=['POST'])
def delete_venue(venue_id):
    # Query the speaker by ID
    venue_to_delete = Venue.query.get_or_404(venue_id)

    try:
        # Delete the speaker from the database
        db.session.delete(venue_to_delete)
        db.session.commit()
        return redirect(url_for('venues.list_venues'))
    except Exception as e:
        # Handle any exceptions
        print(f"Error occurred: {e}")
        return redirect(url_for('venues.list_venues'))

@bp.route('/update_venue', methods=['POST'])
def update_venue():
    venue_id = request.form.get('venue_id')
    name = request.form.get('name')
    location = request.form.get('location')
    capacity = request.form.get('capacity')

    # Fetch the venue from the database
    venue = Venue.query.get_or_404(venue_id)
    venue.name = name
    venue.location = location
    venue.capacity = capacity

    # Save the changes to the database
    db.session.commit()
    return redirect(url_for('venues.list_venues'))
