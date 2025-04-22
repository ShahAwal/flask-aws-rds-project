from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy() # Initialize SQLAlchemy extension

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)

    def __repr__(self):
        return f'<User {self.name}>'

    # Optional: Add a method to easily convert to dictionary
    def to_dict(self):
        return {"id": self.id, "name": self.name}
