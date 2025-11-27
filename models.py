from database import db
import enum
from werkzeug.security import generate_password_hash, check_password_hash
class BookingStatus(enum.Enum):
    PENDING = "pending"
    CONFIRMED = "confirmed"
    CANCELLED = "cancelled"

class Role(enum.Enum):
    USER = "user"
    ADMIN = "admin" 

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)
    role= db.Column(db.Enum(Role), default=Role.USER)  # e.g., user, admin
    def set_password(self, password):
        """Hash and store the password"""
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        """Check if provided password matches the stored hash"""
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f'<User {self.username}>'
    
class Sport(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    max_players = db.Column(db.Integer, default=10)
    default_slot_minutes = db.Column(db.Integer, default=60)

    def __repr__(self):
        return f'<Sport {self.name}>'
    
    
class DayOfWeek(enum.Enum):
    SUNDAY = 0
    MONDAY = 1
    TUESDAY = 2
    WEDNESDAY = 3
    THURSDAY = 4
    FRIDAY = 5
    SATURDAY = 6

class Schedule(db.Model):
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    facility_id = db.Column(db.Integer, db.ForeignKey("facility.id"), nullable=False)
    day_of_week = db.Column(db.Enum(DayOfWeek), nullable=False)  # Which day
    start_time = db.Column(db.Time, nullable=False)  # Time only, not datetime
    end_time = db.Column(db.Time, nullable=False)    # Time only, not datetime
    seats_available = db.Column(db.Integer)
    # Relationship

    def set_seats_available(self, seats):
        self.seats_available = seats

    def __repr__(self):
        return f'<Schedule {self.facility.name} - {self.day_of_week.name} {self.start_time}-{self.end_time}>'
    
    def get_day_name(self):
        """Return readable day name"""
        day_names = {
            DayOfWeek.SUNDAY: "Sunday",
            DayOfWeek.MONDAY: "Monday", 
            DayOfWeek.TUESDAY: "Tuesday",
            DayOfWeek.WEDNESDAY: "Wednesday",
            DayOfWeek.THURSDAY: "Thursday",
            DayOfWeek.FRIDAY: "Friday",
            DayOfWeek.SATURDAY: "Saturday"
        }
        return day_names[self.day_of_week]


class Facility(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(120), nullable=False)
    location = db.Column(db.String(255))
    sport_id = db.Column(db.Integer, db.ForeignKey("sport.id"), nullable=False)
    price_per_hour = db.Column(db.Float, nullable=False, default=0.0)
    max_capacity = db.Column(db.Integer, default=100)
    is_active = db.Column(db.Boolean, default=True)
    schedules = db.relationship("Schedule", backref="facility", lazy=True)
    sport = db.relationship("Sport", backref="facilities")
    def __repr__(self):
        return f'<Facility {self.name}>'


class Booking(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    facility_id = db.Column(db.Integer, db.ForeignKey('facility.id'), nullable=False)
    start = db.Column(db.DateTime, nullable=False)
    end = db.Column(db.DateTime, nullable=False)
    seats = db.Column(db.Integer, default=1)
    price = db.Column(db.Float, nullable=False)
    status = db.Column(db.Enum(BookingStatus), default=BookingStatus.CONFIRMED)  

    user = db.relationship('User', backref='bookings')
    facility = db.relationship('Facility', backref='bookings')

    def __repr__(self):
        return f'<Booking User: {self.user_id}, Facility: {self.facility_id}>'