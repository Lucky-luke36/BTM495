
# MCC Event Manager

MCC Event Manager is a web-based application designed to manage events, speakers, venues, and users. 
The platform supports creating, editing, and deleting events, managing schedules, assigning speakers and event hosts, and more. 
It is built using Flask and Bootstrap for a responsive, user-friendly experience and quick prototyping.

## Table of Contents
- [Features](#features)
- [Technologies](#technologies)
- [Setup](#setup)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [Contributing](#contributing)
- [License](#license)

## Features
- User authentication and authorization with roles such as Admin, Event Host, and Speaker.
- CRUD operations for managing events, speakers, and venues.
- Dynamic scheduling and assignment of speakers to events.
- Venue management for associating events with specific locations.
- Responsive design using Bootstrap.

## Technologies
- **Backend**: Python, Flask
- **Frontend**: HTML, CSS, JavaScript, Bootstrap
- **Database**: SQLite (can be configured for PostgreSQL or MySQL)
- **Version Control**: Git

## Setup

### Prerequisites
Ensure you have the following installed on your system:
- Python 3.7 or later
- Git

### Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/yourusername/mcc-event-manager.git
   cd mcc-event-manager
   ```

2. **Create and activate a virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. **Install the required dependencies**:
   ```bash
   pip install -r requirements.txt (currently not reuired)
   ```

4. **Set up the database**:
   ```bash
   flask db upgrade
   ```

5. **Run the application**:
   ```bash
   flask run
   ```
   The application will be accessible at `http://127.0.0.1:5000`.

## Usage
1. **Access the application**: Open `http://127.0.0.1:5000` in your web browser.
2. **Login**: Use username "alice" and "password1" to log in and access the manager features. 
Or bypass login by navigating directly to `http://127.0.0.1:5000/Manager`
3. **Manage Events**: Create, update, or delete events using the event management section.
4. **Add Speakers and Event**: Add speakers and events hosts to manage events.

## Project Structure
```
mcc-event-manager/
├── app.py             # Main application file
├── config.py          # Database configuration file
├── crm.db             # SQLite databse
├── add_data_to_db.py  # Mock data for poputating db
├── models/            # SQLAlchemy class models for database entities
├── templates/         # HTML templates
└── README.md          # Project documentation
```

## Acknowledgements
- [Flask](https://flask.palletsprojects.com/) for the backend framework.
- [Bootstrap](https://getbootstrap.com/) for responsive design.
- [Flatpickr](https://flatpickr.js.org/) for the time picker component.

