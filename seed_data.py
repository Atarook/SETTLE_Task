from database import db
from models import User, Sport, Facility, Schedule, DayOfWeek, Role
from datetime import time

def seed_database():
    # Clear existing data
    db.drop_all()
    db.create_all()
    
    # Create Sports
    sports = [
        Sport(name="Basketball", max_players=10, default_slot_minutes=90),
        Sport(name="Football", max_players=22, default_slot_minutes=90),
        Sport(name="Tennis", max_players=4, default_slot_minutes=60),
        Sport(name="Swimming", max_players=20, default_slot_minutes=45),
        Sport(name="Volleyball", max_players=12, default_slot_minutes=60)
    ]
    
    for sport in sports:
        db.session.add(sport)
    
    db.session.commit()
    
    # Create Facilities
    facilities = [
        Facility(
            name="Basketball Court A", 
            location="Building A, Floor 2", 
            sport_id=1, 
            price_per_hour=25.0, 
            max_capacity=20
        ),
        Facility(
            name="Football Field", 
            location="Outdoor Area", 
            sport_id=2, 
            price_per_hour=50.0, 
            max_capacity=30
        ),
        Facility(
            name="Tennis Court 1", 
            location="Tennis Complex", 
            sport_id=3, 
            price_per_hour=20.0, 
            max_capacity=4
        ),
        Facility(
            name="Swimming Pool", 
            location="Aquatic Center", 
            sport_id=4, 
            price_per_hour=15.0, 
            max_capacity=25
        ),
        Facility(
            name="Volleyball Court", 
            location="Gymnasium", 
            sport_id=5, 
            price_per_hour=20.0, 
            max_capacity=15
        )
    ]
    
    for facility in facilities:
        db.session.add(facility)
    
    db.session.commit()
    
    # Create Schedules with FULL CAPACITY for all schedules
    schedules = [
        # Basketball Court A - Facility ID 1 (max_capacity=20) - facilities[0]
        Schedule(
            facility_id=1,
            day_of_week=DayOfWeek.SUNDAY,
            start_time=time(15, 0),
            end_time=time(17, 0),
            seats_available=facilities[0].max_capacity  # Full capacity (20)
        ),
        Schedule(
            facility_id=1,
            day_of_week=DayOfWeek.TUESDAY,
            start_time=time(15, 0),
            end_time=time(17, 0),
            seats_available=facilities[0].max_capacity  # Full capacity (20)
        ),
        Schedule(
            facility_id=1,
            day_of_week=DayOfWeek.FRIDAY,
            start_time=time(18, 0),
            end_time=time(20, 0),
            seats_available=facilities[0].max_capacity  # Full capacity (20)
        ),
        
        # Football Field - Facility ID 2 (max_capacity=30) - facilities[1]
        Schedule(
            facility_id=2,
            day_of_week=DayOfWeek.SATURDAY,
            start_time=time(9, 0),
            end_time=time(11, 0),
            seats_available=facilities[1].max_capacity  # Full capacity (30)
        ),
        Schedule(
            facility_id=2,
            day_of_week=DayOfWeek.SUNDAY,
            start_time=time(14, 0),
            end_time=time(16, 0),
            seats_available=facilities[1].max_capacity  # Full capacity (30)
        ),
        
        # Tennis Court 1 - Facility ID 3 (max_capacity=4) - facilities[2]
        Schedule(
            facility_id=3,
            day_of_week=DayOfWeek.MONDAY,
            start_time=time(8, 0),
            end_time=time(10, 0),
            seats_available=facilities[2].max_capacity  # Full capacity (4)
        ),
        Schedule(
            facility_id=3,
            day_of_week=DayOfWeek.WEDNESDAY,
            start_time=time(16, 0),
            end_time=time(18, 0),
            seats_available=facilities[2].max_capacity  # Full capacity (4)
        ),
        Schedule(
            facility_id=3,
            day_of_week=DayOfWeek.FRIDAY,
            start_time=time(19, 0),
            end_time=time(21, 0),
            seats_available=facilities[2].max_capacity  # Full capacity (4)
        ),
        
        # Swimming Pool - Facility ID 4 (max_capacity=25) - facilities[3]
        Schedule(
            facility_id=4,
            day_of_week=DayOfWeek.MONDAY,
            start_time=time(6, 0),
            end_time=time(8, 0),
            seats_available=facilities[3].max_capacity  # Full capacity (25)
        ),
        Schedule(
            facility_id=4,
            day_of_week=DayOfWeek.WEDNESDAY,
            start_time=time(18, 0),
            end_time=time(20, 0),
            seats_available=facilities[3].max_capacity  # Full capacity (25)
        ),
        Schedule(
            facility_id=4,
            day_of_week=DayOfWeek.SATURDAY,
            start_time=time(10, 0),
            end_time=time(12, 0),
            seats_available=facilities[3].max_capacity  # Full capacity (25)
        ),
        
        # Volleyball Court - Facility ID 5 (max_capacity=15) - facilities[4]
        Schedule(
            facility_id=5,
            day_of_week=DayOfWeek.TUESDAY,
            start_time=time(17, 0),
            end_time=time(19, 0),
            seats_available=facilities[4].max_capacity  # Full capacity (15)
        ),
        Schedule(
            facility_id=5,
            day_of_week=DayOfWeek.THURSDAY,
            start_time=time(19, 0),
            end_time=time(21, 0),
            seats_available=facilities[4].max_capacity  # Full capacity (15)
        ),
        Schedule(
            facility_id=5,
            day_of_week=DayOfWeek.SATURDAY,
            start_time=time(16, 0),
            end_time=time(18, 0),
            seats_available=facilities[4].max_capacity  # Full capacity (15)
        )
    ]
    
    for schedule in schedules:
        db.session.add(schedule)
    
    db.session.commit()
    
    # Create Users
    users = [
        User(username="Ahmed", role=Role.USER),
        User(username="tarek", role=Role.USER),
        User(username="admin", role=Role.USER),
        User(username="mike_jones", role=Role.USER)
    ]
    
    # Set passwords
    users[0].set_password("aaaaaa")  # Ahmed
    users[1].set_password("aaaaaa")  # tarek
    users[2].set_password("admin")   # admin
    users[3].set_password("password")  # mike_jones
    
    for user in users:
        db.session.add(user)
    
    db.session.commit()
    
    print("Database seeded successfully!")
    print("\nCreated Schedules:")
    for schedule in Schedule.query.all():
        print(f"- {schedule.facility.name}: {schedule.get_day_name()} {schedule.start_time.strftime('%H:%M')}-{schedule.end_time.strftime('%H:%M')} ({schedule.seats_available} seats)")

if __name__ == "__main__":
    from main import app
    with app.app_context():
        seed_database()