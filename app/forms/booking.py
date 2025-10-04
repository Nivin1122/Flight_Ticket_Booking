from flask_wtf import FlaskForm
from wtforms import SubmitField

class BookingForm(FlaskForm):
    submit = SubmitField("Confirm Booking")