import os
from flask import Blueprint, render_template, redirect, url_for, flash, request, current_app
from flask_login import login_user, logout_user, login_required, current_user
from app import db
from app.models.admin import Admin
from flask import session
from functools import wraps
from app.models.flight import Flight
from app.forms.flight import FlightForm
from werkzeug.utils import secure_filename
from app.models.booking import Booking




admin_bp = Blueprint('admin', __name__, url_prefix="/admin")

# Admin-only decorator
def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        from flask import session, abort
        if not session.get('is_admin'):
            abort(403)
        return f(*args, **kwargs)
    return decorated_function



@admin_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        admin = Admin.query.filter_by(email=email).first()
        if admin and admin.check_password(password):
            login_user(admin)
            session['is_admin'] = True
            flash("Admin logged in successfully!", "success")
            return redirect(url_for("admin.dashboard"))
        else:
            flash("Invalid email or password", "danger")

    return render_template("admin/login.html")


@admin_bp.route("/logout")
@login_required
def logout():
    logout_user()
    flash("Admin logged out.", "info")
    return redirect(url_for("admin.login"))


@admin_bp.route("/dashboard")
@login_required
def dashboard():
    return render_template("admin/dashboard.html")



# Add Flight
@admin_bp.route("/add-flight", methods=["GET", "POST"])
@login_required
@admin_required
def add_flight():
    form = FlightForm()
    if form.validate_on_submit():
        filename = None
        if form.flight_image.data:
            image = form.flight_image.data
            filename = secure_filename(image.filename)
            image.save(os.path.join(current_app.root_path, 'static/images/flights', filename))

        flight = Flight(
            flight_name=form.flight_name.data,
            flight_image=filename,
            price=form.price.data,
            departure_time=form.departure_time.data,
            arrival_time=form.arrival_time.data,
            description=form.description.data
        )
        db.session.add(flight)
        db.session.commit()
        flash("Flight added successfully!", "success")
        return redirect(url_for("admin.add_flight"))

    return render_template("admin/add_flight.html", form=form)



@admin_bp.route("/all-bookings")
@login_required
@admin_required
def all_bookings():
    bookings = Booking.query.all()
    return render_template("admin/bookings.html", bookings=bookings)



@admin_bp.route("/reject-booking/<int:booking_id>")
@login_required
@admin_required
def reject_booking(booking_id):
    booking = Booking.query.get_or_404(booking_id)
    booking.status = "Rejected"
    db.session.commit()
    flash("Booking rejected successfully!", "warning")
    return redirect(url_for("admin.all_bookings"))