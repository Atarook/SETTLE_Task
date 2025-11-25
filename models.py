from database import db
import enum

class BookingStatus(enum.Enum):
    PENDING = "pending"
    CONFIRMED = "confirmed"
    CANCELLED = "cancelled"

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)

    def __repr__(self):
        return f'<User {self.username}>'
    
class Sport(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    max_players = db.Column(db.Integer, default=10)
    default_slot_minutes = db.Column(db.Integer, default=60)

    def __repr__(self):
        return f'<Sport {self.name}>'
    
class Facility(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    location = db.Column(db.String(255))
    sport_id = db.Column(db.Integer, db.ForeignKey("sport.id"), nullable=False)
    price_per_hour = db.Column(db.Float, nullable=False, default=0.0)
    max_capacity = db.Column(db.Integer, default=100)
    is_active = db.Column(db.Boolean, default=True)

    sport = db.relationship("Sport", backref="facilities")

    def __repr__(self):
        return f'<Facility {self.name}>'

class Booking(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    facility_id = db.Column(db.Integer, db.ForeignKey('facility.id'), nullable=False)
    start = db.Column(db.DateTime, nullable=False)
    end = db.Column(db.DateTime, nullable=False)
    players = db.Column(db.Integer, default=1)
    price = db.Column(db.Float, nullable=False)
    status = db.Column(db.Enum(BookingStatus), default=BookingStatus.CONFIRMED)  

    user = db.relationship('User', backref='bookings')
    facility = db.relationship('Facility', backref='bookings')

    def __repr__(self):
        return f'<Booking User: {self.user_id}, Facility: {self.facility_id}>'