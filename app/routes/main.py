from flask import Blueprint, render_template
from flask_login import login_required, current_user
from app.models.flight import Flight



main_bp = Blueprint('main', __name__)

@main_bp.route("/")
# @login_required
def index():
    flights = Flight.query.all()
    return render_template("index.html",flights=flights)

@main_bp.route("/profile")
@login_required
def profile():
    return render_template("user/profile.html", user=current_user)


