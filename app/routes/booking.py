from flask import session, Blueprint, render_template, redirect, url_for, flash
from flask_login import login_required, current_user
from app import db
from app.models.flight import Flight
from app.models.booking import Booking
from app.forms.booking import BookingForm

from functools import wraps
from flask import abort


booking_bp = Blueprint('booking', __name__, url_prefix="/booking")



@booking_bp.route("/details/<int:flight_id>", methods=["GET", "POST"])
@login_required
def details(flight_id):
    flight = Flight.query.get_or_404(flight_id)
    form = BookingForm()
    if form.validate_on_submit():
       
        booking = Booking(user_id=current_user.id, flight_id=flight.id)
        db.session.add(booking)
        db.session.commit()
        flash("Flight booked successfully!", "success")
        return redirect(url_for('booking.confirmation', booking_id=booking.id))
    return render_template("booking/details.html", flight=flight, form=form)


@booking_bp.route("/confirmation/<int:booking_id>")
@login_required
def confirmation(booking_id):
    booking = Booking.query.get_or_404(booking_id)
    return render_template("booking/confirmation.html", booking=booking)



@booking_bp.route("/my-bookings")
@login_required
def my_bookings():
    bookings = current_user.bookings  
    return render_template("booking/my_bookings.html", bookings=bookings)



@booking_bp.route("/cancel-booking/<int:booking_id>")
@login_required
def cancel_booking(booking_id):
    booking = Booking.query.filter_by(id=booking_id, user_id=current_user.id).first()

    if not booking:
        flash("Booking not found.", "danger")
        return redirect(url_for("booking.my_bookings"))

    booking.status = "Canceled"
    db.session.commit()
    flash("Booking canceled successfully!", "success")
    return redirect(url_for("booking.my_bookings"))