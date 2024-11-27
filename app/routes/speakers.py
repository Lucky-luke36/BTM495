from flask import Blueprint, render_template, request, redirect, url_for
from app.models import Speaker
from app.extentions import db

bp = Blueprint('speakers', __name__, url_prefix='/')

####### Speakers Page #################

# Defining route to display speakers
@bp.route('/speakers')
def list_speakers():
    speakers = Speaker.query.all()
    return render_template('speakers.html', speakers=speakers)

# Route to handle form submission to add a speaker
@bp.route('/add_speaker', methods=['POST'])
def add_speaker():
    # Print form data for debugging
    print("Form submitted")

    # Check if the form has data
    if 'name' in request.form and 'email' in request.form and 'expertise' in request.form:
        # Get the form data
        name = request.form['name']
        email = request.form['email']
        expertise = request.form['expertise']

        # Debug print to verify form data
        print(f"Received data - Name: {name}, Email: {email}, Expertise: {expertise}")

        # Create a new speaker instance and save it to the database
        new_speaker = Speaker(name=name, email=email, expertise=expertise)
        db.session.add(new_speaker)
        db.session.commit()

        # Redirect back to the speakers list
        return redirect(url_for('list_speakers'))
    
    else:
        # If form data is missing, print an error message for debugging
        print("Form data missing")
        return redirect(url_for('list_speakers'))  # Redirect to speakers list even if something is wrong


@bp.before_request
def override_method():
    if request.method == 'POST' and '_method' in request.form:
        method = request.form['_method']
        if method.upper() in ['DELETE']:
            request.environ['REQUEST_METHOD'] = method.upper()

@bp.route('/delete_speaker/<int:speaker_id>', methods=['POST'])
def delete_speaker(speaker_id):
    # Query the speaker by ID
    speaker_to_delete = Speaker.query.get_or_404(speaker_id)

    try:
        # Delete the speaker from the database
        db.session.delete(speaker_to_delete)
        db.session.commit()
        return redirect(url_for('list_speakers'))
    except Exception as e:
        # Handle any exceptions
        print(f"Error occurred: {e}")
        return redirect(url_for('speakers.list_speakers'))

@bp.route('/update_speaker', methods=['POST'])
def update_speaker():
    speaker_id = request.form.get('speaker_id')
    name = request.form.get('name')
    email = request.form.get('email')
    expertise = request.form.get('expertise')

    # Fetch the speaker from the database
    speaker = Speaker.query.get_or_404(speaker_id)
    speaker.name = name
    speaker.email = email
    speaker.expertise = expertise

    # Save the changes to the database
    db.session.commit()
    return redirect(url_for('speakers.list_speakers'))



