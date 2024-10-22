from werkzeug.security import generate_password_hash, check_password_hash
from models import db
from models.user import User

admin_event_association = db.Table('admin_event_association',
    db.Column('event_id', db.Integer, db.ForeignKey('events.event_id'), primary_key=True),
    db.Column('admin_id', db.Integer, db.ForeignKey('admins.admin_id'), primary_key=True)
)

class Admin(User):
    __tablename__ = 'admins'
    
    admin_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)

    # Many-to-many relationship with Event
    events = db.relationship('Event', secondary=admin_event_association, back_populates='admins')

    __mapper_args__ = {
        'polymorphic_identity': 'admin'
    }

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f"<Admin {self.username}>"

