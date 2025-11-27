from main import app
from database import db
import models
from datetime import time

def seed_database():
    with app.app_context():
        # Clear existing data
        db.drop_all()
        db.create_all()
        
        # Add Sports
        sports = [
            models.Sport(name="Football", max_players=22, default_slot_minutes=120),
            models.Sport(name="Basketball", max_players=10, default_slot_minutes=60),
            models.Sport(name="Tennis", max_players=4, default_slot_minutes=60),
            models.Sport(name="Swimming", max_players=50, default_slot_minutes=45),
            models.Sport(name="Volleyball", max_players=12, default_slot_minutes=60),
            models.Sport(name="Badminton", max_players=4, default_slot_minutes=45)
        ]
        
        for sport in sports:
            db.session.add(sport)
        
        db.session.commit()
        
        # Add Facilities
        facilities = [
            models.Facility(
                name="City Stadium",
                location="Downtown Sports Complex",
                sport_id=1,  # Football
                price_per_hour=100.0,
                max_capacity=200,
                is_active=True
            ),
            models.Facility(
                name="Community Football Field",
                location="West Park",
                sport_id=1,  # Football
                price_per_hour=50.0,
                max_capacity=100,
                is_active=True
            ),
            models.Facility(
                name="Indoor Basketball Court A",
                location="Sports Center Building 1",
                sport_id=2,  # Basketball
                price_per_hour=30.0,
                max_capacity=50,
                is_active=True
            ),
            models.Facility(
                name="Tennis Court 1",
                location="Tennis Club",
                sport_id=3,  # Tennis
                price_per_hour=40.0,
                max_capacity=4,
                is_active=True
            ),
            models.Facility(
                name="Olympic Pool",
                location="Aquatic Center",
                sport_id=4,  # Swimming
                price_per_hour=25.0,
                max_capacity=100,
                is_active=True
            ),
        ]
        
        for facility in facilities:
            db.session.add(facility)
        
        db.session.commit()
        
        # Add Fixed Weekly Schedules
        schedules = [
            # City Stadium - Football (Sunday, Monday, Tuesday 3:00-5:00 PM)
            models.Schedule(facility_id=1, day_of_week=models.DayOfWeek.SUNDAY, start_time=time(15, 0), end_time=time(17, 0)),
            models.Schedule(facility_id=1, day_of_week=models.DayOfWeek.MONDAY, start_time=time(15, 0), end_time=time(17, 0)),
            models.Schedule(facility_id=1, day_of_week=models.DayOfWeek.TUESDAY, start_time=time(15, 0), end_time=time(17, 0)),
            
            # Community Football Field (Wednesday, Thursday 4:00-6:00 PM)
            models.Schedule(facility_id=2, day_of_week=models.DayOfWeek.WEDNESDAY, start_time=time(16, 0), end_time=time(18, 0)),
            models.Schedule(facility_id=2, day_of_week=models.DayOfWeek.THURSDAY, start_time=time(16, 0), end_time=time(18, 0)),
            
            # Basketball Court A (Monday, Wednesday, Friday 6:00-8:00 PM)
            models.Schedule(facility_id=3, day_of_week=models.DayOfWeek.MONDAY, start_time=time(18, 0), end_time=time(20, 0)),
            models.Schedule(facility_id=3, day_of_week=models.DayOfWeek.WEDNESDAY, start_time=time(18, 0), end_time=time(20, 0)),
            models.Schedule(facility_id=3, day_of_week=models.DayOfWeek.FRIDAY, start_time=time(18, 0), end_time=time(20, 0)),
            
            # Tennis Court 1 (Tuesday, Thursday, Saturday 2:00-4:00 PM)
            models.Schedule(facility_id=4, day_of_week=models.DayOfWeek.TUESDAY, start_time=time(14, 0), end_time=time(16, 0)),
            models.Schedule(facility_id=4, day_of_week=models.DayOfWeek.THURSDAY, start_time=time(14, 0), end_time=time(16, 0)),
            models.Schedule(facility_id=4, day_of_week=models.DayOfWeek.SATURDAY, start_time=time(14, 0), end_time=time(16, 0)),
            
            # Olympic Pool (Daily 6:00-8:00 AM and 7:00-9:00 PM)
            models.Schedule(facility_id=5, day_of_week=models.DayOfWeek.MONDAY, start_time=time(6, 0), end_time=time(8, 0)),
            models.Schedule(facility_id=5, day_of_week=models.DayOfWeek.MONDAY, start_time=time(19, 0), end_time=time(21, 0)),
            models.Schedule(facility_id=5, day_of_week=models.DayOfWeek.TUESDAY, start_time=time(6, 0), end_time=time(8, 0)),
            models.Schedule(facility_id=5, day_of_week=models.DayOfWeek.TUESDAY, start_time=time(19, 0), end_time=time(21, 0)),
            models.Schedule(facility_id=5, day_of_week=models.DayOfWeek.WEDNESDAY, start_time=time(6, 0), end_time=time(8, 0)),
            models.Schedule(facility_id=5, day_of_week=models.DayOfWeek.WEDNESDAY, start_time=time(19, 0), end_time=time(21, 0)),
            models.Schedule(facility_id=5, day_of_week=models.DayOfWeek.THURSDAY, start_time=time(6, 0), end_time=time(8, 0)),
            models.Schedule(facility_id=5, day_of_week=models.DayOfWeek.THURSDAY, start_time=time(19, 0), end_time=time(21, 0)),
            models.Schedule(facility_id=5, day_of_week=models.DayOfWeek.FRIDAY, start_time=time(6, 0), end_time=time(8, 0)),
            models.Schedule(facility_id=5, day_of_week=models.DayOfWeek.FRIDAY, start_time=time(19, 0), end_time=time(21, 0)),
            models.Schedule(facility_id=5, day_of_week=models.DayOfWeek.SATURDAY, start_time=time(8, 0), end_time=time(10, 0)),
            models.Schedule(facility_id=5, day_of_week=models.DayOfWeek.SUNDAY, start_time=time(8, 0), end_time=time(10, 0)),
        ]
        
        for schedule in schedules:
            db.session.add(schedule)
        
        db.session.commit()
        
        print("Database seeded successfully!")
        print(f"Added {len(sports)} sports, {len(facilities)} facilities, and {len(schedules)} weekly schedule slots")

if __name__ == "__main__":
    seed_database()