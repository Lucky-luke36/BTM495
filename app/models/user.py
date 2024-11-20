from models import db

class User(db.Model):
    __tablename__ = 'users'
    
    user_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

    type = db.Column(db.String(50))  # Discriminator column for subclasses

    __mapper_args__ = {
        'polymorphic_on': type,
        'polymorphic_identity': 'user'
    }

    def update_profile(self, name, email):
        self.name = name
        self.email = email
        db.session.commit()

    def __repr__(self):
        return f"<User {self.name}>"
