from flask import Blueprint, render_template, request, redirect, url_for, flash, session, jsonify
from database import db
import models
from models import Sport
from datetime import datetime, timedelta, date

routes = Blueprint('routes', __name__)

@routes.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("register.html")
    
    data = request.form
    username = data.get("username")
    password = data.get("password")
    
    if not username or not password:
        flash("Username and password are required.", "error")
        return render_template("register.html")
    
    existing_user = models.User.query.filter_by(username=username).first()
    if existing_user:
        flash("Username already exists.", "error")
        return render_template("register.html")

    try:
        new_user = models.User(username=username)
        new_user.set_password(password)        
        db.session.add(new_user)
        db.session.commit()
        
        flash("Registration successful! Please login.", "success")
        return redirect(url_for('routes.login'))
    
    except Exception as e:
        db.session.rollback()
        flash("Registration failed. Please try again.", "error")
        return render_template("register.html")

@routes.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")
    
    data = request.form
    username = data.get("username")
    password = data.get("password")

    if not username or not password:
        flash("Username and password are required.", "error")
        return render_template("login.html")

    user = models.User.query.filter_by(username=username).first()
    
    if user and user.check_password(password):
        session['user_id'] = user.id
        session['username'] = user.username
        flash(f"Welcome back, {user.username}!", "success")

        if user.role == models.Role.ADMIN:
            session['is_admin'] = True
            return redirect(url_for('routes.admin_dashboard'))
        else:
            session['is_admin'] = False
            return redirect(url_for('home'))  # Changed to home route
    
    flash("Invalid username or password.", "error")
    return render_template("login.html")

@routes.route("/logout")
def logout():
    session.clear()
    flash("You have been logged out.", "info")
    return redirect(url_for('routes.login'))

@routes.route("/view-facilities")
def view_facility():
    sports = models.Sport.query.all()
    facilities = models.Facility.query.filter_by(is_active=True).all()
    
    return render_template("view_facilities.html", 
                         sports=sports, 
                         facilities=facilities)

