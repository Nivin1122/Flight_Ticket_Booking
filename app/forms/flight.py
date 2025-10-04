from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, FloatField, FileField, SubmitField
from wtforms.validators import DataRequired



class FlightForm(FlaskForm):
    flight_name = StringField("Flight Name", validators=[DataRequired()])
    flight_image = FileField("Flight Image")
    price = FloatField("Price", validators=[DataRequired()])
    departure_time = StringField("Departure Time", validators=[DataRequired()])
    arrival_time = StringField("Arrival Time", validators=[DataRequired()])
    description = TextAreaField("Description")
    submit = SubmitField("Add Flight")