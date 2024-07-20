from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin




db = SQLAlchemy()

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    role = db.Column(db.String(20), nullable=False)  # 'admin', 'student', etc.
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    phone = db.Column(db.String(15))
    studentCId = db.Column(db.String(20))
    createdAt = db.Column(db.DateTime, default=datetime.utcnow)
    course = db.Column(db.String(50))
    passingYear = db.Column(db.Integer)
    branch = db.Column(db.String(50))
    def is_active(self):
        return True  # Return True if the user is active, or implement your logic here


class Ticket(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    createdAt = db.Column(db.DateTime, default=datetime.utcnow)
    createdBy = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    updatedBy = db.Column(db.Integer, db.ForeignKey('user.id'))
    lastUpdated = db.Column(db.DateTime)
    asset = db.Column(db.String(100))
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    status = db.Column(db.String(20), default='Open')  # 'Open', 'Approved', 'Rejected', 'Completed', etc.
    estimatedTimetoComplete = db.Column(db.String(50))
    remark = db.Column(db.Text)

    # Define relationships
    created_user = db.relationship('User', foreign_keys=[createdBy], backref='created_tickets')
    updated_user = db.relationship('User', foreign_keys=[updatedBy])