@routes.route("/booking/<int:facility_id>", methods=["GET", "POST"])
def booking(facility_id):
    if 'user_id' not in session:
        flash("Please login to make a booking.", "error")
        return redirect(url_for('routes.login'))
    
    facility = models.Facility.query.get_or_404(facility_id)
    
    if request.method == "GET":
        # Get next 7 days and their available schedules
        upcoming_dates = []
        for i in range(7):
            booking_date = date.today() + timedelta(days=i)
            # Convert Python weekday (Monday=0) to our enum (Sunday=0, Monday=1, etc.)
            day_of_week = (booking_date.weekday() + 1) % 7
            
            # Get available schedules for this day and facility
            available_schedules = models.Schedule.query.filter(
                models.Schedule.facility_id == facility_id,
                models.Schedule.day_of_week == models.DayOfWeek(day_of_week)
            ).all()
            
            # Only add dates that have scheduled slots
            if available_schedules:
                upcoming_dates.append({
                    'date': booking_date,
                    'date_str': booking_date.strftime('%Y-%m-%d'),
                    'display_date': booking_date.strftime('%A, %B %d, %Y'),
                    'day_name': booking_date.strftime('%A'),
                    'schedules': available_schedules
                })
        
        # Get user's recent bookings
        user_bookings = models.Booking.query.filter_by(
            user_id=session['user_id']
        ).order_by(models.Booking.start.desc()).limit(5).all()
        
        return render_template("booking.html", 
                             facility=facility, 
                             upcoming_dates=upcoming_dates,
                             user_bookings=user_bookings,
                             today=date.today().strftime('%Y-%m-%d'),
                             # Add datetime functions to template context
                             datetime=datetime,
                             timedelta=timedelta)
    
    # Handle POST request - Work with schedule selection
    try:
        data = request.form
        booking_date_str = data.get("booking_date")
        schedule_id = data.get("schedule_id")
        seats = int(data.get("seats", 1))
        
        # Validate inputs
        if not all([booking_date_str, schedule_id]):
            flash("Please select a date and time slot.", "error")
            return redirect(url_for('routes.booking', facility_id=facility_id))
        
        # Get the schedule and validate it belongs to this facility
        schedule = models.Schedule.query.filter_by(
            id=int(schedule_id),
            facility_id=facility_id
        ).first()
        
        if not schedule:
            flash("Invalid schedule selection.", "error")
            return redirect(url_for('routes.booking', facility_id=facility_id))
        
        booking_date = datetime.strptime(booking_date_str, '%Y-%m-%d').date()
        
        # Calculate start and end times based on schedule
        start_datetime = datetime.combine(booking_date, schedule.start_time)
        slot_minutes = facility.sport.default_slot_minutes
        end_datetime = start_datetime + timedelta(minutes=slot_minutes)
        
        # Validate capacity
        if seats > facility.max_capacity:
            flash(f"Maximum capacity is {facility.max_capacity} people.", "error")
            return redirect(url_for('routes.booking', facility_id=facility_id))
        
        # Check for overlapping bookings
        existing_booking = models.Booking.query.filter(
            models.Booking.facility_id == facility_id,
            models.Booking.start < end_datetime,
            models.Booking.end > start_datetime,
            models.Booking.status != models.BookingStatus.CANCELLED
        ).first()
        
        if existing_booking:
            flash("This time slot is already booked.", "error")
            return redirect(url_for('routes.booking', facility_id=facility_id))
        
        # Calculate price
        duration_hours = slot_minutes / 60
        total_price = duration_hours * facility.price_per_hour * seats
        
        # Create booking
        booking = models.Booking(
            user_id=session['user_id'],
            facility_id=facility_id,
            start=start_datetime,
            end=end_datetime,
            seats=seats,
            price=total_price,
            status=models.BookingStatus.CONFIRMED
        )
        
        db.session.add(booking)
        db.session.commit()
        
        flash(f"Booking confirmed for {facility.name} on {booking_date.strftime('%A, %B %d')} from {schedule.start_time.strftime('%H:%M')} to {end_datetime.strftime('%H:%M')}!", "success")
        return redirect(url_for('routes.my_bookings'))
        
    except ValueError as e:
        flash("Invalid date or schedule selection.", "error")
        return redirect(url_for('routes.booking', facility_id=facility_id))
    except Exception as e:
        db.session.rollback()
        flash(f"Booking failed: {str(e)}", "error")
        return redirect(url_for('routes.booking', facility_id=facility_id))

@routes.route("/my-bookings")
def my_bookings():
    if 'user_id' not in session:
        flash("Please login to view bookings.", "error")
        return redirect(url_for('routes.login'))
    
    user_bookings = models.Booking.query.filter_by(
        user_id=session['user_id']
    ).order_by(models.Booking.start.desc()).all()
    
    return render_template("my_bookings.html", 
                         bookings=user_bookings,
                         today=date.today())

@routes.route("/cancel-booking/<int:booking_id>", methods=["POST"])
def cancel_booking(booking_id):
    if 'user_id' not in session:
        return jsonify({"error": "Not authenticated"}), 401
    
    booking = models.Booking.query.get_or_404(booking_id)
    
    if booking.user_id != session['user_id']:
        return jsonify({"error": "Unauthorized"}), 403
    
    if booking.start < datetime.now():
        return jsonify({"error": "Cannot cancel past bookings"}), 400
    
    booking.status = models.BookingStatus.CANCELLED
    db.session.commit()
    
    return jsonify({"message": "Booking cancelled successfully"})

@routes.route("/admin-dashboard")
def admin_dashboard():
    if 'user_id' not in session or not session.get('is_admin'):
        flash("Access denied.", "error")
        return redirect(url_for('routes.login'))
    
    return render_template("admin_dashboard.html")

@routes.route("/index")
def index():
    return redirect(url_for('home'))




